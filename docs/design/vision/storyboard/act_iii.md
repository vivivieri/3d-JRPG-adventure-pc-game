---
id: act-iii
type: reference
audience: [narrative, builder, flow]
phase: [1, 2, 3, 4, 5, 6]
status: active
authority: vision
tokens_est: 893
summary: "Storyboard — Act III — The Tide"
---
# Storyboard — Act III — The Tide

**Hub:** [`STORYBOARD.md`](../STORYBOARD.md)

## Act III — The Tide

### SC-13 — The Truth of the Box
| Field | Detail |
|-------|--------|
| **Location** | Gate interior — mirror chamber |
| **Camera** | Mirror reflection shows young AND old Urashima |
| **Summary** | Roku: "The box holds their years. Open it, they live — you won't." |
| **Gameplay** | Dialogue choice (recorded, not branching yet); quest `knows_box_truth` |
| **Mood** | Heavy revelation |
| **Assets** | `palace_mirror_chamber`, mirror shader, dual character lighting |
| **Camera** | Young + old Urashima in reflection (`CINEMATICS.md` SC-13) |

### SC-14 — Palace Sentinel
| Field | Detail |
|-------|--------|
| **Location** | Gate — sentinel hall |
| **Camera** | Boss intro |
| **Summary** | Armored guardian: "No mortal leaves with stolen time." |
| **Gameplay** | Miniboss; weak to Spirit element (Yuzu) |
| **Mood** | Epic, disciplined |
| **Assets** | Palace Sentinel model (ryūgū armor), sentinel hall |
| **Gameplay note** | Spirit weakness tutorial for Yuzu |

### SC-15 — Tide Keeper Confrontation
| Field | Detail |
|-------|--------|
| **Location** | Gate — throne of tides |
| **Camera** | Circular arena; camera orbits during phase 2 |
| **Summary** | Tide Keeper: "Paradise is mercy." Urashima: "Mercy that drowns the world isn't mercy." |
| **Gameplay** | Final boss (3 phases); at 10% HP, combat pauses for choice prompt |
| **Mood** | Cathartic, cosmic |
| **Assets** | Tide Keeper boss, tide VFX, phase transition audio |
| **Camera** | 6s intro; slow orbit phase 2 (`CINEMATICS.md`) |

### SC-16 — The Choice
| Field | Detail |
|-------|--------|
| **Location** | Same arena (time frozen) |
| **Camera** | Close on Urashima's face; UI choice overlay |
| **Summary** | Three options presented with no timer. |
| **Gameplay** | Branching ending selection |
| **Mood** | Stillness |
| **Assets** | Choice UI, box glow intensify |
| **Camera** | Close on Urashima; combat frozen (`CINEMATICS.md` SC-16) |

### SC-17a — Ending: Rewind
| Field | Detail |
|-------|--------|
| **Location** | Village — restored variant |
| **Camera** | Crane up from festival (`CINEMATICS.md` — 15s total) |
| **Summary** | Village lives again. Urashima's figure dissolves at the edge of the crowd. Yuzu feels a breeze. |
| **Gameplay** | Credits roll |
| **Mood** | Bittersweet |
| **Assets** | `village_restored_kit`, `village_festival_lantern_row`, `village_crowd_silhouettes` (8–12), credits |

### SC-17b — Ending: Anchor
| Field | Detail |
|-------|--------|
| **Location** | Village shore — dawn |
| **Camera** | Wide rebuild shot → sapling close (`CINEMATICS.md`) |
| **Summary** | Spirits fade into the land. Roku plants a new sapling. Urashima stays, older but present. |
| **Gameplay** | Credits roll |
| **Mood** | Hopeful |
| **Assets** | `shore_dawn_skybox`, `prop_sapling_new`, `rebuilder_figures` (×3), spirit dissolve VFX |

### SC-17c — Ending: Drift
| Field | Detail |
|-------|--------|
| **Location** | Open sea |
| **Camera** | Pull back from lone boat; underwater palace glimpse (`CINEMATICS.md`) |
| **Summary** | Urashima rows toward horizon. Otohime's palace glimmers beneath the waves. Cycle continues. |
| **Gameplay** | Credits roll |
| **Mood** | Tragic, open |
| **Assets** | `boat_urashima`, endless sea plane, `palace_underwater_glimpse` |

---
