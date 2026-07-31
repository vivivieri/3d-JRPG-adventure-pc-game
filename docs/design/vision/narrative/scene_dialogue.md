---
id: scene-dialogue
type: reference
audience: [narrative]
phase: [3, 6]
status: active
authority: narrative
tokens_est: 592
---
# Narrative — Scene dialogue

**Hub:** [`NARRATIVE_WRITING_GUIDE.md`](../NARRATIVE_WRITING_GUIDE.md)

## 4. Scene dialogue rules

### Line count limits

| Scene type | Max lines | Max chars/line (EN) |
|------------|-----------|---------------------|
| Field greeting | 4 | 90 |
| Inspect / lore | 2 | 100 |
| Boss intro | 3 | 80 |
| Boss mid-fight | 1 per phase | 60 |
| Revelation (SC-13) | 8 | 100 |
| Choice (SC-16) | UI copy only — see `ENDING_DESIGN.md` |
| Ending cinematic | 6 | 120 |

**Combat:** Minimize dialogue during fights except phase banners and SC-15 choice gate.

### Intentional silence — SC-07

**SC-07 has no dialogue block in `chapter_01.json` — by design.**

| Field | Detail |
|-------|--------|
| **Purpose** | Pacing breather after SC-06; quiet problem-solving before SC-08 horror |
| **Mood** | *Quiet problem-solving* (`STORYBOARD.md`, `PACING_CHART.md`) |
| **Story** | Water raises/lowers; player learns tide logic without words |
| **Feedback** | Switch SFX, water animation, quest log hint after 3 min (`PUZZLE_DESIGN.md`) |
| **Do not add** | Urashima muttering, Roku radio bark before hint timer |

Other silent beats:

| Scene | Silence type |
|-------|--------------|
| SC-02 explore | Minimal lines at entry; inspectables carry weight |
| SC-16 choice | Urashima **silent** — player projects (`ENDING_DESIGN.md`) |
| SC-17 endings | 1–2 lines max before credits |

---


## 5. Scene writing reference (from storyboard)

| Scene | Dialogue focus | Data ID |
|-------|----------------|---------|
| SC-00 | Mythic setup; box origin | `SC-00` |
| SC-01 | Disorientation; "three days" | `SC-01` |
| SC-02 | Emptiness; 3 inspect sub-scenes | `SC-02`, `SC-02-BANNER`, etc. |
| SC-03 | Yuzu accusation | `SC-03` |
| SC-04 | Roku warning + map | `SC-04` |
| SC-05 | Crab prelude | `SC-05` |
| SC-06 | Cave wonder | `SC-06` |
| SC-07 | **No dialogue** | — |
| SC-08 | Drowned voices (text) | `SC-08` |
| SC-09 | Shore Wraith | `SC-09` |
| SC-10 | Yuzu join | `SC-10` |
| SC-11 | Otohime flashback | `SC-11` |
| SC-12 | Palace gate | `SC-12` |
| SC-13 | Box truth + mirror flavor choice | `SC-13` |
| SC-14 | Sentinel | `SC-14` |
| SC-15 | Tide Keeper | `SC-15` |
| SC-16 | Choice UI only | `SC-16` |
| SC-17a/b/c | Ending lines | `SC-17a`, etc. |

**Inspect vs lore:** Village inspect scenes (`SC-02-*`) deliver immediate dialogue. Separate lore pickups (`game/data/lore/`) deliver journal entries — see `LORE_AND_ENVIRONMENTAL_STORY.md`.

---
