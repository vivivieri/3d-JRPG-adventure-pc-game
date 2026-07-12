# Agile Within Phases — Hybrid Delivery Model

**Version:** 1.0  
**Model name:** **Phase-gated Agile** (waterfall roadmap · agile execution)  
**Machine-readable:** `game/data/qa/sprint_phases.json`  
**Cross-refs:** `docs/IMPLEMENTATION_PLAN.md`, `docs/PROJECT_MANAGEMENT.md`, `docs/MULTI_AGENT_TEAM.md`, `docs/ENVIRONMENTS.md`

---

## 1. Summary

| Layer | Style | Tool | Changes when? |
|-------|-------|------|----------------|
| **Roadmap** | Waterfall | `IMPLEMENTATION_PLAN.md` Phases 0–8 | Major milestone only |
| **Scope** | Fixed (GDD + `game/data/`) | `docs/` + JSON | Data PRs to `main` |
| **Sprint execution** | Agile | **Linear** cycles (optional) + GitHub Issues | Every 1–2 weeks |
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
| **Cycles** | 2-week sprints **inside** current implementation phase |
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

### Phase1-Sprint1 (week 1–2)

| Issue | Agent | Gates |
|-------|-------|-------|
| Draft `toon_base.gdshader` + `zone_visuals.gd` | architect | L1 |
| GDAI: ruined_village greybox lights/fog | builder | L3, L2_scene_primitives |
| CI green on PR | qa | L0, L1, L2 |

### Phase1-Sprint2 (week 3–4)

| Issue | Agent | Gates |
|-------|-------|-------|
| `water_stylized.gdshader` + beach greybox | architect + builder | L2_scene_primitives |
| SC-02 screenshot + palette smoke | qa + visual | L2_visual_palette |
| Phase 1 exit review | qa | `phase_1` required_gates |

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

- `docs/PROJECT_MANAGEMENT.md` — labels, GitHub setup  
- `docs/GITHUB_SETUP.md` — labels/milestones script  
- `docs/MULTI_AGENT_TEAM.md` — role handoffs  
- `docs/ENVIRONMENTS.md` — dev → qa → uat promotion  
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
| Timebox the cycle | Cycle end | Close or carry over issues; schedule sprint review with QA |
| Retro | After UAT or phase exit | Update `sprint_phases.json` notes; adjust next `recommended_cadence_weeks` if needed |

**Human** retains veto on phase order, ship scope, and L6 sign-off — not day-to-day ceremony facilitation.

### What PM Agent must not do (even as facilitator)

- Write `.gd` / `.tscn` / shaders (R&R — Architect + Builder)  
- Mark gates PASS without QA evidence  
- Extend a phase deadline by reprioritizing waterfall milestones  

---

## 12. Sprint duration — recommendations

**Default:** **2 weeks** per Linear cycle (`sprint_phases.json` → `sprint_cadence.default_weeks`).

Allowed range: **1–3 weeks**. Change only when the phase row’s `recommended_cadence_weeks` or retro notes justify it — not for arbitrary deadline pressure.

### Per-phase cadence

| Phase | Focus | Recommended | Rationale |
|-------|-------|-------------|-----------|
| **1** | SC-02 vertical slice, shaders, first GDAI scenes | **1–2 weeks** | Tight feedback on palette/fog; first sprint can be **1 week** to learn agent throughput |
| **2** | Boot shell, localization, settings | **2 weeks** | Several small systems; stable integration window |
| **3** | Dialogue, quests, exploration | **2 weeks** | L4 scenarios need full cycle to stabilize |
| **4** | Combat vertical slice | **2 weeks** | Combat + boss framework = multi-agent handoffs |
| **5** | Chapter 1 dungeons | **2 weeks** | Zone flow tests span Architect → Builder → Flow |
| **6** | Full story, three endings | **2–3 weeks** | L5 E2E is long; prefer **3 weeks** for final integration sprint |
| **7** | M5 art rebuild | **3 weeks** | Asset import, jury loops, visual gates need buffer |
| **8** | M6 Steam ship | **2–3 weeks** | Checklist + export + store assets; last sprint often **3 weeks** |

### When to shorten (1 week)

- Phase 1 greybox iteration before first UAT screenshot  
- Hotfix sprint after `env/uat` feedback (RC tag already cut)  
- Single-gate remediation (one shader, one scene) with ≤3 issues  

### When to lengthen (3 weeks)

- Phase 6 or 8 integration sprint (L5 / L6 adjacent)  
- Phase 7 jury cycle (model + audio + visual evidence)  
- First sprint after a **phase kickoff** if planning uncovered >8 issues — split across two cycles instead of inflating WIP  

### Linear configuration

1. Set team **default cycle length** = 2 weeks.  
2. Override per cycle in Linear UI when starting Phase1-Sprint1 (1 week) or Phase6-SprintN (3 weeks).  
3. Name cycles `Phase{N}-Sprint{K}`; description = phase task IDs from `IMPLEMENTATION_PLAN.md`.  

**Do not** use velocity or burndown to skip **phase exit gates** — cadence only affects issue batching inside a phase.
