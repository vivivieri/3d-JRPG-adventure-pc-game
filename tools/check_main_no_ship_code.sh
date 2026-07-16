#!/usr/bin/env bash
# main branch must not contain ship Godot implementation (spec-first policy).
# See docs/technical/SPEC_FIRST_DEVELOPMENT.md, docs/workflow/BRANCHING.md
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

FAIL=0
fail() { echo "[FAIL] $*"; FAIL=1; }
ok() { echo "[OK]   $*"; }

echo "==> Main-branch ship code check (spec-first policy)"
echo ""

BRANCH="$(git -C "$ROOT" rev-parse --abbrev-ref HEAD 2>/dev/null || echo unknown)"
if [[ "$BRANCH" != "main" ]]; then
  ok "skipped on ${BRANCH} — main-only gate (ship code allowed on game/development)"
  echo ""
  echo "Main ship code check: PASSED (skipped off main)"
  exit 0
fi

if [[ -f "${ROOT}/game/project.godot" ]]; then
  fail "game/project.godot must not exist on main (implementation belongs on game/development)"
else
  ok "no game/project.godot"
fi

SHIP_GD=()
while IFS= read -r -d '' f; do
  rel="${f#${ROOT}/}"
  # Third-party addons are gitignored; any tracked .gd under game/scripts is a violation
  SHIP_GD+=("$rel")
done < <(find "${ROOT}/game/scripts" -name '*.gd' -print0 2>/dev/null)

if [[ ${#SHIP_GD[@]} -gt 0 ]]; then
  for rel in "${SHIP_GD[@]}"; do
    fail "Ship GDScript on main: $rel"
  done
else
  ok "no game/scripts/**/*.gd"
fi

SHIP_TSCN=()
while IFS= read -r -d '' f; do
  SHIP_TSCN+=("${f#${ROOT}/}")
done < <(find "${ROOT}/game/scenes" -name '*.tscn' -print0 2>/dev/null)

if [[ ${#SHIP_TSCN[@]} -gt 0 ]]; then
  for rel in "${SHIP_TSCN[@]}"; do
    fail "Ship scene on main: $rel"
  done
else
  ok "no game/scenes/**/*.tscn"
fi

echo ""
if [[ "$FAIL" -ne 0 ]]; then
  echo "Main ship code check: FAILED — move implementation to game/development"
  exit 1
fi
echo "Main ship code check: PASSED"
exit 0
