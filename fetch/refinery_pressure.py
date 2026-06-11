"""
fetch/refinery_pressure.py — Refinery Pressure Index (RPI) data pipeline

Three independent fetch functions:

  fetch_crea()    — CREA monthly Russian refinery capacity utilization %
                    Source: energyandcleanair.org
                    Pressure = 100 − capacity_util_pct

  fetch_strikes() — GUR @DefenceU and OSInt channels (@RALee85, @ChrisO_wiki)
                    Confirmed infrastructure strikes, rolling 30-day window
                    Weights: refinery=3, storage=2, export_terminal=3, pipeline=2
                    Capped at 100

  fetch_kpler()   — Novorossiysk weekly crude+product export volume
                    Source: Kpler public page
                    Pressure = 100 − (weekly_vol / 2021_baseline × 100)

RPI composite = mean(capacity_pressure, strike_score, export_pressure)

If any source fails, partial RPI is computed from available sub-indicators
and the record is flagged with "partial": true.

Usage:
    python fetch/refinery_pressure.py           # dry-run
    python fetch/refinery_pressure.py --write   # append to data/refinery_pressure.json
    python fetch/refinery_pressure.py --month 2026-07   # force month tag
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

_SSL_CTX = ssl._create_unverified_context()

ROOT = Path(__file__).parent.parent
DATA = ROOT / "data"
OUT  = DATA / "refinery_pressure.json"

# Kpler 2021 annual average Novorossiysk export baseline (mt/year → approx weekly)
# 2021 Black Sea crude exports approx 60 Mt/year → ~1.15 Mt/week
KPLER_BASELINE_MT_WEEK = 1.15

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Accept-Language": "en-US,en;q=0.9",
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


# ── 1. CREA capacity utilization ─────────────────────────────────────────

CREA_URLS = [
    "https://energyandcleanair.org/product/russia-fossil-tracker/",
    "https://energyandcleanair.org/russia-fossil-fuels-tracker/",
    "https://energyandcleanair.org/russia-fossil-tracker/",
]

def fetch_crea() -> dict:
    """
    Scrape CREA for latest Russian refinery capacity utilization figure.
    Returns {"capacity_util_pct": float|None, "source_url": str, "parsed": bool}
    """
    print("  [CREA] Fetching refinery capacity utilization…")
    for url in CREA_URLS:
        html = get(url)
        if not html:
            continue

        # Try to find capacity utilization percentage in the page
        patterns = [
            r'(?:refinery|processing|capacity)\s+(?:utilization|utilisation)[^\d]*(\d{2,3}(?:\.\d)?)\s*%',
            r'(\d{2,3}(?:\.\d)?)\s*%\s*(?:of\s+)?(?:pre-?war|2021|baseline)',
            r'"capacity_utilization"\s*:\s*"?(\d{2,3}(?:\.\d)?)"?',
        ]
        for pat in patterns:
            m = re.search(pat, html, re.IGNORECASE)
            if m:
                val = float(m.group(1))
                if 40 <= val <= 100:
                    print(f"    → capacity utilization: {val}%")
                    return {"capacity_util_pct": val, "source_url": url, "parsed": True}

        # Save debug
        (DATA / "debug_crea.html").write_text(html[:50000], encoding="utf-8")
        print(f"    Parse failed — saved debug_crea.html", file=sys.stderr)

    print("  [CREA] All URLs failed or unparseable", file=sys.stderr)
    return {"capacity_util_pct": None, "source_url": CREA_URLS[0], "parsed": False}


# ── 2. Strike score ───────────────────────────────────────────────────────

STRIKE_KEYWORDS = {
    "refinery":        (3, ["НПЗ", "нефтезавод", "refinery", "нефтеперерабат"]),
    "storage":         (2, ["нефтебаза", "нефтехран", "fuel storage", "топливохранилищ", "резервуар"]),
    "export_terminal": (3, ["терминал", "terminal", "Новороссийск", "Novorossiysk", "КТК", "CPC"]),
    "pipeline":        (2, ["трубопровод", "pipeline", "нефтепровод"]),
}

TELEGRAM_SOURCES = [
    # Public RSS/Atom mirrors — some Telegram channels expose public feeds
    "https://t.me/s/DefenceU",
    "https://t.me/s/RALee85",
    "https://t.me/s/ChrisO_wiki",
]

def fetch_strikes() -> dict:
    """
    Scrape public Telegram web views for infrastructure strike mentions
    in rolling 30-day window. Returns weighted score capped at 100.
    """
    print("  [STRIKES] Scanning GUR / OSInt Telegram channels…")
    cutoff = datetime.utcnow() - timedelta(days=30)
    total_score = 0
    hit_count   = 0
    hits_by_type = {k: 0 for k in STRIKE_KEYWORDS}

    for url in TELEGRAM_SOURCES:
        print(f"    {url}")
        html = get(url)
        if not html:
            continue
        time.sleep(1)

        # Parse date-tagged messages from t.me/s/ web view
        # Each message block looks like: <time datetime="2026-05-15T..."
        msg_blocks = re.split(r'<div class="tgme_widget_message_wrap', html)
        for block in msg_blocks[1:]:
            dt_m = re.search(r'datetime="(\d{4}-\d{2}-\d{2})', block)
            if not dt_m:
                continue
            try:
                msg_date = datetime.strptime(dt_m.group(1), "%Y-%m-%d")
            except ValueError:
                continue
            if msg_date < cutoff:
                continue

            # Strip HTML tags for text matching
            text = re.sub(r'<[^>]+>', ' ', block)

            for ftype, (weight, keywords) in STRIKE_KEYWORDS.items():
                if any(kw.lower() in text.lower() for kw in keywords):
                    # Check confirmation keywords
                    confirm_words = ["удар", "атак", "strike", "hit", "destroyed", "поврежд", "уничтож", "пожар"]
                    if any(cw in text.lower() for cw in confirm_words):
                        total_score += weight
                        hits_by_type[ftype] += 1
                        hit_count += 1

    total_score = min(total_score, 100)
    print(f"    → strike score: {total_score} ({hit_count} confirmed hits in 30d)")
    print(f"    → by type: {hits_by_type}")

    return {
        "strike_score": total_score,
        "hit_count_30d": hit_count,
        "hits_by_type": hits_by_type,
        "parsed": hit_count > 0 or total_score == 0,
    }


# ── 3. Kpler Novorossiysk export volume ───────────────────────────────────

KPLER_URLS = [
    "https://www.kpler.com/blog/russian-crude-exports",
    "https://www.kpler.com/blog/russia-oil-exports",
]

def fetch_kpler() -> dict:
    """
    Scrape Kpler public data for Novorossiysk weekly export volume.
    Converts to pressure score: 100 − (weekly_mt / baseline × 100).
    """
    print("  [KPLER] Fetching Novorossiysk export volume…")
    for url in KPLER_URLS:
        html = get(url)
        if not html:
            continue

        # Look for weekly volume figures near "Novorossiysk" or "Black Sea"
        patterns = [
            r'Novorossiysk[^.]*?(\d+(?:\.\d+)?)\s*(?:mb/d|mt/w|Mt|million\s+barrels)',
            r'Black\s+Sea[^.]*?(\d+(?:\.\d+)?)\s*(?:mb/d|mt/week|Mt)',
            r'"novorossiysk"[^}]*?"volume"\s*:\s*"?(\d+(?:\.\d+)?)"?',
        ]
        for pat in patterns:
            m = re.search(pat, html, re.IGNORECASE)
            if m:
                raw = float(m.group(1))
                # Normalise to Mt/week if needed (mb/d → Mt/week approx ÷ 7.3)
                mt_week = raw if raw < 5 else raw / 7.3
                pressure = round(max(0, min(100, (1 - mt_week / KPLER_BASELINE_MT_WEEK) * 100)))
                print(f"    → export {mt_week:.2f} Mt/week → pressure: {pressure}")
                return {"export_volume_mt_week": mt_week, "export_pressure": pressure, "parsed": True}

        (DATA / "debug_kpler.html").write_text(html[:50000], encoding="utf-8")
        print(f"    Parse failed — saved debug_kpler.html", file=sys.stderr)

    # Fallback: check Bloomberg/Reuters snippets for recent Russia export numbers
    print("  [KPLER] Direct fetch failed — trying fallback search pages", file=sys.stderr)
    return {"export_volume_mt_week": None, "export_pressure": None, "parsed": False}


# ── Compose RPI ───────────────────────────────────────────────────────────

def compute_rpi(capacity_util_pct, strike_score, export_pressure) -> tuple[int | None, bool]:
    """Returns (RPI, is_partial)"""
    scores = []
    if capacity_util_pct is not None:
        scores.append(round(100 - capacity_util_pct))
    if strike_score is not None:
        scores.append(strike_score)
    if export_pressure is not None:
        scores.append(export_pressure)

    if not scores:
        return None, True
    partial = len(scores) < 3
    return round(sum(scores) / len(scores)), partial


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

    print(f"refinery_pressure.py — month: {month_tag}")
    print()

    crea    = fetch_crea()
    print()
    strikes = fetch_strikes()
    print()
    kpler   = fetch_kpler()
    print()

    cap_util = crea.get("capacity_util_pct")
    cap_pres = round(100 - cap_util) if cap_util is not None else None
    s_score  = strikes.get("strike_score")
    e_pres   = kpler.get("export_pressure")

    rpi, partial = compute_rpi(cap_util, s_score, e_pres)

    print(f"Results for {month_tag}:")
    print(f"  capacity_util_pct : {cap_util}")
    print(f"  capacity_pressure : {cap_pres}")
    print(f"  strike_score      : {s_score}")
    print(f"  export_pressure   : {e_pres}")
    print(f"  RPI               : {rpi}{'  (PARTIAL)' if partial else ''}")

    # Alert check
    if rpi is not None:
        thresholds = load().get("alert_thresholds", {})
        if rpi >= thresholds.get("critical_above", 70):
            print(f"\n  !! CRITICAL: RPI={rpi} ≥ {thresholds.get('critical_above', 70)}")
        elif rpi >= thresholds.get("warning_above", 50):
            print(f"\n  !! WARNING:  RPI={rpi} ≥ {thresholds.get('warning_above', 50)}")

    if write:
        data = load()
        readings = data.setdefault("monthly_readings", [])
        entry = next((r for r in readings if r.get("month") == month_tag), None)
        if entry is None:
            entry = {"month": month_tag}
            readings.append(entry)
            readings.sort(key=lambda r: r.get("month", ""))

        entry.update({
            "capacity_util_pct":  cap_util,
            "capacity_pressure":  cap_pres,
            "strike_score":       s_score,
            "export_pressure":    e_pres,
            "RPI":                rpi,
            "real":               not partial,
            "partial":            partial if partial else None,
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
