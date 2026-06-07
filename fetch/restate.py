"""
fetch/restate.py — scrape Crimea biweekly price index from Restate.ru

Target: krym.restate.ru/graph/
Extracts the biweekly ₽/m² table for secondary apartments and appends
new readings to data/crimea_prices.json.

Usage:
    python fetch/restate.py           # dry-run: print new readings only
    python fetch/restate.py --write   # append to data/crimea_prices.json
    python fetch/restate.py --all     # print all scraped readings (debugging)
"""

import sys
import json
import re
import time
import urllib.request
import urllib.error
from datetime import datetime, date
from pathlib import Path

ROOT    = Path(__file__).parent.parent
DATA    = ROOT / "data" / "crimea_prices.json"
URL     = "https://krym.restate.ru/graph/"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/124.0.0.0 Safari/537.36",
    "Accept-Language": "ru-RU,ru;q=0.9",
    "Referer": "https://krym.restate.ru/",
}


# ── HTTP fetch ────────────────────────────────────────────────────────────

def fetch_html(url: str, retries: int = 3) -> str:
    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, headers=HEADERS)
            with urllib.request.urlopen(req, timeout=20) as resp:
                return resp.read().decode("utf-8", errors="replace")
        except urllib.error.URLError as e:
            print(f"  Attempt {attempt+1}/{retries} failed: {e}", file=sys.stderr)
            if attempt < retries - 1:
                time.sleep(3 * (attempt + 1))
    raise RuntimeError(f"Failed to fetch {url} after {retries} attempts")


# ── Parse ─────────────────────────────────────────────────────────────────

def parse_readings(html: str) -> list[dict]:
    """
    Restate.ru embeds price data as a JS array inside the page, typically in
    one of these forms:
        var graph_data = [[timestamp_ms, price], ...];
        data: [[1718000000000, 173540], ...]
    We also try parsing an HTML table as a fallback.
    """
    readings = []

    # Strategy 1: JS array of [unix_ms, value] pairs
    pat_js = re.compile(
        r'(?:graph_data|graphData|chartData|data)\s*[=:]\s*\[(\[[\s\S]*?\])\]',
        re.IGNORECASE
    )
    m = pat_js.search(html)
    if m:
        raw = m.group(0)
        pairs = re.findall(r'\[\s*(\d{10,13})\s*,\s*([\d.]+)\s*\]', raw)
        for ts_str, val_str in pairs:
            ts = int(ts_str)
            if ts > 1e11:   # milliseconds → seconds
                ts //= 1000
            dt = datetime.utcfromtimestamp(ts).date()
            readings.append({"date": str(dt), "value": float(val_str), "real": True})

    # Strategy 2: HTML table rows  <td>DD.MM.YYYY</td><td>NNN NNN</td>
    if not readings:
        rows = re.findall(
            r'<td[^>]*>(\d{1,2}\.\d{2}\.\d{4})</td>\s*<td[^>]*>([\d\s,.]+)</td>',
            html
        )
        for date_str, val_str in rows:
            try:
                dt = datetime.strptime(date_str, "%d.%m.%Y").date()
                value = float(val_str.replace(" ", "").replace(",", "."))
                readings.append({"date": str(dt), "value": value, "real": True})
            except ValueError:
                continue

    # Strategy 3: any dense numeric pairs that look like (date_string, price)
    if not readings:
        pat_text = re.compile(r'(\d{2}\.\d{2}\.\d{4})[^\d]*([\d\s]{6,})')
        for m in pat_text.finditer(html):
            try:
                dt    = datetime.strptime(m.group(1), "%d.%m.%Y").date()
                value = float(m.group(2).replace(" ", ""))
                if 50_000 < value < 1_000_000:   # sanity: ₽/m² range
                    readings.append({"date": str(dt), "value": value, "real": True})
            except ValueError:
                continue

    # Deduplicate and sort
    seen = {}
    for r in readings:
        seen[r["date"]] = r
    return sorted(seen.values(), key=lambda x: x["date"])


# ── Load / save JSON ──────────────────────────────────────────────────────

def load_existing() -> dict:
    if not DATA.exists():
        return {
            "source": "Restate.ru — krym.restate.ru/graph/",
            "market": "Crimea secondary apartments",
            "unit": "RUB per m²",
            "cadence": "biweekly",
            "readings": []
        }
    with open(DATA, encoding="utf-8") as f:
        return json.load(f)


def save(data: dict) -> None:
    with open(DATA, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


# ── Diff ──────────────────────────────────────────────────────────────────

def find_new(existing_readings: list, scraped: list) -> list:
    known_dates = {r["date"] for r in existing_readings}
    return [r for r in scraped if r["date"] not in known_dates]


# ── Main ──────────────────────────────────────────────────────────────────

def main():
    write  = "--write" in sys.argv
    show_all = "--all" in sys.argv

    print(f"Fetching {URL} …")
    html = fetch_html(URL)
    print(f"  Got {len(html):,} bytes")

    scraped = parse_readings(html)
    if not scraped:
        print("ERROR: No readings parsed. Page structure may have changed.", file=sys.stderr)
        print("  Saving raw HTML to debug_restate.html for inspection.", file=sys.stderr)
        Path("debug_restate.html").write_text(html, encoding="utf-8")
        sys.exit(1)

    print(f"  Parsed {len(scraped)} readings ({scraped[0]['date']} → {scraped[-1]['date']})")

    if show_all:
        for r in scraped:
            print(f"  {r['date']}  {r['value']:>10,.0f} ₽/m²")
        return

    data = load_existing()
    new  = find_new(data["readings"], scraped)

    if not new:
        print("No new readings — already up to date.")
        return

    print(f"  {len(new)} new reading(s):")
    for r in new:
        print(f"    {r['date']}  {r['value']:>10,.0f} ₽/m²")

    if write:
        data["readings"].extend(new)
        data["readings"].sort(key=lambda x: x["date"])
        data["data_type"] = f"real — scraped {date.today()}"
        save(data)
        print(f"  Written → {DATA}")
    else:
        print("  (dry-run — pass --write to save)")


if __name__ == "__main__":
    main()
