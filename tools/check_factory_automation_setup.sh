#!/usr/bin/env bash
# Validate repo-side factory automation setup (catalog, prompts, orchestrator wiring).
# Cannot verify Cursor dashboard automations exist — prints manual checklist.
#
# Usage: bash tools/check_factory_automation_setup.sh
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

echo "==> Factory automation setup check"
echo "    Authority: docs/agents/FACTORY_SETUP_GUIDE.md"
echo ""

FAIL=0

if python3 tools/validate_factory_automations.py; then
  echo ""
else
  FAIL=1
fi

echo "── Repo files"
for f in \
  game/data/qa/factory_automations.json \
  docs/agents/FACTORY_SETUP_GUIDE.md \
  docs/agents/automation_prompts/pm_cycle_dispatch.md \
  docs/agents/automation_prompts/worker_sprint_issue.md; do
  if [[ -f "$f" ]]; then
    echo "[OK]   $f"
  else
    echo "[FAIL] $f missing"
    FAIL=1
  fi
done

echo ""
echo "── GitHub labels (requires GH_TOKEN)"
if [[ -n "${GH_TOKEN:-}" ]] && command -v gh >/dev/null 2>&1 && gh auth status >/dev/null 2>&1; then
  for label in dispatch/ready agent/flow agent/visual agent/pm agent/analyst; do
    if gh label list --limit 200 2>/dev/null | grep -q "^${label}\b"; then
      echo "[OK]   label ${label}"
    else
      echo "[WARN] label ${label} missing — run: bash tools/setup_github_project.sh"
    fi
  done
else
  echo "[SKIP] GH_TOKEN/gh not available — run setup_github_project.sh when ready"
fi

echo ""
echo "── Cursor dashboard (manual — cannot verify from repo)"
echo "  [ ] Environment snapshot saved; id matches .cursor/environment.json"
echo "  [ ] Automation A: webhook → CURSOR_PM_CYCLE_WEBHOOK_URL"
echo "  [ ] Automation D: webhook → CURSOR_FACTORY_ALERT_WEBHOOK_URL"
echo "  [ ] Automation E: GitHub issue labeled dispatch/ready → Worker prompt"
echo "  [ ] All automations: repo 3d-JRPG-adventure-pc-game branch game/development"
echo "  [ ] MCP: godot-mcp, godotiq, godot-mcp-pro, gamelab-mcp registered"
echo "  [ ] Test: bash tools/pm_emit_cycle_event.sh agent_cycle_complete --issue P1-00 --agent pm --note test"
echo ""
echo "  Dashboard: https://cursor.com/dashboard/cloud-agents/environments/r/github.com/vivivieri/3d-jrpg-adventure-pc-game"
echo "  Automations: https://cursor.com/automations"

echo ""
if [[ "$FAIL" -eq 0 ]]; then
  echo "[PASS] Factory automation repo setup"
  exit 0
fi
echo "[FAIL] Factory automation repo setup — fix errors above"
exit 1
