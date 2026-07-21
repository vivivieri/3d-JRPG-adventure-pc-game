# Generation brief — `village_well_stone`

**Status:** Phase 1 prop
**Authority:** `ENVIRONMENT_KITS.md` §4, `ruined_village.md`, `qa_catalog.json`
**Phase:** SC-02 save point

## Intent

Old stone well — granite basin + weathered wood rim; **interact highlight** readable; visible from main path without compass.

## Emotional intent (jury + human rubric)

| Field | Value |
|-------|-------|
| Primary mood | Lonely save anchor, village memory |
| Secondary mood | Utility worn by time — not fairy-tale wishing well |
| Audience read | Discoverable save without UI compass |
| Static read (screenshot) | Stone mass readable on path sightline |
| Motion feel (human L6) | Interact prompt feels safe but melancholy |
| Must avoid | Glowing magic well, European fountain, pristine stone |
| Story anchor | SC-02 well save |

## Tool chain

Material Maker stone + Blender → GLB.

**Export:** `game/assets/models/environment/ruined_village/village_well_stone.glb`

## Positive prompts

- Round stone well, moss on north edge, rope optional
- Granite `#6A6A62`, wood rim `#5C4A3A`, rust chain accent `#8B3A2A`
- ~1.2 m rim height — interact at gameplay cam 1.6 m

## Negative prompts

modern metal well, European stone fountain, bright clean stone

## Hard metrics

| Field | Value |
|-------|-------|
| Tris | 500 – 5,000 |
| Marker | `VillageWell` / `SavePoint_well` |

## Acceptance

- [ ] Save interact prompt readable at 3 m
- [ ] Visible from shack–torii path line-of-sight
- [ ] `check_model_technical.py --model village_well_stone` PASS
