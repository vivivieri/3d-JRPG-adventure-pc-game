#!/usr/bin/env bash
# Idempotent GitHub repo setup: labels, milestones, environments, branch protection.
# Requires: GH_TOKEN or GITHUB_TOKEN with repo scope (and admin for branch protection).
#
# Usage:
#   export GH_TOKEN=ghp_...   # or add to Cursor Secrets
#   bash tools/setup_github_project.sh
#   bash tools/setup_github_project.sh --dry-run
#
# See docs/ci-cd/GITHUB_SETUP.md
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
if [[ -z "$TOKEN" && "$DRY_RUN" -eq 0 ]]; then
  echo "[FAIL] GH_TOKEN or GITHUB_TOKEN not set."
  echo "       Create a fine-grained PAT — see docs/ci-cd/GITHUB_SETUP.md §1"
  echo "       Add to Cursor Secrets as GH_TOKEN, then re-run this script."
  exit 1
fi

if [[ -z "$TOKEN" && "$DRY_RUN" -eq 1 ]]; then
  REPO="OWNER/REPO (dry-run)"
else
  export GH_TOKEN="$TOKEN"
  if ! gh auth status >/dev/null 2>&1; then
    echo "==> Authenticating gh with GH_TOKEN..."
    echo "$TOKEN" | gh auth login --with-token
  fi
  REPO="$(gh repo view --json nameWithOwner -q .nameWithOwner)"
fi
echo "==> GitHub setup for ${REPO}"
echo ""

urlencode() {
  python3 -c "import urllib.parse,sys; print(urllib.parse.quote(sys.argv[1], safe=''))" "$1"
}

# name|color|description
LABELS=(
  "env/development|1a3a5c|Active implementation on game/development"
  "env/qa|0e8a16|Automated CI gate failure"
  "env/uat|c5def5|Human playtest or RC build"
  "env/preprod|fb8500|Steam beta channel"
  "env/production|d1242f|Ship blocker or production"
  "severity/S0|b60205|Blocker — cannot progress"
  "severity/S1|d93f0b|Major bug"
  "severity/S2|fbbf24|Minor bug"
  "severity/S3|fef9c3|Polish"
  "gate/L0_story_data|5319e7|Story data validator"
  "gate/L1_unit_tests|8250df|Unit tests"
  "gate/L4_integration|116329|Integration tests"
  "gate/L5_e2e|006b75|E2E three endings"
  "domain/visual|e99695|Visual or art jury"
  "domain/audio|a371f7|Audio technical or jury"
  "domain/flow|1d76db|Flow or soft-lock"
  "agent/architect|c933c3|GodotPrompter architect"
  "agent/builder|006b75|GDAI MCP builder"
  "agent/qa|0e8a16|QA agent gate run"
  "agent/release|6f42c1|Release or CD agent"
  "status/blocked|000000|Blocked on MCP secrets or human"
  "status/in-progress|1d76db|Agent actively working"
  "status/done|0e8a16|Verified fixed"
)

echo "==> Labels (${#LABELS[@]})"
for spec in "${LABELS[@]}"; do
  IFS='|' read -r name color desc <<< "$spec"
  if [[ "$DRY_RUN" -eq 1 ]]; then
    echo "  [DRY] ${name}"
    continue
  fi
  enc="$(urlencode "$name")"
  if gh label create "$name" --color "$color" --description "$desc" --force 2>/dev/null; then
    echo "  [OK] ${name}"
  else
    gh api -X PATCH "repos/${REPO}/labels/${enc}" \
      -f "color=${color}" -f "description=${desc}" >/dev/null 2>&1 || true
    echo "  [OK] ${name} (updated)"
  fi
done

MILESTONES=(
  "M1-core|Core systems and narrative exploration"
  "M5-art|Art rebuild Phase 7"
  "M6-steam|Steam ship Phase 8"
)

echo ""
echo "==> Milestones"
for spec in "${MILESTONES[@]}"; do
  IFS='|' read -r title desc <<< "$spec"
  if [[ "$DRY_RUN" -eq 1 ]]; then
    echo "  [DRY] ${title}"
    continue
  fi
  existing="$(gh api "repos/${REPO}/milestones?state=all" --jq ".[] | select(.title==\"${title}\") | .number" | head -1)"
  if [[ -n "$existing" ]]; then
    echo "  [SKIP] ${title} (#${existing})"
  else
    gh api "repos/${REPO}/milestones" -f "title=${title}" -f "description=${desc}" -f "state=open" >/dev/null
    echo "  [OK] ${title}"
  fi
done

# env_name|min_approvals|description
ENVIRONMENT_SPECS=(
  "qa|0|Automated nightly gate sweep — no approval gate"
  "uat|1|RC artifact tags (v*-rc*) — human playtest gate"
  "steam-beta|1|Steam beta CD — manual workflow_dispatch"
  "steam-production|2|Steam production CD — requires two approvers when configured"
)

resolve_user_id() {
  local login="$1"
  gh api "users/${login}" --jq .id 2>/dev/null || echo ""
}

configure_environment() {
  local env_name="$1"
  local min_approvals="$2"
  local desc="$3"
  if [[ "$DRY_RUN" -eq 1 ]]; then
    echo "  [DRY] ${env_name} (min approvals: ${min_approvals})"
    return 0
  fi

  local owner_login
  owner_login="$(gh repo view --json owner -q .owner.login)"
  local primary="${GITHUB_ENV_REVIEWER_LOGIN:-$owner_login}"
  local secondary="${GITHUB_ENV_REVIEWER_LOGIN_2:-}"

  local reviewers_json="[]"
  if [[ "$min_approvals" -gt 0 ]]; then
    local ids=()
    local pid
    pid="$(resolve_user_id "$primary")"
    if [[ -z "$pid" ]]; then
      echo "  [WARN] ${env_name} — could not resolve reviewer login '${primary}'"
    else
      ids+=("$pid")
    fi
    if [[ "$min_approvals" -ge 2 ]]; then
      if [[ -n "$secondary" ]]; then
        local sid
        sid="$(resolve_user_id "$secondary")"
        if [[ -n "$sid" ]]; then
          ids+=("$sid")
        else
          echo "  [WARN] ${env_name} — GITHUB_ENV_REVIEWER_LOGIN_2 '${secondary}' not found"
        fi
      else
        echo "  [WARN] ${env_name} — wants 2 approvers; set GITHUB_ENV_REVIEWER_LOGIN_2 for second reviewer"
      fi
    fi
    if [[ ${#ids[@]} -gt 0 ]]; then
      reviewers_json="$(IDS="${ids[*]}" python3 -c "
import json, os
ids = [int(x) for x in os.environ.get('IDS', '').split() if x]
print(json.dumps([{'type': 'User', 'id': i} for i in ids]))
")"
    fi
  fi

  if gh api -X PUT "repos/${REPO}/environments/${env_name}" --input - <<JSON
{
  "wait_timer": 0,
  "prevent_self_review": false,
  "reviewers": ${reviewers_json}
}
JSON
  then
    echo "  [OK] ${env_name} — ${desc}"
  else
    echo "  [WARN] ${env_name} — could not configure (needs admin PAT)"
  fi
}

echo ""
echo "==> GitHub Environments"
for spec in "${ENVIRONMENT_SPECS[@]}"; do
  IFS='|' read -r env_name min_approvals desc <<< "$spec"
  configure_environment "$env_name" "$min_approvals" "$desc"
done

protect_branch() {
  local branch="$1"
  local check_name="$2"
  local review_count="${3:-1}"
  local enc_branch
  enc_branch="$(urlencode "$branch")"
  if [[ "$DRY_RUN" -eq 1 ]]; then
    echo "  [DRY] protect ${branch} — require ${check_name} + ${review_count} PR review(s)"
    return 0
  fi
  local reviews_json="null"
  if [[ "$review_count" -gt 0 ]]; then
    reviews_json="{\"required_approving_review_count\": ${review_count}, \"dismiss_stale_reviews\": false}"
  fi
  if gh api -X PUT "repos/${REPO}/branches/${enc_branch}/protection" --input - <<JSON
{
  "required_status_checks": {
    "strict": true,
    "checks": [{"context": "${check_name}"}]
  },
  "enforce_admins": false,
  "required_pull_request_reviews": ${reviews_json},
  "restrictions": null,
  "required_linear_history": false,
  "allow_force_pushes": false,
  "allow_deletions": false
}
JSON
  then
    echo "  [OK] ${branch} — status: ${check_name}; PR reviews: ${review_count}"
  else
    echo "  [WARN] Could not protect ${branch} — needs admin PAT. See docs/ci-cd/GITHUB_SETUP.md §2"
  fi
}

echo ""
echo "==> Branch protection"
protect_branch "main" "Docs + design data gates" 1
protect_branch "game/development" "L0–L2 headless gates" 1

echo ""
echo "==> GitHub Projects (manual)"
echo "  Projects tab → New project → Board"
echo "  Columns: Backlog | Ready | In Progress | QA | UAT | Done"

echo ""
if [[ "$DRY_RUN" -eq 1 ]]; then
  echo "Dry run complete. Re-run without --dry-run to apply."
else
  echo "GitHub setup complete: https://github.com/${REPO}/labels"
fi
