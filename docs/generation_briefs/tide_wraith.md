# Generation brief — `tide_wraith`

**Status:** M5 standard enemy
**Authority:** `CHARACTER_BIBLE.md` §6, `qa_catalog.json`
**Phase:** Caves + palace trash mobs

## Intent

Tall dripping spirit — **no legs**, tapers to mist; featureless face; additive drip highlights without Z-fighting.

## Emotional intent (jury + human rubric)

| Field | Value |
|-------|-------|
| Primary mood | Coastal dread, impersonal guilt |
| Secondary mood | Wrongness without gore |
| Audience read | Standard enemy — unsettling not scary-movie |
| Static read (turntable) | Tall taper to mist; faceless smooth head |
| Motion feel (human L6) | Float lunge feels cold and inevitable |
| Must avoid | Zombie gore, skeleton horror, jump-scare monster |
| Story anchor | Caves trash mob — guilt made ambient |

## Tool chain

Meshy → Blender (alpha mist cards at base) → rig → GLB with emission-friendly materials.

**Export:** `game/assets/models/enemies/tide_wraith/tide_wraith.glb`

## Positive prompts

- Tall humanoid upper body, `#3A5A6A` body, drip highlights `#4AE8D8`
- No legs — lower body fades to mist cards (max 4 cards)
- Smooth featureless "face" — unsettling, not zombie gore
- Float idle; lunge attack with arm extension

## Negative prompts

skeleton, zombie gore, European ghost sheet, opaque legs, readable human face, heavy bloom

## Hard metrics

| Field | Value |
|-------|-------|
| Tris | 4,000 – 14,000 |

### Required animations

| Clip | Loop | Duration |
|------|------|----------|
| `idle` | Yes | 2.0–3.0 s float |
| `attack` | No | 0.7–1.0 s lunge |
| `hit` | No | 0.3 s |
| `death` | No | 1.2 s mist dissolve |

## Transparency limits

- Base mist alpha ≤55%; sort priority documented for GDAI
- No overlapping additive planes >3 deep at gameplay cam

## Acceptance

- [ ] No Z-fight in `tidal_caves` lighting
- [ ] `check_animation_whitelist.py --phase m5 --strict` PASS
- [ ] Silhouette distinct from Shore Wraith at 8 m
