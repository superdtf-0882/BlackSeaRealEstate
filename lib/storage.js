const fs   = require('fs');
const path = require('path');

const SCORES_PATH = path.join(__dirname, '..', 'public', 'data', 'scores.json');
const RPI_PATH   = path.join(__dirname, '..', 'public', 'data', 'refinery_pressure.json');
const CCI_PATH   = path.join(__dirname, '..', 'public', 'data', 'civilian_confidence.json');
const OFP_PATH   = path.join(__dirname, '..', 'public', 'data', 'occupation_financial_pressure.json');

function read(filePath) {
  return JSON.parse(fs.readFileSync(filePath, 'utf8'));
}

function write(filePath, data) {
  fs.writeFileSync(filePath, JSON.stringify(data, null, 2), 'utf8');
}

function getScores() {
  return read(SCORES_PATH);
}

function setScores(data) {
  write(SCORES_PATH, data);
}

function getEvents() {
  return read(SCORES_PATH).key_events || [];
}

function appendEvent(event) {
  const scores = read(SCORES_PATH);
  scores.key_events = scores.key_events || [];
  scores.key_events.push(event);
  scores.key_events.sort((a, b) => a.date.localeCompare(b.date));
  write(SCORES_PATH, scores);
}

function getAllScores() {
  const scores = read(SCORES_PATH);
  let rpi = {}, cci = {}, ofp = {};
  try { const d = read(RPI_PATH); rpi = d.monthly_readings?.at(-1) ?? {}; } catch (_) {}
  try { const d = read(CCI_PATH); cci = d.monthly_readings?.at(-1) ?? {}; } catch (_) {}
  try { const d = read(OFP_PATH); ofp = d.monthly_readings?.at(-1) ?? {}; } catch (_) {}
  return { ...scores, rpi_current: rpi, cci_current: cci, ofp_current: ofp };
}

module.exports = { getScores, setScores, getEvents, appendEvent, getAllScores };
