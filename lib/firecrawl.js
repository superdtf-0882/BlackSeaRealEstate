require('dotenv').config({ path: '.env', override: true });

const FirecrawlApp = require('@mendable/firecrawl-js').default;

const QUERIES = [
  'Crimea fuel shortage rationing',
  'Mariupol Ukraine strike',
  'Berdiansk Ukraine drone',
  'Russia refinery strike Novorossiysk',
  'Azov corridor R-280 logistics',
  'Donetsk Luhansk occupied Russia',
  'Russia occupied Ukraine economic',
  'Sevastopol Black Sea Fleet',
  'ISW Russian occupation update',
];

async function fetchNews() {
  const app = new FirecrawlApp({ apiKey: process.env.FIRECRAWL_API_KEY });
  const allResults = [];

  for (let i = 0; i < QUERIES.length; i++) {
    const query = QUERIES[i];
    try {
      const response = await app.search(query, {
        limit: 5,
        sources: [{ type: 'news' }],
        tbs: 'qdr:d',
        scrapeOptions: { formats: [{ type: 'markdown' }] },
      });

      const raw = response?.news || response?.web || [];
      const results = raw
        .filter(r => r.title && r.url)
        .map(r => ({
          query,
          title: r.title,
          url: r.url,
          date: r.date || r.metadata?.date || null,
          markdown: r.markdown || r.description || '',
        }));

      console.log(`Query ${i + 1}/${QUERIES.length} (${query}): ${results.length} results`);
      allResults.push(...results);
    } catch (err) {
      console.error(`Query ${i + 1}/${QUERIES.length} (${query}) failed: ${err.message}`);
    }
  }

  return allResults;
}

module.exports = { fetchNews, QUERIES };
