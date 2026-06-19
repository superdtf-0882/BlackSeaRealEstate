require('dotenv').config({ path: '.env', override: true });

const SYSTEM_PROMPT = `You are producing a news digest for the Black Sea Monitor — an early warning dashboard tracking real estate, energy infrastructure, and civilian conditions in Russian-occupied Ukraine (Mariupol, Donetsk, Luhansk, Crimea, Berdiansk).

You will be given: (1) news search results from the last 24 hours, and (2) the current dashboard state including all dial values and key_events already logged.

Produce TWO outputs, separated by a line containing exactly: ===DIGEST===

1. SUMMARY (above the separator): 3-5 sentences, plain text, no markdown formatting:
   - If nothing significant: state that plainly. Do not manufacture urgency.
   - If something significant: name it specifically (what, where, when) in the first sentence.
   - If an item is already in key_events (check the current_scores.key_events array), do not treat it as new.

2. MARKDOWN DIGEST (below the separator):
   - Use this exact structure, including headers even if a section is empty:

# Black Sea Monitor — Digest [DATE]

## Civilian Conditions (Crimea/Azov fuel, food, rationing)
[Findings with source + date, or "No significant developments."]

## Infrastructure & Logistics (strikes, corridor, ports)
[Findings with source + date, or "No significant developments."]

## Real Estate & Property Administration
[Findings with source + date, or "No significant developments."]

## Refinery & Export Pressure
[Findings with source + date, or "No significant developments."]

## Banking & Mortgage Programs
[Findings with source + date, or "No significant developments."]

## Dashboard Relevance
[Only include items here that plausibly affect RPI, CCI, SCI, Track A, or Track B AND are not already in key_events. For each: name the metric, its current value from current_scores, suggested direction and magnitude, reasoning in 1-2 sentences. If nothing qualifies write "No items meet dashboard-update threshold."]

RULES:
- Every factual claim must cite source name and date from the news results.
- Ignore irrelevant results (generic war coverage, opinion pieces, duplicates).
- Do not speculate beyond what sources state.
- Label Russian state media claims [unverified - Russian state source].
- Label Ukrainian partisan/resistance network claims (Atesh, NRC) [unverified - Ukrainian partisan source].
- Keep each category section to 2-4 sentences max.
- The string "===DIGEST===" must appear exactly once. Do not use horizontal rules (---) anywhere.
- Within Dashboard Relevance, always state the current dial value before suggesting a change.

DASHBOARD METHODOLOGY REFERENCE:
- SCI (State Commitment Index): Federal budget + contractor starts + mortgage subsidy cost. Higher = more state investment.
- Track A (Private Market): Non-state developer entry + cash transactions + price momentum. Higher = genuine private capital.
- Track B (Residential Outcome): Listing depth + buyer permanence + rental ratio. Higher = locals making irreversible bets.
- Composite Spread = B − (SCI×0.4 + A×0.6). Negative = fragility signal.
- RPI (Refinery Pressure Index): Infrastructure strikes + corridor traffic + export capacity. Higher = more fiscal pressure on occupation funding.
- CCI (Civilian Confidence Index): Fuel rationing + food shortages + panic purchasing + grey market. Higher = more acute civilian distress.
- ECS = (RPI×0.5) + (CCI×0.5)
- MTCS = synthesizes real estate pressure and ECS (0-100, higher = more fragile).
Alert thresholds: RPI/CCI >50 = warning, >70 = critical. Single-period increase >25pts = structural event flag.`;

async function synthesize(newsResults, currentScores) {
  const apiKey = process.env.ANTHROPIC_API_KEY;
  if (!apiKey) throw new Error('ANTHROPIC_API_KEY not set');

  const userMessage = JSON.stringify({
    news: newsResults,
    current_scores: currentScores,
    date: new Date().toISOString().split('T')[0],
  });

  const res = await fetch('https://api.anthropic.com/v1/messages', {
    method: 'POST',
    headers: {
      'x-api-key': apiKey,
      'anthropic-version': '2023-06-01',
      'content-type': 'application/json',
    },
    body: JSON.stringify({
      model: 'claude-sonnet-4-6',
      max_tokens: 2000,
      system: SYSTEM_PROMPT,
      messages: [{ role: 'user', content: userMessage }],
    }),
  });

  if (!res.ok) {
    const err = await res.text();
    throw new Error(`Anthropic API error ${res.status}: ${err}`);
  }

  const data = await res.json();
  return data.content[0].text;
}

module.exports = { synthesize };
