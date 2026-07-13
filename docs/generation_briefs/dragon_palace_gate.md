# Generation brief — `dragon_palace_gate`

**Status:** Phase 6 finale zone (SC-12–16)  
**Authority:** `ENVIRONMENT_KITS.md` §6, `LEVEL_DESIGN.md`, `RENDERING_GUIDE.md`

## Intent

Ryūgū-jō palace void — awe and sterile perfection; **corridor module every 8 m**; void sky `#1A1A3A` **no stars**; gold trim emission capped; Sentinel hall + Tide Keeper throne.

## Emotional intent (jury + human rubric)

| Field | Value |
|-------|-------|
| Primary mood | Awe, sterile perfection vs living world |
| Secondary mood | Void loneliness — not triumphant fantasy castle |
| Audience read | Finale zone — scale and moral coldness |
| Static read (screenshot) | Gold trim restrained; void sky without stars; long corridors |
| Motion feel (human L6) | Vertigo in gate approach; throne arena tragic |
| Must avoid | European castle triumph, starry void sky, neon gold bloom |
| Story anchor | SC-12–16 palace arc |

## Tool chain

ComfyUI marble/lacquer → modular palace kit → hero gates/halls → GDAI + glow tuning.

## Palette

| Role | Hex |
|------|-----|
| Coral gold | `#D4A55A` |
| Palace crimson | `#8B2A3A` |
| Void blue | `#1A1A3A` |
| Directional | `#FFD890` |
| Fog | `#1A1A3A` density 0.012 |

## Composition contract

| Field | Target |
|-------|--------|
| `corridor_module_repeat_m` | 8.0 |
| `min_path_width_m` | 2.5 |
| `void_sky_stars` | **false** |
| `vista_anchor` | `palace_gate_main` |
| `save_shrine_exterior` | Before sentinel hall |
| `golden_screenshot` | `artifacts/screenshots/phase6_dragon_palace_gate_gameplay.png` |

## Hero set-pieces (build order)

1. `palace_gate_main` — SC-12 vertigo  
2. `palace_mirror_chamber` — SC-13 dual rim lights  
3. `palace_sentinel_hall` — SC-14 scale for 12 m sentinel read  
4. `palace_throne_tides` — SC-15–16 arena  
5. `palace_void_sea` — void plane below walkways  

## Critical rules

- **No European castle geometry** — karahafu eaves, lacquer pillars only
- Floating walkways — reverse gravity **cut from v1**
- Mirror chamber: young/old Urashima rim light per `CINEMATICS.md`
- Gold emissive ≤0.4; glow on trim only

## Negative prompts

European castle, Roman columns, stars in void, neon gold, medieval throne room, brick walls

## Acceptance

- [ ] Void sky has no stars (vision jury)
- [ ] Corridor rhythm visible in establishing pan
- [ ] Sentinel hall scale shot with party
- [ ] Throne arena Tide Keeper phase swaps
- [ ] ≤8 materials at gameplay cam
