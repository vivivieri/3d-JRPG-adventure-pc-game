# Generation brief — `beach_shore`

**Status:** Phase 2 zone (SC-01 prologue)
**Authority:** `ENVIRONMENT_KITS.md` §3, `LEVEL_DESIGN.md` §2, `RENDERING_GUIDE.md`

## Intent

Lonely grey arrival beach — spawn path to ruined gate silhouette; **min path 2 m**; ≤**3 hero props** in spawn sightline; dunes ≤30% of vista.

## Emotional intent (jury + human rubric)

| Field | Value |
|-------|-------|
| Primary mood | Lonely arrival, grey grief |
| Secondary mood | Distant thunder — unease not action |
| Audience read | SC-01 prologue isolation |
| Static read (screenshot) | Pale sand, muted sky, ruined gate silhouette at vista |
| Motion feel (human L6) | Slow walk to village; surf ambient oppressive |
| Must avoid | Tropical paradise, sunny vacation beach, bright blue sky |
| Story anchor | SC-01 after prologue |

## Tool chain

ComfyUI sand textures → sculpted terrain meshes → GDAI `beach_shore.tscn` + `WaterController` hook.

## Palette

| Role | Hex |
|------|-----|
| Pale sand | `#C9B89A` |
| Surf teal | `#1A6A62` |
| Fog | `#8B9DAF` |
| Directional | `#F0E8D0` warm |

## Composition contract

| Field | Target |
|-------|--------|
| `min_path_width_m` | 2.0 |
| `max_hero_props_spawn_sightline` | 3 |
| `dune_vista_max_pct` | 30% |
| `vista_anchor` | `beach_ruined_gate_silhouette` |
| `golden_screenshot` | `artifacts/screenshots/phase1_beach_shore_gameplay.png` |

## Layout

```
[Spawn] ──path──► [Ruined gate silhouette] ──transition──► ruined_village
         driftwood clusters          low cliff left
```

## Hero set-pieces

| ID | Tris | Notes |
|----|------|-------|
| `beach_ruined_gate_silhouette` | ~3k | Distant torii fragment |
| `beach_lacquer_box_prop` | ~500 | Optional SC-01 inspect |
| `beach_shoreline_water` | — | Water plane + foam shader |

## Negative prompts

tropical paradise, sunny blue sky, palm trees, European coast, bright saturated sand

## Acceptance

- [ ] Path 2 m clear spawn → gate
- [ ] ≤3 hero props in first camera frustum
- [ ] `check_screenshot_palette.py --zone beach_shore` PASS
- [ ] Transition to `ruined_village` without greybox
