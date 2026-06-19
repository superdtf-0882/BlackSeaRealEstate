require('dotenv').config();
const fs   = require('fs');
const path = require('path');
const FirecrawlApp = require('@mendable/firecrawl-js').default;

const FIRECRAWL_API_KEY = process.env.FIRECRAWL_API_KEY;
if (!FIRECRAWL_API_KEY) {
  console.error('ERROR: FIRECRAWL_API_KEY not set in .env');
  process.exit(1);
}

const app = new FirecrawlApp({ apiKey: FIRECRAWL_API_KEY });

const queries = [
  'Crimea fuel shortage rationing',           // CCI anchor
  'Mariupol Ukraine strike',                  // infrastructure
  'Berdiansk Ukraine drone',                  // infrastructure (revised)
  'Russia refinery strike Novorossiysk',      // RPI anchor
  'Azov corridor R-280 logistics',            // RPI/infrastructure
  'Donetsk Luhansk occupied Russia',          // Track B/SCI
  'Russia occupied Ukraine economic',         // SCI/macro
  'Sevastopol Black Sea Fleet',               // Crimea catch-all (revised)
  'ISW Russian occupation update',            // daily ISW report
];

function fmt(date) {
  if (!date) return 'no date';
  const d = new Date(date);
  return isNaN(d.getTime()) ? String(date) : d.toISOString().slice(0, 10);
}

async function runQuery(query) {
  console.log('\n' + '─'.repeat(60));
  console.log(`QUERY: "${query}"`);
  console.log('─'.repeat(60));

  let results;
  try {
    const response = await app.search(query, {
      limit: 5,
      sources: [{ type: 'news' }],
      tbs: 'qdr:d',
      scrapeOptions: { formats: [{ type: 'markdown' }] },
    });

    // Log raw response shape on first query to confirm structure
    if (query === queries[0]) {
      console.log('[DEBUG] Top-level response keys:', Object.keys(response));
    }

    results = response?.news || response?.web || [];
  } catch (err) {
    console.log(`ERROR: ${err.message}`);
    return [];
  }

  if (!results.length) {
    console.log('  ⚠ Zero results returned');
    return [];
  }

  console.log(`  ${results.length} result(s):`);
  for (const r of results) {
    console.log(`\n  • ${r.title || '(no title)'}`);
    console.log(`    URL:  ${r.url}`);
    console.log(`    Date: ${fmt(r.date || r.metadata?.date)}`);
    const md = r.markdown || r.description || '';
    console.log(`    Preview: ${md.slice(0, 200).replace(/\n/g, ' ')}${md.length > 200 ? '…' : ''}`);
  }

  return results;
}

async function main() {
  console.log('Black Sea Monitor — Firecrawl PoC');
  console.log(`Running ${queries.length} queries  |  source: news  |  tbs: qdr:d (past 24h)`);

  const allResults = [];
  const zeroQueries = [];

  for (const q of queries) {
    const results = await runQuery(q);
    if (!results.length) zeroQueries.push(q);
    allResults.push(...results);
  }

  // Summary
  const dates = allResults
    .map(r => r.date || r.metadata?.date)
    .filter(Boolean)
    .map(d => new Date(d).getTime())
    .filter(t => !isNaN(t));

  const now = Date.now();
  const last24h = dates.filter(t => now - t < 86400000).length;

  console.log('\n' + '═'.repeat(60));
  console.log('SUMMARY');
  console.log('═'.repeat(60));
  console.log(`Total results:       ${allResults.length}`);
  console.log(`With parseable date: ${dates.length}`);
  if (dates.length) {
    console.log(`Earliest result:     ${fmt(Math.min(...dates))}`);
    console.log(`Latest result:       ${fmt(Math.max(...dates))}`);
    console.log(`From last 24h:       ${last24h} / ${dates.length}`);
  }
  if (zeroQueries.length) {
    console.log(`\nZero-result queries (${zeroQueries.length}):`);
    zeroQueries.forEach(q => console.log(`  - "${q}"`));
  } else {
    console.log('\nAll queries returned at least one result ✓');
  }

  const outPath = path.join(__dirname, 'last-run.json');
  fs.writeFileSync(outPath, JSON.stringify(allResults, null, 2), 'utf8');
  console.log(`\nFull results written to scripts/last-run.json (${allResults.length} items)`);
}

main().catch(err => {
  console.error('Fatal:', err.message);
  process.exit(1);
});
