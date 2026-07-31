---
id: implementation-phase-1
type: how-to
audience: [pm, architect, builder]
phase: [1]
status: active
authority: workflow
tokens_est: 605
summary: "`bash tools/bootstrap_game_development.sh` — `project.godot`, `EventBus` autoload stub, unit test shell. See `docs/ops/sprints/Phase1-Sprint1-issues.md` §P1-00."
---
# Implementation Plan — Phase 1

**Hub:** [`IMPLEMENTATION_PLAN.md`](../IMPLEMENTATION_PLAN.md)

## Phase 1 — Environment foundation (NEXT)

**Bootstrap (P1-00):** `bash tools/bootstrap_game_development.sh` — `project.godot`, `EventBus` autoload stub, unit test shell. See `docs/ops/sprints/Phase1-Sprint1-issues.md` §P1-00.

**Read first:** `docs/design/world/LEVEL_DESIGN.md` (zone `ruined_village`), `docs/design/art/RENDERING_GUIDE.md`

Build stylized zone rendering before gameplay systems. Follow `docs/design/art/RENDERING_GUIDE.md`.

| # | Task | Docs |
|---|------|------|
| 1.1 | `environments/*.tres` — WorldEnvironment per zone (tonemap, fog, glow) | RENDERING_GUIDE §3–6 |
| 1.2 | `scripts/exploration/zone_visuals.gd` — apply palette, sky, lights at runtime | ENVIRONMENT_KITS §1 |
| 1.3 | `shaders/toon_base.gdshader` — single ramp family | ART_DIRECTION §7 |
| 1.4 | `shaders/water_stylized.gdshader` — foam + gentle displacement | ART_DIRECTION §3.6 |
| 1.5 | Greybox zone scenes: `beach_shore`, `ruined_village`, `tidal_caves`, `dragon_palace_gate` | STORYBOARD, ENVIRONMENT_KITS |
| 1.6 | DirectionalLight3D + fog per zone table | RENDERING_GUIDE §5 |
| 1.7 | ProceduralSky per zone (no HDRI) | RENDERING_GUIDE §4 |
| 1.8 | Component scenes from `LEVEL_DESIGN.md` §1b — wells, doors, triggers via GDAI | CODE_BASE_CLASS_RULES, LEVEL_DESIGN §1b |
| 1.9 | **Vertical slice gate:** SC-02 Ruined Village passes art checklist (**Phase 1 greybox section** of ART_DIRECTION §10; final-art section lands in Phase 7) | ART_DIRECTION §10 |
| 1.10 | **Golden gameplay screenshot** — `ruined_village` path in `zone_composition.json` → `artifacts/screenshots/phase1_ruined_village_gameplay.png` (GDAI capture) | GENERATION_READINESS §X-02, **GR-001** |
| 1.11 | Zone composition smoke (warn) — `bash tools/run_zone_composition_checks.sh` after greybox zones load | `zone_composition.json`, **GR-003** |

**GDAI workflow:** GodotPrompter drafts shaders/`zone_visuals.gd` → GDAI MCP places nodes in `.tscn` → F5 verify. **Acceptance criteria:** `docs/ops/workflow/AI_DEV_WORKFLOW.md` §4 Phase 1.

---

