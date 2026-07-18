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
EventBus="*res://scripts/core/event_bus.gd"

[rendering]
renderer/rendering_method="forward_plus"
GODOT
  echo "[OK] Created game/project.godot (EventBus autoload stub — verify via GDAI when MCP up)"
fi

bash "${ROOT}/tools/setup_dev_environment.sh"

mkdir -p "${GAME_DIR}/tests/unit"
if [[ ! -f "${GAME_DIR}/tests/unit/test_runner.gd" ]]; then
  git show 952dfe4:game/tests/unit/test_runner.gd > "${GAME_DIR}/tests/unit/test_runner.gd" 2>/dev/null || true
  git show 952dfe4:game/tests/unit/test_story_data_paths.gd > "${GAME_DIR}/tests/unit/test_story_data_paths.gd" 2>/dev/null || true
  git show 952dfe4:game/tests/unit/test_story_data_json.gd > "${GAME_DIR}/tests/unit/test_story_data_json.gd" 2>/dev/null || true
  if [[ -f "${GAME_DIR}/tests/unit/test_runner.gd" ]]; then
    echo "[OK] Restored game/tests/unit/test_runner.gd (+ story data tests)"
  fi
fi

if [[ ! -f "${GAME_DIR}/scenes/README.md" ]]; then
  cat > "${GAME_DIR}/scenes/README.md" <<'MD'
# Scenes — GDAI MCP policy

**Branch:** `game/development` only. No ship `.tscn` on `main`.

## Rules

1. **Build scenes in Godot via GDAI MCP** (`godot-mcp`) — not Cursor hand-edits.
2. After F5 verify, update `game/scenes/.gdai_built`:
   - `verified_f5=true`
   - `main_scene=` (when `run/main_scene` is set)
   - `scenes_touched=` list of `res://` paths
3. Greybox paths (`greybox/`, `_dev/`, `*.greybox.tscn`) are exempt from the marker until promoted.

## Docs

- `docs/agents/MCP_STACK.md`
- `.cursorrules` §0
- `tools/check_rr_compliance.sh`
MD
  echo "[OK] Created game/scenes/README.md"
fi

mkdir -p "${GAME_DIR}/scenes" "${GAME_DIR}/scripts" "${GAME_DIR}/assets"
touch "${GAME_DIR}/scenes/.gitkeep" "${GAME_DIR}/scripts/.gitkeep"

if [[ -f tools/install_ci_deps.sh ]]; then
  bash tools/install_ci_deps.sh || echo "[WARN] install_ci_deps had issues"
fi

echo ""
echo "Next:"
echo "  1. bash tools/run_bootstrap_ci_checks.sh   (P1-00 — on ${BRANCH})"
echo "  2. git add game/project.godot && git commit -m 'feat(P1-00): bootstrap Godot project shell'"
echo "  3. git push -u origin ${BRANCH}"
echo "  4. bash tools/run_post_agent_cycle.sh --issue P1-00 --agent pm --commit \$(git rev-parse HEAD) --run-orchestrator"
echo "  (full game CI after P1-02: bash tools/run_ci_checks.sh)"
