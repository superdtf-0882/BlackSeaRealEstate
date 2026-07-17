require('dotenv').config({ path: '.env', override: true });

const { head }   = require('@vercel/blob');
const { marked } = require('marked');

function formatDate(d, sequence) {
  const label = new Date(d + 'T00:00:00').toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
  return sequence > 1 ? `${label} (${ordinal(sequence)} update)` : label;
}

function ordinal(n) {
  const s = ['th','st','nd','rd'];
  const v = n % 100;
  return n + (s[(v - 20) % 10] || s[v] || s[0]);
}

module.exports = async (req, res) => {
  if (req.method !== 'GET') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  // Date param — Vercel rewrite passes /api/digest/:date as ?date=
  const rawDate = req.query?.date || req.params?.date
    || req.url.split('?')[0].split('/').filter(Boolean).pop();
  const requestedDate = (!rawDate || rawDate === 'latest' || rawDate === 'digest')
    ? null
    : rawDate;

  // Optional sequence param: ?seq=N
  const requestedSeq = req.query?.seq ? parseInt(req.query.seq, 10) : null;

  try {
    // Load index
    let index = [];
    try {
      const indexBlob = await head('digests/index.json');
      index = await fetch(indexBlob.url).then(r => r.json());
    } catch (_) {}

    if (!index.length) {
      return res.status(404).send('No digests yet.');
    }

    // Resolve primary entry
    let primary;
    if (requestedDate) {
      const dateEntries = index.filter(e => e.date === requestedDate);
      if (!dateEntries.length) {
        return res.status(404).send(`No digest found for ${requestedDate}`);
      }
      if (requestedSeq) {
        primary = dateEntries.find(e => (e.sequence || 1) === requestedSeq);
        if (!primary) return res.status(404).send(`No digest for ${requestedDate} seq ${requestedSeq}`);
      } else {
        // Default: highest sequence for that date
        primary = dateEntries.reduce((best, e) => (e.sequence || 1) > (best.sequence || 1) ? e : best);
      }
    } else {
      // Latest: highest sequence of the most recent date
      const latestDate = index[0].date;
      const latestEntries = index.filter(e => e.date === latestDate);
      primary = latestEntries.reduce((best, e) => (e.sequence || 1) > (best.sequence || 1) ? e : best);
    }

    // Fetch primary content
    const primaryContent = await fetch(primary.url).then(r => r.text());
    const primaryHtml = marked.parse(primaryContent);

    // Sidebar — all entries except current primary, sorted newest/highest-seq first
    const sidebarItems = index.filter(e => !(e.date === primary.date && (e.sequence || 1) === (primary.sequence || 1)));

    function sidebarHref(item) {
      const seq = item.sequence || 1;
      return seq > 1
        ? `/api/digest/${item.date}?seq=${seq}`
        : `/api/digest/${item.date}`;
    }

    const sidebarHtml = sidebarItems.map(item => {
      const seq = item.sequence || 1;
      const excerpt = item.summary.length > 120 ? item.summary.slice(0, 120) + '…' : item.summary;
      return `<a href="${sidebarHref(item)}" class="sidebar-card">
        <div class="sidebar-date">${formatDate(item.date, seq)}</div>
        <div class="sidebar-excerpt">${excerpt}</div>
        <div class="sidebar-arrow">→</div>
      </a>`;
    }).join('');

    const navDate = formatDate(primary.date, primary.sequence || 1);

    const html = `<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Black Sea Monitor — Digest ${primary.date}${(primary.sequence || 1) > 1 ? ' #' + primary.sequence : ''}</title>
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
      font-size: 14px; line-height: 1.7;
      color: #c9d1d9; background: #0d1117;
    }
    .site-topbar {
      background: #0d1117; border-bottom: 1px solid #21262d;
      padding: 12px 24px 10px; display: flex; flex-direction: column; gap: 6px;
    }
    .site-identity-mark { display: flex; align-items: center; gap: 10px; text-decoration: none; width: fit-content; }
    .site-identity-mark img { width: 28px; height: 34px; border-radius: 6px; object-fit: cover; object-position: center 30%; border: 1px solid #21262d; }
    .site-identity-mark span { font-size: 13px; color: #8b949e; letter-spacing: 0.02em; }
    .site-breadcrumb { font-size: 11px; text-transform: uppercase; letter-spacing: 0.08em; color: #8b949e; }
    .site-breadcrumb a { color: #8b949e; text-decoration: none; }
    .site-breadcrumb a:hover { text-decoration: underline; }
    .site-breadcrumb-sep { margin: 0 8px; opacity: 0.5; }
    .site-attribution {
      position: fixed; bottom: 16px; right: 20px; z-index: 30;
      font-size: 11px; color: #8b949e; text-decoration: none;
      background: #0d1117; padding: 2px 6px; border-radius: 4px;
    }
    .site-attribution:hover { color: #e6edf3; }
    .layout {
      display: grid;
      grid-template-columns: 4fr 1fr;
      min-height: 100vh;
    }
    .main { padding: 32px 40px 60px; max-width: 740px; }
    .nav {
      display: flex; justify-content: space-between; align-items: center;
      padding-bottom: 16px; margin-bottom: 8px;
      border-bottom: 1px solid #21262d;
      font-size: 12px; color: #8b949e;
    }
    .nav a { color: #58a6ff; text-decoration: none; }
    .nav a:hover { text-decoration: underline; }
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
    a { color: #58a6ff; }
    .footer {
      margin-top: 48px; padding-top: 16px;
      border-top: 1px solid #21262d;
      font-size: 11px; color: #8b949e;
    }
    .sidebar {
      background: #161b22;
      border-left: 1px solid #21262d;
      padding: 32px 16px;
      overflow-y: auto;
      max-height: 100vh;
      position: sticky;
      top: 0;
    }
    .sidebar-header {
      font-size: 11px; font-weight: 600; color: #8b949e;
      text-transform: uppercase; letter-spacing: 0.05em;
      margin-bottom: 16px; padding-bottom: 8px;
      border-bottom: 1px solid #21262d;
    }
    .sidebar-card {
      display: block; text-decoration: none;
      background: #0d1117; border: 1px solid #21262d;
      border-radius: 8px; padding: 12px 14px; margin-bottom: 10px;
      transition: border-color 0.15s ease;
    }
    .sidebar-card:hover { border-color: #58a6ff; }
    .sidebar-date { font-size: 11px; font-weight: 600; color: #58a6ff; margin-bottom: 6px; }
    .sidebar-excerpt { font-size: 12px; line-height: 1.5; color: #8b949e; margin-bottom: 6px; }
    .sidebar-arrow { font-size: 12px; color: #58a6ff; text-align: right; }
    @media (max-width: 900px) {
      .layout { grid-template-columns: 1fr; }
      .sidebar { border-left: none; border-top: 1px solid #21262d; position: static; max-height: none; }
    }
  </style>
</head>
<body>
  <div class="site-topbar">
    <a href="https://davidfacer.com/" class="site-identity-mark">
      <img src="/HeadshotBW.jpg" alt="">
      <span>David Facer</span>
    </a>
    <div class="site-breadcrumb">
      <a href="https://davidfacer.com/">← davidfacer.com</a>
      <span class="site-breadcrumb-sep">/</span>
      <span>Research</span>
    </div>
  </div>
  <div class="layout">
    <div class="main">
      <div class="nav">
        <a href="https://davidfacer.com/blackseamonitor/">← Black Sea Monitor</a>
        <span>${navDate}</span>
      </div>
      ${primaryHtml}
      <div class="footer">Black Sea Monitor · Methodology v5.0</div>
    </div>
    <div class="sidebar">
      <div class="sidebar-header">Previous Digests</div>
      ${sidebarHtml || '<div style="font-size:12px;color:#8b949e">No earlier digests yet.</div>'}
    </div>
  </div>
  <a href="https://davidfacer.com/" class="site-attribution">© 2026 David Facer</a>
</body>
</html>`;

    res.setHeader('Content-Type', 'text/html; charset=utf-8');
    res.setHeader('X-Digest-Date', primary.date);
    res.setHeader('X-Digest-Sequence', String(primary.sequence || 1));
    res.status(200).send(html);

  } catch (err) {
    console.error('digest.js error:', err.message);
    return res.status(500).json({ error: err.message });
  }
};
