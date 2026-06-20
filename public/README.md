# Black Sea Monitor
## Geopolitical Early Warning — Real Estate & Energy Signal Tracker
### Methodology v4.0 · Live at [davidfacer.com](https://davidfacer.com)

---

> **TL;DR** — The Black Sea Monitor tracks the balance of Russia's
> occupation of Eastern Ukraine, the Azov Corridor, and Crimea as
> self-sustaining or sustained primarily through efforts of the Russian
> central government. It does this by watching three things: what Moscow is
> deploying (state commitment), what private investors are betting (market
> confidence), and what locals with no exit option are actually doing with
> their money (residential permanence). When state spending is doing all
> the work and neither private capital nor local residents are independently
> confident, the system is fragile. A daily news pipeline monitors energy
> infrastructure and civilian conditions as fast-moving early warning
> signals. All scoring decisions go through human review before the
> dashboard updates.

---

## What this is

The Black Sea Monitor started as an experiment: could real estate market
behavior in Russian-occupied Ukraine function as an early warning system
for the eventual collapse of Russian territorial control?

The premise was that real estate is one of the most commitment-intensive
economic acts available to civilians. A Donetsk resident taking a 30-year
mortgage is making a bet that Russian control is permanent. A mainland
Russian speculator buying a Mariupol apartment on a 2% subsidized mortgage
is making a different kind of bet — one with exit optionality. Watching
what both populations actually do with their money, rather than what they
say, produces a signal that propaganda cannot easily manufacture.

The project evolved. Real estate captures the slow, structural signal —
what we call the "climate." But climate needs weather to be readable in
real time. We added energy infrastructure pressure (refinery strikes,
export corridor disruption) and civilian consumer stress (fuel rationing,
panic purchasing, grey market activation) as fast-moving indicators that
precede and sometimes predict the slower real estate signal.

The result is an eight-dial instrument tracking three distinct voices:

- **The State** — what Moscow is spending and deploying to project
  permanence, independent of whether anyone believes it
- **The Private Market** — what non-state actors do with their own money,
  independent of subsidy
- **Local Residents** — what people with no exit option bet their
  financial lives on

The spread between these voices is the primary intelligence product.

---

## Human in the loop

This monitor is not automated end-to-end, by design.

A daily news pipeline (Firecrawl → Claude synthesis) produces a structured
digest with proposed dial adjustments. Every proposed adjustment is reviewed
by a human before being applied. The scoring decisions — how much a given
event moves RPI, whether a partisan-source claim warrants CCI movement,
whether a Restate.ru price drop is signal or noise — require judgment that
no automated system should make unilaterally for an instrument meant to
inform geopolitical analysis.

Sources in this domain carry bias. Ukrainian government sources, Russian
state media, and partisan intelligence networks (ATESH, NRC) all have
informational incentives. The digest prompt explicitly flags each source
type. The human reviewer decides how much weight to give unverified claims
— and the scoring record shows those decisions transparently in the
`data_quality` field of each reading.

When something significant happens — the Chistikov/UNN fuel crisis
confirmation, the ISW tourist cancellation figure, the Bellingcat contractor
analysis — it gets sourced to a named person or publication with a date.
If you can't find the source, the claim shouldn't be in the model.

---

## The eight dials

### Real estate sector

**SCI — State Commitment Index** (0–100, higher = more state deployment)

Measures what Moscow is spending to project permanence: federal budget
allocations to occupied territories, state-linked contractor activity,
and the cost of the 2% mortgage subsidy program. SCI is not a confidence
signal — it measures state *intent*, not market *belief*. A high SCI
sustained against low Track A and Track B is the critical fragility
configuration: the state is doing all the work.

Key finding: Bellingcat (Nov 2025) confirmed that virtually all Mariupol
construction is state-linked or entered under federal reconstruction
decree. Ilya Shumanov (Transparency International Russia) stated directly
that contractors only enter DNR if the state compensates all costs or
rewards them via government contract. This finding caused us to separate
SCI from Track A entirely in Methodology v3.0.

Sources: Federal budget execution (minfin.gov.ru), ЕИСЖС developer
registry (наш.дом.рф), PSB/VTB/Sberbank quarterly disclosures via
Kommersant and RBC, ДОМ.РФ monthly mortgage analytics.

Alert: SCI is read *against* the A−B spread, not into it. High SCI +
wide spread = state sustaining a confidence gap that neither private
market nor locals independently produce.

---

**Track A — Private Market Signal** (0–100, higher = genuine private confidence)

Measures non-state actor behavior: independent developer entry (not
under federal contract mandate), cash ДКП transactions (non-mortgage),
and asking price momentum on secondary market platforms. Mariupol's
Track A score is structurally penalized because the Bellingcat/Shumanov
finding leaves almost no genuine private capital identifiable there.

Crimea's Track A is meaningfully higher — a decade of integration has
produced real private market dynamics, resort developers making
independent decisions, mainland Russians buying second homes with their
own cash. That independence makes Crimea's Track A a more honest signal
than Mariupol's.

Sources: Restate.ru biweekly price index (krym.restate.ru/graph/),
GID.HOUSE developer listings, Realytix transaction database (Rosreestr
ЕГРН data), ЦИАН listing analytics.

---

**Track B — Residential Outcome Signal** (0–100, higher = local permanence confidence)

Measures what people with no exit option actually do: secondary market
listing depth on Домклик, buyer permanence composition (local residents
vs inter-regional speculators per PSB/VTB disclosures), and the
rental-to-purchase ratio. At 2% mortgage rates, buying is cheaper than
renting on a monthly cash flow basis in every occupied city except
Mariupol new-build. Anyone renting despite this is paying a measurable
premium for optionality — that premium is the permanence uncertainty
signal.

Track B is the quietest and most informationally dense dial. It doesn't
move on news. It moves when Домклик listing counts shift, when PSB
discloses buyer composition changes, when the rental market absorbs
demand that should be going to purchase. It is the climate dial.

Sources: Домклик live listing counts (domclick.ru), PSB/VTB buyer
composition disclosures (RBC Jan 2025), Avito rental listings for
rental-to-purchase ratio estimation.

---

**Composite Spread** = Track B − (SCI×0.4 + A×0.6)

The primary intelligence product of the real estate sector. Negative
means the state+private composite is outpacing residential reality —
the fragility signal. More negative = more fragile.

The weighting (SCI×0.4, Track A×0.6) reflects that private market
signal is more informationally meaningful per unit than state expenditure.
State spending is loud but can sustain a false signal far longer than
private capital can.

---

### Energy & consumer sector

**RPI — Refinery Pressure Index** (0–100, higher = more fiscal pressure)

Measures systemic pressure on Russian oil refining, Black Sea export
infrastructure, and logistics corridors. Three sub-indicators: CREA
monthly refinery capacity utilization (inverted), confirmed infrastructure
strike score (weighted by facility type: refinery/export terminal = 3pts,
storage = 2pts, pipeline = 2pts), and Novorossiysk/Black Sea export
volume vs pre-war baseline (inverted).

RPI connects to SCI sustainability: Russia's ability to fund the 2%
mortgage program, the ₽11.8B occupied-territory construction allocation,
and the Sberbank/PSB expansion depends on oil revenue. Every percentage
point of refining capacity offline is pressure on the budget line that
funds the permanence projection.

As of June 2026: ~33% of Russian refining capacity offline, fuel
rationing confirmed in 53 regions, Russia importing gasoline from Asia
by sea for the first time (first time this has been necessary; 2025 was
managed domestically).

Sources: CREA (energyandcleanair.org) monthly capacity reports, GUR
Ukraine (@DefenceU Telegram), ISW daily occupation updates
(understandingwar.org), Kpler public export data, RFE/RL, Energy
Intelligence.

Alert thresholds: >50 = warning, >70 = critical. Single-period increase
>25pts = structural event flag requiring source verification before
treating as noise.

---

**CCI — Civilian Confidence Index** (0–100, higher = more acute civilian stress)

Measures acute civilian stress in occupied territories: fuel rationing
intensity (Rosstat weekly price data by oblast), panic purchasing of
staple goods (keyword monitoring in local Telegram channels and Яндекс
review signals), and grey market activation (Avito premium pricing for
гречка, sugar, diesel canisters vs mainland equivalents).

The "buckwheat index" is the CCI's most sensitive component. Гречка
(buckwheat) disappears from occupied-city retail within hours of genuine
population fear — documented in the 2014 Crimea annexation and the
September 2022 mobilization announcement. Grey market Avito activation
(2–5× retail price) indicates official supply chain failure. When a real
estate agency in Sevastopol offers villa stays in exchange for fuel
canisters, as documented by Denys Chistikov (Deputy Permanent
Representative of the President of Ukraine in Crimea) on June 12, 2026,
the currency system itself is breaking down.

CCI and Track B measure different time horizons of the same underlying
question. CCI measures the 30-day survival bet. Track B measures the
30-year permanence bet. A population can exhibit high CCI stress while
maintaining Track B stability if they believe the disruption is temporary.
If both move together, behavioral change is likely imminent.

Sources: Rosstat weekly fuel prices by federal subject (rosstat.gov.ru),
local Telegram community channels (Mariupol, Donetsk, Luhansk), UNN
(June 12 2026, Chistikov), ISW occupation updates, RFE/RL Crimea.Realities.

Alert thresholds: >50 = warning, >70 = critical, >65 first crossing =
"buckwheat index active."

---

**ECS — Energy & Consumer Stress** = (RPI × 0.5) + (CCI × 0.5)

Sector-level summary of the energy and consumer tracks. Equal weighting
reflects that infrastructure pressure (RPI) and civilian response (CCI)
are both necessary signals — one without the other is incomplete. RPI
without CCI could mean successful interdiction that hasn't reached
civilians yet. CCI without RPI could mean local supply chain failures
unconnected to the broader campaign.

---

**MTCS — Master Territorial Confidence Signal** (0–100, higher = more fragile)

Synthesizes the real estate and energy sectors into one territorial
fragility reading.

Computation:
1. Convert each city's composite spread to a Real Estate Pressure score:
   REP = 50 − spread. Apply city weights (Crimea 1.2×, Berdiansk 0.7×,
   others 1.0×) and compute weighted corridor average.
2. MTCS = (Corridor REP × 0.5) + (ECS × 0.5)

Plain-language thresholds:
- <30: Occupation self-sustaining, signals aligned
- 30–50: State working harder than independent actors to project confidence
- 50–65: Structural stress confirmed across sectors
- 65–80: System held together primarily by state expenditure and inertia —
  vulnerable to any shock that interrupts either
- \>80: Acute signal — immediate behavioral change expected

Equal weighting (real estate 50%, energy/consumer 50%) is a starting
assumption, subject to revision once live data from both sectors has
accumulated across multiple distinct events.

---

## City profiles

| City | Weight | Buyer profile | Track B quality | Primary watch |
|---|---|---|---|---|
| **Mariupol** | 1.0 | Inter-regional speculative (PSB: ~82%) | Low — thin secondary market | ДДУ contraction; PSB approval slowdown |
| **Donetsk** | 1.0 | Local residents (PSB confirmed) | Medium — 385 Домклик apts | Listing count trend; price-cut ratio |
| **Luhansk** | 1.0 | Local residents (VTB primary) | Medium — 974 Домклик houses | VTB volume disclosures; listing trend |
| **Crimea** | 1.2× | Mainland Russian resort/second-home | Good — Restate.ru real data | Spread vs Sochi/Krasnodar; ДКП volume |
| **Berdiansk** | 0.7× | Unknown — thin data | Very low | Any PSB/VTB Zaporizhzhia disclosures |

Crimea carries 1.2× weight because it is Moscow's stated red line —
voluntary withdrawal from Crimea would represent a categorically different
political event than retreat from the Azov corridor. A Crimea market
collapse means something that no other city's collapse means.

---

## Data sources

### Real estate
- **Restate.ru** (krym.restate.ru/graph/) — Crimea biweekly secondary
  price index. 26 real readings Jun 2025–Jun 2026. Only fully real
  time-series in the dataset.
- **Домклик** (domclick.ru) — Sberbank's property platform. Live listing
  counts for Donetsk and Luhansk. Track B anchor.
- **GID.HOUSE** (gid.house/mariupol) — Mariupol new-build developer
  listings. Track A for Mariupol.
- **ЕИСЖС** (наш.дом.рф) — Official Russian developer registry.
  Quarterly real anchors for developer/building counts.
- **ДОМ.РФ** (дом.рф/analytics/mortgage/) — Monthly regional mortgage
  volumes. SCI input.
- **Realytix** (realytix.ru) — Rosreestr ЕГРН transaction data.
  Best source for actual closed transaction prices (ДКП/ДДУ).
- **PSB, VTB, Sberbank** — Quarterly disclosures via Kommersant and
  RBC. Buyer composition and mortgage volume data.

### Energy & consumer
- **CREA** (energyandcleanair.org) — Monthly Russian refinery capacity
  utilization. RPI anchor.
- **Kpler** — Weekly Russian crude/product export volumes from Black Sea
  ports. RPI export sub-indicator.
- **Rosstat** (rosstat.gov.ru) — Weekly retail fuel prices by federal
  subject, including occupied oblasts. CCI fuel sub-indicator.
- **GUR Ukraine** (@DefenceU Telegram) — Confirmed infrastructure strike
  data. RPI strike sub-indicator.
- **ISW** (understandingwar.org) — Daily Russian Occupation Update.
  Highest-quality consistent source for occupied-territory developments.
- **UNN / Denys Chistikov** — June 12 2026 fuel/food crisis confirmation.
  Highest-confidence single CCI reading in dataset.
- **RFE/RL Crimea.Realities** — Regional civilian conditions reporting.

### Source bias acknowledgment
Ukrainian government sources, Ukrainian partisan/resistance networks
(ATESH, National Resistance Center), and Russian state media (TASS,
RIA Novosti, Kremlin readouts) all have informational incentives. The
digest prompt explicitly labels:
- `[unverified - Russian state source]` — claim from Russian state media
  not corroborated elsewhere
- `[unverified - Ukrainian partisan source]` — claim from resistance
  networks (ATESH, NRC) not corroborated by wire services or independent
  OSINT

Wire services (Reuters, AP, AFP) and named officials making on-record
statements (Chistikov, Razvozhayev, Brovdi) are treated as higher-quality
sources. ISW is treated as independent analysis, not a partisan source.

---

## The monitor pipeline

```
Daily Vercel Cron (07:00 UTC)
  → api/monitor.js
      → lib/firecrawl.js: 9 search queries, sources:["news"], qdr:d
      → lib/claude.js: synthesis with full methodology context +
                       current scores as input
      → Write digest to Vercel Blob: digests/YYYY-MM-DD.md
      → Update digests/index.json: { date, summary, url } per entry
      → Write pending.json: { pending: true, date, summary,
                              last_digest_date, digest_url }
      → lib/telegram.js: summary + link to dashboard

Dashboard (public/index.html)
  → checkPending() on load
  → If pending and last_updated < digest date: show green banner
  → If pending and last_updated >= digest date: auto-clear, show
    quiet digest link
  → If not pending: show quiet digest link if last_digest_date exists

Digest reader (api/digest/[date].js, api/digest/latest)
  → Two-column layout: requested digest (4/5 width) + sidebar archive (1/5)
  → Sidebar lists all other digests, newest first, 120-char summary excerpts
  → Click any sidebar entry to make it primary

Human review
  → Read full digest via dashboard link or Telegram
  → Evaluate Dashboard Relevance section
  → Decide: score changes, key_events, or no action needed
  → If changes: edit index.html seed data, commit, push
  → Vercel deploys → last_updated advances → banner auto-clears
```

### Firecrawl query list (v1)
```
"Crimea fuel shortage rationing"
"Mariupol Ukraine strike"
"Berdiansk Ukraine drone"
"Russia refinery strike Novorossiysk"
"Azov corridor R-280 logistics"
"Donetsk Luhansk occupied Russia"
"Russia occupied Ukraine economic"
"Sevastopol Black Sea Fleet"
"ISW Russian occupation update"
```

### Low-news threshold
- 0 results: pipeline health alert to Telegram, no digest written
- Results present, Dashboard Relevance = "No items meet threshold":
  quiet Telegram ping, digest written, no green banner
- Results present, at least one metric suggestion: full green banner
  + Telegram summary

---

## What this model says — and doesn't

**It says:** how much load-bearing capacity the territorial confidence
structure has — how much of apparent stability is self-sustaining versus
how much requires continuous state input to maintain.

**It doesn't say:** when. A fragile configuration can persist for a long
time if no trigger arrives. MTCS=70 means the structure is under
significant stress. It does not mean retreat is imminent.

**It doesn't capture:** information that isn't in formal markets. The
most important Track B signals — decisions made in Donetsk kitchens,
informal cash deals that never touch Домклик — are invisible to the
model. The Telegram channel monitoring is an approximation, not a
substitute.

**It can be confused by:** exogenous shocks. The Iran ceasefire and
resulting oil price decline (June 2026) pressure Russian export revenue
through a completely separate mechanism from the Black Sea corridor
interdiction campaign. Both show up in the same fiscal space but for
different reasons. The model currently doesn't distinguish them.

**The most honest description:** a stress test, not a forecast. It tells
you the structure's load-bearing capacity. It cannot tell you when the
weight becomes too much.

---

## Reproducing this work

This README is intentionally complete enough that a reader could
reconstruct the Monitor from scratch. The scoring methodology, data
sources, prompt architecture, and pipeline design are all documented
here. If you find errors in the scoring logic, gaps in the source
coverage, or a better framing for any of the dials, that's exactly the
kind of feedback this kind of public analytical work benefits from.

The dashboard is built with vanilla HTML/CSS/JS (no framework),
Vercel serverless functions, and Chart.js. The monitor pipeline uses
the Firecrawl search API and the Anthropic Claude API. No proprietary
data sources — everything listed above is publicly accessible.

---

## Architecture

```
black-sea-monitor/
├── api/
│   ├── scores.js          # GET current dial values
│   ├── events.js          # GET key_events array
│   ├── digest/
│   │   ├── latest.js      # GET latest digest, two-column reader
│   │   └── [date].js      # GET specific digest, two-column reader
│   ├── monitor.js         # GET (cron) / POST (manual): full pipeline
│   └── pending.js         # GET/DELETE pending state
├── lib/
│   ├── firecrawl.js       # Search wrapper + 9 queries
│   ├── claude.js          # Synthesis API call + prompt
│   ├── telegram.js        # Outbound notification
│   └── storage.js         # Data read/write abstraction
├── public/
│   ├── index.html         # Dashboard (self-contained)
│   └── data/               # Seed JSON files
├── server.js               # Express local dev server
└── vercel.json              # Cron schedule + CORS headers
```

---

## Version history

- **v1.0** — Static real estate dashboard, GitHub Pages, manual updates
- **v2.0** — Three-dial model (SCI, Track A, Track B), spread as primary
  signal
- **v3.0** — SCI decomposed from Track A (Bellingcat finding), composite
  spread formula revised
- **v4.0** — RPI + CCI + ECS + MTCS added; Vercel migration; automated
  Firecrawl pipeline; pending review workflow; Vercel Blob digest
  persistence; two-column digest archive reader

---

*Black Sea Monitor is an independent analytical project. It is not
affiliated with any government, intelligence agency, or news organization.
All source attributions are to publicly available reporting.*
