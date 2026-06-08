# Black Sea Territorial Confidence Monitor

Early warning system tracking real estate market signals across the Russian-occupied Black Sea coastal corridor. Based on a three-dial model separating state commitment from private market and residential signals, expanded in v4.0 with independent Refinery Pressure and Civilian Confidence indices.

## Model architecture

**Three core dials per city:**
- **SCI** (State Commitment Index) — what Moscow deploys: federal budget, contractor mandates, subsidized mortgage cost. Not a confidence signal. Read against the A−B spread.
- **Track A** (private market) — non-state developer entry, cash ДКП transactions, asking price momentum.
- **Track B** (residential outcome) — secondary listing depth, buyer permanence composition, rental-to-purchase ratio.

**Composite Spread = Track B − (SCI×0.4 + Track A×0.6)**. Negative = composite outpaces residential reality (fragility signal). More negative = more fragile.

**Two independent system-level dials:**
- **RPI** (Refinery Pressure Index) — systemic pressure on Russian oil infrastructure. High = fiscal base of occupation funding under stress.
- **CCI** (Civilian Confidence Index) — acute civilian stress: fuel shortages, panic goods purchasing, grey market activation. Captures the 30-day survival bet as distinct from the 30-year permanence bet (Track B).

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
- **Avito** (avito.ru) — rental listing counts and grey market staple goods prices.

## Additional data sources — v4.0

**Refinery Pressure Index (RPI)**
- CREA (energyandcleanair.org) — monthly Russian refinery capacity utilization
- GUR Ukraine (@DefenceU Telegram) — confirmed infrastructure strikes
- OSInt channels (@RALee85, @ChrisO_wiki) — strike classification and confirmation
- Kpler public data — Novorossiysk weekly export volumes

**Civilian Confidence Index (CCI)**
- Rosstat (rosstat.gov.ru) — weekly retail fuel prices by federal subject including occupied oblasts
- Telegram community channels — Mariupol, Donetsk, Luhansk local groups — panic goods keyword monitoring
- Avito (avito.ru) — grey market staple goods price premium in occupied cities vs mainland

**Buckwheat signal rationale**
Buckwheat (гречка) is the most reliable panic purchasing indicator in the Russian/Ukrainian cultural space.
Documented shortage events: 2014 Crimea annexation, 2020 COVID, September 2022 mobilization announcement.
Disappears from retail within hours of genuine population-level fear. Grey market Avito activation
(гречка appearing at 2–5× retail price) indicates official supply chain failure. Monitor alongside
sugar, canned meat (тушёнка), and diesel canisters for compound signal confirmation.

## Update workflow

```bash
python fetch/restate.py --write       # pull latest Crimea biweekly reading
python fetch/domclick.py --write      # pull Donetsk and Luhansk listing counts
python fetch/avito_rental.py --write  # pull rental counts and median prices
python fetch/refinery_pressure.py --write  # CREA + strikes + Kpler
python fetch/civilian_confidence.py --write  # Rosstat + Telegram + Avito staples
python fetch/compute.py --write       # recalculate all scores → data/scores.json
```

Or run all at once:
```bash
bash update.sh
```

## Alert conditions

| Condition | Threshold | Interpretation |
|-----------|-----------|----------------|
| Spread ≤ −20 | Warning | Composite outpacing B — state+private well ahead of residential reality |
| Spread change ≥ +5 pts/period | Watch | Spread widening rapidly |
| Domclick surge > 50% baseline | Watch | Sellers exiting — market stress |
| Domclick collapse < 75% baseline | Watch | Market frozen |
| 3 consecutive Crimea price drops | Watch | Sustained price reversal |
| RPI > 50 | Warning | Meaningful fiscal pressure on occupation funding base |
| RPI > 70 | Critical | Acute threat to SCI sustainability |
| CCI > 25 | Watch | Elevated stress visible in informal channels |
| CCI > 45 | Warning | Multi-signal shortage confirmation |
| CCI > 65 | Critical | Buckwheat index activating — systemic civilian confidence failure |
| CCI rising + Permanence ratio stable | Divergence | Riding out shock, long-term bet intact |
| CCI rising + Permanence ratio falling | Compound | Behavioral change likely imminent |

## Scoring methodology version

Current: v4.0 (June 2026). RPI and CCI added as independent system-level dials. Three-dial model unchanged. Spread definition updated in v3.1: now B − (SCI×0.4 + A×0.6). See data/scores.json methodology_version for history.
