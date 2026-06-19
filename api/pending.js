const fs   = require('fs');
const path = require('path');

const PENDING_PATH = path.join(__dirname, '..', 'public', 'data', 'pending.json');

module.exports = (req, res) => {
  res.setHeader('Content-Type', 'application/json');

  if (req.method === 'GET') {
    if (!fs.existsSync(PENDING_PATH)) {
      return res.status(200).json({ pending: false });
    }
    try {
      const data = JSON.parse(fs.readFileSync(PENDING_PATH, 'utf8'));
      return res.status(200).json(data);
    } catch (err) {
      return res.status(500).json({ error: 'Failed to read pending state' });
    }
  }

  if (req.method === 'DELETE') {
    try {
      let existing = {};
      try { existing = JSON.parse(fs.readFileSync(PENDING_PATH, 'utf8')); } catch (_) {}
      fs.writeFileSync(PENDING_PATH, JSON.stringify({
        pending: false,
        last_digest_date: existing.last_digest_date || existing.date || null,
      }, null, 2), 'utf8');
      return res.status(200).json({ ok: true, cleared: true });
    } catch (err) {
      return res.status(500).json({ error: 'Failed to clear pending state' });
    }
  }

  return res.status(405).json({ error: 'Method not allowed' });
};
