# Tides of Urashima — Alignment Audit Report

**Alignment audit — FAIL (cursor/audit-two-streams-68f4 @ 937ee8b) · Spec 4.2/10 · Build 2.27/10**
Generated: 2026-07-18T15:19:26Z · Audit ID: `20260718T151926Z_post_merge`
Branch: `cursor/audit-two-streams-68f4` · Commit: `937ee8b`

## Verdict: **FAIL**

## Streams (management view)

| Stream | Score | Status | Question |
|--------|-------|--------|----------|
| Design & Preparation | 4.2/10 | Fail | Can we dispatch builders? Is design truth complete? |
| Development & Shipping | 2.27/10 | Fail | Does the game run, pass gates, and approach Steam? |

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

### Development & Shipping domains

| Domain | Score |
|--------|-------|
| Runtime Proof | 3.5 |
| Steam Ship | 1.05 |

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

## Stakeholder visuals
![Ruined village key art](../../alignment_audit_visuals/concept_ruined_village.png)
*Ruined village key art*
![9-domain production radar (legacy)](../../alignment_audit_visuals/audit_radar_6axis.png)
*9-domain production radar (legacy)*
![6-phase production roadmap](../../alignment_audit_visuals/roadmap_6phase.png)
*6-phase production roadmap*
![Beach shore SC-01](../../alignment_audit_visuals/tides_concept_beach_shore.png)
*Beach shore SC-01*
![Palace gate SC-12](../../alignment_audit_visuals/tides_concept_palace_gate.png)
*Palace gate SC-12*
![Post-alignment radar](../../alignment_audit_visuals/tides_audit_radar_updated.png)
*Post-alignment radar*
![Data alignment radar](../../alignment_audit_visuals/tides_audit_alignment_radar.png)
*Data alignment radar*
![12-phase roadmap](../../alignment_audit_visuals/tides_roadmap_12phase.png)
*12-phase roadmap*
![Zone vertical slice path](../../alignment_audit_visuals/tides_roadmap_zone_slice.png)
*Zone vertical slice path*
![Tidal caves SC-08](../../alignment_audit_visuals/tides_concept_tidal_caves.png)
*Tidal caves SC-08*
![Three endings triptych](../../alignment_audit_visuals/tides_concept_three_endings.png)
*Three endings triptych*
![Post P1-00 dispatch radar](../../alignment_audit_visuals/tides_audit_post_p1_dispatch.png)
*Post P1-00 dispatch radar*
![MCP stack readiness](../../alignment_audit_visuals/tides_audit_mcp_stack.png)
*MCP stack readiness*
![P1-00 dispatch path](../../alignment_audit_visuals/tides_roadmap_p1_dispatch.png)
*P1-00 dispatch path*
![Three endings branch](../../alignment_audit_visuals/tides_roadmap_three_endings.png)
*Three endings branch*
![Boss arena combat](../../alignment_audit_visuals/tides_combat_boss_arena.png)
*Boss arena combat*
![Ink overlay VFX](../../alignment_audit_visuals/tides_combat_ink_overlay.png)
*Ink overlay VFX*
![Combat presentation radar](../../alignment_audit_visuals/tides_audit_combat_presentation.png)
*Combat presentation radar*
![Audio QA radar](../../alignment_audit_visuals/tides_audit_audio_qa.png)
*Audio QA radar*
![Combat presentation path](../../alignment_audit_visuals/tides_roadmap_combat_presentation.png)
*Combat presentation path*
![Audio zones & VO](../../alignment_audit_visuals/tides_roadmap_audio_zones_vo.png)
*Audio zones & VO*
![Visual QA village palette](../../alignment_audit_visuals/tides_visualqa_village_palette.png)
*Visual QA village palette*
![Model QA turntable](../../alignment_audit_visuals/tides_modelqa_turntable.png)
*Model QA turntable*
![Visual QA radar](../../alignment_audit_visuals/tides_audit_visual_qa.png)
*Visual QA radar*
![Flow & model QA radar](../../alignment_audit_visuals/tides_audit_flow_model_qa.png)
*Flow & model QA radar*
![Visual QA pipeline](../../alignment_audit_visuals/tides_roadmap_visual_qa.png)
*Visual QA pipeline*
![Flow QA E2E path](../../alignment_audit_visuals/tides_roadmap_flow_qa_e2e.png)
*Flow QA E2E path*
![Steam capsule key art](../../alignment_audit_visuals/tides_steam_capsule_keyart.png)
*Steam capsule key art*
![RC ship build](../../alignment_audit_visuals/tides_steam_rc_ship_build.png)
*RC ship build*
![Steam ship readiness](../../alignment_audit_visuals/tides_audit_steam_ship.png)
*Steam ship readiness*
![M6 milestone gates](../../alignment_audit_visuals/tides_audit_m6_gates.png)
*M6 milestone gates*
![Steam ship M6 path](../../alignment_audit_visuals/tides_roadmap_steam_ship.png)
*Steam ship M6 path*
![Mega dashboard (all radars)](../../alignment_audit_visuals/tides_mega_dashboard_all_radars.png)
*Mega dashboard (all radars)*

---
Authority: `docs/qa/ALIGNMENT_AUDIT.md` · Re-run: `bash tools/run_alignment_audit.sh`
