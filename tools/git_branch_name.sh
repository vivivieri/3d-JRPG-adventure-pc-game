#!/usr/bin/env bash
# Print current git branch (or "unknown").
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
git -C "$ROOT" rev-parse --abbrev-ref HEAD 2>/dev/null || echo unknown
