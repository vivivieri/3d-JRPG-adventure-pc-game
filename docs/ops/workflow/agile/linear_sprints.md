---
id: linear-sprints
type: how-to
audience: [pm, architect]
status: active
authority: workflow
tokens_est: 1343
summary: "Linear setup & sprint flow"
---
# Agile Within Phases — Linear setup & sprint flow

**Hub:** [`AGILE_WITHIN_PHASES.md`](../AGILE_WITHIN_PHASES.md)

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
**Issue pack:** `docs/ops/sprints/Phase1-Sprint1-issues.md`

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
