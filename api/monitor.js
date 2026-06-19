require('dotenv').config({ path: '.env', override: true });

const fs      = require('fs');
const path    = require('path');
const storage = require('../lib/storage');
const { fetchNews }    = require('../lib/firecrawl');
const { synthesize }   = require('../lib/claude');
const { sendMessage }  = require('../lib/telegram');

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

    // 6. Write pending state (preserve last_digest_date across future clears)
    const pendingPath = path.join(__dirname, '..', 'public', 'data', 'pending.json');
    let existing = {};
    try { existing = JSON.parse(fs.readFileSync(pendingPath, 'utf8')); } catch (_) {}
    fs.writeFileSync(pendingPath, JSON.stringify({
      pending: true,
      date: today,
      summary,
      resultsCount: newsResults.length,
      last_digest_date: today,
    }, null, 2), 'utf8');

    // 7. Send Telegram
    const tgMessage = `📋 *Black Sea Monitor — ${today}*\n\n${summary}\n\n_${newsResults.length} news results processed_\n\nReview at: https://black-sea-real-estate.vercel.app`;
    try {
      await sendMessage(tgMessage);
    } catch (tgErr) {
      console.error('Telegram send failed:', tgErr.message);
    }

    // 8. Respond
    return res.status(200).json({
      ok: true,
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
