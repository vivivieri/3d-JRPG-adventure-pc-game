#!/usr/bin/env bash
# Checklist + validation for porting Phase 1 visuals from main specs to game/development.
# See docs/technical/GDSCRIPT_REGENERATION.md §10
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

MODE="${1:---all}"

print_checklist() {
  echo "==> Phase 1 visuals regeneration checklist (game/development)"
  echo ""
  echo "Sprint issue: P1-01 (docs/sprints/Phase1-Sprint1-issues.md)"
  echo "Unblocks: P1-02 Builder — ruined_village.tscn greybox (GDAI MCP)"
  echo ""
  echo "R&R (who does what):"
  echo "  Spec + Python ref on main          -> Architect (GodotPrompter)"
  echo "  GDScript + .gdshader on dev        -> Architect (GodotPrompter)"
  echo "  .tscn placement + materials        -> Builder (GDAI MCP) — P1-02"
  echo "  Gate verification                  -> QA Agent"
  echo "  Dispatch timing                    -> PM: run_agent_session_gate.sh architect P1-01"
  echo "  Full policy: docs/technical/GDSCRIPT_REGENERATION.md §10"
  echo ""
  echo "Prerequisites:"
  echo "  git checkout game/development && git merge main"
  echo "  bash tools/run_agent_session_gate.sh architect P1-01"
  echo "  bash tools/ensure_mcp_stack.sh        # before P1-02 scene work"
  echo ""
  echo "Regeneration order (mandatory):"
  echo "  1. toon_base.gdshader     <- tools/godot_templates/shaders/toon_base.gdshader"
  echo "                             spec: game/data/code/shader_registry.json"
  echo "  2. zone_visuals.gd        <- tools/zone_visuals_lib.py"
  echo "                             spec: game/data/code/base_classes.json (ZoneVisuals)"
  echo "                             data: game/data/world/zone_palettes.json"
  echo "  3. ruined_village.tres    <- game/data/code/environment_registry.json (optional)"
  echo "                             runtime build via ZoneVisuals.build_environment() is OK"
  echo "  4. test_zone_visuals.gd   <- game/data/qa/unit_test_specs.json"
  echo ""
  echo "Per artifact steps:"
  echo "  A. Read machine spec (registry / base_classes public_api)"
  echo "  B. Read Python reference (zone_visuals) or shader template (toon_base)"
  echo "  C. Port to game/development path — never invent behavior"
  echo "  D. python3 tools/test_reference_libs.py  # ZoneVisualsLibTests parity"
  echo "  E. bash tools/run_unit_tests.sh          # after test_zone_visuals.gd exists"
  echo "  F. bash tools/run_ci_checks.sh           # game/development PR"
  echo ""
  echo "Recover prior ports (diff hints only — spec wins on conflict):"
  echo "  git show 87a5ace:game/scripts/exploration/zone_visuals.gd"
  echo "  git show 87a5ace:game/shaders/toon_base.gdshader"
  echo "  git show 87a5ace:game/environments/ruined_village.tres"
  echo "  git show 87a5ace:game/tests/unit/test_zone_visuals.gd"
  echo ""
  echo "Full guide: docs/technical/GDSCRIPT_REGENERATION.md §10"
}

run_check() {
  echo "==> Phase 1 visual spec validation"
  python3 tools/validate_base_classes.py
  python3 tools/validate_zone_visuals_contract.py
  python3 - <<'PY'
import json
from pathlib import Path

root = Path(".")
errors = []
for rel in [
    "game/data/world/zone_palettes.json",
    "game/data/code/environment_registry.json",
    "game/data/code/shader_registry.json",
    "game/data/qa/unit_test_specs.json",
    "tools/zone_visuals_lib.py",
]:
    if not (root / rel).is_file():
        errors.append(f"missing spec artifact: {rel}")

bases = json.loads((root / "game/data/code/base_classes.json").read_text())
zv = next((b for b in bases["bases"] if b["id"] == "ZoneVisuals"), None)
if not zv or not zv.get("public_api"):
    errors.append("ZoneVisuals missing public_api in base_classes.json")
if zv and not (root / zv["python_reference"]).is_file():
    errors.append(f"ZoneVisuals missing python_reference: {zv.get('python_reference')}")

shaders = json.loads((root / "game/data/code/shader_registry.json").read_text())
toon = next((s for s in shaders["shaders"] if s["id"] == "toon_base"), None)
if not toon:
    errors.append("shader_registry missing toon_base")
elif not (root / toon["template_path"]).is_file():
    errors.append(f"toon_base template missing: {toon['template_path']}")

if errors:
    print("Phase 1 visual spec validation: FAILED", flush=True)
    for e in errors:
        print(f"  - {e}", flush=True)
    raise SystemExit(1)
print("Phase 1 visual spec validation: OK")
PY
}

run_test() {
  echo "==> Reference lib parity tests (includes ZoneVisualsLibTests)"
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
    echo "Usage: bash tools/regenerate_phase1_visuals.sh [--check|--test|--all]"
    echo ""
    echo "  --all    Print checklist + validate specs + run reference tests (default)"
    echo "  --check  Validate Phase 1 visual spec artifacts on main"
    echo "  --test   Run tools/test_reference_libs.py (ZoneVisuals parity)"
    ;;
  *)
    echo "Unknown mode: $MODE (use --check, --test, or --all)" >&2
    exit 1
    ;;
esac
