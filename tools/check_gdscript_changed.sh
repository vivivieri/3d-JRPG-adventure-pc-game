#!/usr/bin/env bash
# Lint changed .gd files (P2) — gdtoolkit gdlint when available, else Godot parse via project load.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

if [[ ! -f "${ROOT}/game/project.godot" ]]; then
  echo "[SKIP] no game/project.godot — gdscript lint runs on game/development only"
  exit 0
fi

export PATH="${HOME}/.local/bin:${PATH}"

DIFF_BASE=""
DIFF_HEAD="HEAD"
if [[ -n "${GITHUB_EVENT_NAME:-}" ]]; then
  case "$GITHUB_EVENT_NAME" in
    pull_request)
      DIFF_BASE="${GITHUB_BASE_SHA:-}"
      DIFF_HEAD="${GITHUB_SHA:-HEAD}"
      ;;
    push)
      DIFF_BASE="${GITHUB_EVENT_BEFORE:-}"
      DIFF_HEAD="${GITHUB_SHA:-HEAD}"
      if [[ "$DIFF_BASE" == "0000000000000000000000000000000000000000" ]]; then
        DIFF_BASE=""
      fi
      ;;
  esac
fi
if [[ -z "$DIFF_BASE" ]]; then
  if git rev-parse origin/game/development >/dev/null 2>&1; then
    DIFF_BASE="$(git merge-base HEAD origin/game/development 2>/dev/null || true)"
  fi
  [[ -z "$DIFF_BASE" ]] && DIFF_BASE="HEAD~1" 2>/dev/null || true
fi

mapfile -t FILES < <(git diff --name-only "$DIFF_BASE" "$DIFF_HEAD" 2>/dev/null | grep '\.gd$' || true)
if [[ ${#FILES[@]} -eq 0 ]]; then
  echo "[SKIP] no .gd changes in diff ${DIFF_BASE}..${DIFF_HEAD}"
  exit 0
fi

echo "==> GDScript lint (${#FILES[@]} changed file(s))"
FAIL=0

if command -v gdlint >/dev/null 2>&1; then
  for f in "${FILES[@]}"; do
    [[ -f "$f" ]] || continue
    echo "── gdlint: $f"
    if gdlint "$f"; then
      echo "[PASS] $f"
    else
      echo "[FAIL] $f"
      FAIL=1
    fi
  done
else
  echo "[WARN] gdtoolkit not installed — pip install gdtoolkit (or run install_ci_deps.sh)"
  echo "── fallback: Godot headless project load"
  if bash "${ROOT}/tools/with_ci_godot.sh" \
    godot4 --headless --rendering-driver opengl3 --path game --quit-after 2; then
    echo "[PASS] project loads with changed scripts"
  else
    echo "[FAIL] Godot reported script/project errors"
    FAIL=1
  fi
fi

exit "$FAIL"
