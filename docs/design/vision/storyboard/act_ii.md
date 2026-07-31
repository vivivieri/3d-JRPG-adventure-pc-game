---
id: act-ii
type: reference
audience: [narrative, builder, flow]
phase: [1, 2, 3, 4, 5, 6]
status: active
authority: vision
tokens_est: 982
summary: "Storyboard — Act II — The Depths"
---
# Storyboard — Act II — The Depths

**Hub:** [`STORYBOARD.md`](../STORYBOARD.md)

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
| **Summary** | Urashima must raise/lower water to reach an ancient latch. **No dialogue — quiet puzzle by design** (`NARRATIVE_WRITING_GUIDE.md` §4). |
| **Gameplay** | Switch puzzle (2 states); LOW-path grants `tide_cut_saber` on puzzle solve (`scenes.json` `grants_items`) |
| **Mood** | Quiet problem-solving |
| **Assets** | Water plane animation, switch props |

### SC-08 — Echo of the Drowned
| Field | Detail |
|-------|--------|
| **Location** | Tidal Caves — deep pool |
| **Camera** | Close on water surface reflection |
| **Cinematic** | 5–8s vignette — faces under water; **not** 15s movie (`CINEMATICS.md` §7 SC-08) |
| **Summary** | Faces appear beneath the water. Voices overlap: "Why didn't you come back?" |
| **Gameplay** | Dialogue + forced encounter (2x Tide Wraith) |
| **Mood** | Horror, guilt |
| **Assets** | Wraith VFX, underwater face decals, echo audio |

### SC-09 — Boss: Shore Wraith
| Field | Detail |
|-------|--------|
| **Location** | Tidal Caves — boss arena |
| **Camera** | Low dramatic angle; boss intro pan |
| **Summary** | Colossal wraith forms from pooled regret. "You chose the palace over us." |
| **Gameplay** | Boss fight; teaches intent UI and phase change at 50% HP |
| **Mood** | Confrontational, tragic |
| **Assets** | Shore Wraith boss model, arena (`cave_boss_arena_ring`), boss HP bar |
| **Gameplay note** | Urashima **solo** fight; Yuzu joins after (SC-10) |
| **Camera** | 5s boss intro (`CINEMATICS.md`) |

### SC-10 — Yuzu Joins
| Field | Detail |
|-------|--------|
| **Location** | Tidal Caves — shrine alcove |
| **Camera** | Soft focus; spirit materialize |
| **Summary** | Yuzu appears fully. "I can't rest until the tide is answered." Joins party. |
| **Gameplay** | Party member unlock; skill tutorial (Heal) |
| **Mood** | Melancholy resolve |
| **Assets** | Yuzu model, join fanfare SFX, party UI update |
| **VFX** | Materialize from torii shards (2s) |

### SC-11 — Palace Vision (Flashback)
| Field | Detail |
|-------|--------|
| **Location** | Overlay on cave wall (ethereal) |
| **Camera** | Dreamlike slow dolly |
| **Summary** | Otohime: "Stay, and the world will not touch you." Urashima almost agrees. |
| **Gameplay** | Non-interactive cutscene (skippable) |
| **Mood** | Seductive, too perfect |
| **Assets** | Palace gold materials, Otohime silhouette/bust, harp audio |
| **Camera** | Letterbox 2.39:1; skippable after 3s |

### SC-12 — Dragon Palace Gate
| Field | Detail |
|-------|--------|
| **Location** | Dungeon 2 entrance — impossible architecture |
| **Camera** | Vertigo tilt up massive gate (`CINEMATICS.md` §7 SC-12) |
| **Cinematic** | 12–15s gate reveal — mid-game hero shot; skippable replay after 3s |
| **Summary** | Gate floats above water. Roku arrives (if not in party, joins here). "This is where time was stolen." |
| **Gameplay** | Party complete; save point; enter dungeon |
| **Mood** | Awe, scale |
| **Assets** | `palace_gate_main` (hero), skybox shift, Roku join if needed |
| **Scope** | No reverse-gravity rooms in v1 — floating walkways only |

---
