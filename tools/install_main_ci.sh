#!/usr/bin/env bash
# Main-branch cloud dev install (docs + design data + Python tooling only).
# Kept as a script so .cursor/environment.json `install` stays a simple,
# dashboard-safe command (no inline &&/{}/|| that trip the env editor).
# Full game stack lives on game/development — see tools/install_cloud_dev.sh.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

echo "==> Main-branch CI deps (pip validators + shellcheck)"

pip3 install --user -q -r tools/requirements-ci.txt numpy

# ShellCheck powers the L1_shellcheck gate (matches .github/workflows/ci.yml).
# Best-effort: never fail pod startup on a transient apt hiccup.
if ! command -v shellcheck >/dev/null 2>&1; then
  if command -v apt-get >/dev/null 2>&1; then
    sudo apt-get update -qq \
      && sudo DEBIAN_FRONTEND=noninteractive apt-get install -y -qq shellcheck \
      || echo "!! shellcheck apt install skipped (offline?) — L1_shellcheck may WARN until installed"
  fi
fi

echo "==> Main CI deps ready"
