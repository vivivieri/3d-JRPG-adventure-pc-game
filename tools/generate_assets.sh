#!/usr/bin/env bash
# Regenerate all procedural game audio and art assets, install CC0 models, verify licenses.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
python3 "$ROOT/tools/generate_game_audio.py"
python3 "$ROOT/tools/generate_game_art.py"
if [[ -d "$ROOT/.asset-dl/nature-kit" && -d "$ROOT/.asset-dl/castle" ]]; then
  bash "$ROOT/tools/install_cc0_assets.sh"
else
  echo "Skipping Kenney CC0 model install — source packs not found in .asset-dl/"
fi
if [[ "${SKIP_POLYHAVEN:-0}" != "1" ]]; then
  if [[ -d "$ROOT/game/assets/models/polyhaven/tree_coastal_a" ]]; then
    echo "Poly Haven models already installed."
  else
    echo "Installing Poly Haven high-poly models (~1.6 GB download)..."
    python3 "$ROOT/tools/install_polyhaven_assets.py"
  fi
fi
python3 "$ROOT/tools/verify_asset_licenses.py"
echo "All assets generated and license-verified."
