#!/usr/bin/env bash
# Cloud Environment install router — works when dashboard cannot set git branch.
#
# Cursor may observe .cursor/environment.json from main (REPO_FILE_OBSERVED) even for
# the game dev Environment. This script checks out game/development when needed, then
# runs the full dev stack install.
#
# Escape hatch for ad-hoc docs-only cloud agents on main:
#   CLOUD_DOCS_ONLY=1 bash tools/bootstrap_cloud_environment.sh
#
# Authority: docs/ops/agents/CLOUD_SNAPSHOT_LAUNCH.md §0
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

if [[ "${CLOUD_DOCS_ONLY:-}" == "1" ]]; then
  echo "==> CLOUD_DOCS_ONLY=1 — main docs/data install only"
  exec bash tools/install_main_ci.sh
fi

BRANCH="$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo unknown)"

if [[ ! -f game/project.godot ]]; then
  echo "==> bootstrap_cloud_environment: no game/project.godot on branch '${BRANCH}'"
  echo "    Fetching and checking out game/development (dev Environment bootstrap)"
  git fetch origin game/development
  git checkout game/development
  bash tools/ensure_dev_environment_branch.sh
fi

echo "==> bootstrap_cloud_environment: running full dev stack install"
exec bash tools/install_cloud_dev.sh
