#!/usr/bin/env bash
# Fail fast when a dev-environment / snapshot task runs on main instead of game/development.
#
# Usage (first command in Setup Agent or snapshot rebuild):
#   bash tools/ensure_dev_environment_branch.sh
#
# Authority: docs/agents/CLOUD_SNAPSHOT_LAUNCH.md
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

BRANCH="$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo unknown)"
ENV_URL="https://cursor.com/dashboard/cloud-agents/environments/r/github.com/vivivieri/3d-jrpg-adventure-pc-game"

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
  - main's .cursor/environment.json only runs install_main_ci.sh (docs CI deps)
  - game/development's .cursor/environment.json has snapshot + install_cloud_dev.sh + ensure_mcp_stack.sh

Agent fix (run now):
  git fetch origin game/development
  git checkout game/development
  bash tools/install_cloud_dev.sh
  bash tools/ensure_mcp_stack.sh

Human fix (dashboard — required for "Update dev environment" / Setup Agent):
  1. Open: ${ENV_URL}
  2. Edit the environment → set Repository branch to game/development (not main)
  3. Save, then Start Setup Agent again

Docs: docs/agents/CLOUD_SNAPSHOT_LAUNCH.md §0
EOF
exit 1
