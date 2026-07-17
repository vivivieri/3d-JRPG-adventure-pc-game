#!/usr/bin/env bash
# Standard alignment audit — report, checklist, history, stakeholder dashboard.
# Authority: docs/qa/ALIGNMENT_AUDIT.md
#
# Usage:
#   bash tools/run_alignment_audit.sh
#   bash tools/run_alignment_audit.sh --trigger post_merge --note "PR #90"
#   bash tools/run_alignment_audit.sh --visuals-from /path/to/png/dir
#   bash tools/run_alignment_audit.sh --skip-ci   # fast dry run
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

exec python3 tools/alignment_audit_lib.py "$@"
