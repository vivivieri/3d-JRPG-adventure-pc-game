---
id: p1-06-review-preview
type: how-to
audience: [pm, architect, builder, qa]
phase: [1]
status: active
authority: ops
tokens_est: 745
summary: "Phase1-Sprint1 — P1-06 review + Sprint2 preview — covers P1-06 — PM: Phase 1 sprint review + carry-over; Phase 1 exit gates (`acceptance_criteria.json`)."
---
# Phase1-Sprint1 — P1-06 review + Sprint2 preview

**Hub:** [`Phase1-Sprint1-issues.md`](../Phase1-Sprint1-issues.md)

## When to read

Use **Phase1-Sprint1 — P1-06 review + Sprint2 preview** (roles: pm, architect, builder, qa) when executing this procedure Jump to a section below instead of reading end-to-end (6 sections).

## Jump to

- [P1-06 — PM: Phase 1 sprint review + carry-over](#p1-06-pm-phase-1-sprint-review-carry-over)
- [Phase 1 exit gates (`acceptance_criteria.json`)](#phase-1-exit-gates-acceptance_criteriajson)
- [Sprint review agenda](#sprint-review-agenda)
- [Definition of done](#definition-of-done)
- [Phase1-Sprint2 preview (file issues next cycle)](#phase1-sprint2-preview-file-issues-next-cycle)
- [Quick copy: GitHub issue titles only](#quick-copy-github-issue-titles-only)


## P1-06 — PM: Phase 1 sprint review + carry-over

**Title:** `[DEV][P1-06] Phase1-Sprint1 review — phase_1 exit gap analysis`

**Labels:** `agent/pm`, `agent/qa`

| Field | Value |
|-------|-------|
| Phase | 1 |
| Lead agent | **pm** |
| Depends on | P1-04 (minimum) |

### Phase 1 exit gates (`acceptance_criteria.json`)

**Required:**

```
L0_rr_compliance
L0_story_data
L0_narrative_density
L1_unit_tests
L2_boot_headless
L2_scene_primitives
```

**Conditional (when assets exist):**

```
L2_visual_palette
L2_visual_jury
L2_zone_composition
L2_model_technical
L2_model_jury
L2_audio_technical
L2_audio_jury
```

### Sprint review agenda

1. Paste QA gate report from P1-04.
2. List PASS / FAIL / SKIP per phase_1 required_gates.
3. Carry over to **Phase1-Sprint2**: remaining greybox zones (1.5 beach/caves/palace), `lantern_fill.tscn` component (1.8), water assign on pier.
4. Optional UAT tag when phase_1 required all PASS: `v0.1.0-rc1` (`sprint_phases.json`).

### Definition of done

- [ ] Sprint review comment on this issue
- [ ] Carry-over issues filed for Phase1-Sprint2
- [ ] `status/done` on closed sprint issues

---


## Phase1-Sprint2 preview (file issues next cycle)

| Issue | Agent | Tasks | Gates |
|-------|-------|-------|-------|
| Greybox `beach_shore`, `tidal_caves`, `dragon_palace_gate` | builder | 1.5–1.7 | L2_scene_primitives, L3 |
| `lantern_fill.tscn` + pier water | builder | 1.8, 1.4 assign | L3 |
| Beach golden screenshot | qa | 1.10 | L2_visual_palette, GR-001 |
| Phase 1 exit review | qa | phase_1 all required | tag `v0.1.0-rc1` optional |

---


## Quick copy: GitHub issue titles only

```
[DEV][P1-00] Bootstrap game/development — project.godot + CI baseline
[DEV][P1-01] Phase 1.1–1.3 — toon_base.gdshader, zone_visuals.gd, ruined_village env preset
[DEV][P1-02] Phase 1.5–1.7 — GDAI ruined_village.tscn greybox + SC-02 lighting
[DEV][P1-03] Phase 1.4 — water_stylized.gdshader (foam + displacement)
[DEV][P1-04] Phase 1 — CI green + L0–L2 gate report on ruined_village PR
[DEV][P1-05] Phase 1.10–1.11 — ruined_village golden screenshot + zone composition smoke
[DEV][P1-06] Phase1-Sprint1 review — phase_1 exit gap analysis
```
