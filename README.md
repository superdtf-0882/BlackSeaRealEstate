# Black Sea Territorial Confidence Monitor

Early warning system tracking real estate market signals across the Russian-occupied Black Sea coastal corridor. Based on a three-dial model separating state commitment from private market and residential signals.

## Model architecture

**Three dials per city:**
- **SCI** (State Commitment Index) — what Moscow deploys: federal budget, contractor mandates, subsidized mortgage cost. Not a confidence signal. Read against the A−B spread.
- **Track A** (private market) — non-state developer entry, cash ДКП transactions, asking price momentum.
- **Track B** (residential outcome) — secondary listing depth, buyer permanence composition, rental-to-purchase ratio.

**Spread = Track A − Track B.** Positive = speculative optimism exceeds residential confidence. High SCI + wide spread = state sustaining a confidence gap neither private market nor locals independently produce.

## Cities monitored

| City | Weight | Primary signal | Data quality |
|------|--------|---------------|-------------|
| Mariupol | 1.0 | Track A (mostly SCI) | Mixed |
| Donetsk | 1.0 | Track B anchor | Mixed |
| Luhansk | 1.0 | Track B anchor | Mixed |
| Crimea | 1.2 | All three (most data) | Good |
| Berdiansk | 0.7 | Thin | Uncertain |

## Data sources

- **Restate.ru** (krym.restate.ru/graph/) — Crimea biweekly price index. Real data.
- **Домклик** (domclick.ru) — secondary listing counts for Donetsk and Luhansk. Real data.
- **GID.HOUSE** (gid.house/mariupol) — developer and building counts. Real data.
- **ЕИСЖС** (наш.дом.рф) — official developer registry. Quarterly real anchors.
- **ДОМ.РФ** (дом.рф/analytics/mortgage/) — monthly regional mortgage volumes. Real data.
- **PSB/VTB/Sberbank** — quarterly bank disclosures via Kommersant and RBC.

## Update workflow

```bash
python fetch/restate.py      # pull latest Crimea biweekly reading
python fetch/domclick.py     # pull Donetsk and Luhansk listing counts
python fetch/compute.py      # recalculate dial scores → data/scores.json
open index.html              # view updated dashboard
```

Or run all at once:
```bash
./update.sh
```

## Alert conditions

Defined in data/domclick_listings.json alert_thresholds. compute.py logs alerts when:
- Домклик listings surge >50% above baseline (sellers exiting)
- Домклик listings collapse >75% below baseline (market frozen)
- Crimea biweekly reading shows 3+ consecutive negative periods
- Spread widens more than 15 points in a single quarter

## Scoring methodology version

Current: v3.0 (June 2026). Track A decomposed from SCI following Bellingcat/Shumanov confirmation that Mariupol construction is state-patronage, not private market. See data/scores.json methodology_version for history.
