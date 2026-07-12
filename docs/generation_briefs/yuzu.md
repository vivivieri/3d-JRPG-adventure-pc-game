# Generation brief — `yuzu`

**Status:** M5 · Phase 4 party gate  
**Authority:** `CHARACTER_BIBLE.md` §3, `qa_catalog.json`  
**Phase:** Unlocks SC-10 (after Shore Wraith)

## Intent

Shrine maiden spirit — white miko haori, red hakama, fox bell on left braid; **semi-transparent legs** with cyan ground tether; readable heal cast at 6 m combat cam.

## Tool chain

Meshy/Tripo → Blender (spirit alpha split on lower body) → Mixamo → `palette_remap.py` → GLB import → GDAI place in `cave_shrine_alcove` + party follower.

**Export:** `game/assets/models/characters/yuzu/yuzu.glb`

## Positive prompts

- Stylized Japanese miko, aged white haori `#F0ECE4`, hakama `#8B2A3A`, torn right hem
- Twin braids; **kitsune bell** `#D4A55A` on left braid — must read in portrait
- Lower body alpha 40–55%, soft noise scroll; cyan ripple `#4AE8D8` at feet
- Adult 1:5 proportions; small, upright silhouette vs Urashima

## Negative prompts

chibi, fanservice pose, PBR glossy, European nun, bright neon, full opaque legs, missing bell

## Hard metrics

| Field | Value |
|-------|-------|
| Tris | 6,000 – 18,000 |
| Rig | `mixamo_humanoid` |
| Category | `party` |

### Required animations

| Clip | Loop | Duration | Notes |
|------|------|----------|-------|
| `idle` | Yes | 2.0–3.0 s | Hands clasped |
| `walk` | Yes | 1.1–1.3 s | **Float** — slight hover, no footprints |
| `heal_cast` | No | 1.5–2.0 s | Hands raised, light pillar |
| `hit` | No | 0.3–0.5 s | |
| `materialize` | No | **2.0 s** | SC-10 torii shard fade-in |
| `purify_cast` | No | 1.2–1.8 s | Bell shake + wave (P1) |

## Shader / VFX

- Spirit lower body: additive/alpha toon — params in `CHARACTER_BIBLE.md` §3
- Bell attachment bone: verify no clip through hair at 45° cam
- Field follower: 2 m behind Urashima

## Camera read

- Combat: heal pillar + bell silhouette at **6 m**
- Portrait: `768×768`, chest up, bell visible

## Acceptance

- [ ] `check_model_technical.py --model yuzu` PASS
- [ ] `check_animation_whitelist.py --phase m5 --strict` PASS
- [ ] `L2_model_jury` PASS
- [ ] In-zone placement `tidal_caves` shrine alcove screenshot
