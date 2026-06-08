#!/usr/bin/env bash
# Build the static charter site into ./dist
#
# Usage:
#   bash build_site.sh            # PREVIEW build (noindex everywhere + robots Disallow)
#   bash build_site.sh prod       # PRODUCTION build (indexable)
#
# Zero external deps: Python 3.11 stdlib only. The connector runs in --fixture
# mode (offline). Replace the fixture / wire real Avinode creds for live legs.
set -euo pipefail
cd "$(dirname "$0")"

MODE="${1:-preview}"
LEGS="$(mktemp -t legs.XXXXXX.json)"

echo "[build] normalising empty legs (fixture mode)…" >&2
python3 connectors/avinode.py \
  --fixture tests/fixtures/avinode_trip_search.json \
  --output "$LEGS" >/dev/null

rm -rf dist
if [ "$MODE" = "prod" ]; then
  echo "[build] PRODUCTION build (indexable)" >&2
  python3 pseo/generate.py --out dist --empty-legs "$LEGS"
else
  echo "[build] PREVIEW build (noindex)" >&2
  python3 pseo/generate.py --out dist --empty-legs "$LEGS" --preview
fi

rm -f "$LEGS"
echo "[build] done → $(pwd)/dist" >&2
