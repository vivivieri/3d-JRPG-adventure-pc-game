#!/usr/bin/env bash
# Lint changed .gd files (P2) — gdtoolkit gdlint when available, else Godot parse.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

if [[ ! -f "${ROOT}/game/project.godot" ]]; then
  echo "[SKIP] no game/project.godot — gdscript lint runs on game/development only"
  exit 2
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
  if [[ -z "$DIFF_BASE" ]]; then
    if git rev-parse HEAD~1 >/dev/null 2>&1; then
      DIFF_BASE="HEAD~1"
    else
      DIFF_BASE="$(git rev-list --max-parents=0 HEAD 2>/dev/null || true)"
    fi
  fi
fi

if [[ -z "$DIFF_BASE" ]]; then
  echo "[SKIP] cannot determine diff base for gdscript lint"
  exit 2
fi

mapfile -t FILES < <(git diff --name-only "$DIFF_BASE" "$DIFF_HEAD" 2>/dev/null | grep '\.gd$' || true)  # swallow-ok: empty diff when no .gd changes
if [[ ${#FILES[@]} -eq 0 ]]; then
  echo "[SKIP] no .gd changes in diff ${DIFF_BASE}..${DIFF_HEAD}"
  exit 2
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
  if [[ "${CI:-}" == "true" ]] || [[ -f "${ROOT}/game/project.godot" ]]; then
    echo "[FAIL] gdtoolkit not installed — run bash tools/install_ci_deps.sh"
    exit 1
  fi
  echo "[WARN] gdtoolkit not installed — pip install gdtoolkit (or run install_ci_deps.sh)"
  echo "── fallback: Godot headless per changed file"
  for f in "${FILES[@]}"; do
    [[ -f "$f" ]] || continue
    echo "── parse: $f"
    if bash "${ROOT}/tools/with_ci_godot.sh" \
      godot4 --headless --rendering-driver opengl3 --path game --quit-after 120 \
      --script "$f" 2>/dev/null; then
      echo "[PASS] $f"
    else
      echo "[FAIL] $f (Godot could not load script)"
      FAIL=1
    fi
  done
fi

exit "$FAIL"
