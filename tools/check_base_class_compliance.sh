#!/usr/bin/env bash
# Enforce CODE_BASE_CLASS_RULES on game/development (forbidden parallel controllers).
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

python3 tools/validate_base_classes.py || exit 1
exec python3 tools/check_base_class_compliance.py
