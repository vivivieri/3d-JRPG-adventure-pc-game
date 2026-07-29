# Generation brief — `village_torii_damaged`

**Status:** Phase 1 set-piece (hero jury)
**Authority:** `ENVIRONMENT_KITS.md` §4, `ruined_village.md`, `qa_catalog.json`
**Phase:** SC-03 spirit shrine

## Intent

Cracked shrine torii — **arch ≥4.0 m** (≥2.3× Urashima); splinter pattern + moss base; vista anchor for hub; spirit particles at interact.

## Emotional intent (jury + human rubric)

| Field | Value |
|-------|-------|
| Primary mood | Sacred threshold in decay |
| Secondary mood | Broken festival gate — grief not demolition porn |
| Audience read | Hub vista anchor — direction without compass |
| Static read (turntable) | Cracked beam, moss, splinters; dominates skyline |
| Motion feel (human L6) | Spirit particles at interact feel solemn |
| Must avoid | Pristine vermillion torii, theme-park gate, European arch |
| Story anchor | SC-03 Yuzu spirit shrine |

## Tool chain

Meshy/Blender → ComfyUI wood + moss → `palette_remap.py --zone ruined_village` → GLB.

**Export:** `game/assets/models/environment/ruined_village/village_torii_damaged.glb`

## Positive prompts

- Weathered cedar torii, cracked crossbeam, splintered wood `#5C4A3A`, moss `#3D5C4A`
- Japanese shrine gate — not Chinese paifang, not European arch
- Base stone pad pairs with `village_shrine_pad`

## Negative prompts

pristine red torii, bright vermillion, European stone arch, low-poly greybox

## Hard metrics

| Field | Value |
|-------|-------|
| Tris | 4,000 – 25,000 |
| Arch height | ≥ 4.0 m |

## Placement

- Marker: `ToriiShrine` — do not move
- Golden shot: torii interact at gameplay cam in `ruined_village`

## Acceptance

- [ ] Silhouette dominates north path vista
- [ ] `L2_model_jury` PASS
- [ ] Scale vs Urashima walk-through screenshot
