# Tides of Urashima — Alignment Audit Report

**Alignment audit — FAIL (cursor/audit-slide-visuals-780b @ 30dce1e) · Spec 4.2/10 · Build N/A/10**
Generated: 2026-07-31T18:26:11Z · Audit ID: `20260731T182611Z_stakeholder_phase_exit`
Branch: `cursor/audit-slide-visuals-780b` · Commit: `30dce1e`

## Verdict: **FAIL**

## Streams (management view)

| Stream | Score | Status | Question |
|--------|-------|--------|----------|
| Design & Preparation | 4.2/10 | Fail | Can we dispatch builders? Is design truth complete? |
| Development & Shipping | N/A | N/A — Build stream applies only on game/development — main holds specs until P1-00 bootstrap | Does the game run, pass gates, and approach Steam? |

> **Do not merge spec + build into one radar for management.** Each stream answers a different question.

### Design & Preparation domains

| Domain | Score |
|--------|-------|
| Ux Controls | 8.2 |
| Data Alignment | 6.8 |
| Narrative | 4.0 |
| Visual Spec | 3.7 |
| Gameplay | 2.5 |
| Pm Workflow | 0.0 |

## Spec domain signal breakdown

Each of the 6 spec domains has its own sub-radar (signals behind the axis score).

### Data Alignment (6.8/10)

| Signal | Score |
|--------|-------|
| `scene_registry_parity` | 10.0 |
| `hooks_parity` | 10.0 |
| `tutorial_flags` | 10.0 |
| `sprint_board_parity` | 10.0 |
| `L0_scene_registry` | 0.0 |
| `L0_story_data` | 0.0 |

### Narrative (4.0/10)

| Signal | Score |
|--------|-------|
| `vo_hit_list` | 10.0 |
| `cinematic_hooks` | 10.0 |
| `L0_story_data` | 0.0 |
| `L0_narrative_density` | 0.0 |

### Gameplay (2.5/10)

| Signal | Score |
|--------|-------|
| `encounters_catalogued` | 10.0 |
| `L0_spec_registry` | 0.0 |
| `L0_difficulty_data` | 0.0 |
| `L0_base_classes` | 0.0 |

### Visual Spec (3.7/10)

| Signal | Score |
|--------|-------|
| `zone_palette_rows` | 10.0 |
| `impl_shaders_partial` | 8.5 |
| `L0_zone_visuals_contract` | 0.0 |
| `L0_zone_composition` | 0.0 |

### Ux Controls (8.2/10)

| Signal | Score |
|--------|-------|
| `settings_accessibility_doc` | 10.0 |
| `combat_presentation_doc` | 10.0 |
| `impl_scenes_not_started` | 4.0 |

### Pm Workflow (0.0/10)

| Signal | Score |
|--------|-------|
| `ci_pass_rate` | 0.0 |
| `L0_doc_sync` | 0.0 |
| `L0_pm_orchestrator` | 0.0 |
| `L0_stakeholder_report` | 0.0 |
| `L0_workflow_integration` | 0.0 |
| `L0_candidate_tournament` | 0.0 |
| `L0_agent_session_telemetry` | 0.0 |
| `L0_factory_watchdog` | 0.0 |
| `L0_sprint_board` | 0.0 |

## Build domain signal breakdown

Each build domain has its own sub-radar (signals behind the axis score).
On `main`, build stream is N/A but domain signal previews still generate.

### Runtime Proof (3.5/10)

| Signal | Score |
|--------|-------|
| `L2_boot_headless` | 4.0 |
| `L4_integration` | 4.0 |
| `L5_e2e_three_endings` | 4.0 |
| `has_project_godot` | 2.0 |

### Steam Ship (1.05/10)

| Signal | Score |
|--------|-------|
| `runtime_proof` | 3.5 |
| `L0_ship_build_security` | 0.0 |
| `L0_player_build_protection` | 0.0 |
| `M5_asset_compliance` | 0.0 |

## All domain scores (0–10)

| Domain | Score |
|--------|-------|
| Ux Controls | 8.2 |
| Data Alignment | 6.8 |
| Narrative | 4.0 |
| Visual Spec | 3.7 |
| Runtime Proof | 3.5 |
| Gameplay | 2.5 |
| Steam Ship | 1.05 |
| Pm Workflow | 0.0 |

## CI summary
- Script: `None`
- PASS: **0** · FAIL: **0** · SKIP: 0

## Data parity
- Encounters: OK
- Hooks: OK
- Tutorial flags: OK
- Sprint board ↔ pack: OK

## Recommendation checklist

### Ship path M6 (P2) (1 open)
- [ ] **P2** L5 three-endings E2E before human QA — bash tools/run_e2e_playthrough.sh on game/development; all SC-17a/b/c paths must PASS.

### Stakeholder comms (P2) (1 open)
- [ ] **P2** Refresh stakeholder visual pack — Place illustrated management PNGs in docs/archive/compliance/alignment_audit_visuals/latest/ (style refs in style/), then: bash tools/run_alignment_audit.sh --visuals-from docs/archive/compliance/alignment_audit_visuals/latest

## Stream radars (overview)

![Exec summary slide (radar + bars + callouts)](visuals/audit_exec_summary.png)
*Exec summary slide (radar + bars + callouts) (auto-generated)*
![Two-stream radar report](visuals/audit_radar_report.png)
*Two-stream radar report (auto-generated)*
![Spec readiness radar](visuals/audit_radar_spec.png)
*Spec readiness radar (auto-generated)*
![Build readiness radar](visuals/audit_radar_build.png)
*Build readiness radar (auto-generated)*

## Spec sub-radar breakdown (6 domains)

Each panel shows signal-level scores within one spec domain.

![Spec sub-radar breakdown (6 domains)](visuals/audit_radar_spec_breakdown.png)
*Spec sub-radar breakdown (6 domains) (auto-generated)*

## Spec domain sub-radars (detail)

![Data Alignment sub-radar](visuals/audit_radar_spec_data_alignment.png)
*Data Alignment sub-radar (auto-generated)*
![Narrative sub-radar](visuals/audit_radar_spec_narrative.png)
*Narrative sub-radar (auto-generated)*
![Gameplay sub-radar](visuals/audit_radar_spec_gameplay.png)
*Gameplay sub-radar (auto-generated)*
![Visual Spec sub-radar](visuals/audit_radar_spec_visual_spec.png)
*Visual Spec sub-radar (auto-generated)*
![UX & Controls sub-radar](visuals/audit_radar_spec_ux_controls.png)
*UX & Controls sub-radar (auto-generated)*
![PM Workflow sub-radar](visuals/audit_radar_spec_pm_workflow.png)
*PM Workflow sub-radar (auto-generated)*

## Build sub-radar breakdown (2 domains)

Each panel shows signal-level scores within one build domain.

![Build sub-radar breakdown (2 domains)](visuals/audit_radar_build_breakdown.png)
*Build sub-radar breakdown (2 domains) (auto-generated)*

## Build domain sub-radars (detail)

![Runtime Proof sub-radar](visuals/audit_radar_build_runtime_proof.png)
*Runtime Proof sub-radar (auto-generated)*
![Steam Ship sub-radar](visuals/audit_radar_build_steam_ship.png)
*Steam Ship sub-radar (auto-generated)*

---
Authority: `docs/ops/qa/ALIGNMENT_AUDIT.md` · Re-run: `bash tools/run_alignment_audit.sh`
