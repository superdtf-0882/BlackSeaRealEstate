const ALLOWED_ORIGINS = ['https://davidfacer.com', 'http://localhost:3000'];

module.exports = (req, res) => {
  const origin = req.headers.origin;
  if (ALLOWED_ORIGINS.includes(origin)) {
    res.setHeader('Access-Control-Allow-Origin', origin);
  }
  res.setHeader('Access-Control-Allow-Methods', 'GET, OPTIONS');
  res.setHeader('Content-Type', 'application/json');

  if (req.method === 'OPTIONS') return res.status(200).end();

  res.json({ digest: 'No digest yet.', date: null });
};
