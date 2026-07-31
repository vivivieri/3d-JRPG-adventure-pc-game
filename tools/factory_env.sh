# shellcheck shell=bash
# Source from factory bash entrypoints:
#   ROOT="$(cd "$(dirname "$0")/.." && pwd)"
#   # shellcheck source=factory_env.sh
#   source "$ROOT/tools/factory_env.sh"
#
# Env overrides (relative to FACTORY_ROOT / ROOT unless absolute):
#   FACTORY_ROOT          — repo root
#   FACTORY_DATA_DIR      — default game/data/qa
#   FACTORY_ARTIFACTS_DIR — default artifacts
#
# Authority: packages/game-dev-factory/CONTROL_PLANE.md

: "${FACTORY_ROOT:=${ROOT:-}}"
: "${FACTORY_DATA_DIR:=game/data/qa}"
: "${FACTORY_ARTIFACTS_DIR:=artifacts}"

export FACTORY_ROOT FACTORY_DATA_DIR FACTORY_ARTIFACTS_DIR

_factory_resolve() {
  local base="$1"
  local rel="$2"
  if [[ "$rel" = /* ]]; then
    printf '%s\n' "$rel"
  else
    printf '%s/%s\n' "$base" "$rel"
  fi
}

FACTORY_DATA_ABS="$(_factory_resolve "${FACTORY_ROOT:-.}" "$FACTORY_DATA_DIR")"
FACTORY_ARTIFACTS_ABS="$(_factory_resolve "${FACTORY_ROOT:-.}" "$FACTORY_ARTIFACTS_DIR")"
export FACTORY_DATA_ABS FACTORY_ARTIFACTS_ABS

FACTORY_BOARD_PATH="${FACTORY_DATA_ABS}/sprint_board.json"
FACTORY_PHASES_PATH="${FACTORY_DATA_ABS}/sprint_phases.json"
FACTORY_ORCH_STEPS_PATH="${FACTORY_DATA_ABS}/pm_orchestrator_steps.json"
FACTORY_ORCH_REPORT_PATH="${FACTORY_ARTIFACTS_ABS}/pm_orchestrator_report.json"
FACTORY_DISPATCH_PATH="${FACTORY_ARTIFACTS_ABS}/pm_dispatch_packet.json"
FACTORY_STATE_PATH="${FACTORY_ARTIFACTS_ABS}/factory_state.json"
export FACTORY_BOARD_PATH FACTORY_PHASES_PATH FACTORY_ORCH_STEPS_PATH
export FACTORY_ORCH_REPORT_PATH FACTORY_DISPATCH_PATH FACTORY_STATE_PATH
