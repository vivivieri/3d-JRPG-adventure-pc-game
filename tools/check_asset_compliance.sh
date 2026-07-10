#!/usr/bin/env bash
# Run full asset compliance check and generate audit proof.
# Exit 0 = safe to ship from a license perspective.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

echo "==> Tides of Urashima — Asset Compliance Check"
echo "    Policy: docs/ASSET_COMPLIANCE.md"
echo ""

echo "==> Step 1/2: Verify licenses..."
python3 tools/verify_asset_licenses.py "$@"

echo ""
echo "==> Step 2/2: Generate compliance report..."
python3 tools/generate_compliance_report.py

echo ""
echo "==> Done. Proof: docs/compliance/COMPLIANCE_REPORT.md"
