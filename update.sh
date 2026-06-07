#!/usr/bin/env bash
# update.sh — full pipeline: scrape → compute → done
set -e
cd "$(dirname "$0")"

echo "=== Black Sea Monitor — Update Pipeline ==="
echo

echo "1/3  Restate.ru Crimea prices…"
python fetch/restate.py --write

echo
echo "2/3  Домклик listing counts…"
python fetch/domclick.py --write

echo
echo "3/3  Recompute dial scores…"
python fetch/compute.py --write

echo
echo "Done. Open index.html to view updated dashboard."
