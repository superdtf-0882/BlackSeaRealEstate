require('dotenv').config({ path: '.env', override: true });

const { put, list } = require('@vercel/blob');

async function readPending() {
  try {
    const { blobs } = await list({ prefix: 'pending.json' });
    const blob = blobs.find(b => b.pathname === 'pending.json');
    if (!blob) return null;
    const res = await fetch(blob.url);
    if (!res.ok) return null;
    return await res.json();
  } catch (_) { return null; }
}

async function writePending(data) {
  await put('pending.json', JSON.stringify(data), {
    access: 'public',
    contentType: 'application/json',
    addRandomSuffix: false,
    allowOverwrite: true,
  });
}

module.exports = async (req, res) => {
  res.setHeader('Content-Type', 'application/json');

  if (req.method === 'GET') {
    try {
      const data = await readPending();
      return res.status(200).json(data || { pending: false });
    } catch (err) {
      return res.status(500).json({ error: 'Failed to read pending state' });
    }
  }

  if (req.method === 'DELETE') {
    try {
      const existing = await readPending() || {};
      await writePending({
        pending: false,
        last_digest_date: existing.last_digest_date || existing.date || null,
        digest_url: existing.digest_url || null,
      });
      return res.status(200).json({ ok: true, cleared: true });
    } catch (err) {
      return res.status(500).json({ error: 'Failed to clear pending state' });
    }
  }

  return res.status(405).json({ error: 'Method not allowed' });
};
