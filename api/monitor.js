require('dotenv').config({ path: '.env', override: true });

const { put, head } = require('@vercel/blob');
const storage = require('../lib/storage');
const { fetchNews }    = require('../lib/firecrawl');
const { synthesize }   = require('../lib/claude');
const { sendMessage }  = require('../lib/telegram');

async function writePending(data) {
  await put('pending.json', JSON.stringify(data), {
    access: 'public',
    contentType: 'application/json',
    addRandomSuffix: false,
    allowOverwrite: true,
  });
}

module.exports = async (req, res) => {
  if (req.method !== 'GET' && req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  // GET = cron-initiated; require CRON_SECRET to prevent casual triggering
  if (req.method === 'GET') {
    const authHeader = req.headers.authorization;
    if (authHeader !== `Bearer ${process.env.CRON_SECRET}`) {
      return res.status(401).json({ error: 'Unauthorized' });
    }
  }

  const now   = new Date();
  const today = now.toISOString().split('T')[0];
  const time  = now.toISOString();

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

    // 5. Load index and determine sequence for today
    let index = [];
    try {
      const indexBlob = await head('digests/index.json');
      index = await fetch(indexBlob.url).then(r => r.json());
    } catch (_) {}

    const todayEntries = index.filter(e => e.date === today);
    const sequence = todayEntries.length + 1;
    const filename = sequence === 1 ? `digests/${today}.md` : `digests/${today}-${sequence}.md`;

    // 6. Write digest to Vercel Blob
    const blob = await put(filename, digest, {
      access: 'public',
      contentType: 'text/markdown',
      addRandomSuffix: false,
      allowOverwrite: true,
    });

    // 7. Update index — append new entry, sort newest first
    const seqSuffix = sequence > 1 ? `?seq=${sequence}` : '';
    const digestApiUrl = `https://black-sea-real-estate.vercel.app/api/digest/${today}${seqSuffix}`;

    index.push({ date: today, sequence, time, summary, url: blob.url });
    index.sort((a, b) => {
      const dateDiff = new Date(b.date) - new Date(a.date);
      return dateDiff !== 0 ? dateDiff : (b.sequence || 1) - (a.sequence || 1);
    });

    await put('digests/index.json', JSON.stringify(index), {
      access: 'public',
      contentType: 'application/json',
      addRandomSuffix: false,
      allowOverwrite: true,
    });

    // 8. Detect significance
    const isSignificant = !digest.includes('No items meet dashboard-update threshold');

    if (!isSignificant) {
      // Condition 2 — nothing dashboard-relevant
      await writePending({
        pending: false,
        date: today,
        time,
        last_digest_date: today,
        digest_url: digestApiUrl,
        summary,
        resultsCount: newsResults.length,
      });
      try {
        await sendMessage(`📰 Monitor ran — ${newsResults.length} results, nothing dashboard-relevant today. Digest at ${digestApiUrl}`);
      } catch (_) {}
      return res.status(200).json({ ok: true, significant: false, date: today, sequence, resultsCount: newsResults.length, digestUrl: digestApiUrl });
    }

    // Condition 3 — dashboard-relevant
    await writePending({
      pending: true,
      date: today,
      time,
      sequence,
      summary,
      resultsCount: newsResults.length,
      last_digest_date: today,
      digest_url: digestApiUrl,
    });

    try {
      const seqLabel = sequence > 1 ? ` (update ${sequence})` : '';
      await sendMessage(`📋 *Black Sea Monitor — ${today}${seqLabel}*\n\n${summary}\n\n_${newsResults.length} news results processed_\n\nReview at: https://black-sea-real-estate.vercel.app`);
    } catch (tgErr) {
      console.error('Telegram send failed:', tgErr.message);
    }

    return res.status(200).json({
      ok: true,
      significant: true,
      date: today,
      sequence,
      time,
      resultsCount: newsResults.length,
      digestUrl: digestApiUrl,
    });

  } catch (err) {
    console.error('Monitor pipeline error:', err.message);
    try {
      await sendMessage(`🚨 Monitor pipeline error: ${err.message}`);
    } catch (_) {}
    return res.status(500).json({ ok: false, error: err.message });
  }
};
