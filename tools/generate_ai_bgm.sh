#!/usr/bin/env bash
# Generate BGM via ACE-Step 1.5 (MIT) — zone, opening, boss, ending hero tracks.
# Wrapper around tools/generate_ai_bgm.py
#
# Usage:
#   bash tools/generate_ai_bgm.sh --list
#   bash tools/generate_ai_bgm.sh --category opening
#   bash tools/generate_ai_bgm.sh --category boss_cinematic --category ending
#   bash tools/generate_ai_bgm.sh --category zone --fallback
#   bash tools/generate_ai_bgm.sh --all-prompts
#   bash tools/generate_ai_bgm.sh --install-ace-step
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

if [[ "${1:-}" == "--install-ace-step" ]]; then
  exec bash "${ROOT}/tools/install_ace_step.sh"
fi

if [[ "${1:-}" == "--all-prompts" ]]; then
  exec python3 "${ROOT}/tools/generate_ai_bgm.py" --category all --prompts-only
fi

exec python3 "${ROOT}/tools/generate_ai_bgm.py" "$@"
