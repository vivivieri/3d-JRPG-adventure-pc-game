---
id: p1-02-builder-village
type: how-to
audience: [pm, architect, builder, qa]
phase: [1]
status: active
authority: ops
tokens_est: 587
summary: "P1-02 Builder greybox + QA handoff"
---
# Phase1-Sprint1 — P1-02 Builder greybox + QA handoff

**Hub:** [`Phase1-Sprint1-issues.md`](../Phase1-Sprint1-issues.md)

## P1-02 — Builder: GDAI ruined_village greybox vertical slice

**Title:** `[DEV][P1-02] Phase 1.5–1.7 — GDAI ruined_village.tscn greybox + SC-02 lighting`

**Labels:** `agent/builder`, `gate/L2_scene_primitives`, `gate/L3_gdai_built`

| Field | Value |
|-------|-------|
| Phase | 1 |
| Implementation plan | **1.5** (ruined_village only), **1.6**, **1.7**, **1.9** — task **1.8** (component scenes) deferred to Phase1-Sprint2 |
| Lead agent | **builder** |
| Depends on | P1-00, P1-01 handoff |
| Unblocks | P1-04, P1-05 |

### Acceptance gate IDs

```
L3_gdai_built
L3_gdai_f5              # agent-local — GDAI F5 in editor
L2_scene_primitives
L2_boot_headless        # if run/main_scene points here
L2_feel_smoke           # constants only — no player yet OK
```

### Spec summary

**GDAI MCP only** — create `res://scenes/world/ruined_village.tscn`:

1. Apply Architect handoff (lights, fog, sky, toon materials on greybox).
2. Greybox layout per `docs/design/world/LEVEL_DESIGN.md` §3 (~120×120 m hub): torii north, well/shack mid, pier south, cave entrance marker.
3. Place **markers** from `game/data/qa/zone_composition.json` → `ruined_village.markers` (do not rename).
4. Greybox meshes allowed at Phase 1 gate (`ART_DIRECTION.md` §10) — no Kenney/European kits.
5. F5 verify: 0 errors, 60 FPS target @ 1080p in viewport.
6. Update `game/scenes/.gdai_built` — `verified_f5=true`, scenes touched listed.

**Phase 1 vertical slice checklist** (`ART_DIRECTION.md` §10 Phase 1 gate):

- [ ] Palette matches §1 hex at gameplay camera
- [ ] Filmic/ACES + zone fog (not default grey)
- [ ] Toon ramp on ground/blockout meshes
- [ ] 60 FPS @ 1080p in editor play

### Builder → QA handoff

```markdown

## Handoff to QA

- Commit: `<sha>`
- Scenes touched: `res://scenes/world/ruined_village.tscn`
- `.gdai_built`: verified_f5=true
- Screenshot: `artifacts/screenshots/phase1_ruined_village_wip.png` (optional WIP)
- Main scene: `<set or unset>`
```

### Design refs

- `docs/design/world/LEVEL_DESIGN.md` §3
- `docs/design/world/ENVIRONMENT_KITS.md` §4
- `docs/design/art/ART_DIRECTION.md` §10 (Phase 1 gate)
- `game/data/qa/zone_composition.json` → `ruined_village`

### Definition of done

- [ ] Scene built via GDAI; no hand-edited `.tscn` in Cursor
- [ ] `.gdai_built` updated
- [ ] F5 clean; handoff posted
- [ ] Reassign to `agent/qa`

---
