// TEMPORARY, ONE-OFF endpoint. Backfills all existing digests/*.md and
// digests/index.json into davidfacer-archive via /api/blob-receive.
// Delete this file (and its Vercel deployment) once the backfill is
// confirmed -- it is not part of the permanent publication flow.
const { list } = require('@vercel/blob');

module.exports = async (req, res) => {
  const authHeader = req.headers.authorization;
  if (authHeader !== `Bearer ${process.env.BACKFILL_SECRET}`) {
    return res.status(401).json({ error: 'Unauthorized' });
  }

  const results = [];
  let cursor;

  try {
    do {
      const page = await list({ prefix: 'digests/', cursor });
      for (const blob of page.blobs) {
        const content = await fetch(blob.url).then((r) => r.text());
        const pushRes = await fetch(process.env.ARCHIVE_ENDPOINT, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${process.env.ARCHIVE_PUSH_SECRET}`,
          },
          body: JSON.stringify({ key: blob.pathname, content }),
        });
        const pushJson = await pushRes.json().catch(() => ({}));
        results.push({ key: blob.pathname, status: pushRes.status, response: pushJson });
        console.log(`[archive-backfill] ${blob.pathname} -> ${pushRes.status}`, JSON.stringify(pushJson));
      }
      cursor = page.cursor;
    } while (cursor);

    return res.status(200).json({ ok: true, count: results.length, results });
  } catch (err) {
    console.error('[archive-backfill] error:', err.message);
    return res.status(500).json({ ok: false, error: err.message, results });
  }
};
