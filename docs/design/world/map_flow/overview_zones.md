---
id: overview-zones
type: reference
audience: [architect, builder, narrative]
status: active
authority: world
tokens_est: 467
summary: "Overview + zones + connections"
---
# World Map & Flow — Overview + zones + connections

**Hub:** [`WORLD_MAP_AND_FLOW.md`](../WORLD_MAP_AND_FLOW.md)

## 1. World overview

Single continuous coastal region — no world map screen v1. Player walks between zones via authored transitions.

```
                    [dragon_palace_gate]
                            ↑
                     wraith_pearl gate
                            ↑
    [beach_shore] ←→ [ruined_village] → [tidal_caves]
         SC-01          hub SC-02–05        SC-06–11
```

---


## 2. Zone reference

| Zone ID | Display name | Act | Scenes | Default BGM |
|---------|--------------|-----|--------|-------------|
| `beach_shore` | Shore of Return | I | SC-01 | `bgm_village` |
| `ruined_village` | Ruined Fishing Village | I | SC-02–05 | `bgm_village` |
| `tidal_caves` | Tidal Caves | II | SC-06–11 | `bgm_caves` |
| `dragon_palace_gate` | Dragon Palace Gate | II–III | SC-12–16 | `bgm_palace` |
| `ending_rewind` | Restored Village | End | SC-17a | `bgm_ending_rewind` |
| `ending_anchor` | Dawn Shore | End | SC-17b | `bgm_ending_anchor` |
| `ending_drift` | Open Sea | End | SC-17c | `bgm_ending_drift` |

---


## 3. Connection table

| From | To | Trigger | Requirement |
|------|-----|---------|-------------|
| `beach_shore` | `ruined_village` | Walk to gate | SC-01 complete |
| `ruined_village` | `tidal_caves` | Cave entrance below cliffs | `cave_entrance_unlocked` (SC-04) |
| `tidal_caves` | `dragon_palace_gate` | Palace gate at cave exit | `wraith_pearl` (key item) + `yuzu_joined` |
| `dragon_palace_gate` | Ending zones | SC-16 choice | `ending_chosen` |

**Backtracking:** Allowed. Village hub revisitable until ending. No fast travel v1.

---
