---
id: sprint-master
type: how-to
phase: [0, 1, 8]
audience: [pm]
status: active
authority: workflow
tokens_est: 499
summary: "In this repo the **PM Agent** is the sprint facilitator — the closest equivalent to a Scrum Master."
---
# Agile — Sprint Master Cadence — Sprint Master role

**Hub:** [`sprint_master_cadence.md`](../sprint_master_cadence.md)

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
