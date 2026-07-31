---
id: recommendations
type: how-to
audience: [pm]
status: active
authority: workflow
tokens_est: 736
summary: "Primary model (pure AI agents): session batches — see §12.1. Close a cycle when gate evidence is on the PR, not when a calendar week ends."
---
# Agile — Sprint Duration — Duration recommendations

**Hub:** [`duration.md`](../duration.md)

## When to read

Use **Agile — Sprint Duration — Duration recommendations** (roles: pm) when executing this procedure Jump to a section below instead of reading end-to-end (5 sections).

## Jump to

- [12. Sprint duration — recommendations](#12-sprint-duration-recommendations)
- [Per-phase calendar ceiling (Linear)](#per-phase-calendar-ceiling-linear)
- [When to use a 1-week ceiling (default)](#when-to-use-a-1-week-ceiling-default)
- [When to extend the ceiling (2–3 weeks)](#when-to-extend-the-ceiling-23-weeks)
- [Linear configuration](#linear-configuration)


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
