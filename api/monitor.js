require('dotenv').config({ path: '.env', override: true });

const fs      = require('fs');
const path    = require('path');
const storage = require('../lib/storage');
const { fetchNews }    = require('../lib/firecrawl');
const { synthesize }   = require('../lib/claude');
const { sendMessage }  = require('../lib/telegram');

const PENDING_PATH = path.join(__dirname, '..', 'public', 'data', 'pending.json');

function readPending() {
  try { return JSON.parse(fs.readFileSync(PENDING_PATH, 'utf8')); } catch (_) { return {}; }
}

function writePending(data) {
  fs.writeFileSync(PENDING_PATH, JSON.stringify(data, null, 2), 'utf8');
}

module.exports = async (req, res) => {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed — use POST' });
  }

  const today = new Date().toISOString().split('T')[0];

  try {
    // 1. Current scores
    const currentScores = storage.getScores();

    // 2. Fetch news
    const newsResults = await fetchNews();

    // Condition 1 — no results
    if (!newsResults || newsResults.length === 0) {
      try {
        await sendMessage('🔍 Monitor ran — 0 results returned. Check Firecrawl API or query list.');
      } catch (_) {}
      return res.status(200).json({ ok: false, reason: 'no_results' });
    }

    // 3. Synthesize
    const raw = await synthesize(newsResults, currentScores);

    // 4. Parse
    let summary, digest;
    if (raw.includes('===DIGEST===')) {
      const parts = raw.split('===DIGEST===');
      summary = parts[0].trim();
      digest  = parts[1].trim();
    } else {
      console.warn('WARNING: ===DIGEST=== delimiter not found in Claude response');
      summary = 'Digest generated — see full text.';
      digest  = raw.trim();
    }

    // 5. Write digest file
    const digestsDir = path.join(__dirname, '..', 'public', 'digests');
    if (!fs.existsSync(digestsDir)) fs.mkdirSync(digestsDir, { recursive: true });
    const digestPath = path.join(digestsDir, `${today}.md`);
    fs.writeFileSync(digestPath, digest, 'utf8');

    // 6. Detect significance
    const isSignificant = !digest.includes('No items meet dashboard-update threshold');

    if (!isSignificant) {
      // Condition 2 — nothing dashboard-relevant
      writePending({
        pending: false,
        last_digest_date: today,
        summary,
        resultsCount: newsResults.length,
      });
      try {
        await sendMessage(`📰 Monitor ran — ${newsResults.length} results, nothing dashboard-relevant today. Digest at /api/digest/latest`);
      } catch (_) {}
      return res.status(200).json({ ok: true, significant: false, date: today, resultsCount: newsResults.length });
    }

    // Condition 3 — dashboard-relevant
    writePending({
      pending: true,
      date: today,
      summary,
      resultsCount: newsResults.length,
      last_digest_date: today,
    });

    try {
      await sendMessage(`📋 *Black Sea Monitor — ${today}*\n\n${summary}\n\n_${newsResults.length} news results processed_\n\nReview at: https://black-sea-real-estate.vercel.app`);
    } catch (tgErr) {
      console.error('Telegram send failed:', tgErr.message);
    }

    return res.status(200).json({
      ok: true,
      significant: true,
      date: today,
      resultsCount: newsResults.length,
      digestPath: `public/digests/${today}.md`,
    });

  } catch (err) {
    console.error('Monitor pipeline error:', err.message);
    try {
      await sendMessage(`🚨 Monitor pipeline error: ${err.message}`);
    } catch (_) {}
    return res.status(500).json({ ok: false, error: err.message });
  }
};
