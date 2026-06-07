"""
fetch/avito_rental.py — scrape rental listing counts + median price from Avito

Targets (long-term residential rental, квартиры):
    Mariupol : avito.ru/mariupol/nedvizhimost/snyat/kvartiru
    Donetsk  : avito.ru/donetsk/nedvizhimost/snyat/kvartiru
    Luhansk  : avito.ru/lugansk/nedvizhimost/snyat/kvartiru
    Crimea   : avito.ru/respublika_krym/nedvizhimost/snyat/kvartiru

Appends monthly readings to data/permanence_ratio.json under each city's
monthly_readings array, updating rental_listings_est and median_rent_rub.
Also writes a raw snapshot to data/avito_rental_raw.json for auditing.

Usage:
    python fetch/avito_rental.py           # dry-run: print counts only
    python fetch/avito_rental.py --write   # append to permanence_ratio.json
    python fetch/avito_rental.py --city donetsk   # single city only
"""

import re
import sys
import json
import time
import urllib.request
import urllib.error
from datetime import date
from pathlib import Path

ROOT = Path(__file__).parent.parent
DATA = ROOT / "data"
PERM = DATA / "permanence_ratio.json"
RAW  = DATA / "avito_rental_raw.json"

TARGETS = {
    "mariupol": {
        "url":   "https://www.avito.ru/mariupol/nedvizhimost/snyat/kvartiru-ASgBAgICAkSSA8YQ",
        "label": "Мариуполь",
    },
    "donetsk": {
        "url":   "https://www.avito.ru/donetsk/nedvizhimost/snyat/kvartiru-ASgBAgICAkSSA8YQ",
        "label": "Донецк",
    },
    "luhansk": {
        "url":   "https://www.avito.ru/lugansk/nedvizhimost/snyat/kvartiru-ASgBAgICAkSSA8YQ",
        "label": "Луганск",
    },
    "crimea": {
        "url":   "https://www.avito.ru/respublika_krym/nedvizhimost/snyat/kvartiru-ASgBAgICAkSSA8YQ",
        "label": "Крым",
    },
}

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "ru-RU,ru;q=0.9",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate, br",
    "DNT": "1",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-Mode": "navigate",
}

# Avito is aggressive about bot detection. These fallback strategies are tried
# in order; the first that returns a plausible count wins.
COUNT_PATTERNS = [
    # JSON blob: "count":385  or "totalCount":385
    re.compile(r'"(?:count|totalCount|itemsCount)"\s*:\s*(\d+)'),
    # "385 объявлений" style text nodes
    re.compile(r'(\d[\d\s]*)\s+объявлен', re.UNICODE),
    # data-marker="page-title/count" or title-count spans
    re.compile(r'data-marker="page-title/count"[^>]*>(\d[\d\s]*)<'),
    # "Найдено X"
    re.compile(r'[Нн]айдено\D{0,10}(\d[\d\s]+)'),
]

PRICE_PATTERNS = [
    # "19 800 ₽/мес" or "19800 ₽ в месяц"
    re.compile(r'([\d\s]{4,8})\s*[₽руб].*?(?:мес|месяц)', re.UNICODE),
    # JSON price fields
    re.compile(r'"(?:price|priceValue|median_price)"\s*:\s*"?([\d\s]+)"?'),
]


# ── HTTP ──────────────────────────────────────────────────────────────────

def fetch_html(url: str, retries: int = 3) -> tuple[str, int]:
    """Returns (html, status_code). html may be empty on failure."""
    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, headers=HEADERS)
            with urllib.request.urlopen(req, timeout=25) as resp:
                raw = resp.read()
                # Handle gzip transparently — urllib does this, but be explicit
                try:
                    import gzip
                    content = gzip.decompress(raw).decode("utf-8", errors="replace")
                except Exception:
                    content = raw.decode("utf-8", errors="replace")
                return content, resp.status
        except urllib.error.HTTPError as e:
            print(f"    HTTP {e.code} on attempt {attempt+1}/{retries}", file=sys.stderr)
            if e.code in (403, 429):
                # Avito rate-limited or blocked — back off longer
                wait = 15 * (attempt + 1)
                print(f"    Rate limited — waiting {wait}s", file=sys.stderr)
                time.sleep(wait)
            elif attempt < retries - 1:
                time.sleep(5)
        except urllib.error.URLError as e:
            print(f"    URL error on attempt {attempt+1}/{retries}: {e}", file=sys.stderr)
            if attempt < retries - 1:
                time.sleep(5)
    return "", 0


# ── Parse helpers ─────────────────────────────────────────────────────────

def _clean_int(s: str) -> int | None:
    try:
        return int(str(s).replace(" ", "").replace(" ", "").replace(",", ""))
    except (ValueError, TypeError):
        return None


def parse_count(html: str) -> int | None:
    if not html:
        return None
    for pat in COUNT_PATTERNS:
        for m in pat.finditer(html):
            n = _clean_int(m.group(1))
            if n is not None and 0 < n < 500_000:
                return n
    return None


def parse_median_price(html: str) -> int | None:
    """
    Avito doesn't publish a median directly. We scrape visible price tags and
    take the median of the first page (~50 listings). Falls back to None.
    """
    if not html:
        return None

    # Pull all price strings from the page
    prices = []
    for m in re.finditer(
        r'([\d\s ]{4,9})\s*[₽]',
        html, re.UNICODE
    ):
        n = _clean_int(m.group(1))
        if n and 3_000 < n < 500_000:
            prices.append(n)

    if not prices:
        return None

    prices.sort()
    mid = len(prices) // 2
    return prices[mid] if len(prices) % 2 else (prices[mid-1] + prices[mid]) // 2


# ── Avito anti-bot note ───────────────────────────────────────────────────
# Avito serves different HTML to bots and may 403 entirely. If this script
# returns zeros consistently, the recommended fallback is:
#   1. Use a residential proxy (e.g. BrightData, Oxylabs)
#   2. Use Selenium/Playwright with a real browser profile
#   3. Query the unofficial Avito API endpoint:
#      https://m.avito.ru/api/9/items?locationId=...&categoryId=24&params[201]=1
#   The script saves debug HTML to data/avito_debug_{city}.html on parse failure
#   so you can diagnose what the server returned.

def fetch_city(city_key: str, config: dict) -> dict:
    url = config["url"]
    print(f"  {config['label']} ({city_key})")
    print(f"    GET {url}")

    html, status = fetch_html(url)

    if not html or status == 403:
        print(f"    !! Status {status} — Avito blocked request. Saving debug file.")
        debug_path = DATA / f"avito_debug_{city_key}.html"
        debug_path.write_text(html or f"[empty — status {status}]", encoding="utf-8")
        print(f"    Inspect {debug_path} to diagnose. Consider residential proxy.")
        return {"city": city_key, "count": None, "median_price": None, "blocked": True}

    count  = parse_count(html)
    median = parse_median_price(html)

    if count is None:
        print(f"    !! Count parse failed — saving debug HTML")
        (DATA / f"avito_debug_{city_key}.html").write_text(html, encoding="utf-8")
    else:
        print(f"    → {count:,} rental listings")

    if median:
        print(f"    → median price ≈ ₽{median:,}/month")

    return {
        "city":         city_key,
        "count":        count,
        "median_price": median,
        "blocked":      False,
        "url":          url,
    }


# ── Load / save permanence_ratio.json ────────────────────────────────────

def load_perm() -> dict:
    if not PERM.exists():
        return {"cities": {}}
    with open(PERM, encoding="utf-8") as f:
        return json.load(f)


def save_perm(data: dict) -> None:
    with open(PERM, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


# ── Append reading ────────────────────────────────────────────────────────

def append_reading(perm: dict, city_key: str, result: dict, month_tag: str) -> bool:
    """
    Updates or appends the monthly_readings entry for month_tag.
    Returns True if data was written.
    """
    if result["count"] is None:
        return False

    city = perm.get("cities", {}).get(city_key)
    if not city:
        return False

    readings = city.setdefault("monthly_readings", [])
    adj      = city.get("adjustment_factor", 1.0)
    count    = result["count"]
    local    = round(count * adj) if count else None  # note: this is rental count, adj is for mortgage

    # Find or create the month entry
    entry = next((r for r in readings if r.get("month") == month_tag), None)
    if entry is None:
        entry = {"month": month_tag, "real": True}
        readings.append(entry)
        readings.sort(key=lambda r: r.get("month", ""))

    entry["rental_listings_avito"] = count
    entry["real"] = True
    entry["source"] = "avito.ru live pull"
    if result.get("median_price"):
        entry["median_rent_avito"] = result["median_price"]

    # Recalculate ratio if we have a mortgage estimate
    mort_adj = entry.get("local_mortgage_adj") or (
        round((entry.get("mortgage_originations_est") or 0) * adj)
    )
    if mort_adj and count:
        ratio = round(mort_adj / (mort_adj + count) * 100)
        entry["ratio"] = ratio
        entry["rental_listings_est"] = count   # update estimate with real value

    return True


# ── Main ─────────────────────────────────────────────────────────────────

def main():
    write   = "--write" in sys.argv
    city_filter = None
    for i, arg in enumerate(sys.argv[1:]):
        if arg == "--city" and i + 1 < len(sys.argv) - 1:
            city_filter = sys.argv[i + 2]

    today     = date.today()
    month_tag = today.strftime("%Y-%m")

    targets = {k: v for k, v in TARGETS.items()
               if city_filter is None or k == city_filter}

    if not targets:
        print(f"Unknown city: {city_filter}. Valid: {', '.join(TARGETS)}", file=sys.stderr)
        sys.exit(1)

    print(f"avito_rental.py — {today}  (month: {month_tag})")
    print()

    perm     = load_perm()
    results  = {}
    raw_snap = {"date": str(today), "cities": {}}

    for city_key, config in targets.items():
        result = fetch_city(city_key, config)
        results[city_key] = result
        raw_snap["cities"][city_key] = result
        time.sleep(4)   # polite delay between cities

    print()

    # Save raw snapshot regardless of --write (audit trail)
    existing_raw = []
    if RAW.exists():
        with open(RAW, encoding="utf-8") as f:
            existing_raw = json.load(f) if RAW.stat().st_size > 2 else []
    existing_raw.append(raw_snap)
    with open(RAW, "w", encoding="utf-8") as f:
        json.dump(existing_raw, f, ensure_ascii=False, indent=2)
    print(f"Raw snapshot saved → {RAW}")

    if write:
        wrote = 0
        for city_key, result in results.items():
            if append_reading(perm, city_key, result, month_tag):
                print(f"  Updated {city_key} for {month_tag}")
                wrote += 1
        if wrote:
            save_perm(perm)
            print(f"Written → {PERM}")
        else:
            print("No data written (all cities blocked or count=None)")
    else:
        print("(dry-run — pass --write to save)")

    # Summary
    blocked = [k for k, r in results.items() if r.get("blocked")]
    if blocked:
        print(f"\n⚠ Blocked by Avito: {', '.join(blocked)}")
        print("  Consider: residential proxy, Playwright/Selenium, or unofficial API.")
        print("  Unofficial API hint: https://m.avito.ru/api/9/items?locationId=<id>&categoryId=24")


if __name__ == "__main__":
    main()
