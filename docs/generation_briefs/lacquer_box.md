# Generation brief — `lacquer_box`

**Status:** P0 hero prop (also on Urashima hip)  
**Authority:** `ITEMS_3D_MODEL_GUIDE.md` §8, `CHARACTER_BIBLE.md` §2, `qa_catalog.json`

## Intent

Edo lacquer box **18×12×8 cm** — gold clasp, red cord; **3 emission material presets** (dormant / awakened / choice); hip attach on Urashima.

## Emotional intent (jury + human rubric)

| Field | Value |
|-------|-------|
| Primary mood | Ominous sacred object, quiet curse |
| Secondary mood | Precious but wrong — not treasure loot |
| Audience read | Story-critical prop — always legible on hip |
| Static read (turntable) | Lacquer mass, gold clasp, worn corners; dormant seam glow |
| Motion feel (human L6) | Emission states sync story beats without blinding bloom |
| Must avoid | Sparkling treasure chest, fantasy loot crate, comedy prop |
| Story anchor | SC-16 choice — box as moral weight |

## Tool chain

Meshy/Blender → 3 material variants or single mesh + shader uniforms → GLB.

**Export:** `game/assets/models/items/lacquer_box/lacquer_box.glb`

## Positive prompts

- Rectangular lacquer box; clasp `#C8A040`; lacquer `#6B1A1A`; cord `#8B2A3A`
- Subtle gold inlay; worn edges; not jewelry-scale

## Negative prompts

treasure chest, European lockbox, glowing entire mesh, PBR mirror lacquer

## Hard metrics

| Field | Value |
|-------|-------|
| Tris | 800 – 4,000 |
| Dimensions | 18 × 12 × 8 cm |

### Emission states

| State | Emission | When |
|-------|----------|------|
| `dormant` | `#8B2A3A` seam @ 15% | Hub, caves |
| `awakened` | Pulse 40–60% + motes | Palace |
| `choice` | Full bloom + UI sync | SC-16 |

## Attach

- Hip offset: ~0.12 m left, 0.08 m forward from pelvis (match `urashima.md`)
- Standalone ground prop: `beach_lacquer_box_prop` simplified 500 tris for SC-01

## Acceptance

- [ ] All 3 states visible in viewport screenshot
- [ ] Box edge in Urashima portrait framing
- [ ] `L2_model_jury` PASS
