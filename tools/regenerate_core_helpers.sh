#!/usr/bin/env bash
# Checklist + validation for porting core helpers from main specs to game/development.
# See docs/technical/GDSCRIPT_REGENERATION.md
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

MODE="${1:---all}"

print_checklist() {
  echo "==> Core helper regeneration checklist (game/development)"
  echo ""
  echo "R&R (who does what):"
  echo "  Spec + Python ref on main     -> Architect (GodotPrompter)"
  echo "  GDScript port on dev branch   -> Architect (GodotPrompter)"
  echo "  EventBus autoload wire-up     -> Builder (GDAI MCP)"
  echo "  Gate verification             -> QA Agent"
  echo "  Dispatch timing               -> PM Agent (helpers_registry dispatch_by_phase)"
  echo "  Full policy: docs/technical/GDSCRIPT_REGENERATION.md §2"
  echo ""
  echo "Prerequisites:"
  echo "  git checkout game/development && git merge main"
  echo "  bash tools/ensure_mcp_stack.sh   # before autoload wiring in editor"
  echo ""
  echo "Order (from game/data/code/helpers_registry.json):"
  python3 - <<'PY'
import json
from pathlib import Path
h = json.loads(Path("game/data/code/helpers_registry.json").read_text())
for i, hid in enumerate(h["regeneration_order"], 1):
    entry = next(x for x in h["helpers"] if x["id"] == hid)
    py = entry.get("python_reference") or "(signals only)"
    print(f"  {i}. {hid} -> {entry['gdscript_path']}  ref: {py}")
PY
  echo ""
  echo "Per helper:"
  echo "  1. Read spec: helpers_registry.json entry"
  echo "  2. Read Python reference (if listed)"
  echo "  3. Port to GDScript at gdscript_path"
  echo "  4. Register EventBus in project.godot autoloads"
  echo "  5. bash tools/regenerate_core_helpers.sh --test"
  echo "  6. Commit on game/development only"
  echo ""
  echo "Recover prior ports (diff hints):"
  echo "  git show 544dca9^:game/scripts/core/<file>.gd"
  echo ""
  echo "Full guide: docs/technical/GDSCRIPT_REGENERATION.md"
}

run_check() {
  echo "==> Helpers registry validation"
  python3 tools/validate_helpers_registry.py
}

run_test() {
  echo "==> Reference lib parity tests"
  python3 tools/test_reference_libs.py
}

case "$MODE" in
  --check)
    run_check
    ;;
  --test)
    run_test
    ;;
  --all|"")
    print_checklist
    echo ""
    run_check
    echo ""
    run_test
    ;;
  -h|--help)
    echo "Usage: bash tools/regenerate_core_helpers.sh [--check|--test|--all]"
    ;;
  *)
    echo "Unknown mode: $MODE (use --check, --test, or --all)" >&2
    exit 1
    ;;
esac
