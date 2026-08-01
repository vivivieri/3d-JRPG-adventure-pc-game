#!/usr/bin/env bash
# Ensure a virtual X display exists for Godot editor on headless cloud VMs.
# Snapshot cold-boot often has plugins on disk but no running X server on :1.
#
# Usage: bash tools/ensure_xvfb_display.sh
set -euo pipefail

DISPLAY_NUM="${DISPLAY_NUM:-1}"
export DISPLAY="${DISPLAY:-:${DISPLAY_NUM}}"

if [[ "$DISPLAY" =~ ^:([0-9]+)$ ]]; then
  DISPLAY_NUM="${BASH_REMATCH[1]}"
fi

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
LOG="${ROOT}/.cache/xvfb.log"
mkdir -p "${ROOT}/.cache"

display_ready() {
  if command -v xdpyinfo >/dev/null 2>&1; then
    xdpyinfo -display "$DISPLAY" >/dev/null 2>&1
    return $?
  fi
  if command -v xset >/dev/null 2>&1; then
    xset -display "$DISPLAY" q >/dev/null 2>&1
    return $?
  fi
  pgrep -f "Xvfb ${DISPLAY} " >/dev/null 2>&1
}

if display_ready; then
  echo "[ensure_xvfb] DISPLAY=${DISPLAY} ready"
  exit 0
fi

if ! command -v Xvfb >/dev/null 2>&1; then
  echo "[ensure_xvfb] WARN: Xvfb not installed — run bash tools/install_cloud_dev.sh"
  exit 0
fi

if pgrep -f "Xvfb ${DISPLAY} " >/dev/null 2>&1; then
  echo "[ensure_xvfb] Xvfb already running on ${DISPLAY}"
  sleep 1
  exit 0
fi

echo "[ensure_xvfb] Starting Xvfb on ${DISPLAY} (log: ${LOG})"
nohup Xvfb "${DISPLAY}" -screen 0 1920x1080x24 -nolisten tcp >>"$LOG" 2>&1 &
sleep 2

if display_ready; then
  echo "[ensure_xvfb] OK — DISPLAY=${DISPLAY}"
else
  echo "[ensure_xvfb] WARN: Xvfb started but display check inconclusive — continuing"
fi
