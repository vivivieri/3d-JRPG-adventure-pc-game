# Tides of Urashima — Storyboard

**Format per scene:** ID, location, camera, dialogue summary, gameplay type, mood, assets needed.

**Total scenes:** 18 (main path)

---

## Act I — The Return

### SC-01 — Arrival at the Shore
| Field | Detail |
|-------|--------|
| **Location** | Beach outside ruined village |
| **Camera** | Wide establishing shot → over-shoulder follow |
| **Summary** | Urashima washes ashore, clutching the lacquer box. Voice-over: "I thought it was three days." |
| **Gameplay** | Tutorial movement (WASD), approach village gate |
| **Mood** | Lonely, grey sky, distant thunder |
| **Assets** | Beach terrain, driftwood, box prop, ruined gate silhouette |

### SC-02 — Empty Village
| Field | Detail |
|-------|--------|
| **Location** | Ruined Fishing Village (hub) |
| **Camera** | Slow pan across submerged houses |
| **Summary** | No people. Banners rotting. A child's sandal floats in a puddle. Urashima: "Anyone...?" |
| **Gameplay** | Free exploration; interact with 3 inspect points (banner, sandal, well) |
| **Mood** | Dread, silence broken by wind |
| **Assets** | Modular ruin kit, water puddles, interactable highlights |

### SC-03 — The Cracked Torii
| Field | Detail |
|-------|--------|
| **Location** | Village shrine |
| **Camera** | Low angle up at broken torii |
| **Summary** | Spirit voice (Yuzu, unseen): "You left. We waited." Urashima recognizes the shrine. |
| **Gameplay** | Dialogue sequence; quest flag `met_yuzu_spirit` |
| **Mood** | Accusatory, spiritual |
| **Assets** | Torii model (damaged), spirit particle VFX |

### SC-04 — Roku's Warning
| Field | Detail |
|-------|--------|
| **Location** | Half-collapsed diver's shack |
| **Camera** | Interior two-shot |
| **Summary** | Old man Roku emerges. "That box isn't a gift. Don't open it." Hints at Tidal Caves path. |
| **Gameplay** | Dialogue + receive map item; unlock cave entrance |
| **Mood** | Urgent, gravelly wisdom |
| **Assets** | Shack interior, Roku character model, map UI icon |

### SC-05 — First Blood (Combat Tutorial)
| Field | Detail |
|-------|--------|
| **Location** | Village outskirts path |
| **Camera** | Standard encounter transition (swirl) |
| **Summary** | A **Salt Crab** blocks the path — "even the sea forgets you." |
| **Gameplay** | Tutorial combat: Attack, Skill, Defend; guaranteed win |
| **Mood** | Tense → empowering |
| **Assets** | Salt Crab enemy, combat UI, tutorial prompts |

---

## Act II — The Depths

### SC-06 — Tidal Caves Entrance
| Field | Detail |
|-------|--------|
| **Location** | Cave mouth below cliffs |
| **Camera** | Tracking shot into darkness |
| **Summary** | Bioluminescent algae. Distant bell sound (palace echo). |
| **Gameplay** | Enter dungeon; lighting shift |
| **Mood** | Wonder tinged with wrongness |
| **Assets** | Cave entrance, algae emissive textures, ambient audio |

### SC-07 — Water Level Puzzle
| Field | Detail |
|-------|--------|
| **Location** | Tidal Caves — flooded chamber |
| **Camera** | Top-down wide for puzzle readability |
| **Summary** | Urashima must raise/lower water to reach an ancient latch. |
| **Gameplay** | Switch puzzle (2 states); optional chest with antidote |
| **Mood** | Quiet problem-solving |
| **Assets** | Water plane animation, switch props, chest |

### SC-08 — Echo of the Drowned
| Field | Detail |
|-------|--------|
| **Location** | Tidal Caves — deep pool |
| **Camera** | Close on water surface reflection |
| **Summary** | Faces appear beneath the water. Voices overlap: "Why didn't you come back?" |
| **Gameplay** | Dialogue + forced encounter (2x Tide Wraith) |
| **Mood** | Horror, guilt |
| **Assets** | Wraith VFX, underwater face decals, echo audio |

### SC-09 — Boss: Shore Wraith
| Field | Detail |
|-------|--------|
| **Location** | Tidal Caves — boss arena |
| **Camera** | Low dramatic angle; boss intro pan |
| **Summary** | Colossal wraith forms from pooled regret. "You chose her over us." |
| **Gameplay** | Boss fight; teaches intent UI and phase change at 50% HP |
| **Mood** | Confrontational, tragic |
| **Assets** | Shore Wraith boss model, arena, boss HP bar |

### SC-10 — Yuzu Joins
| Field | Detail |
|-------|--------|
| **Location** | Tidal Caves — shrine alcove |
| **Camera** | Soft focus; spirit materialize |
| **Summary** | Yuzu appears fully. "I can't rest until the tide is answered." Joins party. |
| **Gameplay** | Party member unlock; skill tutorial (Heal) |
| **Mood** | Melancholy resolve |
| **Assets** | Yuzu model, join fanfare SFX, party UI update |

### SC-11 — Palace Vision (Flashback)
| Field | Detail |
|-------|--------|
| **Location** | Overlay on cave wall (ethereal) |
| **Camera** | Dreamlike slow dolly |
| **Summary** | Otohime: "Stay, and the world will not touch you." Urashima almost agrees. |
| **Gameplay** | Non-interactive cutscene (skippable) |
| **Mood** | Seductive, too perfect |
| **Assets** | Palace gold materials, Otohime silhouette, harp audio |

### SC-12 — Dragon Palace Gate
| Field | Detail |
|-------|--------|
| **Location** | Dungeon 2 entrance — impossible architecture |
| **Camera** | Vertigo tilt up massive gate |
| **Summary** | Gate floats above water. Roku arrives (if not in party, joins here). "This is where time was stolen." |
| **Gameplay** | Party complete; save point; enter dungeon |
| **Mood** | Awe, scale |
| **Assets** | Palace gate kit, skybox shift, Roku join if needed |

---

## Act III — The Tide

### SC-13 — The Truth of the Box
| Field | Detail |
|-------|--------|
| **Location** | Gate interior — mirror chamber |
| **Camera** | Mirror reflection shows young AND old Urashima |
| **Summary** | Roku: "The box holds their years. Open it, they live — you won't." |
| **Gameplay** | Dialogue choice (recorded, not branching yet); quest `knows_box_truth` |
| **Mood** | Heavy revelation |
| **Assets** | Mirror shader, dual character lighting |

### SC-14 — Palace Sentinel
| Field | Detail |
|-------|--------|
| **Location** | Gate — sentinel hall |
| **Camera** | Boss intro |
| **Summary** | Armored guardian: "No mortal leaves with stolen time." |
| **Gameplay** | Miniboss; weak to Spirit element (Yuzu) |
| **Mood** | Epic, disciplined |
| **Assets** | Sentinel armor model, hall pillars |

### SC-15 — Tide Keeper Confrontation
| Field | Detail |
|-------|--------|
| **Location** | Gate — throne of tides |
| **Camera** | Circular arena; camera orbits during phase 2 |
| **Summary** | Tide Keeper: "Paradise is mercy." Urashima: "Mercy that drowns the world isn't mercy." |
| **Gameplay** | Final boss (3 phases); at 10% HP, combat pauses for choice prompt |
| **Mood** | Cathartic, cosmic |
| **Assets** | Tide Keeper boss, tide VFX, phase transition audio |

### SC-16 — The Choice
| Field | Detail |
|-------|--------|
| **Location** | Same arena (time frozen) |
| **Camera** | Close on Urashima's face; UI choice overlay |
| **Summary** | Three options presented with no timer. |
| **Gameplay** | Branching ending selection |
| **Mood** | Stillness |
| **Assets** | Choice UI, box glow intensify |

### SC-17a — Ending: Rewind
| Field | Detail |
|-------|--------|
| **Location** | Village — restored |
| **Camera** | Crane up from festival |
| **Summary** | Village lives again. Urashima's figure dissolves at the edge of the crowd. Yuzu feels a breeze. |
| **Gameplay** | Credits roll |
| **Mood** | Bittersweet |
| **Assets** | Restored village variant, festival lanterns, credits |

### SC-17b — Ending: Anchor
| Field | Detail |
|-------|--------|
| **Location** | Village shore — dawn |
| **Camera** | Wide; small figures rebuilding |
| **Summary** | Spirits fade into the land. Roku plants a new sapling. Urashima stays, older but present. |
| **Gameplay** | Credits roll |
| **Mood** | Hopeful |
| **Assets** | Dawn lighting, sapling prop, rebuilding NPCs (silhouettes) |

### SC-17c — Ending: Drift
| Field | Detail |
|-------|--------|
| **Location** | Open sea |
| **Camera** | Pull back from lone boat |
| **Summary** | Urashima rows toward horizon. Otohime's palace glimmers beneath the waves. Cycle continues. |
| **Gameplay** | Credits roll |
| **Mood** | Tragic, open |
| **Assets** | Boat model, endless sea, palace underwater glimpse |

---

## Scene flow diagram

```mermaid
flowchart LR
    SC01 --> SC02 --> SC03 --> SC04 --> SC05
    SC05 --> SC06 --> SC07 --> SC08 --> SC09
    SC09 --> SC10 --> SC11 --> SC12 --> SC13
    SC13 --> SC14 --> SC15 --> SC16
    SC16 --> SC17a
    SC16 --> SC17b
    SC16 --> SC17c
```

---

## Production priority (for greybox)

1. SC-01, SC-02, SC-05 (movement + first fight)
2. SC-06, SC-09 (dungeon + boss template)
3. SC-15, SC-16 (final boss + choice UI)
4. Remaining scenes as content pass
