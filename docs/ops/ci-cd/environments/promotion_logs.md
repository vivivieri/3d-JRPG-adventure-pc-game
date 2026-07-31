---
id: promotion-logs
type: reference
phase: [6, 8]
audience: [pm, release]
status: active
authority: ci-cd
tokens_est: 490
summary: "Environments — Promotion, log correlation, refs — Never promote with SKIP gates (`skip_is_not_pass` in `acceptance_criteria.json`)."
---
# Environments — Promotion, log correlation, refs

**Hub:** [`ENVIRONMENTS.md`](../ENVIRONMENTS.md)

## When to read

Use **Environments — Promotion, log correlation, refs** (roles: pm, release) when you need this reference during the current task Jump to a section below instead of reading end-to-end (3 sections).

## Jump to

- [5. Promotion rules](#5-promotion-rules)
- [6. Log & trace correlation](#6-log-trace-correlation)
- [7. Cross-refs](#7-cross-refs)


## 5. Promotion rules

| From → To | Promotion criteria |
|-----------|-------------------|
| Dev → QA | Push to `game/development`; **CI green required** (bootstrap `project.godot` + tests first) |
| QA → UAT | All phase gates for milestone; tag RC |
| UAT → Preprod | L6 playtest ≥80%; S0/S1 = 0; Steamworks ready |
| Preprod → Prod | Beta soak complete; store page live; compliance pass |

**Never promote with SKIP gates** (`skip_is_not_pass` in `acceptance_criteria.json`).

---


## 6. Log & trace correlation

Every environment run should be traceable:

| Field | Where |
|-------|--------|
| Commit SHA | GitHub Actions run, issue body |
| Gate ID | `L0_story_data`, `L4_integration`, etc. |
| Agent session | Cloud agent URL or Cursor run ID |
| Artifacts | `artifacts/screenshots/`, `artifacts/test-reports/`, Actions logs |
| Remediation | `bash tools/qa_emit_remediation.sh <brief-id>` |

Issue title format: `[ENV][S1][L4] Short description`
Example: `[UAT][S1][L5] Drift ending soft-lock at SC-16`

---


## 7. Cross-refs

- `docs/ops/workflow/DEVELOPMENT_LIFECYCLE.md` — end-to-end lifecycle and promotion checklist
- `docs/ops/workflow/BRANCHING_DECISION_RECORD.md` — why env stages use tags + CI, not env branches
- `docs/ops/agents/PROJECT_MANAGEMENT.md` — issues, labels, MCP PM tools
- `docs/ops/agents/MULTI_AGENT_TEAM.md` — which agent owns each environment
- `docs/ops/ci-cd/CD.md` — artifact and Steam deploy
- `docs/ops/ci-cd/STEAM_RELEASE_CHECKLIST.md` — prod readiness
