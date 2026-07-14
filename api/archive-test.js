// TEMPORARY, ONE-OFF endpoint. Writes a labelled synthetic test blob to
// black-sea-digests, pushes it through the real archive flow, and reports
// the result. Delete this file (and its Vercel deployment) after the
// synthetic test is confirmed -- not part of the permanent publication flow.
const { put } = require('@vercel/blob');

const TEST_KEY = 'digests/test-archive-2026-07-13.md';
const TEST_CONTENT = '# TEST — synthetic blob for archive push verification\n\nThis is a labelled test blob, not a real digest. Safe to delete.';

module.exports = async (req, res) => {
  const authHeader = req.headers.authorization;
  if (authHeader !== `Bearer ${process.env.BACKFILL_SECRET}`) {
    return res.status(401).json({ error: 'Unauthorized' });
  }

  try {
    await put(TEST_KEY, TEST_CONTENT, {
      access: 'public',
      contentType: 'text/markdown',
      addRandomSuffix: false,
      allowOverwrite: true,
    });

    const pushRes = await fetch(process.env.ARCHIVE_ENDPOINT, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${process.env.ARCHIVE_PUSH_SECRET}`,
      },
      body: JSON.stringify({ key: TEST_KEY, content: TEST_CONTENT }),
    });
    const pushJson = await pushRes.json().catch(() => ({}));

    return res.status(200).json({
      ok: true,
      source_write: TEST_KEY,
      push_status: pushRes.status,
      push_response: pushJson,
    });
  } catch (err) {
    console.error('[archive-test] error:', err.message);
    return res.status(500).json({ ok: false, error: err.message });
  }
};
