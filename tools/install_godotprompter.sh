#!/usr/bin/env bash
# Install GodotPrompter skills for Cursor (dev-only; not shipped in Steam builds).
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
DEST="$ROOT/.godot-prompter"
REPO="${GODOTPROMPTER_REPO:-https://github.com/jame581/GodotPrompter.git}"
REF="${GODOTPROMPTER_REF:-master}"

if [[ -d "$DEST/skills" ]]; then
  echo "GodotPrompter already installed at $DEST"
  exit 0
fi

echo "Cloning GodotPrompter ($REF) into $DEST..."
git clone --depth 1 --branch "$REF" "$REPO" "$DEST"

echo "Done. Cursor loads skills from .cursor-plugin/plugin.json"
echo "Primary skills for this project:"
echo "  - godot-project-setup"
echo "  - event-bus"
echo "  - dialogue-system"
echo "  - gdscript-patterns"
echo "  - 3d-essentials"
echo "  - godot-ui"
echo "  - save-load"
echo "  - audio-system"
echo "  - export-pipeline"
