#!/usr/bin/env bash
# L0 — scan tracked files for accidental secret commits.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
python3 tools/check_no_secrets.py
