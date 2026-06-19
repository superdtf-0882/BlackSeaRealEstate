const fs   = require('fs');
const path = require('path');

const DIGESTS_DIR = path.join(__dirname, '..', 'public', 'digests');

module.exports = (req, res) => {
  if (req.method !== 'GET') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  // Extract optional date param from URL: /api/digest/YYYY-MM-DD or /api/digest/latest
  const urlParts = req.url.split('/').filter(Boolean);
  const dateParam = urlParts[urlParts.length - 1];

  if (!fs.existsSync(DIGESTS_DIR)) {
    return res.status(404).json({ error: 'No digests yet' });
  }

  const files = fs.readdirSync(DIGESTS_DIR)
    .filter(f => f.endsWith('.md'))
    .sort()
    .reverse();

  if (!files.length) {
    return res.status(404).json({ error: 'No digests yet' });
  }

  let targetFile;
  if (!dateParam || dateParam === 'latest' || dateParam === 'digest') {
    targetFile = files[0];
  } else {
    targetFile = files.find(f => f === `${dateParam}.md`);
    if (!targetFile) {
      return res.status(404).json({ error: `No digest for ${dateParam}` });
    }
  }

  const content = fs.readFileSync(path.join(DIGESTS_DIR, targetFile), 'utf8');
  res.setHeader('Content-Type', 'text/markdown; charset=utf-8');
  res.status(200).send(content);
};
