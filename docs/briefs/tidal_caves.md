# Generation brief — `tidal_caves`

**Status:** Phase 5 dungeon (SC-06–10)
**Authority:** `ENVIRONMENT_KITS.md` §5, `LEVEL_DESIGN.md` §4, `RENDERING_GUIDE.md`

## Intent

Bioluminescent guilt caves — **no sky**; cyan emissive algae primary fill; ceiling **≥3 m**; puzzle water heights readable; Shore Wraith arena at SC-09.

## Emotional intent (jury + human rubric)

| Field | Value |
|-------|-------|
| Primary mood | Wonder mixed with wrongness |
| Secondary mood | Biolume beauty hiding guilt |
| Audience read | Dungeon — awe then dread at boss |
| Static read (screenshot) | Cyan algae on wet stone; no sky; readable tunnels |
| Motion feel (human L6) | Puzzle water shifts feel deliberate; boss arena oppressive |
| Must avoid | Horror gore dungeon, generic grey cave, lava, torch medieval |
| Story anchor | SC-06–09 caves arc |

## Tool chain

ComfyUI wet stone + emissive algae → modular tunnel kit → GDAI assembly + point lights.

## Palette

| Role | Hex |
|------|-----|
| Deep teal | `#1A4A5A` |
| Biolume | `#4AE8D8` |
| Wet stone | `#3A3A45` |
| Fog | `#0A141C` density 0.028 |

## Composition contract

| Field | Target |
|-------|--------|
| `min_path_width_m` | 2.0 |
| `min_ceiling_height_m` | 3.0 |
| `max_emissive_intensity` | 0.4 (avoid bloom clip) |
| `vista_anchor` | `cave_shrine_alcove` (SC-10) |
| `golden_screenshot` | `artifacts/screenshots/phase5_tidal_caves_gameplay.png` |

## Water puzzle (SC-07)

| State | Water Y | Access |
|-------|---------|--------|
| Low | −0.5 m | Switch A, dry chest |
| High | +0.8 m | Latch platform |

**Markers:** `WaterPuzzle`, `DeepPoolEncounter`, `ShoreWraithBoss`

## Hero set-pieces (priority)

`cave_entrance_arch` → `cave_flood_basin` → `cave_deep_pool` → `cave_boss_arena_ring` → `cave_shrine_alcove`

## Lighting rules

- Emissive algae primary — **no pure white** point lights
- Glow on algae enabled; restrained intensity
- Puzzle switch sightlines from tunnel entry

## Negative prompts

generic grey cave, torch medieval dungeon, lava, bright white lights, stalactite clutter blocking path

## Acceptance

- [ ] Ceiling ≥3 m on main routes
- [ ] Cyan emissive does not clip to white in screenshot
- [ ] Puzzle water states visible without UI
- [ ] Boss arena + shrine alcove golden shots
