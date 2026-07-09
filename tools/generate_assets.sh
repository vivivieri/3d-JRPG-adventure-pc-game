#!/usr/bin/env bash
# Regenerate all procedural game audio and art assets.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
python3 "$ROOT/tools/generate_game_audio.py"
python3 "$ROOT/tools/generate_game_art.py"
echo "All assets generated."
