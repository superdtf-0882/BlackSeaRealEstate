"""
fetch/restate.py -- scrape Crimea biweekly price index from Restate.ru

Target: krym.restate.ru/graph2/data/ (JSON API, discovered from page source)
The page loads chart data via fetch(item.dataset.href) in graphChart.js.
data-href value: /graph2/data/?region=60983&type=112&period=2&influence=3&op=1&form=9&sy=1
  region=60983 = Crimea, type=112 = secondary apartments, op=1 = sell

Usage:
    python fetch/restate.py           # dry-run: print new readings only
    python fetch/restate.py --write   # append to data/crimea_prices.json
    python fetch/restate.py --all     # print all scraped readings (debugging)
"""

import sys
import json
import time
import urllib.request
import urllib.error
from datetime import datetime, date
from pathlib import Path

ROOT = Path(__file__).parent.parent
DATA = ROOT / "data" / "crimea_prices.json"

API_URL = (
    "https://krym.restate.ru/graph2/data/"
    "?region=60983&type=112&period=2&influence=3"
    "&money=&metro=&area=&okrug=&op=1&form=9&sy=1"
)
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/124.0.0.0 Safari/537.36",
    "Accept-Language": "ru-RU,ru;q=0.9",
    "Referer": "https://krym.restate.ru/graph/",
}


# -- HTTP fetch ---------------------------------------------------------------

def fetch_json(url: str, retries: int = 3) -> dict | None:
    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, headers=HEADERS)
            with urllib.request.urlopen(req, timeout=20) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except urllib.error.URLError as e:
            print(f"  Attempt {attempt+1}/{retries} failed: {e}", file=sys.stderr)
            if attempt < retries - 1:
                time.sleep(3 * (attempt + 1))
        except json.JSONDecodeError as e:
            print(f"  JSON parse error: {e}", file=sys.stderr)
            return None
    return None


# -- Parse --------------------------------------------------------------------

def parse_readings(data: dict) -> list[dict]:
    """
    API response schema:
      {"columns": [{"name": "Даты"}, {"name": "Квартиры (вторичный рынок)"}, ...],
       "rows": [["24.06.25", 180625.68, 71.79], ...]}
    Column 0 = date string DD.MM.YY, column 1 = RUB/m2 price.
    """
    readings = []
    for row in data.get("rows", []):
        if len(row) < 2 or row[1] is None:
            continue
        try:
            dt = datetime.strptime(str(row[0]), "%d.%m.%y").date()
            price = float(row[1])
            if 50_000 < price < 1_000_000:
                readings.append({"date": str(dt), "value": round(price, 2), "real": True})
        except (ValueError, TypeError):
            continue
    seen = {}
    for r in readings:
        seen[r["date"]] = r
    return sorted(seen.values(), key=lambda x: x["date"])


# -- Load / save JSON ---------------------------------------------------------

def load_existing() -> dict:
    if not DATA.exists():
        return {
            "source": "Restate.ru -- krym.restate.ru/graph/",
            "market": "Crimea secondary apartments",
            "unit": "RUB per m2",
            "cadence": "biweekly",
            "readings": [],
        }
    with open(DATA, encoding="utf-8") as f:
        return json.load(f)


def save(payload: dict) -> None:
    with open(DATA, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)


# -- Diff ---------------------------------------------------------------------

def find_new(existing: list, scraped: list) -> list:
    known = {r["date"] for r in existing}
    return [r for r in scraped if r["date"] not in known]


# -- Main ---------------------------------------------------------------------

def main():
    write    = "--write" in sys.argv
    show_all = "--all"   in sys.argv

    print(f"Fetching {API_URL} ...")
    raw = fetch_json(API_URL)
    if not raw:
        print("ERROR: Failed to fetch or parse JSON response.", file=sys.stderr)
        sys.exit(1)

    scraped = parse_readings(raw)
    if not scraped:
        print("ERROR: No readings parsed from API response.", file=sys.stderr)
        print(f"  Raw keys: {list(raw.keys())}", file=sys.stderr)
        sys.exit(1)

    print(f"  Parsed {len(scraped)} readings ({scraped[0]['date']} -> {scraped[-1]['date']})")

    if show_all:
        for r in scraped:
            print(f"  {r['date']}  {r['value']:>10,.0f} RUB/m2")
        return

    payload = load_existing()
    new = find_new(payload["readings"], scraped)

    if not new:
        print("No new readings -- already up to date.")
        return

    print(f"  {len(new)} new reading(s):")
    for r in new:
        print(f"    {r['date']}  {r['value']:>10,.0f} RUB/m2")

    if write:
        payload["readings"].extend(new)
        payload["readings"].sort(key=lambda x: x["date"])
        payload["data_type"] = f"real -- scraped {date.today()}"
        save(payload)
        print(f"  Written -> {DATA}")
    else:
        print("  (dry-run -- pass --write to save)")


if __name__ == "__main__":
    main()
