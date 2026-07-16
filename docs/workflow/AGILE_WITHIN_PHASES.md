# Agile Within Phases — Hybrid Delivery Model

**Version:** 1.0  
**Model name:** **Phase-gated Agile** (waterfall roadmap · agile execution)  
**Machine-readable:** `game/data/qa/sprint_phases.json`  
**Cross-refs:** `docs/workflow/IMPLEMENTATION_PLAN.md`, `docs/agents/PROJECT_MANAGEMENT.md`, `docs/agents/MULTI_AGENT_TEAM.md`, `docs/ci-cd/ENVIRONMENTS.md`

---

## 1. Summary

| Layer | Style | Tool | Changes when? |
|-------|-------|------|----------------|
| **Roadmap** | Waterfall | `IMPLEMENTATION_PLAN.md` Phases 0–8 | Major milestone only |
| **Scope** | Fixed (GDD + `game/data/`) | `docs/` + JSON | Data PRs to `main` |
| **Sprint execution** | Agile | **Linear** cycles (optional) + GitHub Issues | Per agent batch (§12.1); ≤1 week calendar ceiling |
| **Task delivery** | Agile | Multi-agent handoffs | Daily / per session |
| **Quality** | Gated | CI + acceptance criteria | Every commit / phase exit |
| **Release** | Staged waterfall | UAT → preprod → prod | RC / beta / ship tags |

**Rule:** Sprints optimize **how** we build the current phase. They do **not** reorder phases (e.g. M5 art still follows Phase 7; Steam still Phase 8).

---

## 2. Why not full Agile or full Waterfall?

### Full waterfall would mean

- No CI until phase end  
- No playtest until ship  
- No iteration within a zone  

**We reject that** — CI runs every push; vertical slice (SC-02) comes first; remediation loops exist.

### Full Agile would mean

- Emergent story design in sprints  
- Ship MVP with one ending, discover the rest  
- Art and gameplay co-evolve from sprint 1  

**We reject that for this project** — 3 endings, fixed scene IDs, and M5 art rebuild are planned upfront (`GDD.md`, `story/scenes.json`).

### Phase-gated Agile (this project)

```
[ Phase N scope frozen from IMPLEMENTATION_PLAN ]
        │
        ├── Sprint A ──► issues ──► agents ──► CI
        ├── Sprint B ──► issues ──► agents ──► CI
        └── Sprint C ──► phase exit gates ──► tag RC (optional UAT)
        │
[ Phase N+1 only after phase gates PASS ]
```

---

## 3. Linear setup (when MCP authenticated)

### 3.1 Linear hierarchy

| Linear entity | Maps to |
|---------------|---------|
| **Workspace** | Your studio / personal workspace |
| **Team** | `Tides of Urashima` |
| **Projects** | `M1-core`, `M5-art`, `M6-steam` (+ optional `M0-foundation`) |
| **Cycles** | 1-week batches **inside** current phase (close on gates, not calendar) |
| **Issues** | GitHub Issues (mirror or primary in Linear, link both ways) |
| **Labels** | Mirror `env/*`, `agent/*`, `gate/*` from `PROJECT_MANAGEMENT.md` |

### 3.2 Linear ↔ implementation phase map

| Impl phase | Linear project | Milestone | Sprint focus (examples) | Phase exit (must PASS) |
|------------|----------------|-----------|-------------------------|-------------------------|
| **0** ✅ | — | M0 | Done — docs/data baseline | `run_docs_ci_checks.sh` |
| **1** ← now | `M1-core` | — | ruined_village slice, toon shader, zone_visuals | `phase_1` gates in `acceptance_criteria.json` |
| **2** | `M1-core` | M1 | boot, LocalizationManager, settings UI | Phase 2 criteria §`AI_DEV_WORKFLOW` |
| **3** | `M1-core` | M1 | dialogue, quests, exploration, shop | L4 integration scenarios |
| **4** | `M1-core` | M2 | combat vertical slice, boss framework | Combat INT-* pass |
| **5** | `M1-core` | M3 | Chapter 1 dungeons, SC-08/11/12 | Zone flow L4 |
| **6** | `M1-core` | M4 | full story, 3 endings, cinematics | **L5 E2E** three endings |
| **7** | `M5-art` | M5 | NPR zones, hero meshes, VO clips | L2 jury + model/audio technical |
| **8** | `M6-steam` | M6 | GodotSteam, export, store, playtest | L6 + `STEAM_RELEASE_CHECKLIST` |

Full machine-readable rows: `game/data/qa/sprint_phases.json`.

### 3.3 Cycle naming convention

```
Phase{N}-Sprint{K}   e.g. Phase1-Sprint1, Phase1-Sprint2
```

Or date-based: `2026-W28` with description `Phase 1 — ruined village`.

**One active implementation phase at a time** on `game/development`. Cycle goals must cite phase task IDs from `IMPLEMENTATION_PLAN.md` (e.g. 1.3, 1.8).

---

## 4. Sprint ceremony (lightweight — AI team)

| Ceremony | When | Owner | Output |
|----------|------|-------|--------|
| **Phase kickoff** | Start of phase N | PM Agent (sprint facilitator) | Linear project/cycle + issues from IMPLEMENTATION_PLAN §Phase N table |
| **Sprint planning** | Cycle start | PM Agent (sprint facilitator) | 5–10 issues max; each has gate IDs + `agent/*` label |
| **Daily** | Each agent session | Active agent | Commit + CI; update issue status |
| **Sprint review** | Cycle end | QA Agent | Gate report pasted in issue/PR |
| **Phase review** | All phase tasks done | QA + Flow Agent | Phase exit gates; optional `v*-rc*` tag → UAT |
| **Retro** | After UAT or phase exit | PM + Human | Update `sprint_phases.json` notes; adjust next cycle WIP |

No standups required — agent session logs + GitHub Actions replace them.

---

## 5. Issue flow (GitHub + Linear)

```
IMPLEMENTATION_PLAN task row
    → Linear issue (cycle = current sprint)
    → GitHub issue (linked, same title)
    → PR on game/development
    → CI (env/qa)
    → Close when gate IDs PASS
```

**Definition of done (sprint issue):**

- [ ] Acceptance gate IDs in issue body  
- [ ] `bash tools/run_ci_checks.sh` PASS on PR commit  
- [ ] L3 F5 + `.gdai_built` if scenes touched  
- [ ] Evidence paths listed  
- [ ] Linear status = Done **and** GitHub issue closed  

---

## 6. Example: Phase 1 sprint breakdown

**Live board:** `game/data/qa/sprint_board.json` → `Phase1-Sprint1` (7 issues).  
**Issue pack:** `docs/sprints/Phase1-Sprint1-issues.md`

### Phase1-Sprint1 (current — ruined_village vertical slice)

| Issue | Agent | Implementation plan | Gates |
|-------|-------|---------------------|-------|
| P1-00 Bootstrap `project.godot` + CI baseline | pm / architect / builder | Phase 0 verify + branch bootstrap | L0 data, L1 unit |
| P1-01 `toon_base` + `zone_visuals` + env preset | architect | 1.1–1.3 | L1 |
| P1-02 GDAI `ruined_village.tscn` greybox | builder | 1.5–1.7, 1.9 | L3, L2_scene_primitives |
| P1-03 `water_stylized.gdshader` (parallel) | architect | 1.4 | L1 |
| P1-04 CI green + gate report | qa | sprint QA | L0–L2 (+ L3 when scenes exist) |
| P1-05 Golden screenshot + zone composition | qa + builder | 1.10–1.11 | L2_visual_palette, GR-001/003 |
| P1-06 Sprint review + carry-over | pm + qa | sprint review | `phase_1` required_gates gap |

**Dependency order:** `P1-00` → `P1-01` → `P1-02` → `P1-04` / `P1-03` (parallel) → `P1-05` → `P1-06`

### Phase1-Sprint2 (preview — remaining Phase 1 scope)

| Issue | Agent | Tasks | Gates |
|-------|-------|-------|-------|
| Greybox `beach_shore`, `tidal_caves`, `dragon_palace_gate` | builder | 1.5–1.7 | L2_scene_primitives, L3 |
| `lantern_fill.tscn` + pier water assign | builder | 1.8, 1.4 assign | L3 |
| Beach golden screenshot | qa | 1.10 | L2_visual_palette |
| Phase 1 exit review | qa | all `phase_1` required | optional `v0.1.0-rc1` tag |

### Phase exit

```bash
bash tools/run_ci_checks.sh
# all phase_1 required_gates PASS
git tag v0.1.0-rc1 && git push origin v0.1.0-rc1   # optional UAT
```

---

## 7. What stays waterfall (do not agile-ify)

| Decision | Authority |
|----------|-----------|
| Phase order 1→8 | `IMPLEMENTATION_PLAN.md` |
| Story scenes, flags, dialogue | `game/data/` |
| Art rebuild after gameplay | Phase 7 before Phase 8 |
| Merge to `main` | Once at M6 ship |
| Three endings scope | `ENDING_DESIGN.md` — not deferred |
| License / compliance | `ASSET_COMPLIANCE.md` |

Change these only via explicit doc + data PR to `main`, not via sprint backlog reprioritization.

---

## 8. Linear MCP — agent commands

After authenticating Linear in Cursor:

| Intent | Skill / action |
|--------|----------------|
| Create sprint tasks from phase | `spec-to-implementation` or `create-task` |
| Query open blockers | `database-query` / Linear search |
| Log retro notes | `knowledge-capture` (optional Notion) |

**PM Agent sprint start checklist:**

1. Read `game/data/qa/sprint_phases.json` → `active_phase`  
2. Read `IMPLEMENTATION_PLAN.md` §Phase N task table  
3. Create Linear cycle `Phase{N}-Sprint{K}`  
4. Create issues (≤10) with gate IDs + agent labels  
5. Mirror critical issues to GitHub for CI linkage  

---

## 9. Metrics (optional, lightweight)

| Metric | Source | Use |
|--------|--------|-----|
| CI pass rate | GitHub Actions | Sprint health |
| Open S0/S1 count | GitHub labels | Block release |
| Gate failure rate | `env/qa` issues | Remediation focus |
| Cycle completion | Linear | Velocity trend (inform WIP, not deadlines) |

Do not use velocity to skip phase gates.

---

## 10. Cross-refs

- `docs/agents/PROJECT_MANAGEMENT.md` — labels, GitHub setup  
- `docs/ci-cd/GITHUB_SETUP.md` — labels/milestones script  
- `docs/agents/MULTI_AGENT_TEAM.md` — role handoffs  
- `docs/ci-cd/ENVIRONMENTS.md` — dev → qa → uat promotion  
- `game/data/qa/sprint_phases.json` — phase ↔ Linear ↔ gates catalog  

---

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

**Enforced by:** `bash tools/run_pm_orchestrator.sh` — see `docs/agents/PM_AGENT_RUNBOOK.md`

1. Pull ≤10 issues from current phase (`sprint_phases.json` → `active_phase`) into `sprint_board.json`.  
2. Label each with gate IDs + `agent/*`; sync `docs/sprints/` issue pack.  
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
