# Generation brief — `village_shack_roku`

**Status:** Phase 1 set-piece  
**Authority:** `ENVIRONMENT_KITS.md` §4, `ruined_village.md`, `qa_catalog.json`  
**Phase:** SC-04 Roku shop

## Intent

Half-collapsed diver shack — **door ~2.0 m**, **3 porch steps**; warm interior lantern glow visible from doorway at gameplay cam; Roku emerges from interior trigger.

## Emotional intent (jury + human rubric)

| Field | Value |
|-------|-------|
| Primary mood | Lived-in decay, last refuge |
| Secondary mood | Warm interior glow — fragile comfort |
| Audience read | Roku's domain — working shack not suburban shed |
| Static read (screenshot) | Collapsed roof; lantern glow through door |
| Motion feel (human L6) | Door scale feels human; interior visible from path |
| Must avoid | Clean suburban shed, brick cottage, bright new lumber |
| Story anchor | SC-04 Roku shop |

## Tool chain

Modular kit + Meshy shack hero → ComfyUI wood → GLB.

**Export:** `game/assets/models/environment/ruined_village/village_shack_roku.glb`

## Positive prompts

- Weathered timber `#5C4A3A`, collapsed roof section, fish net on exterior
- Interior warm `#D4A880` glow through door — not pure white
- Japanese coastal shack — not suburban shed

## Negative prompts

European cottage, clean new lumber, brick house, oversized door

## Hard metrics

| Field | Value |
|-------|-------|
| Tris | 3,000 – 15,000 |
| Door height | ~2.0 m |
| Porch steps | **3** |
| Marker | `RokuShack` |

## Acceptance

- [ ] Interior lantern read from path at 6 m
- [ ] Door scale vs Urashima 1.7 m
- [ ] SC-04 emerge trigger tested in GDAI F5
