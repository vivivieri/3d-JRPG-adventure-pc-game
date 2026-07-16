#!/usr/bin/env bash
# Generate 256-bit ship protection keys (store in GitHub Secrets — never commit).
set -euo pipefail

echo "==> Ship protection keys (docs/SECURITY.md §9)"
echo ""
echo "Store these in GitHub Environment steam-production (and Cursor Secrets for local RC builds):"
echo ""

if command -v openssl >/dev/null 2>&1; then
  ENC="$(openssl rand -hex 32)"
  SAVE="$(openssl rand -hex 32)"
else
  ENC="$(python3 -c 'import secrets; print(secrets.token_hex(32))')"
  SAVE="$(python3 -c 'import secrets; print(secrets.token_hex(32))')"
fi

echo "GODOT_SCRIPT_ENCRYPTION_KEY=${ENC}"
echo "GODOT_SAVE_HMAC_KEY=${SAVE}"
echo ""
echo "PCK encryption also requires custom export templates:"
echo "  export SCRIPT_AES256_ENCRYPTION_KEY=\"\${GODOT_SCRIPT_ENCRYPTION_KEY}\""
echo "  bash tools/build_godot_export_templates_encrypted.sh"
echo ""
echo "Never commit keys or game/.godot/export_credentials.cfg"
