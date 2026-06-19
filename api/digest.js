require('dotenv').config({ path: '.env', override: true });

const { list } = require('@vercel/blob');

module.exports = async (req, res) => {
  if (req.method !== 'GET') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  // Extract date param — Vercel rewrites pass it as query string (?date=latest)
  const dateParam = req.query?.date || req.params?.date
    || req.url.split('/').filter(Boolean).pop();

  try {
    const { blobs } = await list({ prefix: 'digests/' });

    const digests = blobs
      .filter(b => b.pathname.endsWith('.md'))
      .sort((a, b) => b.pathname.localeCompare(a.pathname));

    if (!digests.length) {
      return res.status(404).json({ error: 'No digests yet' });
    }

    let target;
    if (!dateParam || dateParam === 'latest' || dateParam === 'digest') {
      target = digests[0];
    } else {
      target = digests.find(b => b.pathname === `digests/${dateParam}.md`);
      if (!target) {
        return res.status(404).json({ error: `No digest for ${dateParam}` });
      }
    }

    const fetchRes = await fetch(target.url);
    if (!fetchRes.ok) {
      return res.status(502).json({ error: 'Failed to fetch digest from storage' });
    }
    const content = await fetchRes.text();
    res.setHeader('Content-Type', 'text/markdown; charset=utf-8');
    res.status(200).send(content);

  } catch (err) {
    console.error('digest.js error:', err.message);
    return res.status(500).json({ error: err.message });
  }
};
