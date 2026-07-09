#!/usr/bin/env bash
# Regenerate all procedural game audio and art assets, then verify licenses.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
python3 "$ROOT/tools/generate_game_audio.py"
python3 "$ROOT/tools/generate_game_art.py"
python3 "$ROOT/tools/verify_asset_licenses.py"
echo "All assets generated and license-verified."
