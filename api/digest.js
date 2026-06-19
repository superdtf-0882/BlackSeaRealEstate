require('dotenv').config({ path: '.env', override: true });

const { list }   = require('@vercel/blob');
const { marked } = require('marked');

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
    const date = target.pathname.replace('digests/', '').replace('.md', '');

    const html = `<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Black Sea Monitor — Digest ${date}</title>
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      max-width: 740px; margin: 40px auto; padding: 0 24px 60px;
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
      font-size: 14px; line-height: 1.7;
      color: #c9d1d9; background: #0d1117;
    }
    h1 {
      font-size: 20px; font-weight: 600; color: #e6edf3;
      margin: 32px 0 8px; padding-bottom: 12px;
      border-bottom: 1px solid #21262d;
    }
    h2 {
      font-size: 14px; font-weight: 600; color: #e6edf3;
      margin: 28px 0 10px; padding-bottom: 8px;
      border-bottom: 1px solid #21262d;
      text-transform: uppercase; letter-spacing: 0.05em;
    }
    p { margin-bottom: 12px; color: #c9d1d9; }
    strong { color: #e6edf3; font-weight: 600; }
    em { color: #8b949e; font-style: italic; }
    a { color: #58a6ff; text-decoration: none; }
    a:hover { text-decoration: underline; }
    .nav {
      display: flex; justify-content: space-between; align-items: center;
      padding: 16px 0; margin-bottom: 8px;
      border-bottom: 1px solid #21262d;
      font-size: 12px; color: #8b949e;
    }
    .nav a { color: #58a6ff; }
    .badge {
      display: inline-block; font-size: 11px; padding: 2px 8px;
      border-radius: 20px; margin-right: 4px; font-weight: 500;
    }
    .high { background: #3d1f1f; color: #f85149; }
    .medium { background: #2d2a1f; color: #d29922; }
    .low { background: #1f2d1f; color: #3fb950; }
    .source { font-size: 11px; color: #8b949e; }
    hr { border: none; border-top: 1px solid #21262d; margin: 24px 0; }
    .footer {
      margin-top: 48px; padding-top: 16px;
      border-top: 1px solid #21262d;
      font-size: 11px; color: #8b949e;
      display: flex; justify-content: space-between;
    }
  </style>
</head>
<body>
  <div class="nav">
    <a href="https://black-sea-real-estate.vercel.app">← Black Sea Monitor</a>
    <span>Digest · ${date}</span>
  </div>
  ${marked.parse(content)}
  <div class="footer">
    <span>Black Sea Monitor · Methodology v4.0</span>
    <a href="https://black-sea-real-estate.vercel.app">Return to dashboard →</a>
  </div>
</body>
</html>`;

    res.setHeader('Content-Type', 'text/html; charset=utf-8');
    res.setHeader('X-Digest-Date', date);
    res.status(200).send(html);

  } catch (err) {
    console.error('digest.js error:', err.message);
    return res.status(500).json({ error: err.message });
  }
};
