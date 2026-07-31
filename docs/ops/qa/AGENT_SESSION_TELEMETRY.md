---
id: agent-session-telemetry
type: reference
phase: [1, 6]
audience: [pm, qa]
status: active
authority: qa
tokens_est: 263
summary: "Session telemetry — load storage, tokens, or analysis"
---
# Agent Session Telemetry

**Hub** — load only the pack for your current pass.

| Pack | Topic |
|------|-------|
| [`what_storage_hooks.md`](telemetry/what_storage_hooks.md) | What logs, storage, hooks |
| [`tokens_analysis.md`](telemetry/tokens_analysis.md) | Token reporting, analysis, categories |
| [`privacy_refs.md`](telemetry/privacy_refs.md) | Privacy, cross-refs, workflow coop |
**Discipline:** Dev-time factory analytics — measure agent performance by role, task category, and issue
**Status:** Active on `main` + `game/development` — hooks wired into session gate, heartbeat, and cycle events
**Authority:** `game/data/qa/agent_session_telemetry_schema.json`
**Analyzer:** `python3 tools/analyze_agent_session_telemetry.py`

## Close path

Workers close sessions with `bash tools/run_post_agent_cycle.sh` — details in `telemetry/` pack siblings.

