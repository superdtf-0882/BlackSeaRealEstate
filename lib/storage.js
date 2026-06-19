const fs   = require('fs');
const path = require('path');

const SCORES_PATH = path.join(__dirname, '..', 'public', 'data', 'scores.json');

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

module.exports = { getScores, setScores, getEvents, appendEvent };
