---
id: flow-example
type: how-to
phase: [0, 1, 8]
audience: [pm]
status: active
authority: workflow
tokens_est: 732
summary: "Agile — Linear Sprints — Issue flow + Phase 1 example — IMPLEMENTATION_PLAN task row"
---
# Agile — Linear Sprints — Issue flow + Phase 1 example

**Hub:** [`linear_sprints.md`](../linear_sprints.md)

## When to read

Use **Agile — Linear Sprints — Issue flow + Phase 1 example** (roles: pm) when executing this procedure Jump to a section below instead of reading end-to-end (5 sections).

## Jump to

- [5. Issue flow (GitHub + Linear)](#5-issue-flow-github-linear)
- [6. Example: Phase 1 sprint breakdown](#6-example-phase-1-sprint-breakdown)
- [Phase1-Sprint1 (current — ruined_village vertical slice)](#phase1-sprint1-current-ruined_village-vertical-slice)
- [Phase1-Sprint2 (preview — remaining Phase 1 scope)](#phase1-sprint2-preview-remaining-phase-1-scope)
- [Phase exit](#phase-exit)


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

**Dependency order:** `P1-00` → `P1-01` ∥ `P1-03` → `P1-02` ∥ `P1-03` → `P1-04` / `P1-05` → `P1-06`

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
