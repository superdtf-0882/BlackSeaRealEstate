# Black Sea Monitor

## 1.1 What this is

The Black Sea Monitor is a daily-updating geopolitical early warning
system. It watches Russian-occupied territory in eastern Ukraine
(Mariupol, Donetsk, Luhansk, Crimea, Berdiansk) and produces a set of
numeric indicators — combining real estate market behavior, energy
infrastructure pressure, civilian conditions, and government fiscal
pressure — that together estimate how much of Russia's control over
that territory is self-sustaining versus propped up by continuous state
spending. A news-scraping and AI-synthesis pipeline runs once a day,
produces a written digest, and alerts a human reviewer; the human
decides whether anything in that digest should move the published
indicator values. If this system stopped running, the published dashboard
would simply stop updating — there is no other process that keeps its
data current.

Within the davidfacer.com portfolio, this is a governed product (not an
experimental prototype) that was elevated from an informal "shadow
topology" deployment under the Prototype Lifecycle Charter (CHARTER-001,
2026-07-13). It has two public-facing surfaces: a static shell embedded
at `davidfacer.com/blackseamonitor/` (which fetches its data live,
cross-origin, from this project), and this project's own backend,
deployed independently at `black-sea-real-estate.vercel.app` with no
custom domain of its own. The digest reader and monitoring API live only
on the backend URL; the embedded shell on the main site is a copy of the
dashboard's front-end HTML, not a separate implementation.

*(The full analytical methodology — the nine-dial scoring model, current
readings, and the reasoning behind it — is preserved below in full under
"Analytical Methodology," clearly separated from the engineering
sections here. If you're operating or debugging this system, you don't
need to read that section first.)*

## 1.2 Architecture and data flows

**Trigger mechanism:** a Vercel Cron fires `GET /api/monitor` daily at
07:00 UTC (schedule defined in `vercel.json`). The same endpoint also
accepts `POST` for manual triggering (used during development and
testing) — both `GET` and `POST` require the same `CRON_SECRET` bearer
token (fixed 2026-07-14; previously `POST` had no auth check, see 1.6).

**Current live flow** (confirmed this session by reading `api/monitor.js`
directly, not assumed from a prior design):

```
Vercel Cron, 07:00 UTC daily (GET, requires CRON_SECRET)
  → api/monitor.js
      → lib/firecrawl.js: 9 search queries, sources:["news"], last 24h
      → lib/claude.js: synthesis (claude-sonnet-4-6) with full
                       methodology context + current scores as input
      → write digest to Vercel Blob: black-sea-digests/digests/YYYY-MM-DD.md
          → [fire-and-forget archive push to davidfacer-archive
             /api/blob-receive — see below]
      → update digests/index.json in the same Blob store
          → [fire-and-forget archive push, same as above]
      → write pending.json (dashboard banner state)
      → lib/telegram.js: send summary + dashboard link
```

**Archive push (added for portfolio backup, ADR-007):** after each of
the two Blob writes above, this project fires a non-blocking POST to a
separate, independently-deployed backup project (`davidfacer-archive`).
This exists because `black-sea-digests` (this project's own Blob store)
has no other backup mechanism, and Black Sea Monitor's published digests
are not recoverable from any other source if this store were ever lost.
The push is fire-and-forget: the request is not awaited, a failed push
is only logged (`console.error`) on this project's side, and it can
never block or delay digest publication, the Telegram alert, or any
other part of this pipeline. See `davidfacer-archive`'s own README and
ADR-007 for the receiving side of this relationship.

**CORS constraint:** `vercel.json` restricts every `/api/*` route to
`Access-Control-Allow-Origin: https://davidfacer.com` (GET/OPTIONS only)
— this is what allows the embedded shell at
`davidfacer.com/blackseamonitor/` to call this backend cross-origin at
all, and nothing else. This is a bare-origin allowlist, not a wildcard —
confirmed by reading `vercel.json` directly.

**Downstream consumers, for context (not part of this project's own
data flow):** the static dashboard (`public/index.html`) reads
`digests/index.json` and `pending.json` to show the "new digest
available" banner; a human reviewer reads the digest and, if warranted,
manually edits this project's own seed data files and redeploys to move
the published indicator values. See "Analytical Methodology" below for
the full pipeline-to-human-review-to-redeploy cycle and the OFP monthly
review cadence, which are analytical/editorial processes rather than
this codebase's own architecture.

## 1.3 Credentials and environment

Every environment variable this project's code actually reads (confirmed
via a direct search of `api/` and `lib/` for `process.env` usage, plus
`BLOB_READ_WRITE_TOKEN` which the `@vercel/blob` SDK reads implicitly and
is never referenced by name in this codebase):

| Variable | What it accesses | Required for | Tier |
|---|---|---|---|
| `BLOB_READ_WRITE_TOKEN` | `black-sea-digests` Blob store (read/write) | All digest read/write operations | High — if revoked, digests can no longer be written or read; the dashboard and digest reader would break entirely |
| `ANTHROPIC_API_KEY` | Claude API (`claude-sonnet-4-6`) | Digest synthesis | High — if revoked, synthesis fails and no digest is produced that day; the pipeline errors out before reaching the Blob write |
| `FIRECRAWL_API_KEY` | Firecrawl web search/scraping service | Daily news fetch | High — if revoked, the fetch step fails with zero results, which triggers the "0 results" pipeline-health alert path and no digest is written |
| `TELEGRAM_BOT_TOKEN` | Telegram Bot API | Alert delivery | Medium — if revoked, digest publication still completes; only the Telegram notification fails |
| `TELEGRAM_CHAT_ID` | Identifies which Telegram chat receives alerts | Alert delivery | Low — identifies a destination, not itself a credential with independent access |
| `CRON_SECRET` | Authenticates the Vercel Cron's `GET` call to `/api/monitor` | Scheduled execution | Low — operational, not a data-access credential |
| `ARCHIVE_ENDPOINT` | URL of `davidfacer-archive`'s `/api/blob-receive` endpoint | Archive push | N/A — not a secret, just a destination URL |
| `ARCHIVE_PUSH_SECRET` | Shared secret authenticating this project's pushes to the archive endpoint | Archive push | Medium — the same value is also set in `davidfacer-archive`'s own environment; compromise would let someone else push arbitrary content into the archive store under this project's name |

Tier definitions (PES-001): **High** = production data or admin-level
access, compromise has material consequences. **Medium** = scoped
operations. **Low** = operational, not data-access.

## 1.4 Deployment and operations

**Deploy from scratch:**

```bash
git clone <this repo>
cd BlackSeaRealEstate
npm install
# Set all 8 env vars from 1.3 in the Vercel dashboard (Production + Preview)
npx vercel link      # one-time
npx vercel --prod
```

No build step — plain Node.js serverless functions under `api/`, no
framework (confirmed via `vercel.json`'s `"framework": null` and
`package.json`'s dependency list — no framework packages, just
`@mendable/firecrawl-js`, `@vercel/blob`, `dotenv`, `express` for local
dev only, and `marked`). Deployment does not auto-promote to production
on push — an explicit `vercel --prod` (or a manual dashboard promotion)
is required every time, same as every other project in this portfolio.

**Verify the cron is registered:**

```bash
vercel crons ls
```
Expected: `/api/monitor` at `0 7 * * *`.

**Confirm a digest ran successfully** (whether triggered by cron or
manually):

- A new dated file appears in the `black-sea-digests` Blob store:
  `digests/YYYY-MM-DD.md` (or `digests/YYYY-MM-DD-2.md`, etc. for a
  second same-day update — see 1.6 for a related discrepancy).
- `digests/index.json` in the same store has a new entry for that date.
- The configured Telegram chat received an alert (either the full
  digest summary, or a quieter "nothing dashboard-relevant" ping,
  depending on content — see "Low-news threshold" under Analytical
  Methodology).
- The corresponding archive push succeeded: check
  `manifest/blacksea-digests.json` in the `davidfacer-archive` project's
  own Blob store for the new key. This step is fire-and-forget and its
  failure would **not** be visible from this project's own logs or
  behavior — see 1.5.

**Manual trigger for testing:** `POST /api/monitor` runs the full
pipeline on demand, with the same `Authorization: Bearer <CRON_SECRET>`
header required for the cron's `GET` call.

## 1.5 Runbook — known failure modes

**Firecrawl fetch fails or returns 0 results.** Not retried within the
same run. If the result count is exactly 0, the pipeline sends a
pipeline-health alert to Telegram ("Monitor ran — 0 results returned.
Check Firecrawl API or query list.") and writes no digest at all that
day. If individual queries fail but others succeed, the pipeline
continues with whatever results it got (errors are caught and logged
per-query in `lib/firecrawl.js`, not fatal to the run).

**Claude synthesis fails.** The whole request fails with a thrown error,
caught by the top-level handler, which sends a Telegram alert
(`🚨 Monitor pipeline error: ...`) and returns a 500. No digest is
produced for that day. Not automatically retried — the next opportunity
is the following day's scheduled cron run, or a manual `POST` trigger.

**Blob write fails** (digest `.md` or `index.json`). This would throw
inside the same top-level `try` block as synthesis, triggering the same
error-alert path above. Telegram would receive the pipeline-error alert,
not the normal digest summary — the two are mutually exclusive for a
given run, not both sent.

**Archive push fails.** Explicitly non-blocking, by design (see 1.2):
the digest is published regardless, the Telegram alert still fires
normally, and the only trace of the failure is a `console.error` line
in this project's own Vercel function logs — nothing surfaces to
Telegram or anywhere else a human would notice. Recovery: the missing
key can be manually re-pushed to `davidfacer-archive`'s
`/api/blob-receive` endpoint, or picked up by re-running that project's
backfill pattern (list `black-sea-digests`, re-POST anything missing
from the archive's manifest). This project's own Blob store
(`black-sea-digests`) is unaffected either way — the archive push never
reads from or depends on anything already written there.

**Telegram alert fails** (bad token, chat ID, or Telegram API error).
Caught separately from the main pipeline (`try`/`catch` around the
`sendMessage` call specifically) — the digest is published regardless,
and the failure is logged (`console.error('Telegram send failed:', ...)`)
but does not fail the overall request or block anything else.

**`POST /api/monitor` previously had no authentication** (fixed
2026-07-14). Since this project has no custom domain and is reachable
directly at its `.vercel.app` URL, anyone who had that URL could
previously trigger a full pipeline run — including the paid Anthropic
and Firecrawl API calls and a real Telegram alert — with a bare
`curl -X POST`, any number of times, with no rate limiting. Both `GET`
and `POST` now require the same `CRON_SECRET` bearer token; there is
still no rate limiting on authenticated calls.

## 1.6 Known limitations and open items

- **No retry logic anywhere in the pipeline.** If Firecrawl or Claude
  synthesis fails on a given day, that day's digest is simply not
  produced — the next chance is tomorrow's scheduled run or a manual
  trigger. There is no queued retry or backoff.
- **No alerting on archive push failure** (see 1.5). A missed archive
  push produces no notification anywhere a human would see it — the
  only way to discover one is to check `davidfacer-archive`'s manifest
  against this project's own `digests/index.json` and look for gaps.
- **A pre-existing discrepancy in `digests/index.json` itself:** it
  lists 26 entries covering 25 distinct calendar dates, while 28 actual
  `.md` digest files exist (26 calendar days between 2026-06-19 and
  2026-07-14, plus two extra same-day sequence files on 2026-06-21 —
  `2026-06-21-2.md` and `2026-06-21-3.md`). This predates the archive
  work and is not something the archive backup caused — the archive
  correctly holds copies of all 28 `.md` files plus the index as-is.
  Worth investigating independently of this README task, since it means
  `index.json` is not a fully reliable index of every digest that
  actually exists.
- **ADR-006** (governing this project's use of the Anthropic/Claude API
  for digest synthesis) exists in the portfolio's architecture corpus
  but is not yet cross-referenced from this README. Added as a forward
  reference here; the decision record itself lives in the `OKF TOGAF`
  repository's corpus, not in this repo.

---

# Analytical Methodology

*The following is the Black Sea Monitor's own analytical/product
documentation — the scoring model, current readings, data sources, and
the reasoning behind the methodology. This section is written for a
reader of the intelligence product itself, not for an engineer
operating the system. If you're deploying, debugging, or maintaining
this codebase, everything you need is in the engineering sections above
— you do not need to read further to do that job.*

## Geopolitical Early Warning — Real Estate & Energy Signal Tracker
### Methodology v5.0 · Live at [davidfacer.com](https://davidfacer.com)

---

> **TL;DR** — The Black Sea Monitor tracks the balance of Russia's
> occupation of Eastern Ukraine, the Azov Corridor, and Crimea as
> self-sustaining or sustained primarily through efforts of the Russian
> central government. It does this by watching four things: what Moscow is
> deploying (state commitment), what private investors are betting (market
> confidence), what locals with no exit option are actually doing with
> their money (residential permanence), and whether Moscow can afford to
> keep doing all of it (occupation financial pressure). When state spending
> is doing all the work, neither private capital nor local residents are
> independently confident, and the fiscal runway is shortening, the system
> is fragile. A daily news pipeline monitors energy infrastructure and
> civilian conditions as fast-moving early warning signals. All scoring
> decisions go through human review before the dashboard updates.

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

v5.0 adds a third sector: occupation financial pressure. By mid-2026 the
war and the occupation had merged into a single fiscal commitment —
front-line operations, occupation administration, reconstruction theater,
military family payments, and the evasion infrastructure required to
maintain all of it under sanctions are no longer separable expenditure
streams. The question is whether Moscow can fund the combined load. OFP
measures the pressure on that funding stream and applies it as a modulator
on the master signal.

The result is a nine-dial instrument tracking four distinct voices:

- **The State** — what Moscow is spending and deploying to project
  permanence, independent of whether anyone believes it
- **The Private Market** — what non-state actors do with their own money,
  independent of subsidy
- **Local Residents** — what the remaining civilian population bets its
  financial lives on, with the important caveat that "remaining civilian
  population" describes very different conditions in different cities
  (see City profiles)
- **The Fiscal Position** — whether the combined occupation-war load is
  financially durable or burning through its buffer

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

OFP scoring follows the same discipline. The five components are updated
monthly from named sources, with event-driven updates when the digest
pipeline surfaces a qualifying event (confirmed regional budget cuts,
shadow fleet enforcement actions, OFZ auction results). OFP does not move
on rumor.

---

## The nine dials

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

**Emerging signal — commandeering:** Reports as of June 2026 indicate
Russian military forces in occupied territories are transitioning in some
areas from formal tenancy and subsidized purchase toward commandeering
civilian property for billeting. If confirmed and widespread, this would
represent a structural shift in how SCI should be read: commandeering is
not a permanence signal, it is an emergency measure that signals the state
can no longer organize or afford the formal program. It also undermines
the property rights framework that makes Track A and Track B meaningful.
Currently logged as a watch condition pending further confirmation. A
verified shift to widespread commandeering would trigger a methodology
review of SCI sub-indicators.

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

Crimea's Track A was meaningfully higher through 2025 — a decade of
integration produced real private market dynamics, resort developers
making independent decisions, mainland Russians buying second homes with
their own cash. As of June 2026, that independence is collapsing. The
tourism season has been effectively cancelled by official decree, summer
camps suspended, hotel bookings down 31–40%, and both buyer and renter
populations are in simultaneous retreat. Crimea Track A is now in active
decline rather than independent operation.

**Note on commandeering:** If Russian forces are requisitioning civilian
property at administrative discretion, the private market framework
breaks down regardless of willingness to transact. A developer whose
completed units can be commandeered is not operating in a market.
Track A scores would need to reflect this risk premium once commandeering
is confirmed as systematic.

Sources: Restate.ru biweekly price index (krym.restate.ru/graph/),
GID.HOUSE developer listings, Realytix transaction database (Rosreestr
ЕГРН data), ЦИАН listing analytics.

---

**Track B — Residential Outcome Signal** (0–100, higher = local permanence confidence)

Measures what the remaining civilian population does with long-horizon
financial decisions: secondary market listing depth on Домклик, buyer
permanence composition (local residents vs inter-regional speculators
per PSB/VTB disclosures), and the rental-to-purchase ratio. At 2%
mortgage rates, buying is cheaper than renting on a monthly cash flow
basis in every occupied city except Mariupol new-build. Anyone renting
despite this is paying a measurable premium for optionality — that
premium is the permanence uncertainty signal.

Track B is the quietest and most informationally dense dial. It doesn't
move on news. It moves when Домклик listing counts shift, when PSB
discloses buyer composition changes, when the rental market absorbs
demand that should be going to purchase. It is the climate dial.

**Critical interpretive caveat — Donbas:** Track B in Donetsk and
Luhansk does not measure a representative civilian population. A decade
of conflict, displacement, and Russian administrative integration has
produced a residual population that is below pre-war levels and
self-selected for pro-Russia orientation — the people who remained when
exit options were available and chose not to use them. Mortgage
participation in Donbas reflects a prior political commitment that
preceded the mortgage, not a market confidence signal generated
independently of that commitment. Stability in Donbas Track B should
not be read the same way as stability in Crimea Track B. It means the
true believers are still betting. It does not mean the general civilian
population is confident.

The corollary is important: if commandeering reaches Donbas at scale,
it means the occupation is putting financial pressure on its own captive
support base — the people who stayed when others left and who have
exhausted their tolerance buffer. That would be a categorically more
acute signal than commandeering in a mixed or resistant population.

**Crimea — phase transition:** As of June 2026, Crimea Track B is not
merely declining — it is in active exit. Both sides of the
permanence/optionality equation are in simultaneous retreat. Buyers are
withdrawing because the product the mortgage finances (stable occupation,
functional infrastructure, personal safety) is visibly degrading. The
renter/optionality population — mainland Russian speculators, military
families, resort visitors — is exercising that optionality and leaving.
The civilian exodus is sustained and structural, not episodic. Russian
Black Sea Fleet families are relocating to Novorossiysk. Summer 2026
tourism has effectively collapsed. The Russian-installed administration
declared a formal state of emergency on June 26, 2026 — an administrative
acknowledgment that normal governance has failed. This is not a market
under stress. It is a market in evacuation.

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

As of June 2026: RPI 97. Approximately 33% of Russian refining capacity
offline, fuel rationing confirmed in 56 regions, Russia importing
gasoline from Asia by sea for the first time. The Sevastopol main power
substation destroyed June 23–24. North Crimean Canal railway bridge
destroyed. Orenburg Gazprom gas processing plant struck (60% of Gazprom
Pererabotka capacity, 1,200km from front). Ukraine has launched a
Zelensky-authorized 40-day intermediate and long-range strike operation
as of June 25, expanding the target set beyond energy infrastructure to
include air defense systems and logistics corridors.

**Ceiling note:** RPI at 97 is effectively at its scoring ceiling. The
indicator cannot meaningfully differentiate between "critical" and
"catastrophic" at this range. New events are captured in scoring notes
and key_events rather than further dial movement. The notes carry the
analytical weight when the dial cannot.

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
When both move together, behavioral change is not imminent — it is
already underway.

As of June 2026: CCI 100 (index ceiling). Sevastopol full city blackout.
Water supply outages. Public transit suspended in occupied Crimea and
four Russian oblasts due to diesel shortages. Formal state of emergency
declared by Russian-installed Crimea administration June 26, 2026.
Ukraine's Foreign Intelligence Service released internal Russian documents
confirming near-daily governance failures and reporting that over 80% of
Russians now consider a large-scale economic crisis inevitable.

**Ceiling note:** CCI at 100 is the index ceiling. The dial cannot move
further. New acute stress events are captured in scoring notes and
key_events. The ceiling does not mean conditions have stopped
deteriorating. It means the model's acute-stress instrument is exhausted
in this dimension and the notes carry the analytical weight.

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

As of June 2026: ECS 99. Both inputs at or near ceiling simultaneously.
This is the configuration the monitor was built to detect: infrastructure
destruction and civilian collapse arriving together, not sequentially.

---

### Fiscal sector

**OFP — Occupation Financial Pressure** (0–100, higher = more pressure on
occupation-war funding)

Measures the fiscal durability of Moscow's combined occupation-war
commitment. By mid-2026 these are no longer separable expenditure
streams. Front-line operations, occupation administration, reconstruction
theater, military family payments (mobilization bonuses, death benefits),
and the sanctions evasion infrastructure required to sustain all of it
have merged into a single fiscal load. OFP asks whether that load is
financially durable or burning through its buffer.

OFP is not a measure of total Russian fiscal capacity — it is scoped
specifically to the occupation-war fusion and the revenue streams that
fund it. A Russia under fiscal stress for reasons unrelated to the
occupation (commodity price collapse, demographic headwinds) would show
OFP pressure only to the extent that stress compresses the occupation
funding line.

**Five components:**

*Export Revenue Proxy (weight 30%)* — Normalized seaborne export volume
index combined with Urals price realization factor (Urals price ÷ Brent
price). Falls when either volume drops or the sanctions discount widens.
At current spreads (~$13–15/barrel on ~$70 Brent) price realization is
approximately 0.80 — Russia is leaving roughly 20% of potential revenue
on the table per barrel. Sources: Kpler/Reuters weekly export data,
Argus/Reuters Urals-Brent spread.

*NWF Liquid % of GDP (weight 25%)* — Russia's National Wealth Fund
liquid, deployable portion as a share of GDP, inverted. Pre-war liquid
NWF was ~8% of GDP (~$185B). Current liquid portion is estimated at
2.5–3% of GDP once committed-but-illiquid positions are stripped out.
This is the runway indicator: how long can Moscow sustain the combined
load if income falls short. Moves slowly and honestly — deterioration
is harder to hide than stability is to fake. Source: Minfin monthly NWF
disclosures (minfin.gov.ru).

*OFZ / Sovereign Debt Stress (weight 20%)* — Direction of OFZ bond
prices and auction coverage ratios. When OFZ yields rise despite CBR
rate cuts, the market is pricing fiscal stress the official rate is
trying to suppress. Falling OFZ prices + ruble weakness = compound
signal. Source: Moscow Exchange, CBR auction results, Reuters/Bloomberg.

*Regional Budget Transfer Cuts (weight 15%)* — Event-driven. Scored
from digest pipeline. Distinguishes cuts to non-occupation regions
(mild signal) from cuts to occupation-adjacent regions like Rostov,
Belgorod, and Kursk (stronger signal) from direct cuts to occupation
territory transfer payments (acute signal). The most honest component
in the set: these are internal administrative decisions not being managed
for external perception.

*Shadow Fleet / Sanctions Enforcement Stress (weight 10%)* — Event-driven.
Lloyd's of London war risk premiums on Black Sea routes, tanker seizures,
and secondary sanctions designations. Rising enforcement friction raises
the cost of maintaining the export revenue stream that funds everything
else. Source: Lloyd's, Reuters tanker tracking, US/EU sanctions registers.

**Directional note:** All five components are oriented so that
deterioration raises OFP. This is consistent with the monitor's 100=bad
convention across all dials. Readers accustomed to thinking of NWF size
as a positive indicator should note that OFP's NWF component scores
*depletion* — a falling NWF raises OFP, as intended.

**Asymmetric signal reliability:** Downward moves in OFP (improving
fiscal position) are less reliable than upward moves. Russia has
demonstrated willingness to burn reserves and suppress monetary signals
to project stability. A reading of "deteriorating" is harder to fake
than a reading of "stable." Score improvements should require stronger
source evidence than score increases.

**Live test — Hormuz MOU:** The Iran nuclear framework agreement (June
2026) creates ambiguity for OFP's export revenue proxy. If Iranian
supply returns to market, global oil prices soften — potentially
narrowing the Urals-Brent discount while reducing the absolute Urals
price. Russia and Iran compete for the same sanctioned-oil customer
base in China and India. A rehabilitated Iran is not straightforwardly
good for Russian price realization. The export revenue proxy is
monitoring for observable Urals price and volume effects before any
scoring adjustment is made. If OFP holds or rises despite the MOU,
that is itself a finding: fiscal pressure is structural, not merely
oil-price-contingent.

**Update cadence:** Monthly anchors from Minfin (NWF), CBR (rate
direction), and Reuters/Kpler (export proxy). Event-driven updates for
regional cuts and shadow fleet enforcement. OFP does not respond to
weekly digest inputs the way RPI and CCI do — it is a slower-moving
structural signal, not a weather indicator.

Alert thresholds: >35 = watch, >50 = warning, >70 = critical.

---

**MTCS — Master Territorial Confidence Signal** (0–100, higher = more fragile)

How much of Russia's territorial control is self-sustaining — and how
much requires continuous state spending to maintain. When private
investors and local residents act independently of the state, the
occupation has a foundation. When the state is the only actor, it
doesn't. MTCS measures the gap between those two conditions.

**v5.0 computation:**

1. Convert each city's composite spread to a Real Estate Pressure score:
   REP = 50 − spread. Apply city weights (Crimea 1.2×, Berdiansk 0.7×,
   others 1.0×) and compute weighted corridor average.
2. Base MTCS = (Corridor REP × 0.5) + (ECS × 0.5)
3. Apply OFP modulator: look up adjustment from threshold table below.
4. Final MTCS = min(100, Base MTCS + OFP modulator)

The dashboard displays the decomposition transparently: Real Estate +
Energy [X] + Fiscal Pressure (OFP) [+N] = Master Signal [total].
Readers can evaluate the modulator's contribution independently.

**OFP modulator thresholds:**

| OFP range | MTCS adjustment | Plain language |
|---|---|---|
| 0–40 | +0 | Fiscal position stable — no amplification |
| 41–55 | +2 | Mild depletion pressure — structural note only |
| 56–70 | +4 | Meaningful pressure — occupation funding under strain |
| 71–85 | +6 | Acute pressure — burn rate exceeding sustainable income |
| 86–100 | +8 | Critical — buffer near exhaustion, funding at risk |

The OFP modulator is additive rather than co-equal because OFP measures
something upstream of the other inputs — the sustainability of the system
that produces those readings. A high OFP amplifies what the real estate
and energy sectors are already saying. It does not average against them.
When OFP is low (≤40), MTCS is unaffected. The modulator earns its
weight by rising.

**Plain-language thresholds:**
- <30: The occupation appears self-sustaining. Signals are aligned.
- 30–50: The state is working harder than the market or residents are.
  Early fragility signal.
- 50–65: Pressure is confirmed across multiple sectors. The state is
  working hard to project stability it is not generating organically.
- 65–80: The occupation is held together by state spending and inertia.
  It has no independent foundation. Any shock to either breaks it.
- >80: The occupation is in acute distress. Behavioral change —
  population movement, market exit, administrative breakdown — is
  expected.

**Current reading:** MTCS 79, Fragility Zone. Base 77 (real estate +
energy) + OFP modulator +2 = 79. One point below the acute threshold.
Both RPI and CCI are at or near ceiling. The formal state of emergency
declaration in Crimea (June 26, 2026) and the ongoing civilian exodus
are behavioral changes already in progress, not anticipated.

---

## City profiles

| City | Weight | Buyer profile | Track B interpretation | Market phase | Primary watch |
|---|---|---|---|---|---|
| **Mariupol** | 1.0 | Inter-regional speculative (PSB: ~82%) | Low signal — state program dominates | State-Only | ДДУ contraction; PSB approval slowdown |
| **Donetsk** | 1.0 | Residual pro-Russia self-selected population, below pre-war levels | Captive — reflects prior commitment, not current confidence | Captive + Watch | Commandeering reports; listing count trend |
| **Luhansk** | 1.0 | Residual pro-Russia self-selected population, below pre-war levels | Captive — reflects prior commitment, not current confidence | Captive + Watch | Commandeering reports; VTB volume disclosures |
| **Crimea** | 1.2× | Collapsing — military families, tourists, speculators exiting | Active exit — both permanence and optionality populations retreating simultaneously | Exiting | State of emergency; civilian exodus pace; Restate.ru price trajectory |
| **Berdiansk** | 0.7× | Unknown — thin data | Unclassifiable | Unknown | Any PSB/VTB Zaporizhzhia disclosures |

**Crimea carries 1.2× weight** because it is Moscow's stated red line —
voluntary withdrawal from Crimea would represent a categorically different
political event than retreat from the Azov corridor. A Crimea market in
active exit means something no other city's signal means.

**Donbas population caveat:** Donetsk and Luhansk are below pre-war
population levels. The residents who remain are not a representative
sample of the pre-war civilian population — they are those who chose to
stay under Russian administration when exit was possible. Mortgage
participation in this population reflects a prior political commitment.
It is not evidence of general civilian confidence in the occupation's
permanence. The model correctly scores Donbas Track B higher than Crimea
Track B on the numbers, but the interpretation requires this context:
Donbas is measuring true believers. Crimea was measuring a genuine
private market. That market is now evacuating.

**Market phase classifications** are documented here as a framework
pending dashboard implementation in v5.1:
- **State-Only** — genuine private market undetectable; state program is the market
- **Captive** — residual self-selected population below pre-war levels; participation reflects prior commitment not current confidence
- **Watch** — emerging structural risk not yet visible in transaction data (commandeering)
- **Exiting** — active departure of prior participants; both buyer and renter populations retreating
- **Unknown** — insufficient data to classify

---

## Planned — v5.1

**Market Directionality indicator**

A per-city phase classification surfaced alongside each city's dial set.
Distinguishes *why* Track A and Track B are at their current levels —
whether scores reflect absence of new entrants, active exit of existing
participants, captive self-selected populations, or state-only activity.

The distinction matters because a falling score caused by active exit is
a categorically more acute signal than a falling score caused by lack of
new interest. The current model captures the level but not the direction
of travel or the composition of the population generating the reading.

Market Directionality is an interpretive layer, not a formula input. It
will not feed into MTCS. Phase transitions will be documented in the
digest's Dashboard Relevance section when they occur.

Current assignments pending implementation:
- Mariupol: State-Only
- Donetsk: Captive + Watch (commandeering risk)
- Luhansk: Captive + Watch (commandeering risk)
- Crimea: Exiting
- Berdiansk: Unknown

---

## Data sources

### Real estate
- **Restate.ru** (krym.restate.ru/graph/) — Crimea biweekly secondary
  price index. Only fully real time-series in the dataset.
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
  ports. RPI export sub-indicator; also feeds OFP export revenue proxy.
- **Rosstat** (rosstat.gov.ru) — Weekly retail fuel prices by federal
  subject, including occupied oblasts. CCI fuel sub-indicator.
- **GUR Ukraine** (@DefenceU Telegram) — Confirmed infrastructure strike
  data. RPI strike sub-indicator.
- **ISW** (understandingwar.org) — Daily Russian Occupation Update.
  Highest-quality consistent source for occupied-territory developments.
- **UNN / Denys Chistikov** — June 12 2026 fuel/food crisis confirmation.
  Highest-confidence single CCI reading in dataset.
- **RFE/RL Crimea.Realities** — Regional civilian conditions reporting.

### Fiscal (OFP)
- **Minfin** (minfin.gov.ru) — Monthly NWF balance disclosures. OFP
  NWF component anchor. Liquid vs. illiquid breakdown requires reading
  against committed-position disclosures; headline NWF figure overstates
  deployable reserves.
- **Argus Media / Reuters** — Weekly Urals-Brent spread. OFP export
  revenue proxy price realization factor.
- **Kpler / Reuters** — Seaborne Russian export volumes. OFP export
  revenue proxy volume index.
- **Moscow Exchange / CBR** — OFZ auction results and price direction.
  OFP sovereign debt stress component.
- **Regional government statements / digest pipeline** — Confirmed
  budget transfer cuts. OFP regional cuts component. Event-driven;
  sourced to named officials or budget documents only.
- **Lloyd's of London / Reuters tanker tracking** — War risk premiums
  and shadow fleet operational status. OFP shadow fleet component.

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

For OFP specifically: Russian state sources (Minfin, CBR, Rosstat) are
used for the NWF and OFZ components because no independent alternative
exists. These are treated as directionally reliable — Russia has incentive
to project stability, meaning adverse readings in state-published data
carry more signal weight than stable or improving readings.

---

## Editorial pipeline (human review and score updates)

*The data-fetch and digest-generation pipeline itself is documented in
the engineering section above (1.2). This section covers what happens
after a digest is published — the analytical/editorial process for
turning a digest into an updated dashboard.*

```
Dashboard (public/index.html)
  → checkPending() on load
  → If pending and last_updated < digest date: show green banner
  → If pending and last_updated >= digest date: auto-clear, show
    quiet digest link
  → If not pending: show quiet digest link if last_digest_date exists

Digest reader (api/digest.js, with /api/digest/:date rewritten to it
by vercel.json)
  → Two-column layout: requested digest (4/5 width) + sidebar archive (1/5)
  → Sidebar lists all other digests, newest first, 120-char summary excerpts
  → Click any sidebar entry to make it primary

Human review
  → Read full digest via dashboard link or Telegram
  → Evaluate Dashboard Relevance section
  → Decide: score changes, key_events, or no action needed
  → If changes: edit data files and index.html seed data, commit, push
  → Vercel deploys → last_updated advances → banner auto-clears

OFP review (monthly)
  → Check Minfin NWF disclosure (monthly release)
  → Check Kpler/Reuters export volume and Urals-Brent spread
  → Check OFZ auction results and ruble direction
  → Check digest pipeline for regional budget cut events
  → Update occupation_financial_pressure.json
  → Sync SEED_OFP in index.html
  → Commit with note on which components moved and why
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
how much requires continuous state input to maintain. With the addition
of OFP, it also says how long that state input can be sustained at
current rates.

**It doesn't say:** when. A fragile configuration can persist for a long
time if no trigger arrives. MTCS 79 means the structure is under
significant stress and has no independent foundation. It does not mean
retreat is imminent — though in Crimea, behavioral change is already
underway rather than anticipated.

**It doesn't capture:** information that isn't in formal markets. The
most important Track B signals — decisions made in Donetsk kitchens,
informal cash deals that never touch Домклик — are invisible to the
model. The Telegram channel monitoring is an approximation, not a
substitute. The model also cannot fully capture the Donbas mortgage
signal without the population context documented above: the numbers are
real, but the population generating them is not representative of the
pre-war civilian base.

**It can be confused by:** exogenous shocks. The Iran nuclear MOU
(June 2026) affects Russian export revenue through a completely separate
mechanism from the Black Sea corridor interdiction campaign. Both show
up in the same OFP fiscal space but for different reasons. The model
currently does not distinguish them.

**When indicators reach their ceilings:** RPI (97) and CCI (100) are
at or near the top of their scoring range. The dials cannot express
"worse than critical." When this happens, the scoring notes and
key_events log carry the analytical weight. A ceiling reading means the
model's sensitivity in that dimension is exhausted, not that conditions
have stabilized.

**On the state of emergency declaration:** The formal declaration by
the Russian-installed Crimea administration on June 26, 2026 is an
event the model can log but not fully score — it is an administrative
acknowledgment of what the dials have been measuring, not a new data
point that moves them further. Its significance is confirmatory: the
occupation authority itself has now stated that normal governance has
failed.

**The most honest description:** a stress test, not a forecast. It tells
you the structure's load-bearing capacity and the durability of the
mechanism sustaining it. It cannot tell you when the weight becomes
too much.

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
│   ├── scores.js          # GET current dial values + computed
│   │                      #   ofp{current,modulator,mtcs_base,mtcs_final} (v5.0)
│   ├── events.js          # GET key_events array
│   ├── digest.js          # GET digest reader, two-column layout
│   │                      #   (/api/digest/:date rewritten here by vercel.json)
│   ├── monitor.js         # GET (cron) / POST (manual): full pipeline
│   └── pending.js         # GET/DELETE pending state
├── lib/
│   ├── firecrawl.js       # Search wrapper + 9 queries
│   ├── claude.js          # Synthesis API call + prompt
│   ├── telegram.js        # Outbound notification
│   └── storage.js         # Data read/write abstraction
├── public/
│   ├── index.html         # Dashboard (self-contained)
│   └── data/
│       ├── scores.json                        # Real estate dial values
│       ├── refinery_pressure.json             # RPI monthly readings
│       ├── civilian_confidence.json           # CCI monthly readings
│       └── occupation_financial_pressure.json # OFP monthly readings (v5.0)
├── server.js               # Express local dev server
└── vercel.json             # Cron schedule + CORS headers + digest rewrite rule
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
- **v5.0** — OFP (Occupation Financial Pressure) added as fiscal sector;
  MTCS modulator architecture (OFP amplifies base signal rather than
  averaging with it); layout inversion (MTCS prominent at top, sector
  signals in middle row, feeder dials below); three-panel MTCS display
  showing base, modulator, and final values transparently; plain-language
  MTCS status text
- **v5.1 (planned)** — Market Directionality indicator per city
  (State-Only / Captive / Watch / Exiting / Unknown);
  documents the phase of market participation, not just its level;
  interpretive layer only, does not feed into MTCS formula
- **Archive push (2026-07-14)** — fire-and-forget backup of every
  published digest to `davidfacer-archive`, per ADR-007. Not a
  methodology change — an infrastructure addition. See 1.2.

---

*Black Sea Monitor is an independent analytical project. It is not
affiliated with any government, intelligence agency, or news organization.
All source attributions are to publicly available reporting.*
