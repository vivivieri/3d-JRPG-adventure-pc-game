---
id: sprint-master-cadence
type: how-to
audience: [pm, architect]
status: active
authority: workflow
tokens_est: 1549
summary: "Sprint Master & AI cadence"
---
# Agile Within Phases — Sprint Master & AI cadence

**Hub:** [`AGILE_WITHIN_PHASES.md`](../AGILE_WITHIN_PHASES.md)

## 11. Sprint Master (facilitator role)

**There is no separate “Sprint Master” hire or agent.** In this repo the **PM Agent** is the sprint facilitator — the closest equivalent to a Scrum Master.

| Question | Answer |
|----------|--------|
| Who runs ceremonies? | **PM Agent** (planning, kickoff, retro notes) |
| Who owns delivery proof? | **QA Agent** (sprint review = gate report) |
| Who unblocks agents? | **PM Agent** first; **Architect** for technical blockers; **Human** for scope/L6 |
| Machine-readable | `sprint_phases.json` → `sprint_master.role` = `"pm"` |

### PM Agent as facilitator (not product owner only)

| Duty | When | Output |
|------|------|--------|
| Protect phase scope | Every cycle | Reject issues that skip phases or change `game/data/` without a `main` PR |
| Run sprint planning | Cycle start | ≤10 issues, gate IDs, `agent/*` labels, Linear cycle name |
| Track WIP | Daily (per session) | No more than 2 in-progress builder issues without QA pickup |
| Surface blockers | When CI/gates fail | `severity/S0`/`S1` issue; assign Architect or Release |
| Timebox the cycle | Batch end | Close Linear cycle when gates PASS — do not wait for calendar week |
| Retro | After UAT or phase exit | Update `sprint_phases.json` notes; adjust next `recommended_cadence_weeks` if needed |

**Human** retains veto on phase order, ship scope, and L6 sign-off — not day-to-day ceremony facilitation.

### What PM Agent must not do (even as facilitator)

- Write `.gd` / `.tscn` / shaders (R&R — Architect + Builder)
- Mark gates PASS without QA evidence
- Extend a phase deadline by reprioritizing waterfall milestones

---


## 12. Sprint duration — recommendations

**Primary model (pure AI agents):** **session batches** — see **§12.1**. Close a cycle when gate evidence is on the PR, not when a calendar week ends.

**Linear calendar ceiling:** **1 week** default (`sprint_phases.json` → `sprint_cadence.default_weeks`). Weeks are a **max batch window** for issue grouping in Linear, **not** expected implementation time.

Allowed ceiling range: **1–3 weeks** (phase rows → `recommended_cadence_weeks`). Extend only for human-blocked work (L6, jury, Steam store) — not because agents “need” two weeks to code.

### Per-phase calendar ceiling (Linear)

| Phase | Focus | Max weeks (ceiling) | AI-native target (active agents) |
|-------|-------|---------------------|----------------------------------|
| **1** | SC-02 vertical slice | **1** | **2–5 days** |
| **2** | Boot shell, localization | **1** | **~1 week** |
| **3** | Dialogue, quests, exploration | **1** | **~1 week** |
| **4** | Combat vertical slice | **1** | **~1 week** |
| **5** | Chapter 1 dungeons | **1** | **~1 week** |
| **6** | Full story, three endings | **2** | **1–2 weeks** (L5 validation depth) |
| **7** | M5 art rebuild | **3** | **Weeks+** (assets + jury, not agent speed) |
| **8** | M6 Steam ship | **2** | **1–2 weeks** (+ external store review) |

Machine-readable targets: `game/data/qa/sprint_phases.json` → `ai_native_target_days` per phase.

### When to use a 1-week ceiling (default)

- Every implementation batch on `game/development` unless a row below applies
- Phase 1 greybox, hotfix after `env/uat`, single-gate remediation (≤3 issues)

### When to extend the ceiling (2–3 weeks)

- Phase 6 or 8 integration batch waiting on **L5 / L6**
- Phase 7 jury cycle (model + audio + visual evidence)
- First batch after phase kickoff with >8 issues — **split into two batches** instead of one long cycle

### Linear configuration

1. Set team **default cycle length** = **1 week** (ceiling only).
2. End cycles early when all batch issues have gate evidence — do not wait for the week to expire.
3. Name cycles `Phase{N}-Sprint{K}`; description = phase task IDs from `IMPLEMENTATION_PLAN.md`.

**Do not** use velocity or burndown to skip **phase exit gates** — cadence only affects issue batching inside a phase.

---


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
