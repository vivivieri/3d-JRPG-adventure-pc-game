# Generation brief — `roku`

**Status:** M5 · Phase 4 party gate  
**Authority:** `CHARACTER_BIBLE.md` §4, `qa_catalog.json`  
**Phase:** SC-04 shack; field follower SC-12+

## Intent

Bulky old diver — patched canvas suit, harpoon across back; **wide stance**; taunt/guard readable at 6 m; harpoon stowed vs strike states distinct.

## Tool chain

Meshy → Blender (harpoon separate mesh, stowed + drawn variants or single with anim) → Mixamo → GLB → GDAI `village_shack_roku` interior.

**Export:** `game/assets/models/characters/roku/roku.glb`

## Positive prompts

- Patched dive suit `#5C5A48`, rubber seals `#2A2A2A`, patches `#7A6A52`
- Harpoon wood `#4A3A2A`, metal `#6A6A6A` — **strapped across back** when stowed
- Weathered face, white stubble, missing left glove finger
- Bowed legs, wide stance; adult 1:5, ~1.75 m height

## Negative prompts

chibi, sci-fi diver, European knight, clean new suit, floating harpoon, PBR wet rubber

## Hard metrics

| Field | Value |
|-------|-------|
| Tris | 6,000 – 18,000 |
| Rig | `mixamo_humanoid` |

### Required animations

| Clip | Loop | Duration | Notes |
|------|------|----------|-------|
| `idle` | Yes | 2.0–3.0 s | Weight on heels |
| `walk` | Yes | 1.1–1.3 s | Heavy gait |
| `harpoon_strike` | No | **0.8–1.2 s** | Wind-up **≥0.3 s** telegraph |
| `hit` | No | 0.3–0.5 s | |
| `taunt` | No | 1.5–2.0 s | Harpoon planted (P1) |
| `guard` | Yes | — | Crouch behind arms (P1) |

## Mesh states

- **Stowed:** harpoon on back, visible in portrait strap line
- **Strike:** harpoon in hands — no pop; swap or anim-driven

## Acceptance

- [ ] Harpoon readable at 6 m in combat cam
- [ ] `check_animation_whitelist.py --phase m5 --strict` PASS
- [ ] `L2_model_jury` PASS
- [ ] Shack doorway silhouette matches field model
