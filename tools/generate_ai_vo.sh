#!/usr/bin/env bash
# Generate selective story VO via ElevenLabs (see docs/VO_HIT_LIST.md).
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
exec python3 "${ROOT}/tools/generate_ai_vo.py" "$@"
