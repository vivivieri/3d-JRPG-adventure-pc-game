# Generation brief — `salt_crab`

**Status:** M5 · Phase 4 tutorial enemy
**Authority:** `CHARACTER_BIBLE.md` §6, `qa_catalog.json`
**Phase:** SC-05 pier tutorial (`ruined_village`)

## Intent

Low wide crab — **one oversized claw**; barnacle shell; claw snap telegraph readable at **6 m** for first combat teach.

## Emotional intent (jury + human rubric)

| Field | Value |
|-------|-------|
| Primary mood | Threatening tutorial menace |
| Secondary mood | Coastal wrongness — not cute pet |
| Audience read | First combat teach — readable danger |
| Static read (turntable) | Low wide silhouette; oversized claw dominates |
| Motion feel (human L6) | Claw snap telegraph obvious; hit react sells impact |
| Must avoid | Cartoon cute crab, bright red meme crab, spider horror |
| Story anchor | SC-05 pier tutorial |

## Tool chain

Meshy (creature) → Blender decimate → Mixamo creature rig or custom → GLB.

**Export:** `game/assets/models/enemies/salt_crab/salt_crab.glb`

## Positive prompts

- Stylized coastal crab, low wide silhouette
- Shell `#4A5A52`, rust spots `#8B3A2A`, wet sheen (toon, not PBR)
- One claw **2×** size of other; barnacles on carapace
- Sideways scuttle idle

## Negative prompts

realistic photo crab, chibi, bright red cartoon crab, European lobster, spider legs

## Hard metrics

| Field | Value |
|-------|-------|
| Tris | 3,000 – 12,000 |
| Rig | `mixamo_humanoid` (or approved creature rig) |

### Required animations

| Clip | Loop | Duration | Notes |
|------|------|----------|-------|
| `idle` | Yes | 1.5–2.5 s | Sideways scuttle micro-motion |
| `attack` | No | **0.6–0.9 s** | Claw snap; telegraph ≥0.25 s |
| `hit` | No | 0.3–0.4 s | |
| `death` | No | 1.0–1.5 s | Flip or collapse |

## Combat read

- Intent UI must match claw snap timing
- Arena: pier in `ruined_village` — scale vs Urashima ~0.4 m body height

## Acceptance

- [ ] Attack telegraph visible at 6 m
- [ ] `check_animation_whitelist.py --phase m5 --strict` PASS
- [ ] Tutorial encounter screenshot on pier
