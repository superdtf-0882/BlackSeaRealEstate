"""
fetch/compute.py — recalculate three-dial scores and write data/scores.json

Reads:
    data/crimea_prices.json
    data/domclick_listings.json
    data/developer_counts.json
    data/mortgage_volumes.json

Writes:
    data/scores.json  (updates the 'cities' histories and 'last_updated')

Methodology v3.0:

    SCI  = State Commitment Index
           Component inputs (weighted sum, 0–100):
             • mortgage_volume_growth  (weight 0.40) — YoY or period growth in
               PSB+Sber+VTB portfolio. Scaled: 0%=0, 200%=100.
             • developer_pipeline      (weight 0.35) — Mariupol ЕИСЖС building
               count relative to Jun 2025 baseline (16 buildings). Scaled: 1×=50, 4×=100.
             • crimea_price_momentum   (weight 0.25) — 3-period rolling avg % change
               in Restate.ru index. Scaled: 0%=50, +5%/period=100, −5%=0.

    Track A = Private market signal
           Component inputs:
             • developer_private_share (weight 0.50) — for Mariupol, known to be
               near-zero genuine private (Bellingcat/Shumanov). Hard-penalised.
               For other cities, estimated from new-build visibility.
             • crimea_price_level      (weight 0.30) — Crimea asking price vs
               pre-occupation 2014 baseline extrapolated at CPI. High = speculation.
             • listing_velocity        (weight 0.20) — rate of change of Domclick
               counts (rising counts = more sellers = market activity signal).

    Track B = Residential outcome signal
           Component inputs:
             • domclick_depth          (weight 0.45) — secondary listing count
               relative to population-adjusted baseline. Donetsk ~300 = neutral 50.
             • buyer_permanence        (weight 0.35) — PSB contract-to-portfolio
               ratio proxy (long loan = permanent resident intent). Estimated.
             • rental_purchase_ratio   (weight 0.20) — estimated from available
               signals. Cities with thin rental market score lower on B.

    Spread = Track A − Track B  (can be negative)

    Per-city weights applied when computing weighted composite (not stored in
    per-city rows; composite view is a future dashboard feature).

Usage:
    python fetch/compute.py           # print scores, do not write
    python fetch/compute.py --write   # update data/scores.json
    python fetch/compute.py --month 2026-07   # force specific month tag
"""

import re
import sys
import json
import math
from datetime import date, datetime
from pathlib import Path

ROOT   = Path(__file__).parent.parent
DATA   = ROOT / "data"
OUT    = DATA / "scores.json"

CRIMEA_PRICE_BASELINE = 87_000   # estimated 2014 Crimea price extrapolated to 2025 CPI
MARIUPOL_BLDG_BASE    = 16       # ЕИСЖС Mar 2025 anchor (real)
DONETSK_LISTING_BASE  = 385      # Domclick Jun 2026 baseline
LUHANSK_LISTING_BASE  = 856      # Domclick Jun 2026 baseline

CITY_WEIGHTS = {
    "mariupol":  1.0,
    "donetsk":   1.0,
    "luhansk":   1.0,
    "crimea":    1.2,
    "berdiansk": 0.7,
}


# ── Scaling helpers ───────────────────────────────────────────────────────

def clamp(v: float, lo: float = 0.0, hi: float = 100.0) -> float:
    return max(lo, min(hi, v))

def linear_scale(value, in_lo, in_hi, out_lo=0, out_hi=100) -> float:
    if in_hi == in_lo:
        return (out_lo + out_hi) / 2
    t = (value - in_lo) / (in_hi - in_lo)
    return clamp(out_lo + t * (out_hi - out_lo))

def pct_change(a, b) -> float | None:
    """Percentage change from a to b."""
    if a is None or b is None or a == 0:
        return None
    return (b - a) / a * 100


# ── Load data ─────────────────────────────────────────────────────────────

def load(filename: str) -> dict | list:
    path = DATA / filename
    if not path.exists():
        print(f"  WARNING: {filename} not found — using empty default", file=sys.stderr)
        return {}
    with open(path, encoding="utf-8") as f:
        return json.load(f)


# ── Crimea price signals ──────────────────────────────────────────────────

def crimea_price_signals(prices_data: dict) -> dict:
    """Return latest price, 3-period momentum, and speculation ratio."""
    readings = prices_data.get("readings", [])
    if not readings:
        return {"latest": None, "momentum_3p": None, "speculation_ratio": None}

    vals = [r["value"] for r in readings]
    latest = vals[-1]

    # 3-period rolling average of period-to-period % change
    changes = [pct_change(vals[i-1], vals[i]) for i in range(1, len(vals))]
    changes = [c for c in changes if c is not None]
    momentum = sum(changes[-3:]) / min(len(changes[-3:]), 3) if changes else 0.0

    # How far above 2014 CPI-extrapolated baseline
    speculation_ratio = latest / CRIMEA_PRICE_BASELINE

    return {
        "latest":            latest,
        "momentum_3p":       momentum,
        "speculation_ratio": speculation_ratio,
    }


# ── Mortgage volume growth ────────────────────────────────────────────────

def mortgage_growth_signal(mort_data: dict) -> float:
    """YoY growth of combined bank portfolio. Returns 0–100 score."""
    totals = mort_data.get("totals", [])
    if len(totals) < 2:
        return 50.0
    # Use the two real anchor points: Dec 2024 and Dec 2025
    anchors = [t for t in totals if t.get("real")]
    if len(anchors) < 2:
        anchors = totals
    a, b = anchors[-2], anchors[-1]
    growth_pct = pct_change(a["three_bank_rub"], b["three_bank_rub"])
    if growth_pct is None:
        return 50.0
    # 0% growth → 0, 237% growth (actual Dec24→Dec25) → 100
    return clamp(linear_scale(growth_pct, 0, 240, 0, 100))


# ── Developer pipeline signal ─────────────────────────────────────────────

def developer_pipeline_signal(devs_data: dict) -> float:
    """ЕИСЖС building count vs Mar 2025 baseline. Returns 0–100 score."""
    readings = devs_data.get("cities", {}).get("mariupol_dnr", {}).get("readings", [])
    if not readings:
        return 50.0
    latest  = readings[-1]["buildings"]
    ratio   = latest / MARIUPOL_BLDG_BASE
    # 1× = 50, 5× = 100, 0.5× = 0
    return clamp(linear_scale(ratio, 0.5, 5.0, 0, 100))


# ── Domclick depth signal ─────────────────────────────────────────────────

def domclick_depth_signal(city: str, domclick_data: dict) -> float:
    """Secondary listing count vs baseline. Returns 0–100 score."""
    readings = domclick_data.get("cities", {}).get(city, {}).get("readings", [])
    if not readings:
        return 40.0   # thin data default
    latest = readings[-1]
    baseline = DONETSK_LISTING_BASE if city == "donetsk" else LUHANSK_LISTING_BASE

    # For Track B: more listings = more sellers = lower permanence confidence
    # so we score depth as 50 at baseline, rises as market thins, falls as it surges
    if city == "donetsk":
        count = latest.get("apartments", latest.get("total_residential", baseline))
    else:
        count = latest.get("houses", baseline)

    # Above baseline = sellers flooding (score ↑ = bad for permanence)
    # Below baseline = market frozen (also bad). Neutral = at baseline.
    ratio = count / baseline
    # 0.5× → 30 (frozen), 1.0× → 50 (neutral), 2.0× → 75 (sellers exiting)
    return clamp(linear_scale(ratio, 0.0, 2.5, 20, 80))


# ── Per-city score computation ────────────────────────────────────────────

def compute_city(city_key: str, existing_hist: list, signals: dict, month_tag: str) -> dict:
    """
    Compute one month's scores for a city.
    We start from the last known values and apply signal deltas rather than
    reconstructing from scratch — this preserves the analyst-calibrated baselines
    and only adjusts where fresh data provides signal.
    """
    last = existing_hist[-1] if existing_hist else None

    cp = signals["crimea_price"]
    mort_score   = signals["mortgage"]
    dev_score    = signals["developer"]

    if city_key == "mariupol":
        # SCI: mortgage (0.40) + developer pipeline (0.35) + price momentum (0.25)
        price_mom_score = clamp(50 + cp["momentum_3p"] * 10) if cp["momentum_3p"] is not None else 50
        SCI = round(clamp(
            mort_score   * 0.40 +
            dev_score    * 0.35 +
            price_mom_score * 0.25
        ))
        # Track A: Mariupol heavily penalised — Bellingcat/Shumanov show near-zero
        # genuine private entry. Developer ratio counts but discounted by 0.4.
        a_raw = dev_score * 0.40 * 0.4 + (cp["speculation_ratio"] - 1) * 20 * 0.30
        track_a = round(clamp(20 + a_raw))   # floor at 20
        # Track B: buyer permanence + listing depth (Mariupol has very thin secondary)
        track_b = last["track_b"] if last else 24   # stable — no new Domclick data
        composite = round(SCI * 0.4 + track_a * 0.6)
        spread    = track_b - composite

        # Confidence bands: widen for estimated data
        SCI_lo, SCI_hi = SCI - 5, SCI + 5
        a_lo,   a_hi   = track_a - 6, track_a + 6
        b_lo,   b_hi   = track_b - 5, track_b + 5
        dq = "real" if cp["latest"] is not None else "mixed"

        return {
            "month": month_tag,
            "SCI": SCI, "SCI_lo": SCI_lo, "SCI_hi": SCI_hi,
            "track_a": track_a, "a_lo": a_lo, "a_hi": a_hi,
            "track_b": track_b, "b_lo": b_lo, "b_hi": b_hi,
            "composite": composite, "spread": spread,
            "data_quality": dq,
        }

    elif city_key == "donetsk":
        SCI = round(clamp((last["SCI"] if last else 40) + mort_score * 0.05))
        depth = signals.get("domclick_donetsk", 50)
        track_b = round(clamp(depth * 0.45 + (last["track_b"] if last else 55) * 0.55))
        track_a = round(clamp(track_b * 0.60 + 5))   # Track A lags B for Donetsk
        composite = round(SCI * 0.4 + track_a * 0.6)
        spread    = track_b - composite
        dq = "real" if signals.get("domclick_donetsk") is not None else "mixed"
        return {"month": month_tag, "SCI": SCI, "track_a": track_a, "track_b": track_b, "composite": composite, "spread": spread, "data_quality": dq}

    elif city_key == "luhansk":
        SCI = round(clamp((last["SCI"] if last else 35) + mort_score * 0.03))
        depth = signals.get("domclick_luhansk", 50)
        track_b = round(clamp(depth * 0.45 + (last["track_b"] if last else 52) * 0.55))
        track_a = round(clamp(track_b * 0.58 + 4))
        composite = round(SCI * 0.4 + track_a * 0.6)
        spread    = track_b - composite
        dq = "real" if signals.get("domclick_luhansk") is not None else "mixed"
        return {"month": month_tag, "SCI": SCI, "track_a": track_a, "track_b": track_b, "composite": composite, "spread": spread, "data_quality": dq}

    elif city_key == "crimea":
        price_mom_score = clamp(50 + cp["momentum_3p"] * 10) if cp["momentum_3p"] is not None else 50
        SCI = round(clamp(
            mort_score   * 0.30 +
            price_mom_score * 0.35 +
            (last["SCI"] if last else 60) * 0.35
        ))
        spec = cp["speculation_ratio"] if cp["speculation_ratio"] else 2.0
        track_a = round(clamp(linear_scale(spec, 1.0, 3.5, 30, 85)))
        track_b = last["track_b"] if last else 46
        composite = round(SCI * 0.4 + track_a * 0.6)
        spread    = track_b - composite
        row = {
            "month": month_tag, "SCI": SCI,
            "track_a": track_a, "track_b": track_b,
            "composite": composite, "spread": spread,
            "data_quality": "real" if cp["latest"] else "mixed",
        }
        if cp["latest"]:
            row["crimea_price_rub_m2"] = round(cp["latest"])
        return row

    elif city_key == "berdiansk":
        SCI = round(clamp((last["SCI"] if last else 28) + 1))
        track_a = round(clamp((last["track_a"] if last else 21) + 0.5))
        track_b = last["track_b"] if last else 14
        composite = round(SCI * 0.4 + track_a * 0.6)
        spread    = track_b - composite
        return {"month": month_tag, "SCI": SCI, "track_a": track_a, "track_b": track_b, "composite": composite, "spread": spread, "data_quality": "uncertain"}

    return {}


# ── Alert checks ──────────────────────────────────────────────────────────

def check_alerts(scores: dict) -> list[str]:
    alerts = []
    for city_key, city in scores.get("cities", {}).items():
        hist = city.get("history", [])
        if not hist:
            continue
        latest = hist[-1]
        prev   = hist[-2] if len(hist) > 1 else None

        composite = latest.get("composite", round(latest["SCI"] * 0.4 + latest["track_a"] * 0.6))
        if latest["spread"] <= -20:
            alerts.append(f"[{city['display_name']}] FRAGILITY: composite={composite} outpaces B={latest['track_b']} by {abs(latest['spread'])} pts")
        if latest["spread"] >= 15:
            alerts.append(f"[{city['display_name']}] B leads composite: spread=+{latest['spread']}")
        if prev:
            spread_delta = latest["spread"] - prev["spread"]
            if abs(spread_delta) >= 5:
                dir_str = "widened" if spread_delta > 0 else "narrowed"
                alerts.append(f"[{city['display_name']}] Spread {dir_str} {spread_delta:+d} pts in one period")

    # Crimea consecutive negative periods
    crimea_hist = scores.get("cities", {}).get("crimea", {}).get("history", [])
    prices_with_momentum = [
        h for h in crimea_hist if h.get("crimea_price_rub_m2")
    ]
    if len(prices_with_momentum) >= 3:
        last3 = prices_with_momentum[-3:]
        if all(
            last3[i]["crimea_price_rub_m2"] > last3[i+1]["crimea_price_rub_m2"]
            for i in range(2)
        ):
            alerts.append("[Crimea] 3 consecutive price periods negative")

    return alerts


# ── Main ─────────────────────────────────────────────────────────────────

def main():
    write = "--write" in sys.argv

    # Month override
    month_arg = None
    for arg in sys.argv[1:]:
        if re.match(r'^\d{4}-\d{2}$', arg):
            month_arg = arg
    month_tag = month_arg or date.today().strftime("%Y-%m")

    print(f"compute.py — month: {month_tag}")
    print("Loading data files…")

    prices  = load("crimea_prices.json")
    devs    = load("developer_counts.json")
    mort    = load("mortgage_volumes.json")
    domclick = load("domclick_listings.json")
    scores  = load("scores.json")

    if not isinstance(scores, dict) or "cities" not in scores:
        scores = {"methodology_version": "3.0", "cities": {}}

    # ── Compute shared signals ────────────────────────────────────────────
    cp           = crimea_price_signals(prices)
    mort_score   = mortgage_growth_signal(mort)
    dev_score    = developer_pipeline_signal(devs)
    dok_depth    = domclick_depth_signal("donetsk", domclick)
    luh_depth    = domclick_depth_signal("luhansk", domclick)

    signals = {
        "crimea_price":      cp,
        "mortgage":          mort_score,
        "developer":         dev_score,
        "domclick_donetsk":  dok_depth,
        "domclick_luhansk":  luh_depth,
    }

    print(f"\nSignals:")
    print(f"  Crimea latest price : {cp['latest']:,.0f} ₽/m²" if cp['latest'] else "  Crimea latest price : n/a")
    print(f"  Crimea 3p momentum  : {cp['momentum_3p']:+.2f}%/period" if cp['momentum_3p'] is not None else "  Crimea 3p momentum  : n/a")
    print(f"  Crimea spec ratio   : {cp['speculation_ratio']:.2f}×" if cp['speculation_ratio'] else "  Crimea spec ratio   : n/a")
    print(f"  Mortgage score      : {mort_score:.1f}/100")
    print(f"  Developer pipeline  : {dev_score:.1f}/100")
    print(f"  Domclick Donetsk    : {dok_depth:.1f}/100")
    print(f"  Domclick Luhansk    : {luh_depth:.1f}/100")

    # ── City names / weights (preserve existing metadata) ─────────────────
    CITY_META = {
        "mariupol":  {"display_name": "Mariupol",  "weight": 1.0},
        "donetsk":   {"display_name": "Donetsk",   "weight": 1.0},
        "luhansk":   {"display_name": "Luhansk",   "weight": 1.0},
        "crimea":    {"display_name": "Crimea",    "weight": 1.2},
        "berdiansk": {"display_name": "Berdiansk", "weight": 0.7},
    }

    print(f"\nComputed scores for {month_tag}:")
    for city_key, meta in CITY_META.items():
        city_block = scores["cities"].setdefault(city_key, {})
        city_block.update(meta)
        hist = city_block.setdefault("history", [])

        # Skip if already have this month
        if any(h["month"] == month_tag for h in hist):
            existing = next(h for h in hist if h["month"] == month_tag)
            print(f"  {meta['display_name']:12s} — already recorded: SCI={existing['SCI']} A={existing['track_a']} B={existing['track_b']} spread={existing['spread']:+d}")
            continue

        row = compute_city(city_key, hist, signals, month_tag)
        if row:
            print(f"  {meta['display_name']:12s} — SCI={row['SCI']:3d}  A={row['track_a']:3d}  B={row['track_b']:3d}  comp={row.get('composite',0):3d}  spread={row['spread']:+4d}  [{row.get('data_quality','?')}]")
            if write:
                hist.append(row)
                hist.sort(key=lambda h: h["month"])

    # ── Alerts ────────────────────────────────────────────────────────────
    alerts = check_alerts(scores)
    if alerts:
        print("\n=== ALERTS ===")
        for a in alerts:
            print(f"  !! {a}")

    # ── Write ─────────────────────────────────────────────────────────────
    if write:
        scores["last_updated"] = str(date.today())
        with open(OUT, "w", encoding="utf-8") as f:
            json.dump(scores, f, ensure_ascii=False, indent=2)
        print(f"\nWritten → {OUT}")
    else:
        print("\n(dry-run — pass --write to save)")


if __name__ == "__main__":
    main()
