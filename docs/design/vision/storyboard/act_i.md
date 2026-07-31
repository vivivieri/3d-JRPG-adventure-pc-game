---
id: act-i
type: reference
audience: [narrative, builder, flow]
phase: [1, 2, 3, 4, 5, 6]
status: active
authority: vision
tokens_est: 869
summary: "Storyboard — Act I — The Return"
---
# Storyboard — Act I — The Return

**Hub:** [`STORYBOARD.md`](../STORYBOARD.md)

## Act I — The Return

### SC-00 — Prologue: The Rescue (new)
| Field | Detail |
|-------|--------|
| **Location** | Black / montage — sea, palace silhouette |
| **Camera** | Slow fades; letterbox optional |
| **Summary** | Urashima saves wounded spirit-turtle. Brief Dragon Palace visit. Otohime gives lacquer box. "Three days." |
| **Gameplay** | Non-interactive; skippable after 3s (hold Confirm after first play) |
| **Mood** | Mythic, fateful |
| **Assets** | Spirit-turtle silhouette, box, palace gold flash |
| **Flag** | `prologue_seen` |

### SC-01 — Arrival at the Shore
| Field | Detail |
|-------|--------|
| **Location** | Beach outside ruined village |
| **Camera** | Wide establishing shot → over-shoulder follow |
| **Summary** | Urashima washes ashore, clutching the lacquer box. Narrator line: "I thought it was only three days." **Default: text only.** Optional selective VO: `sc01_urashima_01` (P1 — `docs/design/vision/VO_HIT_LIST.md`) |
| **Gameplay** | Tutorial movement (WASD), approach village gate |
| **Mood** | Lonely, grey sky, distant thunder |
| **Assets** | Beach terrain, driftwood, box prop, ruined gate silhouette |
| **Camera** | See `CINEMATICS.md` SC-01 — wide establishing → follow |

### SC-02 — Empty Village
| Field | Detail |
|-------|--------|
| **Location** | Ruined Fishing Village (hub) |
| **Camera** | Slow pan across submerged houses |
| **Summary** | No people. Banners rotting. A child's sandal floats in a puddle. Urashima: "Anyone...?" |
| **Gameplay** | Free exploration; interact with 3 inspect points (banner, sandal, well) |
| **Mood** | Dread, silence broken by wind |
| **Assets** | Modular ruin kit (`village_*`), water puddles, interactable highlights |
| **Camera** | 4s hub pan on first enter (`CINEMATICS.md` SC-02) |

### SC-03 — The Cracked Torii
| Field | Detail |
|-------|--------|
| **Location** | Village shrine |
| **Camera** | Low angle up at broken torii |
| **Summary** | Spirit voice (Yuzu, unseen): "You left. We waited." Urashima recognizes the shrine. |
| **Gameplay** | Dialogue sequence; quest flag `met_yuzu_spirit` |
| **Mood** | Accusatory, spiritual |
| **Assets** | `village_torii_damaged` (hero prop), spirit particle VFX |
| **Camera** | Low angle up torii (`CINEMATICS.md`) |

### SC-04 — Roku's Warning
| Field | Detail |
|-------|--------|
| **Location** | Half-collapsed diver's shack |
| **Camera** | Interior two-shot |
| **Summary** | Old man Roku emerges. "That box isn't a gift. Don't open it." Hints at Tidal Caves path. |
| **Gameplay** | Dialogue + receive map item; unlock cave entrance |
| **Mood** | Urgent, gravelly wisdom |
| **Assets** | `village_shack_roku` interior, Roku model, map UI icon |

### SC-05 — First Blood (Combat Tutorial)
| Field | Detail |
|-------|--------|
| **Location** | Village outskirts path |
| **Camera** | Standard encounter transition (swirl) |
| **Summary** | A **Salt Crab** blocks the path — "even the sea forgets you." |
| **Gameplay** | Tutorial combat: Attack, Skill, Defend; guaranteed win |
| **Mood** | Tense → empowering |
| **Assets** | Salt Crab model + portrait, combat UI, tutorial prompts |
| **Gameplay note** | Limit gauge visible; tutorial optional |

---
