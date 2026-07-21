#!/usr/bin/env bash
# L0_game_branch_bootstrap — truth check for P1-00 Godot tree on game/development tip.
# On main: advisory PASS with WARN if origin/game/development lacks project.godot.
# On game/development: FAIL if project.godot missing.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

BRANCH="$(bash "${ROOT}/tools/git_branch_name.sh")"
PROJECT="${ROOT}/game/project.godot"

echo "==> Game branch bootstrap check (P1-00)"
echo "    Branch: ${BRANCH}"

if [[ -f "$PROJECT" ]]; then
  echo "[PASS] L0_game_branch_bootstrap — game/project.godot present"
  exit 0
fi

if [[ "$BRANCH" == "game/development" || "$BRANCH" == "origin/game/development" ]]; then
  echo "[FAIL] L0_game_branch_bootstrap — missing game/project.godot on game/development" >&2
  echo "       Restore: bash tools/bootstrap_game_development.sh" >&2
  echo "       Or checkout files from commit 9aa5fb5 (P1-00 boot bootstrap)" >&2
  exit 1
fi

# main / docs branches — probe remote tip when available
REMOTE_HAS=""
if git rev-parse --verify origin/game/development >/dev/null 2>&1; then
  if git cat-file -e "origin/game/development:game/project.godot" 2>/dev/null; then
    REMOTE_HAS=1
  else
    REMOTE_HAS=0
  fi
fi

if [[ "$REMOTE_HAS" == "0" ]]; then
  echo "[WARN] origin/game/development tip has no game/project.godot — P1-00 must stay blocked"
  echo "[PASS] L0_game_branch_bootstrap — advisory on ${BRANCH} (restore on game/development)"
  exit 0
fi

if [[ "$REMOTE_HAS" == "1" ]]; then
  echo "[PASS] L0_game_branch_bootstrap — origin/game/development has project.godot (local tree is docs-only)"
  exit 0
fi

echo "[WARN] could not probe origin/game/development — local game/project.godot missing"
echo "[PASS] L0_game_branch_bootstrap — advisory on ${BRANCH}"
exit 0
