#!/usr/bin/env bash
# Bootstrap game/development branch — P1-00 PM task.
# Creates minimal Godot 4.7 project shell on game/development (not main).
#
# Usage:
#   bash tools/bootstrap_game_development.sh
#   bash tools/bootstrap_game_development.sh --dry-run
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

DRY=0
[[ "${1:-}" == "--dry-run" ]] && DRY=1

BRANCH="game/development"
GAME_DIR="${ROOT}/game"

echo "==> Bootstrap ${BRANCH} (P1-00)"

if [[ "$DRY" -eq 1 ]]; then
  echo "[dry-run] would checkout/create ${BRANCH}, add project.godot, push"
  exit 0
fi

if ! git show-ref --verify --quiet "refs/heads/${BRANCH}"; then
  git fetch origin "${BRANCH}" 2>/dev/null || true
  if git show-ref --verify --quiet "refs/remotes/origin/${BRANCH}"; then
    git checkout -b "${BRANCH}" "origin/${BRANCH}"
  else
    git checkout -b "${BRANCH}"
  fi
else
  git checkout "${BRANCH}"
fi

git merge origin/main --no-edit 2>/dev/null || git merge main --no-edit 2>/dev/null || true

if [[ ! -f "${GAME_DIR}/project.godot" ]]; then
  cat > "${GAME_DIR}/project.godot" <<'GODOT'
; Engine configuration file.
; Bootstrap shell — P1-00. Expand via GDAI MCP on game/development.

config_version=5

[application]
config/name="Tides of Urashima"
config/features=PackedStringArray("4.7", "Forward Plus")
run/main_scene=""

[autoload]

[rendering]
renderer/rendering_method="forward_plus"
GODOT
  echo "[OK] Created game/project.godot"
fi

mkdir -p "${GAME_DIR}/scenes" "${GAME_DIR}/scripts" "${GAME_DIR}/assets"
touch "${GAME_DIR}/scenes/.gitkeep" "${GAME_DIR}/scripts/.gitkeep"

if [[ -f tools/install_ci_deps.sh ]]; then
  bash tools/install_ci_deps.sh || echo "[WARN] install_ci_deps had issues"
fi

echo ""
echo "Next:"
echo "  1. bash tools/run_ci_checks.sh   (on ${BRANCH})"
echo "  2. git add game/project.godot && git commit -m 'feat(P1-00): bootstrap Godot project shell'"
echo "  3. git push -u origin ${BRANCH}"
echo "  4. python3 tools/pm_update_issue.py P1-00 --status done --commit \$(git rev-parse HEAD)"
echo "  5. bash tools/pm_emit_cycle_event.sh agent_cycle_complete --issue P1-00 --agent pm"
