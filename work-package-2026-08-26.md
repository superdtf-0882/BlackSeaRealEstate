# Black Sea Monitor — Aug 26 Data Update (backlog: Aug 10 – Aug 26)

**Work package for Claude Code.** Prepared 2026-08-26. Source material: `digest-backlog-2026-08-10-to-08-26.md` (same directory), plus direct corroboration of the fiscal and export anchors listed at the end of that file.

---

## Scoring summary (approved)

| Dial | Before | After | Basis |
|---|---|---|---|
| Crimea Track A | 40 | **38** | Crimean Wind hotel occupancy −35% Jul / −30% Aug during peak season; NPR Aug 13 ground-truth ("no gasoline, no fuel, no power," stores and banks closed). August is the month a Crimea private market recovery would show. It did not. |
| Crimea Track B | 26 | **25** | Water cut off in 35 settlements, gasoline out at most stations again (Aug 16); hot school meals to be replaced with dry rations — civic services failure reaching education provisioning; Euro-2/3 fuel causing civilian vehicle breakdowns; Rosgvardia deployed to fuel stations in occupied Crimea. |
| Crimea composite | 49 | **48** | SCI(62)×0.4 + A(38)×0.6 = 24.8 + 22.8 = 47.6 → 48 |
| Crimea spread | −23 | **−23** | 25 − 48. *Unchanged — A and B fell together, so the fragility gap is flat while both sides deteriorate. Note this explicitly in the scoring note; it is a finding, not an oversight.* |
| Mariupol Track A | 29 | **29 (hold)** | DW confirms real transaction velocity — Mariupol leads occupied-territory mortgage volume, prices +33% YoY — but every buyer is on a 2% state mortgage requiring Russian citizenship. Per Methodology v3.0 (Bellingcat/Shumanov), state-subsidised settler purchasing is SCI expenditure, not private market signal. Raising Track A on this would collapse the SCI/Track A separation. |
| Mariupol Track B | 22 | **21** | Buyers insuring mortgages against war risks — the settler buyer population is itself pricing impermanence, a direct Track B signal. Aug 8 substation strike caused power and water failure with Koltsov acknowledging inability to restore; Aug 13–14 USF struck four Mariupol 110 kV substations (Misto-3, NS-2, Illich, Misto-6) and the GRS-1 gas distribution station. Original residents excluded from replacement units; ~900 further apartments listed for redistribution. |
| Mariupol composite | 54 | **54** | SCI(91)×0.4 + A(29)×0.6 = 36.4 + 17.4 = 53.8 → 54 (unchanged) |
| Mariupol spread | −32 | **−33** | 21 − 54 |
| Berdiansk Track B | 12 | **11** | Fourth and fifth confirmed rounds of energy strikes: 7+ substations across 150 kV and 110 kV tiers Aug 13–14; energy hubs Aug 10–11; substations near Berdiansk Aug 17–22 (ISW Aug 23); fuel/ammunition/logistics depots Aug 24–25. Infrastructure failure is now continuous rather than recurring. Held to −1 rather than −2 given `data_quality: uncertain` and 0.7 weight. |
| Berdiansk composite | 26 | **26** | SCI(31)×0.4 + A(22)×0.6 = 12.4 + 13.2 = 25.6 → 26 (unchanged) |
| Berdiansk spread | −14 | **−15** | 11 − 26 |
| Donetsk Track B | 58 | **58 (hold)** | Evidence is partisan-sourced only (NRC wage arrears, ATESH fuel diversion). Track B is the climate dial — it moves on Domclick listing depth and PSB buyer composition, not news. Logged as key_events with unverified tags plus an explicit corroboration trigger. |
| Luhansk Track B | 54 | **54 (hold)** | As above. |
| OFP | 70 | **74** | See the threshold note below. |
| OFP modulator | +4 | **+6** | 74 is in the 71–85 band. |
| RPI | 100 | **100** | Ceiling. |
| CCI | 100 | **100** | Ceiling. |
| ECS | 100 | **100** | Ceiling. |
| MTCS | 82 | **CC computes — expect 84** | Base 78 + modulator 6. |
| last_updated | 2026-08-09 | **2026-08-26** | |

### The OFP threshold crossing — read this before scoring

Last cycle set OFP 70 as the ceiling of the 56–70 band and named three specific triggers for crossing to 71+: emissions-supported OFZ auctions confirmed structural, liquid assets below 1% of GDP, or a missed occupation transfer payment. **None of those three fired.** The crossing is being made on a fourth fact of the same class, decided deliberately:

Minfin's Jan–July execution, published Aug 12, puts the federal deficit at **6.5 trillion rubles / 2.8% of GDP against a full-year target of 3.8 trillion — 1.7× the annual plan with five months still to run.** Planned annual spending was revised 44.1T → 45.1T. That is the outcome the three named triggers were proxies for, arriving directly rather than through its indicators.

The NWF component does **not** move. There was no Minfin NWF disclosure in this window; the Aug 6 release (Aug 1 data) remains the anchor and the next is expected ~Sept 3. Holding a monthly-anchor component flat when its anchor has not refreshed is the discipline that makes the other components' movement meaningful.

### OFP component detail

| Component | Weight | Before | After | Basis |
|---|---|---|---|---|
| export_revenue_proxy | 30% | 62 | **72** | CREA July (pub Aug 10): oil product loadings 4.7 Mt, **−23% MoM and the lowest on record**, under half July 2025's 9.6 Mt; product export revenue €116M/day, −45% MoM; total fossil export revenue €683M/day, −12% MoM; Urals $60.22 at a 26% ($21) discount, so price realisation ~0.74 against the README's 0.80 baseline. Bloomberg Aug 25: seaborne crude 3.46M bpd four-week average to Aug 23 (four-month low, fifth consecutive weekly decline); gross export value $1.65bn/week, −$80M; crude output 8.89M bpd, a six-year low and ~1M bpd below the OPEC+ quota. Novorossiysk loadings ~400k bpd vs 800k–1,000k in Jun/Jul; western-port exports 2.3M bpd against a 2.7M plan; zero crude loadings in the week to Aug 16. Both legs of the component — volume and price realisation — deteriorated simultaneously. |
| nwf_liquid_pct_gdp_score | 25% | 72 | **72 (hold)** | No new Minfin NWF disclosure this window. Next anchor ~Sept 3. |
| ofz_debt_stress | 20% | 63 | **66** | Jan–Jul deficit 1.7× the full-year target; defence ministry seeking an additional 3T rubles; Finance Ministry still withholding a detailed spending breakdown since May 2022. VEB.RF chief economist Klepach fired ~Aug 18 after publicly stating Russia "will not win" the attrition war — suppression of a state development bank's own chief forecaster is a sovereign-credibility signal, not merely a personnel event. |
| regional_budget_cuts | 15% | 55 | **57** | Crimea occupation authorities planning to replace hot school meals with dry rations — municipal fiscal strain reaching statutory child provisioning; Rosgvardia deployed to fuel stations across Russia and occupied Crimea (public-order expenditure substituting for supply); entry to occupied Kakhovka restricted. Marginal move; the component remains the thinnest-sourced of the five. |
| shadow_fleet_stress | 10% | 42 | **52** | Turkey's coastguard restricting/delaying Dardanelles transit licences for Novorossiysk-bound vessels (Aug 9) — institutional friction at the chokepoint itself, contested by Turkish officials but real. Suezmax *Skiros* struck at the CPC terminal Aug 16, ending a three-week lull and breaking the US-brokered understanding for Russian-cargo vessels. Barbados-flagged *RMS TEAM* abandoned by crew and Turkish-owned *VOLGO-BALT 226* damaged Aug 21 — third-country-flagged tonnage now being hit, which is what moves war-risk premiums. ISW: 36 vessels struck Aug 17–22; Operation MoLoChKa 218+ vessels since Jul 6; Kerch Strait blocked 30 consecutive days. |

Weighted computation: (72×0.30) + (72×0.25) + (66×0.20) + (57×0.15) + (52×0.10) = 21.6 + 18.0 + 13.2 + 8.55 + 5.2 = **66.55 → 67**.

Stored OFP is **74**, a **+7.45 judgment overlay** carrying forward the emissions-supported-OFZ / debt-monetisation assessment made on Aug 9. That overlay was +8.35 last cycle and is now smaller — the components are catching up to the qualitative judgment, which is the correct direction of travel. **Step 2 requires this to be recorded in the file itself, not just in prose.**

---

## Step 0 — Preflight

Read all current data files completely before touching anything:

- `public/data/scores.json`
- `public/data/refinery_pressure.json`
- `public/data/civilian_confidence.json`
- `public/data/occupation_financial_pressure.json`
- `public/index.html` seed data: `SEED_SCORES`, `SEED_RPI`, `SEED_CCI`, `SEED_OFP`. **`key_events` is not a separate top-level constant — it is a property inside `SEED_SCORES`** (opens around line 811, closes around 952). Grepping for `const key_events` will find nothing.

### The root `data/` tree is NOT a mirror — do not edit it

`data/*.json` is a **June vintage, wholly divergent from `public/data/`**, and every step in this package targets `public/` only:

| | `public/data/scores.json` | `data/scores.json` |
|---|---|---|
| `last_updated` | 2026-08-09T20:00:00Z | **2026-06-14** |
| `key_events` | 140 | **21** |
| Crimea 2026-06 | 40 / 26 / 49 / −23 | **58 / 46 / 60 / −14** |
| Mariupol 2026-06 | 29 / 22 / 54 / −32 | **31 / 24 / 55 / −31** |
| RPI / CCI | 100 / 100 | **83 / 77** |

Do not bump, append to, or reconcile `data/`. It is out of scope for this update.

### Deployment integrity — resolve before Step 15, do not assume

There are **two publish targets and they disagree**:

- `.github/workflows/jekyll-gh-pages.yml` builds with `source: ./` (repo **root**) and deploys to GitHub Pages **on every push to `main`**.
- `vercel.json` sets `"outputDirectory": "public"`.

Root `index.html` is **110,668 bytes with `SEED_SCORES.last_updated` = `2026-06-18`**. `public/index.html` is 188,754 bytes at `2026-08-09T20:00:00Z`. The live monitor at davidfacer.com currently displays "Data as of 2026-07-17", which matches **neither**.

Before pushing, determine what actually serves davidfacer.com/blackseamonitor/ — the Vercel `public/` build, the GitHub Pages root build, or a separate repo consuming the Vercel API (note `vercel.json` sets an `Access-Control-Allow-Origin` of `https://davidfacer.com`, and commit `14ad779` references a `davidfacer-archive` push). **Report the finding; do not attempt to fix the deployment as part of this work package.** If the root tree is genuinely live, that is a separate and higher-priority problem than this data update.

### Seed data is abridged, not identical

`SEED_*` constants in `public/index.html` are deliberately abridged first-paint fallbacks and have **never** matched the JSON files byte-for-byte — `SEED_SCORES` has no `methodology_version` or `scoring_notes`, 30 of its `key_events` labels are shortened, and the Crimea note is ~360 characters shorter than the file's. There is also a pre-existing numeric divergence: `SEED_RPI` carries `"strike_score":88` against 95 in `public/data/refinery_pressure.json` — **report this, do not silently fix it in this commit.**

Practical consequence: wherever a step says "append to the note", the seed note and the file note are **different baseline strings**. Append the same new text to each, against its own baseline. Do not copy the file's note over the seed's.

**Working-tree noise:** `git status` shows 16 modified files. This is a CRLF/LF line-ending artifact only — `git diff --stat --ignore-all-space` returns empty. Do not treat it as pending work and do not "fix" it as part of this commit. If it interferes, set `core.autocrlf` appropriately, but keep line-ending churn out of the data commit.

**Confirm current scored state before proceeding.** Stop and report if any of these do not match:

- `last_updated`: `2026-08-09T20:00:00Z`
- RPI 100, CCI 100, ECS 100 (all `2026-06` monthly readings)
- OFP 70, components 62 / 72 / 63 / 55 / 42, modulator +4
- Crimea: SCI 62, track_a 40, track_b 26, composite 49, spread −23
- Mariupol: SCI 91, track_a 29, track_b 22, composite 54, spread −32
- Berdiansk: SCI 31, track_a 22, track_b 12, composite 26, spread −14
- Donetsk: SCI 44, track_a 36, track_b 58, composite 39, spread 19
- Luhansk: SCI 38, track_a 33, track_b 54, composite 35, spread 19
- `key_events` length: **140**, last entries dated `2026-08-08`

Note the data model: `scores.json` has `cities` as an **object** keyed by city name, each with a `history` array of monthly entries. All city edits below target the `2026-06` entry in each city's `history` array — the same convention the Jul 17 and Aug 9 updates used. Do not create a `2026-08` entry.

---

## Step 1 — Bump `last_updated`

`"2026-08-09T20:00:00Z"` → `"2026-08-26T20:00:00Z"`.

Apply in `public/data/scores.json` and in `SEED_SCORES` in `public/index.html`. Grep for `2026-08-09T20:00:00Z` and confirm both occurrences are updated. Do **not** touch `data/scores.json` (see Step 0).

---

## Step 2 — OFP: 70 → 74, and document the override

In `public/data/occupation_financial_pressure.json` and `SEED_OFP` in `public/index.html`, update the `2026-06` entry:

- `export_revenue_proxy`: 62 → **72**
- `nwf_liquid_pct_gdp_score`: 72 → **72** (unchanged)
- `ofz_debt_stress`: 63 → **66**
- `regional_budget_cuts`: 55 → **57**
- `shadow_fleet_stress`: 42 → **52**
- `OFP`: 70 → **74**

**Add two new fields to this reading** so the gap between the components and the composite is explicit and auditable rather than looking like an arithmetic error:

```json
"computed_from_components": 66.55,
"override_rationale": "Stored OFP 74 carries a +7.45 judgment overlay above the weighted component computation (66.55). The overlay represents CBR emissions support for OFZ auctions - debt monetisation rather than market demand - which the five-component structure has no line item for and which the ofz_debt_stress component alone would overstate if forced to carry it. Overlay was +8.35 at the Aug 9 review and is narrowing as components catch up to the qualitative assessment. Reviewed and reaffirmed 2026-08-26."
```

Append to the `note` field:

> "Aug 26: OFP 70→74; modulator advances +4→+6 (71–85 band). Threshold crossed on Minfin Jan–Jul budget execution (pub Aug 12): federal deficit 6.5T rubles / 2.8% of GDP against a full-year target of 3.8T — 1.7× the annual plan with five months to run; revenue 22.1T, spending 28.6T (+14.5% YoY); planned annual spending revised 44.1T→45.1T, projecting a full-year deficit near 4.8T. None of the three triggers named on Aug 9 (structural emissions-supported OFZ auctions, liquid assets below 1% GDP, missed occupation transfer payment) fired; the crossing is made deliberately on the deficit blowout as a fact of the same class — the outcome those triggers were proxies for. NWF component held at 72: no Minfin NWF disclosure this window, Aug 6 release (Aug 1 data) remains the anchor, next expected ~Sept 3. Export revenue proxy 62→72 on CREA July data (pub Aug 10): oil product loadings 4.7Mt, −23% MoM and lowest on record, under half July 2025's 9.6Mt; product export revenue €116M/day −45% MoM; total fossil export revenue €683M/day −12% MoM; Urals $60.22 at 26% ($21) discount, price realisation ~0.74 vs 0.80 baseline. Bloomberg Aug 25: seaborne crude 3.46M bpd four-week average (four-month low, fifth consecutive weekly decline), gross export value $1.65bn/week (−$80M), crude output 8.89M bpd (six-year low, ~1M bpd below OPEC+ quota). Novorossiysk loadings ~400k bpd vs 800k–1,000k Jun/Jul; western-port exports 2.3M bpd vs 2.7M plan; zero crude loadings week ending Aug 16. OFZ 63→66 on the deficit and on VEB.RF chief economist Klepach's dismissal (~Aug 18) after stating Russia 'will not win' the attrition war. Shadow fleet 42→52: Turkish Dardanelles transit restrictions (Aug 9), Skiros struck at CPC terminal Aug 16 ending the three-week lull, third-country-flagged RMS TEAM abandoned and VOLGO-BALT 226 damaged Aug 21, 36 vessels struck Aug 17–22, Kerch Strait blocked 30 consecutive days. Counter-signal logged and rejected as an anchor: a European intelligence source cited by Ukraine Business News (Aug 20) claims Urals averaged $82/bbl in Q2 adding ~$30bn in export revenue and fiscal runway to spring 2027 — this conflicts with CREA's $60.22 July figure; CREA is the methodology's named source for this component and the $82 figure is treated as a Q2 average at best, not an August anchor. Next watch: liquid assets below 1% GDP at the ~Sept 3 Minfin disclosure, or OFP above 85 (modulator +8). Sources: Minfin via Interfax/NV Aug 12, CREA monthly analysis Aug 10, Bloomberg Aug 25, Reuters Aug 17 and Aug 19, ISW Aug 19–23, Firstpost Aug 18."

---

## Step 3 — Crimea: Track A 40 → 38, Track B 26 → 25

In the `2026-06` entry of `cities.crimea.history` (both `scores.json` files and `SEED_SCORES`):

- `track_a`: 40 → **38**
- `track_b`: 26 → **25**
- `composite`: 49 → **48**   (SCI 62 × 0.4 + 38 × 0.6 = 24.8 + 22.8 = 47.6 → 48)
- `spread`: −23 → **−23**   (25 − 48; unchanged)

Append to the `note`:

> "Aug 26: Track A 40→38. Crimean Wind (Aug 19, via ISW) reports hotel occupancy in occupied Crimea down roughly 35% in July and 30% in August [unverified — Ukrainian partisan source]. August is the month in which any Crimea private-market recovery would have to appear; peak season produced no bounce off the Aug 9 floor. NPR Aug 13 provides independent English-language ground truth — a resident describing 'no gasoline, no fuel, no power,' with stores and banks closed. Fuel availability nationally at 28% of stations (ISW Aug 19, citing Izvestia/GdeBENZ); Rosgvardia paramilitary units deployed to fuel stations across Russia and occupied Crimea to manage civil unrest. No new Restate.ru transaction data — see Step 10. | Aug 26: Track B 26→25. Water cut off in 35 settlements and gasoline out at most peninsula filling stations again as of Aug 16 (intent.press); occupation authorities planning to replace hot school meals with dry rations (intent.press Aug 17) — civic services failure now reaching statutory child provisioning, a category not previously logged. Mandatory Euro-2/Euro-3 fuel is causing civilian vehicle breakdowns (ISW Aug 21) — the rationing regime is now damaging the private capital stock, not merely restricting access to it. Krymenergo and Sevastopolenergo on restricted schedules; Balaklava TPP struck Aug 13–14 with Razvozhayev confirming city-wide outages. | Aug 26: Crimea spread holds at −23 despite both tracks falling. Track A and Track B declined together, so the composite fell in step with residential reality and the fragility gap is flat. This is a finding, not an omission: Crimea's deterioration this cycle is uniform across state, private and residential signals rather than divergent, which is what a market completing its exit looks like rather than one still separating."

---

## Step 4 — Mariupol: Track A holds 29, Track B 22 → 21

In the `2026-06` entry of `cities.mariupol.history`:

- `track_a`: **29 (unchanged — do not edit)**
- `track_b`: 22 → **21**
- `composite`: **54 (unchanged)**   (SCI 91 × 0.4 + 29 × 0.6 = 36.4 + 17.4 = 53.8 → 54)
- `spread`: −32 → **−33**   (21 − 54)

Append to the `note`:

> "Aug 26: Track A holds at 29 — deliberately, against new transaction data. DW's Aug 14–15 investigation is the richest Mariupol market evidence in the dataset: contractor Su-2007 has completed multiple 12–15 storey blocks (Leningradsky Kvartal) on cleared sites where residents were killed or displaced in 2022; apartments sell at 7.5–10M rubles (€104,000+); Mariupol leads all occupied cities in mortgage loan volume per Russian banking statistics; prices are up roughly one third year-on-year per economist Vyacheslav Shiryaev. Every one of those transactions runs through the 2% state mortgage, capped at 6M rubles, requiring Russian citizenship and a 2% deposit, with buyers drawn from security personnel, officials and military logistics workers. Under Methodology v3.0 (Bellingcat Nov 2025 / Shumanov) this is state expenditure projecting permanence, not private capital expressing confidence, and it belongs to SCI. Scoring it into Track A would collapse the SCI/Track A separation that the methodology exists to maintain. Recorded here so the hold is legible as a judgment rather than an oversight. | Aug 26: Track B 22→21. DW confirms buyers are insuring their mortgages against war risks — the settler buyer population is itself pricing impermanence, which is the most direct Track B signal available and the first time the buyer side has been observed hedging. Original residents received no units in the replacement stock and some were ordered out of surviving apartments into hostels or the city outskirts; approximately 900 further apartments are listed for redistribution. Infrastructure: Aug 8 substation strike caused confirmed power and water failure with occupation head Koltsov acknowledging inability to fully restore services; Aug 13–14 USF struck four Mariupol 110 kV substations (Misto-3, NS-2, Illich, Misto-6) and the GRS-1 gas distribution station. Mariupol City Council has won $34.12M across 16 judgments against Russia for destroyed municipal property with 40 further assessments pending (UA News Aug 17) — the legal overhang on title is now quantified and growing. | Aug 26: SCI holds at 91. EJIL:Talk (Aug 26) confirms the 2% programme runs to 2030 with 6,000+ loans issued by late 2025 and continued growth, and that Federal Constitutional Law No. 4-FKZ (Dec 2025) enables redistribution of confiscated Ukrainian property to Russian citizens; official territorial planning projects an additional 113,800 residents across the occupied oblasts by 2045. This is consistent with 91 rather than a step-change above it."

---

## Step 5 — Berdiansk: Track B 12 → 11

In the `2026-06` entry of `cities.berdiansk.history`:

- `track_b`: 12 → **11**
- `composite`: **26 (unchanged)**   (SCI 31 × 0.4 + 22 × 0.6 = 12.4 + 13.2 = 25.6 → 26)
- `spread`: −14 → **−15**   (11 − 26)

Append to the `note`:

> "Aug 26: Track B 12→11. Fourth and fifth confirmed rounds of energy infrastructure strikes in six weeks: energy hubs struck Aug 10–11 as part of a 43-target USF operation; at least seven substations across 150 kV and 110 kV tiers struck Aug 13–14 under Crimean Switch Off, including repeated hits on the Berdiansk and Morska nodes; electrical substations near Berdiansk struck again in the Aug 17–22 window (ISW Aug 23); fuel, ammunition and logistics depots at Berdiansk and Prymorsk struck Aug 24–25. Infrastructure failure in Berdiansk is now continuous rather than episodic or even recurring — the city has no observed interval of restored normal service across the period. Held to −1 rather than the −2 suggested by the Aug 14 digest, on the discipline that Berdiansk carries data_quality 'uncertain' and a 0.7 city weight; a two-point move on thin data would propagate into MTCS with more confidence than the sourcing supports."

---

## Step 6 — Donetsk and Luhansk: hold, log as watch condition

**Do not change any Donetsk or Luhansk values.** Two digests recommended −2 on Track B for each. That is declined this cycle.

Append to `scoring_notes.track_b` in `public/data/scores.json`. The Donetsk and Luhansk `2026-06` entries have no `note` field, so `scoring_notes.track_b` is the correct home. **There is no seed target for this** — `SEED_SCORES` has only `last_updated`, `cities` and `key_events`, with no `scoring_notes` key. Do not add one; the note lives in the JSON file alone.

> "Aug 26 — Donbas Track B watch condition (Donetsk 58, Luhansk 54, both held). Two independent signals this window point downward, both partisan-sourced and neither corroborated: the National Resistance Center (Aug 9) reports occupation administrations across the occupied territories exploiting unemployment and months-long wage arrears to recruit civilians into the Russian army under false pretenses; ATESH (Aug 26) reports commanders of the 70th Motorized Rifle Division selling military fuel allocations to civilians in Donetsk, Luhansk and Rostov-on-Don at prices from 300 rubles per litre. If the ATESH report is corroborated it would be the first confirmed acute fuel-access failure in the Donbas cities at Crimea intensity, and grey-market fuel reaching the captive population matters more than the same signal in Crimea: per the README's Donbas caveat, Track B there measures a residual self-selected population whose participation reflects a prior political commitment, so movement in it is categorically more acute than movement elsewhere. Three Galaktika shopping-centre fires in a single month (Makiivka Aug 9–10, Yenakiieve Aug 14, Donetsk Aug 16, the last with eyewitness drone flyovers) add commercial-stock attrition alongside the already-logged Aug 8 school and kindergarten closures. Track B is nonetheless the climate dial and moves on Domclick listing depth and PSB/VTB buyer composition, not on news or partisan reporting. Explicit corroboration trigger for the next cycle: a second independent source on the fuel diversion, or any Domclick listing-count or PSB disclosure movement in Donetsk or Luhansk. If either arrives, move both to 56/52 and note that the trigger was pre-registered here."

---

## Step 7 — RPI note (ceiling holds at 100)

No numeric change. Append to the `2026-06` note in `public/data/refinery_pressure.json` and `SEED_RPI`:

> "Aug 10–26: RPI holds at 100 (ceiling). Reuters tracker Aug 11 confirms 15+ major refining facilities struck or halted since late June — Orsk (6M t/yr), TANECO (17M t/yr), ZapSibNeftekhim (2.5M t/yr), Yaroslavl (15M t/yr), Volgograd Lukoil (13.5M t/yr, halted since Jul 31), Saratov (5.8M t/yr, halted Aug 2), Ryazan (13.1M t/yr, halted Jul 29), Perm (12.6M t/yr, one CDU down), Tyumen (6M t/yr, halted). S&P Global via United24: 26 facilities knocked offline in 2026, only 8 returned to full operations by late July, 11 partial, 7 idle. Orsk confirmed a full halt with the governor stating repairs could take up to six months due to imported equipment under sanctions. Further strikes: Gazprom Neftekhim Salavat (7.5–10M t/yr) Aug 12–13, its second of 2026; Ufa/Bashneft AVT-6 primary refining unit destroyed Aug 18–19; Lukoil Permnefteorgsintez Aug 20–21; Lukoil NORSI Kstovo — Russia's fourth-largest refinery and second-largest gasoline producer — Aug 25–26, alongside a Wildberries hub at Kotovsk burning over 100,000 m², both executed by Fire Point FP-1 drones in a single night. Export infrastructure: Novorossiysk naval harbour struck Aug 11–12 with fires at the Grushovaya oil depot and four warships damaged; Sheskharis crude exports suspended Aug 14, resumed Aug 17; Russian Railways cargo loading restrictions at Novorossiysk Aug 13–22; all three Novorossiysk grain terminals halted, with KSK (40%+ of Novorossiysk grain throughput) suspending Aug 15; Moscow Times Aug 17 puts over 90% of Azov–Black Sea grain export capacity offline at peak harvest, threatening $15bn in annual revenue. Novorossiysk loadings fell to ~400k bpd against 800k–1,000k in Jun/Jul with zero crude loadings in the week to Aug 16. ISW Aug 23: 267 power plants struck since Aug 1 (27 in Aug 17–22 alone) and 36 vessels in the same window, including the 500 kV Taman substation, a key node for power transfer to Crimea. Qualitative escalation worth recording despite the ceiling: leaked communications from Moscow Deputy Mayor Gorbenko's office show officials privately conceding Russia cannot defend Moscow's refineries and proposing decentralised mini-refinery networks; Putin signed a decree Aug 25 authorising temporary state control of critical infrastructure whose private owners fail to protect or rebuild it, which analyst Abbas Gallyamov characterised as an ultimatum to refinery owners. Russia is importing refined product at scale — Belarus rail shipments up 25-fold Jan–Jul YoY, an Oman-flagged cargo of ~68,000 t of Indian gasoline discharged at Vitino, further Indian and Kazakh volumes en route. **Ceiling note: the index cannot differentiate further at this range. Three structurally new target categories emerged this window — grain export infrastructure, third-country-flagged tonnage, and Black Sea Fleet surface combatants with confirmed multi-year repair timelines (Militarnyi satellite analysis Aug 19: Admiral Makarov and Admiral Essen 3S14 VLS damaged, Kalibr capability likely lost). None of these can be expressed in the dial. Flag for the v5.1 methodology review: RPI needs either a higher ceiling or a separate export-corridor sub-index.**"

---

## Step 8 — CCI note (ceiling holds at 100)

No numeric change. Append to the `2026-06` note in `public/data/civilian_confidence.json` and `SEED_CCI`:

> "Aug 10–26: CCI holds at 100 (ceiling). Crimea: fuel sales reduced at TES and Atan with diesel capped at 109 rubles/litre for the week of Aug 9–15, occupation head Gotsanyuk deferring increases to the 'next shipment'; gasoline out at most peninsula stations again by Aug 16 with electricity rationed and water cut off in 35 settlements; occupation authorities planning to replace hot school meals with dry rations; mandatory Euro-2/Euro-3 fuel now causing civilian vehicle breakdowns — the rationing regime is damaging the private capital stock, not merely restricting access; Krymenergo and Sevastopolenergo on restricted schedules; Balaklava TPP struck Aug 13–14 with Razvozhayev confirming city-wide outages; inflation surging with fuel prices reported more than tripled (mezha.net Aug 25); explosions and power outages again Aug 26. NPR Aug 13 carries independent ground truth — a resident describing 'no gasoline, no fuel, no power' with stores and banks closed. National context: fuel available at only 28% of Russian filling stations as of Aug 18 (ISW citing Izvestia/GdeBENZ); purchase caps at Rosneft 30 L, Gazprom Neft 40–60 L, Tatneft 50 L; kilometre-long queues in Moscow; **Rosgvardia paramilitary units deployed to filling stations in Moscow Oblast and at least 13 stations across Russia and occupied Crimea to manage fuel-related civil unrest — armed public-order deployment to civilian retail supply is a category not previously logged.** Occupied corridor: complete simultaneous power and water failure in Mariupol Aug 8 with Koltsov conceding services cannot be fully restored; grain carriers refusing to enter occupied agricultural territories on drone risk, harvest accumulating unsold and agricultural enterprises pushed toward bankruptcy (Ukraine Business News Aug 14); three Galaktika shopping-centre fires in one month (Makiivka Aug 9–10, Yenakiieve Aug 14, Donetsk Aug 16); entry to occupied Kakhovka restricted Aug 24. Freedom House rated Russian-occupied Ukrainian territory at −1/100, below North Korea's 3/100 (KHPG Aug 10). **Ceiling does not mean stabilisation. The distress is also now migrating: the ATESH report of military fuel sold into Donetsk and Luhansk civilian grey markets at 300 rubles/litre (Aug 26) would, if corroborated, be the first acute fuel-access failure in the Donbas cities at Crimea intensity — see the Donbas Track B watch condition in scoring_notes.**"

---

## Step 9 — Add `key_events`

Append the following after the existing `2026-08-08` entries, then re-sort the array by date ascending. Add to **`public/data/scores.json`** and to the `key_events` property **inside `SEED_SCORES`** in `public/index.html`. Do **not** touch `data/scores.json` (see Step 0) — appending there would produce 57 entries against a 21-entry June baseline, not 176.

Note that 30 of the existing seed `key_events` labels are abridged relative to the file. Append the new entries in full to both; do not retro-expand the existing abridged ones in this commit.

```json
{"date":"2026-08-10","label":"CREA monthly analysis: Russian oil product loadings 4.7M tonnes in July — lowest on record, −23% MoM and under half July 2025's 9.6M tonnes; product export revenue €116M/day (−45% MoM); total fossil fuel export revenue €683M/day (−12% MoM); Urals averaged $60.22/bbl at a 26% ($21) discount to Brent (CREA Aug 10)","category":"macro","significance":"high"},
{"date":"2026-08-10","label":"Freedom House Freedom in the World 2026 rates Russian-occupied Ukrainian territory at −1/100 — below North Korea's 3/100 — citing deliberate demographic change through Russian resettlement, forced passportization and systematic persecution of Ukrainian and Crimean Tatar identity; anonymous 'treason' convictions accelerating, including 12- and 14-year sentences for two women from Berdiansk and Tokmak for donations to Ukrainian forces (KHPG Aug 10)","category":"policy","significance":"high"},
{"date":"2026-08-10","label":"Ukrainian substation strike causes confirmed power and water outages in occupied Mariupol Aug 8; occupation head Koltsov publicly acknowledges inability to fully restore services (ISW Aug 9)","category":"civilian","significance":"high"},
{"date":"2026-08-10","label":"Turkey's coastguard temporarily restricts Dardanelles transit licences for Novorossiysk-bound vessels after attacks on civilian ships including two Turkish vessels struck Aug 3; Turkish officials state passage continues under Montreux Convention terms — institutional friction at the chokepoint governing access to Russia's primary crude export artery. Kerch Strait blocked by Operation MoLoChKa for 30 consecutive days (Anewz/Reuters/ISW Aug 9)","category":"infrastructure","significance":"high"},
{"date":"2026-08-11","label":"National Resistance Center: occupation administrations across occupied territories exploiting unemployment and months-long wage arrears to recruit civilians into the Russian army under false promises of safe rear-area service [unverified — Ukrainian partisan source] (UNN/NRC Aug 9)","category":"civilian","significance":"medium"},
{"date":"2026-08-12","label":"Ukraine strikes Novorossiysk naval harbour overnight Aug 11–12 with Neptune missiles, Palianytsia drones and naval drones: four Russian warships damaged (frigates Admiral Makarov and Admiral Essen, a Buyan-M missile ship, patrol ship Vasil Bykov), NASA FIRMS confirming fires across navy piers and the adjacent Grushovaya oil depot; Novorossiysk grain elevator struck, 2 killed and 13 injured — largest confirmed Black Sea Fleet damage since relocation to Novorossiysk began (Kyiv Independent/Reuters/Censor.NET Aug 12)","category":"infrastructure","significance":"high"},
{"date":"2026-08-12","label":"Minfin Jan–July budget execution: federal deficit 6.5 trillion rubles ($78.9bn) or 2.8% of GDP against a full-year target of 3.8 trillion (1.6% of GDP) — 1.7× the annual plan with five months remaining; revenue 22.1T, spending 28.6T (+14.5% YoY); planned annual spending revised 44.1T→45.1T, projecting a full-year deficit near 4.8T; Finance Ministry has withheld a detailed federal spending breakdown since May 2022 (Minfin via Interfax/NV Aug 12)","category":"macro","significance":"high"},
{"date":"2026-08-12","label":"Mandatory Russian textbook series 'History of Our Region: Donbas and Novorossiya' added to the federal curriculum for grades 5–7 across occupied Donetsk, Luhansk, Zaporizhzhia and Kherson, compulsory from Sept 1 2026 — formal Russification milestone in institutional infrastructure supporting the long-horizon demographic engineering thesis (Euromaidan Press/Intent Press Aug 11)","category":"policy","significance":"high"},
{"date":"2026-08-12","label":"Reuters tracker confirms 15+ major Russian refining facilities struck or halted since late June, including Orsk (6M t/yr), TANECO (17M t/yr), Yaroslavl (15M t/yr), Volgograd Lukoil (13.5M t/yr, halted since Jul 31), Saratov (halted Aug 2) and Ryazan (halted Jul 29); S&P Global: 26 facilities offline in 2026 with only 8 returned to full operations by late July; Belarus gasoline rail imports up 25-fold Jan–Jul YoY (Reuters/United24 Aug 11)","category":"macro","significance":"high"},
{"date":"2026-08-14","label":"USF strikes 29 energy nodes overnight Aug 13–14 under Crimean Switch Off: Balaklava TPP in Sevastopol, four Mariupol 110 kV substations (Misto-3, NS-2, Illich, Misto-6), the GRS-1 Mariupol gas distribution station, and at least seven Berdiansk substations across 150 kV and 110 kV tiers; Razvozhayev confirms city-wide Sevastopol outages (Ukrainska Pravda/Mezha.net/USF Brovdi Aug 14)","category":"infrastructure","significance":"high"},
{"date":"2026-08-14","label":"Orsk refinery confirms full operational halt after the Aug 11 strike, with the governor stating repairs could take up to six months due to imported equipment under sanctions; Orenburg region introduces fuel rationing; more than 50 Russian regions now under some form of fuel restriction (EA WorldView/ISW Aug 13–14)","category":"infrastructure","significance":"high"},
{"date":"2026-08-14","label":"FSB begins dismantling the internal border zone separating Russia from annexed Ukrainian territories in Rostov, Voronezh and Crimea, citing 'completed annexation' of Donetsk, Luhansk and Kherson despite Russia lacking full control of any of the four claimed oblasts; Ukraine's CEC declares the planned Sept 20 Duma elections in the occupied territories illegitimate (Meduza/Agentstvo Aug 13, UNN Aug 13)","category":"policy","significance":"high"},
{"date":"2026-08-14","label":"Grain carriers refusing to enter occupied agricultural territories due to drone threat; harvested grain accumulating unsold in warehouses and agricultural enterprises pushed toward bankruptcy — occupied-territory agricultural commerce failure is a new category of civilian economic distress (Center of National Resistance via Ukraine Business News Aug 14)","category":"civilian","significance":"medium"},
{"date":"2026-08-15","label":"DW investigation: contractor Su-2007 has built multiple 12–15 storey blocks (Leningradsky Kvartal) on cleared central Mariupol sites where residents were killed or displaced in 2022; apartments sell at 7.5–10M rubles (€104,000+) under the 2% state mortgage — Russian citizenship required, 2% minimum deposit, 6M ruble cap — to security personnel, officials and military logistics workers; Mariupol leads all occupied cities in mortgage volume and prices are up roughly one third YoY; buyers are insuring mortgages against war risks; original residents received no units and some were ordered out of surviving apartments into hostels or the outskirts (DW Aug 14–15)","category":"policy","significance":"high"},
{"date":"2026-08-15","label":"Sheskharis crude export terminal at Novorossiysk suspends operations Aug 14 after Aug 12 strikes damaged main berths, storage reaching capacity with one tanker moving to sea rather than loading; KSK grain terminal — handling over 40% of Novorossiysk grain exports — halts Aug 15 with all three Novorossiysk grain terminals suspended simultaneously; Russian Railways imposes cargo loading restrictions at Novorossiysk Aug 13–22 (Reuters/NV Ukraine/UA News/ISW Aug 15)","category":"infrastructure","significance":"high"},
{"date":"2026-08-16","label":"Third Galaktika chain shopping centre fire in occupied Donetsk oblast within one month — Makiivka Aug 9–10, Yenakiieve Aug 14, Donetsk Kuibyshevskyi district Aug 16 with eyewitness drone flyovers reported before the fire (RBC Ukraine/ASTRA Aug 16)","category":"civilian","significance":"medium"},
{"date":"2026-08-17","label":"Moscow Times: more than 90% of Russia's grain export capacity in the Azov–Black Sea basin is offline — all three Novorossiysk terminals, the Taman terminal and Sea of Azov navigation all suspended at peak harvest, threatening $15bn in annual Russian grain export revenue (Moscow Times Aug 17)","category":"macro","significance":"high"},
{"date":"2026-08-17","label":"Greek-flagged Suezmax tanker Skiros struck by drone at the CPC terminal near Novorossiysk on the evening of Aug 16 after loading Russian-origin crude — first CPC-terminal vessel strike after a near three-week lull, confirming the US-brokered understanding did not extend to Russian-cargo vessels; cumulative disruption has cut CPC shipments by roughly 600,000 bpd against May; Sheskharis resumed loadings Aug 17 (Bloomberg/Meduza/Reuters Aug 17–18)","category":"infrastructure","significance":"high"},
{"date":"2026-08-18","label":"Occupied Crimea: gasoline out at most filling stations again as of Aug 16, electricity rationed and water cut off in 35 settlements; occupation authorities planning to replace hot school meals with dry rations — civic services failure reaching statutory child provisioning (intent.press Aug 16–17)","category":"civilian","significance":"high"},
{"date":"2026-08-18","label":"VEB.RF chief economist Andrei Klepach dismissed after publicly stating Russia 'will not win' its war of attrition and citing losses from Ukrainian strikes on ports, oil and gas facilities, chemical plants and logistics as a 'significant macroeconomic barrier'; suppression of a state development bank's own chief forecaster read as a sovereign-credibility signal (Firstpost Aug 18, Ukrainska Pravda/Moscow Times Aug 16)","category":"macro","significance":"high"},
{"date":"2026-08-19","label":"Ukrainian Neptune cruise missiles strike the Kamensky Combine in Rostov Oblast Aug 16, destroying two explosive and gunpowder production workshops and damaging four more — the facility produces solid rocket fuel for Uragan, Smerch and Tornado-S systems, a new upstream military-industrial target category beyond refining (Ukrainska Pravda/Censor.NET Aug 17)","category":"infrastructure","significance":"medium"},
{"date":"2026-08-19","label":"Mariupol City Council confirms $34.12M won across 16 court judgments against Russia for destroyed municipal property, with 40 further assessments pending — quantified and growing legal overhang on title in the occupied city (UA News Aug 17)","category":"policy","significance":"medium"},
{"date":"2026-08-21","label":"Fuel available at only 28% of Russian filling stations as of Aug 18; purchase caps reinstated nationally (Rosneft 30L, Gazprom Neft 40–60L, Tatneft 50L gasoline/60L diesel); Rosgvardia paramilitary units deployed to filling stations in Moscow Oblast and at least 13 stations across Russia and occupied Crimea to manage fuel-related civil unrest — armed public-order deployment to civilian retail supply (ISW citing Izvestia/GdeBENZ and Moscow Times Aug 19)","category":"civilian","significance":"high"},
{"date":"2026-08-21","label":"Hotel occupancy in occupied Crimea down roughly 35% in July and 30% in August on combined fuel shortages, power disruption and logistical collapse [unverified — Ukrainian partisan source] — peak season produced no recovery in the private market (Crimean Wind via ISW Aug 19)","category":"civilian","significance":"high"},
{"date":"2026-08-21","label":"Russian oil exports from western ports fall to ~2.3M bpd in the first half of August, 15% below the 2.7M bpd plan; Novorossiysk loadings collapse to roughly 400,000 bpd against 800,000–1,000,000 bpd in June and July, running more than two weeks behind schedule with zero tanker crude loadings in the week ending Aug 16; seaborne crude exports at 3.58M bpd for the four weeks to Aug 16, a fifth consecutive weekly decline (Reuters Aug 19, Ukraine Business News Aug 20)","category":"macro","significance":"high"},
{"date":"2026-08-21","label":"Satellite imagery analysis indicates Black Sea Fleet frigates Admiral Makarov and Admiral Essen, struck at Novorossiysk Aug 12, sustained damage to their 3S14 vertical launch systems and may have lost Kalibr missile capability, with repairs likely exceeding one year; Ufa/Bashneft AVT-6 primary refining unit destroyed overnight Aug 18–19 (Militarnyi Aug 19, ISW/CriticalThreats Aug 19)","category":"infrastructure","significance":"high"},
{"date":"2026-08-22","label":"Civilian vehicles breaking down across occupied Crimea due to mandatory lower-grade Euro-2 and Euro-3 gasoline replacing Euro-5 — the rationing regime is now damaging the private capital stock rather than merely restricting access; kilometre-long queues in Moscow; an Oman-flagged tanker discharges ~68,000 tonnes of Indian-origin gasoline at the Arctic port of Vitino with further Indian, Belarusian and Kazakh volumes en route (ISW/Kyiv Post Aug 21)","category":"civilian","significance":"high"},
{"date":"2026-08-22","label":"Leaked communications from Moscow Deputy Mayor Gorbenko's office show officials privately acknowledging Russia cannot defend Moscow's refineries and proposing decentralised mini-refinery networks; Lukoil Permnefteorgsintez in Perm struck overnight Aug 20–21 with geolocated footage confirming a fire at a tank farm or phenolic oil purification unit (ISW Aug 21)","category":"macro","significance":"high"},
{"date":"2026-08-22","label":"Ukrainian naval drones strike two third-country cargo vessels in the Black Sea Aug 21 — the Barbados-flagged container ship RMS TEAM, whose crew abandoned ship, and the Turkish-owned VOLGO-BALT 226, with bridge and living quarters damaged — extending the interdiction campaign to third-country-flagged tonnage (ISW Aug 21)","category":"infrastructure","significance":"high"},
{"date":"2026-08-24","label":"ISW: Ukrainian forces struck 27 power plants across occupied southern Ukraine and Crimea between Aug 17–22, bringing the total to 267 since Aug 1, plus 36 vessels in the Azov and Black Seas in the same window; targets included the 500 kV Taman electrical substation in Krasnodar Krai — a key node for power transfer to Crimea — and electrical substations near occupied Berdiansk (ISW Aug 23)","category":"infrastructure","significance":"high"},
{"date":"2026-08-24","label":"Putin publicly characterises the Ukrainian strike campaign as having opened 'Pandora's box' and threatens retaliation against Ukraine's 'most sensitive economic sectors'; USF strikes four Ozon logistics centres across Krasnodar, Adygea, Stavropol Krai and Dagestan over three consecutive nights (Taipei Times/AFP Aug 24, Reuters Aug 23, Kyiv Post Aug 24)","category":"macro","significance":"medium"},
{"date":"2026-08-25","label":"Putin signs a decree authorising temporary state control of critical infrastructure — energy, industry, communications, transport and logistics — where private owners fail to protect facilities or rebuild them after attacks; Deputy PM Manturov frames it as state 'involvement in the management of an enterprise' rather than nationalisation, Peskov citing inadequate anti-drone measures by owners; analyst Abbas Gallyamov characterises it as an ultimatum to refinery owners reluctant to reinvest under repeated targeting. Direct property-rights signal: the Russian state is asserting conditional control over privately held productive assets on the mainland (AP/ABC, CNN, Washington Post Aug 25)","category":"policy","significance":"high"},
{"date":"2026-08-25","label":"Bloomberg: Russian seaborne crude exports fall to 3.46M bpd in the four weeks to Aug 23 — the lowest in four months — with 33 tankers loading 24.79M barrels in the week to Aug 23; four-week gross export value $1.65bn per week, down $80M; Russian crude output at 8.89M bpd, a six-year low and nearly 1M bpd below the OPEC+ quota; Kazakh crude redirected to Novorossiysk to free Baltic Ust-Luga capacity for Russian barrels (Bloomberg Aug 25)","category":"macro","significance":"high"},
{"date":"2026-08-26","label":"Lukoil NORSI refinery at Kstovo, Nizhny Novgorod Oblast — Russia's fourth-largest refinery and second-largest gasoline producer — struck overnight Aug 25–26, alongside a Wildberries logistics hub at Kotovsk, Tambov Oblast burning over 100,000 m² and halting deliveries; Ukrainian defence firm Fire Point confirmed its FP-1 drones executed both strikes in a single night; fuel, ammunition and logistics depots struck at Berdiansk and Prymorsk Aug 24–25 (Kyiv Post/Ukrainska Pravda Aug 25–26)","category":"infrastructure","significance":"high"},
{"date":"2026-08-26","label":"ATESH reports commanders of the Russian 70th Motorized Rifle Division selling military fuel allocations to civilians in Donetsk, Luhansk and Rostov-on-Don at prices from 300 rubles per litre, leaving the unit with shortages affecting armoured operations and casualty evacuation [unverified — Ukrainian partisan source]. If corroborated this is the first acute fuel-access failure in the Donbas cities at Crimea intensity — see Donbas Track B watch condition (Ukrinform Aug 26)","category":"civilian","significance":"high"},
{"date":"2026-08-26","label":"EJIL:Talk legal analysis (Vozniuk): Russia's 2% mortgage programme for the occupied territories runs to 2030 and had issued more than 6,000 loans by late 2025; Federal Constitutional Law No. 4-FKZ (Dec 2025) enables redistribution of confiscated Ukrainian property to Russian citizens; official territorial planning documents project an additional 113,800 residents across the occupied oblasts by 2045; GUR documents ~200,000 ethnic Russians in occupied Donetsk, Luhansk, Zaporizhzhia and Kherson plus 200,000–300,000 in Crimea as of July 2026 (EJIL:Talk Aug 26)","category":"policy","significance":"high"}
```

That is **36 new entries**. Expected `key_events` length in `public/data/scores.json` after append: **176** (140 + 36).

---

## Step 10 — Crimea price series: stale, refresh required

`public/data/crimea_prices.json` declares `"cadence": "biweekly"` but its last reading is **2026-06-02** (221,332 ₽/m²). Six biweekly readings are missing: Jun 16, Jun 30, Jul 14, Jul 28, Aug 11, Aug 25. The dashboard renders "26 readings" against a price series nearly three months stale, while Crimea Track A is the dial most dependent on it.

**Path trap:** `fetch/restate.py` line 25 sets `DATA = ROOT / "data" / "crimea_prices.json"` — the **root** copy, which is out of scope per Step 0. Running the scraper as-is will not update `public/data/crimea_prices.json`, which is what the dashboard actually fetches (`public/index.html` ~line 2283) and which `SEED_PRICES` shadows on first paint.

Run `fetch/restate.py` and report what it returns. Then:

- **If it returns fresh readings:** report the values before writing anything. A Crimea price move of any magnitude since June is directly material to Track A 38 and must be reviewed by David before it lands, not applied silently. When approved, write to **`public/data/crimea_prices.json`** and update **`SEED_PRICES`** in `public/index.html` to match, then fix the scraper's `DATA` path to point at `public/data/` so this does not recur.
- **If the scraper fails** (blocked, selector drift, site change): do not fabricate or interpolate. Report the failure mode, and add `"stale_since": "2026-06-02"` plus an explanatory note to **`public/data/crimea_prices.json`** so the dashboard's own data declares the gap rather than presenting a three-month-old reading as current.

Either way, do not let this step block Steps 1–9.

---

## Step 11 — Pipeline defect: the digest generator cannot see RPI, CCI or OFP

**This is a real bug, found while preparing this package, and it has been degrading every digest for months.**

`api/monitor.js` line 40 calls `storage.getScores()`, and `lib/storage.js` `getScores()` reads **only** `scores.json`. But `lib/claude.js` instructs the synthesis model to "state the current dial value before suggesting a change" for RPI, CCI, SCI, Track A and Track B — and `refinery_pressure.json`, `civilian_confidence.json` and `occupation_financial_pressure.json` are never passed into that context.

The model therefore invents these values. Every digest from Aug 10–26 reports "RPI current value: 96" — a figure the data file has not held since before the Jul 17 update, when it went to 100. CCI is variously reported as "implied near ceiling," "current value: 100," and "not separately enumerated." OFP is never stated at all. The Dashboard Relevance section — the most decision-relevant part of each digest — is being generated against hallucinated baselines.

Fix, as a **separate commit** from the data update:

1. Add a **new** `getAllScores()` in `lib/storage.js` that reads and returns `scores.json`, `refinery_pressure.json`, `civilian_confidence.json` and `occupation_financial_pressure.json` as a single object, with the latest reading of each surfaced explicitly.

   **Do not extend or change the return shape of the existing `getScores()`.** `api/scores.js` (~line 80) calls the same `storage.getScores()` and returns it as the `/api/scores` payload, which `public/index.html` (~line 2286) consumes as the entire live `SCORES` object. Changing `getScores()` changes the production dashboard feed. Add alongside; do not modify in place.

2. Pass `getAllScores()` into `synthesize()` in `api/monitor.js` (currently line 40, `const currentScores = storage.getScores()`).

3. Update the prompt in `lib/claude.js`. Two changes, not one:
   - Line ~35 lists only "RPI, CCI, SCI, Track A, or Track B" and the DASHBOARD METHODOLOGY REFERENCE block (~lines 48–56) has **no OFP entry at all**. OFP's absence from every digest is therefore by design, not only a context gap — **add OFP to both.**
   - Add an explicit instruction: **if a dial's current value is not present in the supplied context, say so rather than estimating.**

4. Do not deploy or trigger the pipeline as part of this work package. Commit the fix and report; David will decide when it goes live.

---

## Step 12 — MTCS recompute and verification gate

Recompute MTCS using the dashboard's own formula (`computeMtcsDetail` in `public/index.html`):

1. Per city, REP = 50 − spread. Expected after Steps 3–6: Mariupol 83, Donetsk 31, Luhansk 31, Crimea 73, Berdiansk 65.
2. Apply weights — Mariupol 1.0, Donetsk 1.0, Luhansk 1.0, Crimea 1.2, Berdiansk 0.7 — for a total weight of 4.9.
3. Weighted sum 278.1 → corridor REP **56.7551**.
4. Base MTCS = round(56.7551 × 0.5 + 100 × 0.5) = round(78.3776) = **78**.
5. OFP 74 → modulator **+6** (`ofpModulator` returns 6 for values above 70).
6. Final MTCS = min(100, 78 + 6) = **84**.

**Gate: report the computed MTCS before writing anything.** Expected **84**. If it lands outside 83–85, stop and report — do not apply. If it exceeds 88, stop and flag regardless.

Note for the record: at OFP 70 the modulator would have held at +4 and MTCS would have stayed at **82** despite three cities deteriorating — the corridor REP moved only 0.35 points and rounding absorbed it entirely. The entire MTCS movement this cycle comes from the OFP threshold crossing. State this in the note so the causality is not misread later.

Append to the MTCS note (in the Crimea `2026-06` note field, where prior MTCS notes live):

> "Aug 26: MTCS 82→84. Base holds at 78; OFP advances 70→74, crossing into the 71–85 band and lifting the modulator +4→+6. The base is unchanged because Crimea's spread held at −23 (Track A and Track B fell together) while Mariupol widened to −33 and Berdiansk to −15 — corridor REP moved only 56.41→56.76 and rounding absorbed it. All MTCS movement this cycle is attributable to the fiscal modulator, not to the real estate sector. ECS remains at ceiling (100), RPI and CCI both at 100. OFP crossing was made on Minfin's Jan–Jul deficit at 1.7× the full-year target rather than on any of the three triggers named Aug 9, none of which fired. Next thresholds: OFP above 85 lifts the modulator to +8; a corridor REP above ~58 would lift the base to 79. Watch the ~Sept 3 Minfin NWF disclosure for the liquid-assets-below-1%-of-GDP condition, and the Donbas Track B corroboration trigger recorded in scoring_notes."

---

## Step 13 — README

Three corrections, as a **separate commit** from the data update:

1. **Stale ceiling note.** README line ~529 reads "RPI at 97 is effectively at its scoring ceiling" while the dial has been at 100 since July. Update to 100 and fold in the Step 7 finding that three structurally new target categories emerged this window which the dial cannot express — flag RPI ceiling recalibration for the v5.1 review.
2. **Current readings.** Update the OFP section, the MTCS "Current reading" block, and the ECS block to the Aug 26 state: OFP 74 (modulator +6), MTCS 84, base 78, last_updated 2026-08-26.
3. **Version mismatch.** `public/data/scores.json` carries `"methodology_version": "4.0"` while the README, the dashboard footer (`public/index.html` ~line 312) and every digest say v5.0. Set it to `"5.0"`. Nothing branches on the value — it appears zero times in `public/index.html`, `index.html`, `README.md` and `api/scores.js` — so the change is safe. Leave `data/scores.json` alone; bumping a version string on a June-vintage out-of-scope file is cosmetic.

---

## Step 14 — Verify before committing

- Parse-check every JSON file touched — no malformed syntax, no trailing commas.
- Confirm `last_updated` is `2026-08-26T20:00:00Z` everywhere, with no stragglers on the old value.
- Confirm OFP 74, components 72 / 72 / 66 / 57 / 52, `computed_from_components` 66.55, `override_rationale` present, modulator resolving to +6.
- Confirm Crimea track_a 38, track_b 25, composite 48, spread −23.
- Confirm Mariupol track_a **29 (unchanged)**, track_b 21, composite 54, spread −33.
- Confirm Berdiansk track_b 11, composite 26, spread −15.
- Confirm Donetsk and Luhansk are **untouched** (58 / 54).
- Confirm RPI 100 and CCI 100 are unchanged and only their notes were appended to.
- Confirm computed MTCS is 84 and was reported before application.
- Confirm `key_events` in `public/data/scores.json` is sorted ascending by date with no duplicates, and the count is 176.
- **Confirm the seed constants match the JSON files on the fields this update touched — and only those.** Do not attempt full seed/file parity: the seeds are deliberately abridged first-paint fallbacks and have never matched (36 pre-existing differences in `SEED_SCORES` alone). The gate is: every value this package changed — `last_updated`, the five OFP components and `OFP`, Crimea `track_a`/`track_b`/`composite`/`spread`, Mariupol `track_b`/`spread`, Berdiansk `track_b`/`spread`, and the 36 new `key_events` entries — is identical in both copies. Diff those fields programmatically rather than by eye.
- Report (do not fix) the pre-existing `SEED_RPI` `strike_score` divergence: 88 in the seed against 95 in `public/data/refinery_pressure.json`.
- Confirm `data/` is untouched: `git diff --stat -- data/` should be empty apart from line-ending noise.
- Confirm the CRLF line-ending churn from Step 0 has not been swept into the commit: `git diff --cached --stat --ignore-all-space` should show only the files intended.

## Step 15 — Commit

Three commits, in this order:

1. `data: Aug 26 update — OFP 74 (+6 modulator), MTCS 84, Crimea/Mariupol/Berdiansk Track B down, 36 key events`
2. `fix: pass RPI/CCI/OFP into digest synthesis context (storage.getScores read only scores.json)`
3. `docs: README current readings to Aug 26 state; RPI ceiling note 97→100; methodology_version 4.0→5.0`

Also commit `digest-backlog-2026-08-10-to-08-26.md` and this work package file with the first commit.

Push to `main`.

---

## Open items carried forward

- **Crimea price series** — three months stale; Track A rests on qualitative evidence alone until it refreshes (Step 10).
- **Donbas Track B** — corroboration trigger pre-registered; move to 56/52 on a second source or any Domclick/PSB movement (Step 6).
- **RPI ceiling** — three new target categories this window (grain export infrastructure, third-country-flagged tonnage, BSF surface combatants with multi-year repair timelines) cannot be expressed. v5.1 needs a higher ceiling or a separate export-corridor sub-index.
- **NWF anchor** — next Minfin disclosure ~Sept 3. Liquid assets below 1% of GDP crosses the condition David named for further OFP movement.
- **Graham sanctions bill** — passed the Senate Aug 7, with the House, no vote in this window. If enacted, the most significant external OFP pressure event since the strike campaign began.
- **Deployment integrity (urgent, see Step 0).** GitHub Pages publishes the repo **root** on every push to `main`, and root `index.html` is a June 18 vintage. Vercel publishes `public/`. The live monitor shows Jul 17, matching neither. Whatever is actually serving davidfacer.com needs to be established before the next push, and the root tree either brought into line or removed from the publish path. This outranks any dial in this package.
- **Root `data/` tree** — June-vintage and divergent from `public/data/` across every file. Decide whether to delete it, sync it, or document it as dead; leaving two contradictory data trees in one repo will eventually be edited by mistake.
- **Seed/file divergence** — `SEED_RPI.strike_score` is 88 against 95 in the file, and 30 seed `key_events` labels are abridged. Harmless on first paint today, but worth a one-time reconciliation pass outside a data cycle.
- **Putin infrastructure decree (Aug 25)** — worth watching as a property-rights signal in its own right. The Russian state asserting conditional control over privately held productive assets on the mainland is the same logic as expropriation in the occupied territories, applied domestically. If it is used, it belongs in the methodology's private-market framework, not only in the energy narrative.
