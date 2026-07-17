#!/usr/bin/env bash
# Install Git LFS and ensure hooks are active for the repo.
# Idempotent — safe in CI, cloud dev, and local shells.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

if command -v apt-get >/dev/null 2>&1 && ! command -v git-lfs >/dev/null 2>&1; then
  echo "==> Installing git-lfs (apt)..."
  sudo apt-get update -qq
  sudo DEBIAN_FRONTEND=noninteractive apt-get install -y -qq git-lfs
fi

if ! command -v git-lfs >/dev/null 2>&1; then
  echo "[FAIL] git-lfs not found — install via package manager or https://git-lfs.com" >&2
  exit 1
fi

git lfs install --local 2>/dev/null || git lfs install

if [[ -f .gitattributes ]] && grep -q "filter=lfs" .gitattributes 2>/dev/null; then
  echo "[OK] Git LFS active — patterns in .gitattributes"
else
  echo "[WARN] .gitattributes missing LFS patterns"
fi

echo "[OK] git-lfs $(git lfs version | head -1)"
