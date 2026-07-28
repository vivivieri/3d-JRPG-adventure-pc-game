#!/usr/bin/env bash
# Push day-one webhook secrets from Cursor/runtime env into GitHub Actions repo secrets.
# Requires GH_TOKEN with repository Secrets: Read and write (fine-grained PAT).
#
# Usage:
#   bash tools/setup_github_actions_secrets.sh
#   bash tools/setup_github_actions_secrets.sh --dry-run
#
# Authority: docs/agents/CURSOR_SECRETS_SETUP.md · docs/ci-cd/GITHUB_SETUP.md
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

DRY_RUN=0
if [[ "${1:-}" == "--dry-run" ]]; then
  DRY_RUN=1
fi

if ! command -v gh >/dev/null 2>&1; then
  echo "[FAIL] gh CLI not found"
  exit 1
fi

TOKEN="${GH_TOKEN:-${GITHUB_TOKEN:-}}"
if [[ -z "$TOKEN" ]]; then
  echo "[FAIL] GH_TOKEN or GITHUB_TOKEN not set — see docs/agents/CURSOR_SECRETS_SETUP.md §5"
  exit 1
fi

export GH_TOKEN="$TOKEN"
if ! gh auth status >/dev/null 2>&1; then
  echo "==> Authenticating gh with GH_TOKEN..."
  echo "$TOKEN" | gh auth login --with-token
fi

REPO="$(gh repo view --json nameWithOwner -q .nameWithOwner)"
echo "==> GitHub Actions secrets for ${REPO}"
echo "    Authority: docs/agents/CURSOR_SECRETS_SETUP.md"
echo ""

if [[ "$DRY_RUN" -eq 0 ]]; then
  if ! gh api "repos/${REPO}/actions/secrets/public-key" >/dev/null 2>&1; then
    cat <<'EOF'
[FAIL] GH_TOKEN cannot manage repository Actions secrets (HTTP 403).

Fine-grained PAT fix (GitHub → Settings → Developer settings → your token):
  Repository access: vivivieri/3d-JRPG-adventure-pc-game
  Permissions → Secrets: Read and write

Also keep: Issues, Pull requests, Actions (Read), Administration (Read and write).

Update Cursor Secrets → GH_TOKEN with the new token, then re-run:
  bash tools/setup_github_actions_secrets.sh

Manual fallback: GitHub repo → Settings → Secrets and variables → Actions
  Add CURSOR_PM_CYCLE_WEBHOOK_URL, CURSOR_FACTORY_ALERT_WEBHOOK_URL, CURSOR_WORKER_WEBHOOK_URL
  (copy values from Cursor Secrets — do not paste in chat/issues)
EOF
    exit 1
  fi
fi

# name|env_var|required
SECRET_SPECS=(
  "CURSOR_PM_CYCLE_WEBHOOK_URL|CURSOR_PM_CYCLE_WEBHOOK_URL|1"
  "CURSOR_FACTORY_ALERT_WEBHOOK_URL|CURSOR_FACTORY_ALERT_WEBHOOK_URL|1"
  "CURSOR_WORKER_WEBHOOK_URL|CURSOR_WORKER_WEBHOOK_URL|1"
  "TELEGRAM_BOT_TOKEN|TELEGRAM_BOT_TOKEN|0"
  "TELEGRAM_CHAT_ID|TELEGRAM_CHAT_ID|0"
)

FAIL=0
SET=0
SKIP=0

for spec in "${SECRET_SPECS[@]}"; do
  IFS='|' read -r secret_name env_var required <<< "$spec"
  val="${!env_var:-}"
  if [[ -z "$val" ]]; then
    if [[ "$required" == "1" ]]; then
      echo "[FAIL] ${env_var} not set in environment"
      FAIL=1
    else
      echo "[SKIP] ${secret_name} — ${env_var} not set"
      SKIP=$((SKIP + 1))
    fi
    continue
  fi
  if [[ "$DRY_RUN" -eq 1 ]]; then
    echo "[DRY]  ${secret_name} ← ${env_var}"
    continue
  fi
  if gh secret set "$secret_name" --body "$val" --repo "$REPO" 2>/dev/null; then
    echo "[OK]   ${secret_name}"
    SET=$((SET + 1))
  else
    echo "[FAIL] ${secret_name} — gh secret set failed"
    FAIL=1
  fi
done

echo ""
if [[ "$DRY_RUN" -eq 1 ]]; then
  echo "Dry run complete. Re-run without --dry-run after GH_TOKEN has Secrets write."
  exit 0
fi

if [[ "$FAIL" -ne 0 ]]; then
  echo "[FAIL] GitHub Actions secrets setup incomplete"
  exit 1
fi

echo "[PASS] GitHub Actions secrets — set=${SET} skip=${SKIP}"
echo "Verify: gh secret list --repo ${REPO}"
