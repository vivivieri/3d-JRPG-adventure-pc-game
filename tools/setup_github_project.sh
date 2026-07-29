#!/usr/bin/env bash
# Idempotent GitHub repo setup: labels, milestones, environments, branch protection.
# Requires: GH_TOKEN or GITHUB_TOKEN with repo scope (and admin for branch protection).
#
# Usage:
#   export GH_TOKEN=ghp_...   # or add to Cursor Secrets
#   bash tools/setup_github_project.sh
#   bash tools/setup_github_project.sh --dry-run
#
# See docs/ops/ci-cd/GITHUB_SETUP.md
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

resolve_gh_auth() {
  local token="${GH_TOKEN:-${GITHUB_TOKEN:-}}"
  if [[ -n "$token" ]]; then
    export GH_TOKEN="$token"
    if gh auth status >/dev/null 2>&1; then
      return 0
    fi
    echo "[WARN] GH_TOKEN/GITHUB_TOKEN is set but invalid — trying gh stored credentials..."
    unset GH_TOKEN
  fi
  if gh auth status >/dev/null 2>&1; then
    return 0
  fi
  if [[ -n "$token" ]]; then
    echo "==> Authenticating gh with GH_TOKEN..."
    echo "$token" | gh auth login --with-token
    return 0
  fi
  return 1
}

if [[ "$DRY_RUN" -eq 1 ]]; then
  REPO="OWNER/REPO (dry-run)"
elif resolve_gh_auth; then
  REPO="$(gh repo view --json nameWithOwner -q .nameWithOwner)"
else
  echo "[FAIL] No valid GitHub credentials."
  echo "       export GH_TOKEN=<fine-grained PAT with admin:repo> — see docs/ops/ci-cd/GITHUB_SETUP.md §1"
  echo "       Or run \`gh auth login\` locally, then re-run this script."
  exit 1
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
  "gate/L0_narrative_density|5319e7|Narrative density budget"
  "gate/L0_rr_compliance|1a3a5c|GDAI-verified scenes only"
  "gate/L0_base_classes|5319e7|Base class registry"
  "gate/L0_base_class_compliance|5319e7|Native extends audit"
  "gate/L0_acceptance_catalog|5319e7|Acceptance criteria catalog"
  "gate/L1_unit_tests|8250df|Unit tests"
  "gate/L1_gdscript_lint|8250df|GDScript lint"
  "gate/L2_boot_headless|116329|Headless boot smoke"
  "gate/L2_scene_primitives|116329|Scene primitives smoke"
  "gate/L2_feel_smoke|116329|Feel smoke checks"
  "gate/L2_glb_import|116329|GLB import scripts"
  "gate/L2_visual_palette|e99695|Visual palette smoke"
  "gate/L2_zone_composition|e99695|Zone composition data"
  "gate/L3_gdai_built|006b75|GDAI MCP scene build"
  "gate/L4_integration|116329|Integration tests"
  "gate/L5_e2e|006b75|E2E three endings"
  "domain/visual|e99695|Visual or art jury"
  "domain/audio|a371f7|Audio technical or jury"
  "domain/flow|1d76db|Flow or soft-lock"
  "agent/architect|c933c3|GodotPrompter architect"
  "agent/builder|006b75|GDAI MCP builder"
  "agent/qa|0e8a16|QA agent gate run"
  "agent/release|6f42c1|Release or CD agent"
  "agent/analyst|5319e7|Factory telemetry analyst"
  "agent/flow|1d76db|Flow / L4-L5 integration agent"
  "agent/visual|e99695|Visual jury agent"
  "agent/pm|8250df|PM sprint master"
  "dispatch/ready|f9d0c4|Triggers Worker automation — snapshot VM"
  "phase/1|0e8a16|Implementation phase 1"
  "phase/2|1d76db|Implementation phase 2"
  "phase/3|5319e7|Implementation phase 3"
  "phase/4|8250df|Implementation phase 4"
  "phase/5|c933c3|Implementation phase 5 (M5 art)"
  "phase/6|6f42c1|Implementation phase 6"
  "phase/7|e99695|Implementation phase 7"
  "phase/8|fb8500|Implementation phase 8 (Steam)"
  "phase/9|d1242f|Implementation phase 9"
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
  "uat|0|RC artifact tags (v*-rc*) — CI gates only"
  "steam-beta|0|Steam beta CD — CI gates only"
  "steam-production|0|Steam production CD — CI gates only (no human approval)"
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
  local review_count="${3:-0}"
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
    echo "  [WARN] Could not protect ${branch} — needs admin PAT. See docs/ops/ci-cd/GITHUB_SETUP.md §2"
  fi
}

echo ""
echo "==> Branch protection"
protect_branch "main" "Docs + design data gates" 0
protect_branch "game/development" "L0–L2 headless gates" 0

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
