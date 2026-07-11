#!/usr/bin/env bash
# Clone ACE-Step 1.5 for local MIT-licensed BGM generation (optional GPU).
# Install location: .cache/ace-step-1.5 (gitignored)
#
# Usage: bash tools/install_ace_step.sh
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
DEST="${ROOT}/.cache/ace-step-1.5"
REPO="https://github.com/ace-step/ACE-Step-1.5.git"

export PATH="${HOME}/.local/bin:${PATH}"

if ! command -v uv >/dev/null 2>&1; then
  echo "uv required — run: bash tools/install_cloud_dev.sh"
  exit 1
fi

if [[ -d "${DEST}/.git" ]]; then
  echo "[install_ace_step] Already cloned at ${DEST}"
else
  echo "[install_ace_step] Cloning ACE-Step 1.5..."
  mkdir -p "$(dirname "$DEST")"
  git clone --depth 1 "$REPO" "$DEST"
fi

echo "[install_ace_step] Installing dependencies (uv sync)..."
(cd "$DEST" && uv sync)

echo ""
echo "=== ACE-Step 1.5 ready ==="
echo "  Gradio UI:  cd ${DEST} && uv run acestep"
echo "  REST API:   cd ${DEST} && uv run acestep-api  # http://127.0.0.1:8001"
echo "  Generate:   export ACESTEP_API_URL=http://127.0.0.1:8001"
echo "              python3 tools/generate_ai_bgm.py --category opening --api"
echo "  Prompts:    bash tools/generate_ai_bgm.sh --all-prompts"
echo "  License:    MIT — commercial use OK; register in docs/LICENSES.md"
echo ""
echo "GPU: ≤6GB VRAM uses turbo DiT only; 8GB+ recommended for LM-assisted prompts."
