---
id: ruined-village
type: reference
audience: [builder, builder_zone, architect]
phase: [1]
status: active
authority: world
tokens_est: 459
summary: "Zone ruined_village"
---
# Level Design — Zone ruined_village

**Hub:** [`LEVEL_DESIGN.md`](../LEVEL_DESIGN.md)

## 3. Zone: `ruined_village` (SC-02–05 hub)

**Scene:** `res://scenes/world/ruined_village.tscn`
**Act:** I · **BGM:** `bgm_village` · **Fog:** heavy `#8B9DAF`

### Blockout

| Metric | Target |
|--------|--------|
| Hub size | ~120m × 120m |
| Vertical | Mostly flat; pier −2m to water |
| First-enter pan | 4s torii silhouette (`CINEMATICS.md` SC-02) |

### Layout

```
        [Torii — SC-03 Yuzu]
              |
    [Banner inspect] — [Festival ground]
              |
    [Well save] — [Shack — Roku SC-04 shop]
              |
         [Pier / SC-05 crab arena]
              |
         [Cave entrance ↓ tidal_caves]
```

### Interactables & triggers

| Node | Scene ID | Sets flag | Requirement |
|------|----------|-----------|-------------|
| `CinematicTrigger_hub_pan` | hook `sc02_hub_pan` | `sc02_hub_pan_seen` | First enter only; SC-02 dialogue sets `village_arrival_seen` |
| `Interactable_SC-02-BANNER` | SC-02-BANNER | `inspected_banner` | — |
| `Interactable_SC-02-SANDAL` | SC-02-SANDAL | `inspected_sandal` | — |
| `SavePoint_well` | SC-02-WELL | `inspected_well` | Manual save + first heal |
| `Interactable_SC-03` | SC-03 | `met_yuzu_spirit` | None (freely reachable) — soft quest arrow appears after 2 inspects (`GAME_FEEL.md`) |
| `Interactable_SC-04` | SC-04 | `met_roku`, `cave_entrance_unlocked` | Grants `cave_map` |
| `EncounterTrigger_enc_sc05_tutorial_crab` | SC-05 | `tutorial_combat_done` | Near pier |
| `ZoneTransition_tidal_caves` | — | `caves_entered` | Requires `cave_entrance_unlocked` |

### Encounters

| Trigger | Encounter ID | Enemy |
|---------|--------------|-------|
| Pier arena | `enc_sc05_tutorial_crab` | Salt Crab (tutorial) |

### Shop

Roku shack — `shop/roku_shop.json`; opens after SC-04.

### Lore placements

See `game/data/lore/lore_placements.json` — banner, well, pier.

---
