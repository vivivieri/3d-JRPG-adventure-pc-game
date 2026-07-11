#!/usr/bin/env bash
# Full three-ending E2E playthrough — headless validation + GUI proof frames/video.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

export PATH="${HOME}/.local/bin:${PATH}"
export DISPLAY="${DISPLAY:-:1}"
export XDG_DATA_HOME="${ROOT}/.cache/godot-data"
export XDG_CONFIG_HOME="${ROOT}/.cache/godot-config"
export XDG_CACHE_HOME="${ROOT}/.cache/godot-cache"

OUT="${ROOT}/artifacts/videos"
mkdir -p "$OUT"
LOG="/tmp/e2e_endings.log"

echo "==> Headless three-ending validation"
godot4 --headless --rendering-driver opengl3 --path game res://tests/e2e_three_endings_test.tscn 2>&1 | tee -a "$LOG"

echo ""
echo "==> GUI autopilot (screenshots + optional video)"
VIDEO="${OUT}/three_endings_playthrough.mp4"
if command -v ffmpeg >/dev/null 2>&1; then
  ffmpeg -y -f x11grab -video_size 1920x1080 -framerate 30 -i "${DISPLAY}" -t 90 "$VIDEO" >/tmp/e2e_ffmpeg.log 2>&1 &
  FFMPEG_PID=$!
  sleep 1
else
  FFMPEG_PID=""
fi

godot4 --rendering-driver opengl3 --resolution 1920x1080 --path game res://tests/e2e_ending_autopilot.tscn 2>&1 | tee -a "$LOG"

if [[ -n "${FFMPEG_PID}" ]]; then
  wait "$FFMPEG_PID" || true
fi

COUNT=$(ls -1 "$OUT"/*.png 2>/dev/null | wc -l)
echo ""
echo "Ending frames: $COUNT in $OUT"
ls -1 "$OUT"/* 2>/dev/null || true
grep -E "E2E_(SAVED|ENDINGS_DONE|PLAY)" "$LOG" || true

test "$COUNT" -ge 3
if [[ -f "$VIDEO" ]]; then
  echo "Video: $VIDEO ($(du -h "$VIDEO" | cut -f1))"
fi
