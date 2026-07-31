---
id: ai-native
type: how-to
phase: [0, 1, 8]
audience: [pm]
status: active
authority: workflow
tokens_est: 735
summary: "For a **pure AI agent team**, sprints are **outcome batches**, not human capacity sprints."
---
# Agile — Sprint Duration — AI-native cadence

**Hub:** [`duration.md`](../duration.md)

## When to read

Use **Agile — Sprint Duration — AI-native cadence** (roles: pm) when executing this procedure Jump to a section below instead of reading end-to-end (5 sections).

## Jump to

- [12.1 AI-native cadence (pure agent implementation)](#121-ai-native-cadence-pure-agent-implementation)
- [Cycle units](#cycle-units)
- [What actually consumes calendar time](#what-actually-consumes-calendar-time)
- [PM Agent batch checklist (replaces “two-week planning”)](#pm-agent-batch-checklist-replaces-two-week-planning)
- [Example: Phase 1 at AI speed](#example-phase-1-at-ai-speed)


## 12.1 AI-native cadence (pure agent implementation)

For a **pure AI agent team**, sprints are **outcome batches**, not human capacity sprints.

### Cycle units

| Unit | Size | Close when |
|------|------|------------|
| **Micro-cycle** | 1–3 issues or 1–2 agent sessions | Named gate IDs PASS on PR |
| **Standard cycle** | ≤10 issues (`max_issues_per_cycle`) | All batch issues closed **or** explicit carry-over logged |
| **Integration cycle** | L4 / L5 scope | `run_integration_tests.sh` / `run_e2e_playthrough.sh` green |
| **Human-blocked** | L6, Steam, external assets | Human sign-off or asset delivery — calendar time irrelevant to agent throughput |

### What actually consumes calendar time

| Bottleneck | AI impact |
|------------|-----------|
| Architect → Builder → QA handoffs | Separate sessions; batch small |
| CI + gate scripts | Wall-clock minutes per run |
| GDAI F5 + `.gdai_built` | One builder session per scene batch |
| Remediation loops | Re-run until PASS — count **iterations**, not weeks |
| L5 three endings, L6 playtest, M5 assets | **Validation / human** — can exceed any sprint ceiling |

### PM Agent batch checklist (replaces “two-week planning”)

**Enforced by:** `bash tools/run_pm_orchestrator.sh` — see `docs/ops/agents/PM_AGENT_RUNBOOK.md`

1. Pull ≤10 issues from current phase (`sprint_phases.json` → `active_phase`) into `sprint_board.json`.
2. Label each with gate IDs + `agent/*`; sync `docs/ops/sprints/` issue pack.
3. Run **micro-cycles** for isolated shaders/scenes (1–2 sessions).
4. Dispatch via orchestrator; agents pass `run_agent_session_gate.sh`.
5. When batch gates PASS → **close Linear cycle immediately** (even mid-week).
6. Open next `Phase{N}-Sprint{K+1}`; carry-over via `pm_close_sprint.py` if needed.

### Example: Phase 1 at AI speed

| Batch | Issues | Sessions (typical) | Close trigger |
|-------|--------|-------------------|---------------|
| Phase1-Sprint1 | P1-00…P1-06 (see `sprint_board.json`) | PM + Architect + Builder + QA | ruined_village gates PASS; carry-over logged in P1-06 |
| Phase1-Sprint2 | beach/caves/palace greybox + 1.8 components | Builder + QA | all `phase_1` required_gates PASS |

Two batches might finish in **2–5 calendar days** with active agents — not three weeks.
