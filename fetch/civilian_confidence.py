"""
fetch/civilian_confidence.py — Civilian Confidence Index (CCI) data pipeline

Three independent fetch functions:

  fetch_rosstat_fuel()      — Rosstat weekly retail fuel prices by federal subject
                              Extracts DNR/LNR/Zaporizhzhia/Kherson rows
                              Score = (occupied_price / russian_avg − 1) × 500, cap 100

  fetch_telegram_keywords() — Monitor Mariupol/Donetsk/Luhansk Telegram community
                              channels for panic goods keywords
                              Normalized to Jun–Aug 2025 baseline, score 0–100

  fetch_avito_staples()     — Avito grey market: гречка, сахар, канистра дизель
                              in Donetsk/Luhansk/Mariupol vs mainland equivalents
                              Score = (occupied_premium / mainland − 1) × 200, cap 100

CCI composite = mean(fuel_score, panic_keyword_score, avito_premium_score)

Usage:
    python fetch/civilian_confidence.py           # dry-run
    python fetch/civilian_confidence.py --write   # append to data/civilian_confidence.json
    python fetch/civilian_confidence.py --month 2026-07
"""

import re
import ssl
import sys
import json
import time
import urllib.request
import urllib.error
from datetime import date, datetime, timedelta
from pathlib import Path

# Windows Python ships without the full CA bundle for some Russian/CIS hosts.
# Use an unverified context so Rosstat SSL doesn't hard-block the fetch.
_SSL_CTX = ssl._create_unverified_context()

ROOT = Path(__file__).parent.parent
DATA = ROOT / "data"
OUT  = DATA / "civilian_confidence.json"

# Baseline keyword hit rate (Jun–Aug 2025) for normalization
# Set after first 3 months of real data; estimated here
KEYWORD_BASELINE_HITS_PER_WEEK = 12

# Pre-war mainland Russian average prices for comparison (estimated 2025 values)
MAINLAND_PRICES = {
    "гречка_kg":     65,    # ₽/kg buckwheat
    "сахар_kg":      72,    # ₽/kg sugar
    "diesel_canister": 280, # ₽/litre diesel
}

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Accept-Language": "ru-RU,ru;q=0.9",
}


# ── HTTP helper ───────────────────────────────────────────────────────────

def get(url: str, timeout: int = 20) -> str:
    try:
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=timeout, context=_SSL_CTX) as r:
            return r.read().decode("utf-8", errors="replace")
    except Exception as e:
        print(f"  GET {url} -> {e}", file=sys.stderr)
        return ""


# ── 1. Rosstat fuel price premium ─────────────────────────────────────────

ROSSTAT_FUEL_URL = "https://rosstat.gov.ru/storage/mediabank/cen_tov.htm"

# Oblast name patterns for occupied territories in Rosstat tables
OCCUPIED_OBLAST_PATTERNS = [
    r'ДНР|Донецк.*?Народн|Donetsk.*?People',
    r'ЛНР|Луганск.*?Народн|Luhansk.*?People',
    r'Запорожск',
    r'Херсонск',
]

def fetch_rosstat_fuel() -> dict:
    """
    Scrape Rosstat weekly fuel price table.
    Returns {"fuel_price_premium_pct": float|None, "fuel_score": int|None, "parsed": bool}
    """
    print("  [ROSSTAT] Fetching weekly fuel prices…")
    html = get(ROSSTAT_FUEL_URL)

    if not html:
        # Try alternate URL pattern
        html = get("https://rosstat.gov.ru/price")

    if not html:
        print("    Rosstat unreachable", file=sys.stderr)
        return {"fuel_price_premium_pct": None, "fuel_score": None, "parsed": False}

    # Parse fuel price table — Rosstat uses HTML tables
    # Look for АИ-92, АИ-95, or дизель columns
    # Find table rows with oblast names, extract prices

    # Strategy: find all numeric price-like values (format: 55.40 or 55,40)
    price_pattern = re.compile(r'(\d{2,3}[,\.]\d{1,2})')

    occupied_prices = []
    russian_prices  = []

    # Split into rows
    rows = re.split(r'<tr[^>]*>', html)
    for row in rows:
        text = re.sub(r'<[^>]+>', ' ', row)
        prices_in_row = [float(p.replace(',', '.')) for p in price_pattern.findall(text)
                         if 30 < float(p.replace(',', '.')) < 200]

        if not prices_in_row:
            continue

        avg_price = sum(prices_in_row) / len(prices_in_row)

        is_occupied = any(re.search(pat, text, re.IGNORECASE | re.UNICODE)
                          for pat in OCCUPIED_OBLAST_PATTERNS)
        if is_occupied:
            occupied_prices.append(avg_price)
        elif re.search(r'Россия|Russian\s+Federation|РФ|в среднем', text, re.IGNORECASE):
            russian_prices.append(avg_price)

    if not russian_prices:
        # Fall back: use all non-occupied prices as proxy for Russian average
        all_prices = []
        for row in rows:
            text = re.sub(r'<[^>]+>', ' ', row)
            prices = [float(p.replace(',', '.')) for p in price_pattern.findall(text)
                      if 30 < float(p.replace(',', '.')) < 200]
            if prices:
                all_prices.extend(prices)
        if all_prices:
            russian_prices = [sum(all_prices) / len(all_prices)]

    if not occupied_prices or not russian_prices:
        (DATA / "debug_rosstat.html").write_text(html[:80000], encoding="utf-8")
        print(f"    Parse failed — saved debug_rosstat.html", file=sys.stderr)
        return {"fuel_price_premium_pct": None, "fuel_score": None, "parsed": False}

    occ_avg = sum(occupied_prices) / len(occupied_prices)
    rus_avg = sum(russian_prices)  / len(russian_prices)
    premium_pct = round((occ_avg / rus_avg - 1) * 100, 1)
    # Score: (premium_pct / 20) × 100, cap 100  → 20% premium = score 100
    score = min(100, round(premium_pct * 5))

    print(f"    → occupied avg: ₽{occ_avg:.1f}, Russian avg: ₽{rus_avg:.1f}")
    print(f"    → premium: {premium_pct}%  score: {score}")

    return {"fuel_price_premium_pct": premium_pct, "fuel_score": score, "parsed": True}


# ── 2. Telegram panic keyword score ───────────────────────────────────────

PANIC_KEYWORDS = [
    "гречка", "сахар", "дефицит", "пустые полки", "всё раскупили",
    "очередь", "тушёнка", "нет топлива", "нет в наличии", "мука", "соль",
    "бензин закончился", "нет бензина",
]

COMMUNITY_CHANNELS = [
    # Public Telegram web views for occupied city community groups
    "https://t.me/s/mariupol_today",
    "https://t.me/s/donetsk_today",
    "https://t.me/s/lugansk_today",
    "https://t.me/s/mariupol_now",
]

def fetch_telegram_keywords() -> dict:
    """
    Scan public Telegram web views for panic goods keywords.
    Returns {"panic_keyword_score": int|None, "weekly_hits": int, "parsed": bool}
    """
    print("  [TELEGRAM] Scanning community channels for panic keywords…")
    cutoff = datetime.utcnow() - timedelta(days=7)
    weekly_hits = 0
    channel_hits = {}

    for url in COMMUNITY_CHANNELS:
        print(f"    {url}")
        html = get(url)
        if not html:
            continue
        time.sleep(1.5)

        msg_blocks = re.split(r'<div class="tgme_widget_message_wrap', html)
        recent = 0
        for block in msg_blocks[1:]:
            dt_m = re.search(r'datetime="(\d{4}-\d{2}-\d{2}T\d{2}:\d{2})', block)
            if not dt_m:
                continue
            try:
                msg_dt = datetime.strptime(dt_m.group(1), "%Y-%m-%dT%H:%M")
            except ValueError:
                continue
            if msg_dt < cutoff:
                continue

            text = re.sub(r'<[^>]+>', ' ', block).lower()
            hits = sum(1 for kw in PANIC_KEYWORDS if kw.lower() in text)
            recent += hits

        channel_hits[url] = recent
        weekly_hits += recent

    if not weekly_hits and not channel_hits:
        print("    All channels unreachable or empty", file=sys.stderr)
        return {"panic_keyword_score": None, "weekly_hits": 0, "parsed": False}

    # Normalize against baseline
    score = min(100, round((weekly_hits / KEYWORD_BASELINE_HITS_PER_WEEK) * 50))
    print(f"    → weekly hits: {weekly_hits}  score: {score}")

    return {"panic_keyword_score": score, "weekly_hits": weekly_hits, "parsed": True}


# ── 3. Avito staple goods price premium ───────────────────────────────────

AVITO_SEARCHES = {
    "гречка": {
        "occupied": "https://www.avito.ru/donetsk/produkty_pitaniya/grechka",
        "mainland": "https://www.avito.ru/rostov-na-donu/produkty_pitaniya/grechka",
        "unit": "kg",
        "baseline_key": "гречка_kg",
    },
    "сахар": {
        "occupied": "https://www.avito.ru/donetsk/produkty_pitaniya/sahar",
        "mainland": "https://www.avito.ru/rostov-na-donu/produkty_pitaniya/sahar",
        "unit": "kg",
        "baseline_key": "сахар_kg",
    },
    "дизель": {
        "occupied": "https://www.avito.ru/donetsk/transport/toplivo",
        "mainland": "https://www.avito.ru/rostov-na-donu/transport/toplivo",
        "unit": "litre",
        "baseline_key": "diesel_canister",
    },
}

PRICE_PATTERN = re.compile(r'(\d[\d\s]{1,6})\s*[₽руб]', re.UNICODE)

def _median_prices(html: str) -> float | None:
    prices = []
    for m in PRICE_PATTERN.finditer(html):
        try:
            v = int(str(m.group(1)).replace(" ", "").replace("\xa0", ""))
            if 10 < v < 100_000:
                prices.append(v)
        except ValueError:
            pass
    if not prices:
        return None
    prices.sort()
    mid = len(prices) // 2
    return prices[mid]

def fetch_avito_staples() -> dict:
    """
    Scrape Avito for staple goods price premium in occupied vs mainland cities.
    Returns {"avito_premium_score": int|None, "premiums": dict, "parsed": bool}
    """
    print("  [AVITO] Checking grey market staple prices…")
    premiums = {}
    any_parsed = False

    for good, cfg in AVITO_SEARCHES.items():
        print(f"    {good}:")
        occ_html = get(cfg["occupied"])
        time.sleep(2)
        ml_html  = get(cfg["mainland"])
        time.sleep(2)

        occ_price = _median_prices(occ_html) if occ_html else None
        ml_price  = _median_prices(ml_html)  if ml_html  else None

        # Fallback to known baseline if mainland fetch fails
        if ml_price is None:
            ml_price = MAINLAND_PRICES.get(cfg["baseline_key"])

        if occ_price and ml_price:
            premium = (occ_price / ml_price - 1) * 100
            premiums[good] = {"occ": occ_price, "mainland": ml_price, "premium_pct": round(premium, 1)}
            print(f"      occ ₽{occ_price} vs mainland ₽{ml_price} → +{premium:.0f}%")
            any_parsed = True
        else:
            premiums[good] = {"occ": occ_price, "mainland": ml_price, "premium_pct": None}
            print(f"      parse failed (occ={occ_price}, mainland={ml_price})", file=sys.stderr)

    valid = [p["premium_pct"] for p in premiums.values() if p["premium_pct"] is not None]
    if not valid:
        return {"avito_premium_score": None, "premiums": premiums, "parsed": False}

    avg_premium = sum(valid) / len(valid)
    # Score: premium% × 200 / 100, cap 100  → 50% avg premium = score 100
    score = min(100, round(avg_premium * 2))
    print(f"    → avg premium: {avg_premium:.1f}%  score: {score}")

    return {"avito_premium_score": score, "premiums": premiums, "parsed": any_parsed}


# ── Compose CCI ───────────────────────────────────────────────────────────

def compute_cci(fuel_score, panic_score, avito_score) -> tuple[int | None, bool]:
    scores = [s for s in [fuel_score, panic_score, avito_score] if s is not None]
    if not scores:
        return None, True
    return round(sum(scores) / len(scores)), len(scores) < 3


# ── Load / save ───────────────────────────────────────────────────────────

def load() -> dict:
    if not OUT.exists():
        return {"monthly_readings": []}
    with open(OUT, encoding="utf-8") as f:
        return json.load(f)

def save(data: dict):
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


# ── Main ─────────────────────────────────────────────────────────────────

def main():
    write = "--write" in sys.argv
    month_arg = next((a for a in sys.argv[1:] if re.match(r'^\d{4}-\d{2}$', a)), None)
    month_tag = month_arg or date.today().strftime("%Y-%m")

    print(f"civilian_confidence.py — month: {month_tag}")
    print()

    rosstat = fetch_rosstat_fuel()
    print()
    tg      = fetch_telegram_keywords()
    print()
    avito   = fetch_avito_staples()
    print()

    f_score = rosstat.get("fuel_score")
    p_score = tg.get("panic_keyword_score")
    a_score = avito.get("avito_premium_score")

    cci, partial = compute_cci(f_score, p_score, a_score)

    print(f"Results for {month_tag}:")
    print(f"  fuel_price_premium_pct : {rosstat.get('fuel_price_premium_pct')}")
    print(f"  fuel_score             : {f_score}")
    print(f"  panic_keyword_score    : {p_score}  (weekly hits: {tg.get('weekly_hits', 0)})")
    print(f"  avito_premium_score    : {a_score}")
    print(f"  CCI                    : {cci}{'  (PARTIAL)' if partial else ''}")

    # Divergence check against latest permanence ratio
    perm_path = DATA / "permanence_ratio.json"
    if perm_path.exists() and cci is not None:
        with open(perm_path, encoding="utf-8") as f:
            perm = json.load(f)
        for city_key, city in perm.get("cities", {}).items():
            readings = [r for r in city.get("monthly_readings", []) if r.get("ratio") is not None]
            if len(readings) >= 2:
                delta = readings[-1]["ratio"] - readings[-2]["ratio"]
                if delta <= -3 and cci >= 25:
                    print(f"\n  !! DIVERGENCE ALERT [{city_key}]: CCI={cci} rising, permanence ratio falling ({delta:+d})")

    if write:
        data = load()
        readings = data.setdefault("monthly_readings", [])
        entry = next((r for r in readings if r.get("month") == month_tag), None)
        if entry is None:
            entry = {"month": month_tag}
            readings.append(entry)
            readings.sort(key=lambda r: r.get("month", ""))

        entry.update({
            "fuel_price_premium_pct": rosstat.get("fuel_price_premium_pct"),
            "fuel_score":             f_score,
            "panic_keyword_score":    p_score,
            "avito_premium_score":    a_score,
            "CCI":                    cci,
            "real":                   not partial,
        })
        if partial:
            entry["partial"] = True
        elif "partial" in entry:
            del entry["partial"]

        save(data)
        print(f"\nWritten → {OUT}")
    else:
        print("\n(dry-run — pass --write to save)")


if __name__ == "__main__":
    main()
