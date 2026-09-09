#!/usr/bin/env node
'use strict';
// scripts/build-seeds.js — regenerate the embedded seed block in
// public/index.html from the live files in public/data/.
//
// WHY THIS EXISTS. The seeds are a hand-maintained copy of the data, and on
// 2026-09-09 they were found stale: SEED_SCORES carried 99 key_events ending
// 2026-07-16 against a live 199 ending 2026-09-07, and SEED_RPI carried
// strike_score 88 against a live 95. fetchJSON falls back to them silently,
// so a fetch failure rendered those numbers with no error shown.
//
// The seeds cannot simply be deleted: index.html's own comment says they are
// "Embedded so the file works from file:// without a server", and under
// file:// a fetch of data/*.json is blocked by the browser. So the fix is to
// make the copy REPRODUCIBLE rather than maintained — run this after any data
// change and the copy is exact again — and to make the fallback VISIBLE, which
// index.html now does with a banner naming every seeded source.
//
// TRIMMING RULE, and it is mechanical rather than editorial: every file is
// mirrored in full EXCEPT `note` fields, which are dropped at every depth.
// Nothing in index.html renders a `note` — verified by grep — so they are
// payload for a fallback that never displays them. They are 14,037 chars of
// city history, 6,261 of scoring_notes, and 6.5k–11k in each index series.
// No other field is dropped, no array is truncated, and no content decision
// is made here.
//
// Usage:
//   node scripts/build-seeds.js            # report the diff in size, write nothing
//   node scripts/build-seeds.js --write    # rewrite the block in public/index.html

const fs = require('fs');
const path = require('path');

const ROOT = path.join(__dirname, '..');
const DATA = path.join(ROOT, 'public', 'data');
const PAGE = path.join(ROOT, 'public', 'index.html');

const BEGIN = '// ── Seed data ──';
const END = '// ── State ──';

// name -> file. Order matches the destructuring in init().
const SEEDS = [
  ['SEED_PRICES', 'crimea_prices.json'],
  ['SEED_DEVS', 'developer_counts.json'],
  ['SEED_MORT', 'mortgage_volumes.json'],
  ['SEED_SCORES', 'scores.json'],
  ['SEED_PERM', 'permanence_ratio.json'],
  ['SEED_DOMCLICK', 'domclick_listings.json'],
  ['SEED_RPI', 'refinery_pressure.json'],
  ['SEED_CCI', 'civilian_confidence.json'],
  ['SEED_OFP', 'occupation_financial_pressure.json'],
];

// Drop `note` at every depth. Returns a new structure; the source is untouched.
function stripNotes(v) {
  if (Array.isArray(v)) return v.map(stripNotes);
  if (v && typeof v === 'object') {
    const out = {};
    for (const [k, val] of Object.entries(v)) {
      if (k === 'note') continue;
      out[k] = stripNotes(val);
    }
    return out;
  }
  return v;
}

function build() {
  const lines = [
    BEGIN + '────────────────────────────────────────────────────',
    '// Embedded so the file works from file:// without a server, where a fetch',
    '// of data/*.json is blocked by the browser.',
    '//',
    '// GENERATED — DO NOT HAND-EDIT. Run `node scripts/build-seeds.js --write`',
    '// after any change under public/data/. Hand-maintained, this block went',
    '// stale by 100 key_events and a strike_score of 88-vs-95 before anyone',
    '// noticed, and fetchJSON served it silently. It is now reproducible, and',
    '// a fallback is announced on the page rather than rendered as if live.',
    '//',
    '// Mirrors public/data/ exactly EXCEPT `note` fields, dropped at every',
    '// depth because nothing in this file renders one.',
    '// Generated from the files as they stood at the SHA this commit records.',
  ];
  let bytes = 0;
  for (const [name, file] of SEEDS) {
    const raw = JSON.parse(fs.readFileSync(path.join(DATA, file), 'utf8'));
    const json = JSON.stringify(stripNotes(raw));
    bytes += json.length;
    lines.push('const ' + name + ' = ' + json + ';   // ← public/data/' + file);
  }
  return { text: lines.join('\n') + '\n', bytes };
}

function main() {
  const write = process.argv.includes('--write');
  const page = fs.readFileSync(PAGE, 'utf8');

  const i = page.indexOf(BEGIN);
  const j = page.indexOf(END);
  if (i < 0 || j < 0 || j < i) {
    console.error('REFUSED: could not locate the seed block between\n  ' + BEGIN + '\n  ' + END);
    process.exit(2);
  }

  const oldBlock = page.slice(i, j);
  const { text, bytes } = build();
  const newBlock = text + '\n';   // the exact bytes written, so a re-run reports +0

  const delta = newBlock.length - oldBlock.length;
  console.log('seed block: ' + oldBlock.length + ' -> ' + newBlock.length + ' bytes'
    + '  (' + (delta >= 0 ? '+' : '') + delta + (delta === 0 ? ' — already current' : '') + ')');
  console.log('payload across ' + SEEDS.length + ' seeds, notes stripped: ' + bytes + ' bytes');

  if (!write) { console.log('(dry-run — pass --write to rewrite public/index.html)'); return; }

  fs.writeFileSync(PAGE, page.slice(0, i) + newBlock + page.slice(j), 'utf8');
  console.log('written -> public/index.html  (' + fs.statSync(PAGE).size + ' bytes)');
}

main();
