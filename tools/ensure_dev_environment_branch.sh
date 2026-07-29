#!/usr/bin/env bash
# Fail fast when a dev-environment / snapshot task runs on main instead of game/development.
#
# Usage (first command in Setup Agent or snapshot rebuild):
#   bash tools/ensure_dev_environment_branch.sh
#
# Authority: docs/ops/agents/CLOUD_SNAPSHOT_LAUNCH.md
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

BRANCH="$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo unknown)"

if [[ "$BRANCH" == "game/development" ]]; then
  if [[ ! -f game/project.godot ]]; then
    echo "[FAIL] On game/development but game/project.godot is missing."
    echo "       Run: git fetch origin game/development && git reset --hard origin/game/development"
    exit 1
  fi
  echo "[PASS] Branch game/development — dev environment OK"
  exit 0
fi

cat <<EOF
[FAIL] Wrong git branch for dev environment setup: '$BRANCH'

The Cloud dev Environment must use branch game/development, not main.

Why you are here:
  - Pod started on '${BRANCH}' without game/project.godot
  - bootstrap_cloud_environment.sh should auto-checkout game/development on install

Agent fix (run now):
  git fetch origin game/development
  git checkout game/development
  bash tools/install_cloud_dev.sh
  bash tools/ensure_mcp_stack.sh

Human fix (no dashboard branch picker — use Setup Agent chat or re-run install):
  1. Re-run environment install (bootstrap should auto-checkout game/development)
  2. Or paste in Setup Agent:
       git fetch origin game/development && git checkout game/development
       bash tools/install_cloud_dev.sh && bash tools/ensure_mcp_stack.sh

Docs: docs/ops/agents/CLOUD_SNAPSHOT_LAUNCH.md §0
EOF
exit 1
