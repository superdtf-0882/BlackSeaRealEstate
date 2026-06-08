#!/usr/bin/env bash
# update.sh — full pipeline: scrape → compute → done
set -e
cd "$(dirname "$0")"

echo "=== Black Sea Monitor — Update Pipeline ==="
echo

echo "1/6  Restate.ru Crimea prices…"
python fetch/restate.py --write

echo
echo "2/6  Домклик listing counts…"
python fetch/domclick.py --write

echo
echo "3/6  Avito rental listings…"
python fetch/avito_rental.py --write

echo
echo "4/6  Refinery Pressure Index…"
python fetch/refinery_pressure.py --write

echo
echo "5/6  Civilian Confidence Index…"
python fetch/civilian_confidence.py --write

echo
echo "6/6  Recompute dial scores…"
python fetch/compute.py --write

echo
echo "Done — $(date)"
echo "Open index.html to view updated dashboard."
