#!/usr/bin/env bash
# Capture end-to-end playthrough screenshots (key milestones).
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
export PATH="${HOME}/.local/bin:${PATH}"
export DISPLAY="${DISPLAY:-:1}"
export XDG_DATA_HOME="${ROOT}/.cache/godot-data"
export XDG_CONFIG_HOME="${ROOT}/.cache/godot-config"
export XDG_CACHE_HOME="${ROOT}/.cache/godot-cache"

OUT="${ROOT}/artifacts/screenshots"
mkdir -p "$OUT"
rm -f "$OUT"/*.png

echo "==> Capturing playthrough screenshots to $OUT"
godot4 --rendering-driver opengl3 --resolution 1920x1080 --path game res://tests/playthrough_capture.tscn 2>&1 | tee /tmp/capture.log

COUNT=$(ls -1 "$OUT"/*.png 2>/dev/null | wc -l)
echo ""
echo "Captured $COUNT screenshots:"
ls -1 "$OUT"/*.png 2>/dev/null || true
grep -E "CAPTURE_(SAVED|DONE)" /tmp/capture.log || true

test "$COUNT" -ge 9
