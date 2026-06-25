const fs = require('fs');
const path = require('path');
const storage = require('../lib/storage');

const ALLOWED_ORIGINS = ['https://davidfacer.com', 'http://localhost:3000'];

const DATA_DIR = path.join(__dirname, '..', 'public', 'data');

function readJSON(filename) {
  try {
    return JSON.parse(fs.readFileSync(path.join(DATA_DIR, filename), 'utf8'));
  } catch (_) {
    return null;
  }
}

// Same modulator bands as the client (index.html ofpModulator) — kept in sync manually.
function ofpModulator(ofpVal) {
  if (ofpVal === null || ofpVal === undefined) return 0;
  if (ofpVal > 85) return 8;
  if (ofpVal > 70) return 6;
  if (ofpVal > 55) return 4;
  if (ofpVal > 40) return 2;
  return 0;
}

// Mirrors the client's computeMtcsDetail — always uses each city's latest history entry
// (server has no "viewMonth" concept; this matches the dashboard's default/live view).
function computeOfpPayload(scores, rpiData, cciData, ofpData) {
  const rpiReadings = (rpiData?.monthly_readings || []).filter(r => r.RPI != null);
  const cciReadings = (cciData?.monthly_readings || []).filter(r => r.CCI != null);
  const ofpReadings = (ofpData?.monthly_readings || []).filter(r => r.OFP != null);

  const latestRpi = rpiReadings[rpiReadings.length - 1];
  const latestCci = cciReadings[cciReadings.length - 1];
  const latestOfp = ofpReadings[ofpReadings.length - 1];

  if (!latestRpi || !latestCci || !latestOfp || !scores?.cities) return null;

  const ecsVal = Math.round(latestRpi.RPI * 0.5 + latestCci.CCI * 0.5);

  const WEIGHTS = { mariupol: 1.0, donetsk: 1.0, luhansk: 1.0, crimea: 1.2, berdiansk: 0.7 };
  let totalW = 0, wREP = 0;
  for (const [key, city] of Object.entries(scores.cities)) {
    const hist = city.history || [];
    const h = hist[hist.length - 1];
    if (!h) continue;
    const spread = h.spread ?? (h.track_b - Math.round(h.SCI * 0.4 + h.track_a * 0.6));
    const rep = 50 - spread;
    const w = WEIGHTS[key] ?? 1.0;
    wREP += rep * w;
    totalW += w;
  }
  if (!totalW) return null;

  const corridorREP = wREP / totalW;
  const base = Math.round(corridorREP * 0.5 + ecsVal * 0.5);
  const modulator = ofpModulator(latestOfp.OFP);
  const mtcs_final = Math.min(100, base + modulator);

  return {
    current: latestOfp.OFP,
    modulator,
    mtcs_base: base,
    mtcs_final,
  };
}

module.exports = (req, res) => {
  const origin = req.headers.origin;
  if (ALLOWED_ORIGINS.includes(origin)) {
    res.setHeader('Access-Control-Allow-Origin', origin);
  }
  res.setHeader('Access-Control-Allow-Methods', 'GET, OPTIONS');
  res.setHeader('Content-Type', 'application/json');

  if (req.method === 'OPTIONS') return res.status(200).end();

  try {
    const scores = storage.getScores();

    const rpiData = readJSON('refinery_pressure.json');
    const cciData = readJSON('civilian_confidence.json');
    const ofpData = readJSON('occupation_financial_pressure.json');

    const ofp = computeOfpPayload(scores, rpiData, cciData, ofpData);
    if (ofp) scores.ofp = ofp;

    res.json(scores);
  } catch (err) {
    res.status(500).json({ error: 'Failed to read scores', detail: err.message });
  }
};
