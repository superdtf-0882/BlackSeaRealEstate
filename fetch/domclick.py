"""
fetch/domclick.py — scrape listing counts from Домклик for Donetsk and Luhansk

Targets:
    Donetsk apartments : doneck.domclick.ru/pokupka/kvartiry
    Donetsk houses     : doneck.domclick.ru/pokupka/doma
    Luhansk houses     : lugansk.domclick.ru/pokupka/doma

Appends new readings to data/domclick_listings.json.

Usage:
    python fetch/domclick.py           # dry-run: print counts only
    python fetch/domclick.py --write   # append to data/domclick_listings.json
"""

import sys
import json
import re
import time
import urllib.request
import urllib.error
from datetime import date
from pathlib import Path

ROOT = Path(__file__).parent.parent
DATA = ROOT / "data" / "domclick_listings.json"

TARGETS = {
    "donetsk": {
        "apartments": "https://doneck.domclick.ru/pokupka/kvartiry",
        "houses":     "https://doneck.domclick.ru/pokupka/doma",
    },
    "luhansk": {
        "houses": "https://lugansk.domclick.ru/pokupka/doma",
    },
}

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/124.0.0.0 Safari/537.36",
    "Accept-Language": "ru-RU,ru;q=0.9",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
}


# ── HTTP ──────────────────────────────────────────────────────────────────

def fetch_html(url: str, retries: int = 3) -> str:
    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, headers=HEADERS)
            with urllib.request.urlopen(req, timeout=20) as resp:
                return resp.read().decode("utf-8", errors="replace")
        except urllib.error.URLError as e:
            print(f"  [{url}] attempt {attempt+1}/{retries}: {e}", file=sys.stderr)
            if attempt < retries - 1:
                time.sleep(4 * (attempt + 1))
    print(f"  WARNING: Could not fetch {url}", file=sys.stderr)
    return ""


# ── Parse listing count ───────────────────────────────────────────────────

COUNT_PATTERNS = [
    # JSON field: "totalCount":385  or "count":385
    re.compile(r'"(?:totalCount|itemsCount|total_count|count)"\s*:\s*(\d+)'),
    # "385 объявлений" / "385 предложений" / "385 квартир"
    re.compile(r'(\d[\d\s]+)\s*(?:объявлен|предложен|квартир|домов|объект)', re.UNICODE),
    # aria-label or title: "Найдено 385"
    re.compile(r'(?:найдено|всего|results)[^\d]*(\d+)', re.IGNORECASE | re.UNICODE),
]

def parse_count(html: str) -> int | None:
    if not html:
        return None
    for pat in COUNT_PATTERNS:
        matches = pat.findall(html)
        if matches:
            # Take the first plausible match (strip whitespace, convert)
            for m in matches:
                try:
                    n = int(str(m).replace(" ", "").replace(" ", ""))
                    if 0 < n < 100_000:
                        return n
                except ValueError:
                    continue
    return None


# ── Alerts ───────────────────────────────────────────────────────────────

def check_alerts(city: str, key: str, new_val: int, thresholds: dict) -> list[str]:
    alerts = []
    surge_key    = f"{city}_{key}_surge"
    collapse_key = f"{city}_{key}_collapse"
    if surge_key in thresholds and new_val >= thresholds[surge_key]:
        alerts.append(f"ALERT [{city}/{key}]: surge threshold hit — {new_val} ≥ {thresholds[surge_key]}")
    if collapse_key in thresholds and new_val <= thresholds[collapse_key]:
        alerts.append(f"ALERT [{city}/{key}]: collapse threshold hit — {new_val} ≤ {thresholds[collapse_key]}")
    return alerts


# ── Load / save ───────────────────────────────────────────────────────────

def load_existing() -> dict:
    if not DATA.exists():
        return {
            "source": "Домклик — domclick.ru (Sberbank property platform)",
            "notes": "Secondary market listing counts. Key Track B indicator.",
            "alert_thresholds": {
                "donetsk_apartments_surge": 600,
                "donetsk_apartments_collapse": 100,
                "luhansk_houses_surge": 1400,
                "luhansk_houses_collapse": 300,
            },
            "cities": {
                "donetsk": {"readings": []},
                "luhansk": {"readings": []},
            }
        }
    with open(DATA, encoding="utf-8") as f:
        return json.load(f)


def save(data: dict) -> None:
    with open(DATA, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


# ── Main ─────────────────────────────────────────────────────────────────

def main():
    write = "--write" in sys.argv
    today = str(date.today())

    data       = load_existing()
    thresholds = data.get("alert_thresholds", {})
    all_alerts = []
    results    = {}

    for city, urls in TARGETS.items():
        city_result = {"date": today, "real": True, "source": "Домклик live pull"}
        print(f"\n{city.capitalize()}")
        for listing_type, url in urls.items():
            print(f"  Fetching {listing_type}: {url}")
            html  = fetch_html(url)
            count = parse_count(html)
            if count is None:
                print(f"    WARNING: could not parse count — site may have changed or blocked scraper.")
                print(f"    Saving debug HTML to debug_domclick_{city}_{listing_type}.html")
                Path(f"debug_domclick_{city}_{listing_type}.html").write_text(html or "", encoding="utf-8")
            else:
                print(f"    → {count:,} listings")
                city_result[listing_type] = count
                alerts = check_alerts(city, listing_type, count, thresholds)
                for a in alerts:
                    print(f"    !! {a}")
                all_alerts.extend(alerts)
            time.sleep(2)   # polite delay
        results[city] = city_result

    print()
    if write:
        for city, entry in results.items():
            if len(entry) > 3:   # has at least one count besides date/real/source
                data["cities"].setdefault(city, {"readings": []})
                data["cities"][city].setdefault("readings", [])
                # Avoid duplicate date
                existing_dates = {r["date"] for r in data["cities"][city]["readings"]}
                if entry["date"] not in existing_dates:
                    data["cities"][city]["readings"].append(entry)
                    print(f"  Appended {city} reading for {entry['date']}")
                else:
                    print(f"  {city}: {entry['date']} already recorded — skipping")
        save(data)
        print(f"Written → {DATA}")
    else:
        print("(dry-run — pass --write to save)")

    if all_alerts:
        print("\n=== ALERTS ===")
        for a in all_alerts:
            print(f"  {a}")


if __name__ == "__main__":
    main()
