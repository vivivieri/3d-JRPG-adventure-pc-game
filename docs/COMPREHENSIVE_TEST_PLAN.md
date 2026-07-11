# Tides of Urashima — Comprehensive Test Plan

**Version:** 1.0  
**Purpose:** Full test-case catalog, end-to-end walk paths (all endings), layout/item reasonableness rubric, and AI-agent automation pipeline.  
**Status:** Plan only — execute after review.  
**Cross-refs:** `docs/PLAYTEST_SCRIPT.md`, `docs/QA_AND_BUG_PROCESS.md`, `tools/run_playtest_smoke.sh`

---

## 0. Executive summary

### Current implementation level (what tests can prove)

| Layer | Status | Testable today? |
|-------|--------|-----------------|
| Story logic (flags, quests, scenes) | Complete in data + code | Yes — automated |
| Zone flow + interactables | Complete (greybox) | Yes — automated + GUI |
| Dialogue (text, choices) | Working — no portraits | Yes |
| Combat (mechanics) | Working — text UI only | Yes — logic, not visuals |
| Save/load | Working | Yes |
| 3 endings + credits | Working (minimal presentation) | Yes — 3 separate runs |
| Shop, tab menu, level-up, XP | Not implemented | Mark **N/A — expected fail** |
| Party followers (field) | Not implemented | Mark **N/A** |
| BGM/SFX | Not implemented | Video will be **silent** |
| Character/enemy art | Greybox only | Layout rubric only |

### Are we using `godot-interactive-testing`?

**No — not currently.**

| Tool | In repo? | Used for testing? |
|------|----------|-------------------|
| **godot-interactive-testing** (MCP skill: launch, screenshot, click, key, scene tree) | No | Not installed |
| **GDAI MCP** (`gdai-mcp-plugin-godot`) | Yes (dev addon) | Editor assist only — not E2E automation |
| **Custom headless tests** | Yes | `movement_smoke_test`, `capture_runner` |
| **Shell smoke** | Yes | `tools/run_playtest_smoke.sh` |
| **GUI agent** | Ad hoc | Cloud `computerUse` + `RecordScreen` |

**Recommendation:** Adopt **godot-mcp** or **godot-interactive-testing** for deterministic E2E (freeze time, inject input, read `GameManager` state as JSON). Until then, use the tiered plan below.

### Video + sound

| Capture method | Video | Sound |
|----------------|-------|-------|
| `RecordScreen` (cloud GUI) | Yes | **No** — project has zero audio files; ALSA dummy driver in cloud |
| `tools/capture_playthrough_screenshots.sh` | PNG milestones only | No |
| Packaged `.exe` on Windows | Yes (manual) | No until Phase 7 audio |

**Sound in tests:** Defer until `assets/audio/` exists. When added, re-run ending-path videos with `master_volume` checks.

---

## 1. Test tiers (automation pyramid)

```
Tier 0 — Data integrity     (every commit, <30s)   validate_story_data.py, check_dev_environment.sh
Tier 1 — Smoke              (every commit, <1min)  run_playtest_smoke.sh
Tier 2 — System integration (per PR, <5min)        headless scene + combat + save tests
Tier 3 — Milestone capture  (per milestone)        capture_playthrough_screenshots.sh
Tier 4 — Full E2E walk      (per release, ~3h×3)  3 ending playthroughs + video
Tier 5 — Reasonableness     (per zone change)      layout + item rubric (§8)
Tier 6 — Localization       (pre-ship)             en / ja / zh full pass
```

### AI agent dev-cycle gates

| Dev phase | Gate tests |
|-----------|------------|
| Phase 0 — Dev env | Tier 0 |
| Phase 1 — Environment | Tier 1 + Tier 5 (zone load screenshots) |
| Phase 2 — Core systems | Tier 1 + save/load cases |
| Phase 3 — Narrative | Tier 2 dialogue + quest flag cases |
| Phase 4 — Combat | Tier 2 combat cases + boss phase cases |
| Phase 5 — Dungeons | Tier 4 Act I–II path |
| Phase 6 — Endings | Tier 4 all 3 endings |
| Phase 7 — Art/audio | Tier 3 + Tier 4 video + sound checklist |
| Phase 8 — Ship | Tier 0–4 + `check_asset_compliance.sh` + export smoke |

---

## 2. Master test case catalog

### 2.1 Boot & shell (TC-BOOT)

| ID | Test case | Steps | Expected | Auto? |
|----|-----------|-------|----------|-------|
| TC-BOOT-01 | Project boots | Launch `main_menu.tscn` | No crash; title visible | Tier 1 |
| TC-BOOT-02 | Story data valid | `validate_story_data.py` | Exit 0; 23 scenes | Tier 0 |
| TC-BOOT-03 | Dev environment | `check_dev_environment.sh` | Godot 4.3+, paths OK | Tier 0 |
| TC-BOOT-04 | New Game | Click New Game | SC-00 on beach; no soft-lock | Tier 4 |
| TC-BOOT-05 | Continue disabled | Fresh `user://` | Continue greyed out | Tier 2 |
| TC-BOOT-06 | Continue loads | Save then restart | Restores zone + flags | Tier 2 |
| TC-BOOT-07 | Settings graphics | Change Low/Med/High | `SettingsManager` updates | Tier 4 |
| TC-BOOT-08 | Dev Zone Hub | Open hub → each zone | Zone loads without crash | Tier 3 |
| TC-BOOT-09 | Quit | Click Quit | Process exits | Manual |
| TC-BOOT-10 | Windows export | `build/TidesOfUrashima.exe` exists | File >50MB launches | Tier 1 |

### 2.2 Movement & field (TC-FIELD)

| ID | Test case | Steps | Expected | Auto? |
|----|-----------|-------|----------|-------|
| TC-FIELD-01 | WASD movement | After SC-01, hold W 2s | Player moves >0.3 units | Tier 1 |
| TC-FIELD-02 | Mouse look | Move mouse captured | Camera orbits | Tier 4 |
| TC-FIELD-03 | Interact prompt | Walk to well | `[E] Inspect well` shows | Tier 4 |
| TC-FIELD-04 | Interact trigger | Press E at well | SC-02-WELL dialogue | Tier 4 |
| TC-FIELD-05 | Zone transition | Beach → ToVillage | `ruined_village` loads | Tier 4 |
| TC-FIELD-06 | Blocked during dialogue | During SC-00 | Player cannot move | Tier 2 |
| TC-FIELD-07 | Unblock after dialogue | SC-00 ends | Player enabled; mouse captured | Tier 2 |
| TC-FIELD-08 | Sprint | Hold Shift + W | Faster movement | Tier 4 |
| TC-FIELD-09 | Gravity / floor | Spawn on beach | Player stands on ground | Tier 1 |
| TC-FIELD-10 | Return path | Caves → ToVillage | Spawns at CaveEntrance | Tier 4 |

### 2.3 Dialogue & narrative (TC-DLG)

| ID | Scene | Trigger | Flags set | Auto? |
|----|-------|---------|-----------|-------|
| TC-DLG-00 | SC-00 | New Game prologue | `prologue_seen` | Tier 4 |
| TC-DLG-01 | SC-01 | Beach WorldSpawn auto | `game_started`, `tutorial_movement_done` | Tier 4 |
| TC-DLG-02 | SC-02 | Village WorldSpawn auto | `village_arrival_seen` | Tier 4 |
| TC-DLG-02B | SC-02-BANNER | InspectBanner | `inspected_banner` | Tier 4 |
| TC-DLG-02S | SC-02-SANDAL | InspectSandal | `inspected_sandal` | Tier 4 |
| TC-DLG-02W | SC-02-WELL | VillageWell | `inspected_well` | Tier 4 |
| TC-DLG-03 | SC-03 | ToriiShrine | `met_yuzu_spirit` | Tier 4 |
| TC-DLG-04 | SC-04 | RokuShack | `met_roku`, `cave_entrance_unlocked`, `cave_map` | Tier 4 |
| TC-DLG-06 | SC-06 | Caves WorldSpawn auto | `caves_entered` | Tier 4 |
| TC-DLG-08 | SC-08 | DeepPoolEncounter | `deep_pool_seen` (pre-fight) | Tier 4 |
| TC-DLG-09 | SC-09 | ShoreWraithBoss | Pre-boss dialogue | Tier 4 |
| TC-DLG-10 | SC-10 | ShrineAlcove | `yuzu_joined`; party +Yuzu | Tier 4 |
| TC-DLG-11 | SC-11 | PalaceVision | `saw_palace_vision` | Tier 4 |
| TC-DLG-12 | SC-12 | Palace WorldSpawn auto | `gate_reached`, `roku_combat_active` | Tier 4 |
| TC-DLG-13 | SC-13 | MirrorChamber | `knows_box_truth` | Tier 4 |
| TC-DLG-14 | SC-14 | PalaceSentinel | Pre-boss dialogue | Tier 4 |
| TC-DLG-15 | SC-15 | TideKeeperBoss | Pre-boss dialogue | Tier 4 |
| TC-DLG-16 | SC-16 | EndingChoice | `ending_chosen` = rewind/anchor/drift | Tier 4 ×3 |
| TC-DLG-17A | SC-17a | ending_rewind spawn | `game_completed` | Tier 4 |
| TC-DLG-17B | SC-17b | ending_anchor spawn | `game_completed` | Tier 4 |
| TC-DLG-17C | SC-17c | ending_drift spawn | `game_completed` | Tier 4 |
| TC-DLG-18 | Typewriter | Any line | Text reveals at CPS | Tier 4 |
| TC-DLG-19 | Choice branch | SC-16 each option | Correct ending zone | Tier 4 ×3 |
| TC-DLG-20 | Portrait display | Any line with portrait | **N/A — not implemented** | — |
| TC-DLG-21 | Localization en | Settings language en | English text | Tier 6 |
| TC-DLG-22 | Localization ja | Language ja | Japanese text | Tier 6 |
| TC-DLG-23 | Localization zh | Language zh | Chinese text | Tier 6 |

### 2.4 Combat (TC-CMB)

| ID | Encounter | Zone | Party | Boss? | Win flags / items | Auto? |
|----|-----------|------|-------|-------|-------------------|-------|
| TC-CMB-01 | enc_sc05_tutorial_crab | ruined_village | Urashima | No | `tutorial_combat_done` | Tier 2 |
| TC-CMB-02 | enc_sc06_cave_crab | tidal_caves | Urashima | No | — | Tier 4 |
| TC-CMB-03 | enc_sc07_optional_crabs | tidal_caves | Urashima | No | Optional | Tier 4 |
| TC-CMB-04 | enc_sc08_deep_pool | tidal_caves | Urashima | No | `deep_pool_seen` | Tier 4 |
| TC-CMB-05 | enc_sc09_shore_wraith | tidal_caves | Urashima | Yes | `shore_wraith_defeated`, `wraith_pearl` | Tier 4 |
| TC-CMB-06 | enc_sc12_palace_wraiths | dragon_palace_gate | Urashima+Yuzu+Roku | No | — | Tier 4 |
| TC-CMB-07 | enc_sc14_sentinel | dragon_palace_gate | Full party | Yes | `sentinel_defeated`, `palace_edge` | Tier 4 |
| TC-CMB-08 | enc_sc15_tide_keeper | dragon_palace_gate | Full party | Yes | `tide_keeper_defeated`, `tide_keeper_phase3` | Tier 4 |
| TC-CMB-09 | Attack action | Any fight | — | — | Damage applied | Tier 2 |
| TC-CMB-10 | Skill MP cost | Tidal Slash | — | — | MP deducted | Tier 2 |
| TC-CMB-11 | Defend | Any fight | — | — | 50% DR next hit | Tier 2 |
| TC-CMB-12 | Sea Salve item | Has salve in inventory | — | — | Heals 80 HP | Tier 2 |
| TC-CMB-13 | Escape | Non-tutorial | — | — | Flee chance roll | Tier 4 |
| TC-CMB-14 | Limit gauge | Take/deal damage | — | — | Gauge fills; LIMIT button | Tier 2 |
| TC-CMB-15 | Yuzu heal skill | Party has Yuzu | — | — | Purify/Spirit Light usable | Tier 4 |
| TC-CMB-16 | Game Over | All allies dead | — | — | Defeat panel; reload behavior | Tier 4 |
| TC-CMB-17 | Intent display | Enemy turn | — | — | `[claw_snap]` etc. in label | Tier 2 |
| TC-CMB-18 | Boss phases | Tide Keeper | — | — | Phase flags at HP thresholds | Tier 2 |
| TC-CMB-19 | XP applied | Win fight | — | — | **N/A — XP not saved** | — |
| TC-CMB-20 | Level up | Gain XP | — | — | **N/A — not implemented** | — |

### 2.5 Items & economy (TC-ITEM)

| ID | Item | How obtained | Verify | Status |
|----|------|--------------|--------|--------|
| TC-ITEM-01 | `lacquer_box` | New Game key item | In `key_items` | Tier 2 |
| TC-ITEM-02 | `cave_map` | SC-04 / Roku | Key item; unlocks cave zone | Tier 4 |
| TC-ITEM-03 | `sea_salve` ×2 | New Game inventory | Usable in combat | Tier 2 |
| TC-ITEM-04 | `tide_cut_saber` | Water puzzle solve | Equipment; ATK+7 | Tier 4 |
| TC-ITEM-05 | `wraith_pearl` | Shore Wraith win | Required for palace gate | Tier 4 |
| TC-ITEM-06 | `palace_edge` | Sentinel win | Key item grant | Tier 4 |
| TC-ITEM-07 | `spirit_shard` | Optional drop | 30% from tide wraith | Tier 4 |
| TC-ITEM-08 | `fisher_katana` | New Game equip | ATK+4 in stats | Tier 2 |
| TC-ITEM-09 | `worn_haori` | New Game equip | DEF+2 in stats | Tier 2 |
| TC-ITEM-10 | Buy salve at shop | Roku shop | **N/A — shop UI missing** | — |
| TC-ITEM-11 | Gold spend | Any purchase | **N/A — shop missing** | — |
| TC-ITEM-12 | Inventory screen | Tab menu | **N/A — not implemented** | — |
| TC-ITEM-13 | Equip swap | Tab menu | **N/A — not implemented** | — |

### 2.6 Quests (TC-QUEST)

| ID | Quest | Stage completion | Auto? |
|----|-------|------------------|-------|
| TC-QUEST-01 | the_return | banner + sandal + well inspected | Tier 4 |
| TC-QUEST-02 | the_return | meet_roku after SC-04 | Tier 4 |
| TC-QUEST-03 | echoes_at_torii | met_yuzu_spirit | Tier 4 |
| TC-QUEST-04 | echoes_at_torii | caves_entered | Tier 4 |
| TC-QUEST-05 | echoes_at_torii | water_puzzle_solved | Tier 4 |
| TC-QUEST-06 | echoes_at_torii | shore_wraith_defeated | Tier 4 |
| TC-QUEST-07 | depths_of_guilt | yuzu_joined | Tier 4 |
| TC-QUEST-08 | depths_of_guilt | saw_palace_vision | Tier 4 |
| TC-QUEST-09 | depths_of_guilt | gate_reached | Tier 4 |
| TC-QUEST-10 | palace_gate | knows_box_truth | Tier 4 |
| TC-QUEST-11 | palace_gate | sentinel_defeated | Tier 4 |
| TC-QUEST-12 | the_tide_answer | tide_keeper_phase3 | Tier 4 |
| TC-QUEST-13 | the_tide_answer | ending_chosen | Tier 4 |
| TC-QUEST-14 | the_tide_answer | game_completed | Tier 4 |
| TC-QUEST-15 | HUD tracker | Active quest | Corner text updates per stage | Tier 4 |

### 2.7 Puzzles & lore (TC-PUZ / TC-LORE)

| ID | Test case | Steps | Expected | Auto? |
|----|-----------|-------|----------|-------|
| TC-PUZ-01 | Water puzzle open | Interact WaterPuzzle | Overlay with Lower/Raise/Try latch | Tier 4 |
| TC-PUZ-02 | Water puzzle solve | Level = 2, Try latch | `water_puzzle_solved`, saber granted | Tier 2 |
| TC-PUZ-03 | Water puzzle fail | Wrong level | No solve | Tier 2 |
| TC-PUZ-04 | Puzzle blocks field | During puzzle | Player blocked | Tier 4 |
| TC-LORE-01 | fishing_ledger | ruined_village [4.5,0,1.5] | Popup + collected | Tier 4 |
| TC-LORE-02 | festival_banner | village | Popup + collected | Tier 4 |
| TC-LORE-03 | yuzu_prayer | village | Popup + collected | Tier 4 |
| TC-LORE-04 | roku_dive_log | village | Popup + collected | Tier 4 |
| TC-LORE-05 | cave_inscription | caves | Popup + collected | Tier 4 |
| TC-LORE-06 | sailor_charm | caves | Popup + collected | Tier 4 |
| TC-LORE-07 | palace_seal | palace | Popup + collected | Tier 4 |
| TC-LORE-08 | otohime_letter | palace | Popup + collected | Tier 4 |
| TC-LORE-09 | Journal UI | 4+ collected | **N/A — no journal screen** | — |

### 2.8 Save / load (TC-SAVE)

| ID | Test case | Expected | Auto? |
|----|-----------|----------|-------|
| TC-SAVE-01 | Manual save at well | `slot1.json` written; toast | Tier 2 |
| TC-SAVE-02 | Load mid Act I | Flags + zone restored | Tier 2 |
| TC-SAVE-03 | Load mid Act II | Party, pearl, puzzle flags | Tier 4 |
| TC-SAVE-04 | Load before boss | HP/MP preserved | Tier 4 |
| TC-SAVE-05 | playtime_sec | Increments in field | Tier 2 |
| TC-SAVE-06 | completed_scenes | Persisted | Tier 2 |
| TC-SAVE-07 | Game Over reload | **Verify spec** — may be partial | Tier 4 |

### 2.9 Endings (TC-END) — requires 3 full runs

| ID | Choice (SC-16) | Zone | Scene | Credits? |
|----|----------------|------|-------|------------|
| TC-END-01 | Open the box → rewind | ending_rewind | SC-17a | Yes |
| TC-END-02 | Break the box → anchor | ending_anchor | SC-17b | Yes |
| TC-END-03 | Walk into the tide → drift | ending_drift | SC-17c | Yes |
| TC-END-04 | Credits → title | Press any key | Returns main_menu | Tier 4 |
| TC-END-05 | Steam achievement | game_completed | **Scaffold only** | — |
| TC-END-06 | Ending gallery | Title screen | **N/A — not implemented** | — |

### 2.10 Regression / negative (TC-REG)

| ID | Test case | Expected |
|----|-----------|----------|
| TC-REG-01 | Cave without map flag | CaveEntrance not interactable |
| TC-REG-02 | Palace without pearl | ToPalace blocked |
| TC-REG-03 | SC-10 before wraith dead | ShrineAlcove blocked |
| TC-REG-04 | Ending before phase3 | EndingChoice blocked |
| TC-REG-05 | Tutorial crab repeat | Hidden after `tutorial_combat_done` |
| TC-REG-06 | Double dialogue | Second play ignored (warning) |
| TC-REG-07 | Soft-lock scan | No input accepted 60s post-dialogue |

---

## 3. End-to-end walk paths

### 3.1 Golden path (shared spine — all endings)

```
MAIN MENU
  └─ New Game
       └─ beach_shore [SC-00 prologue → SC-01]
            └─ [E] Path to village → ruined_village [SC-02]
                 ├─ [E] Inspect banner      → SC-02-BANNER
                 ├─ [E] Inspect sandal      → SC-02-SANDAL
                 ├─ [E] Inspect well        → SC-02-WELL
                 ├─ [E] Save at well        → SAVE
                 ├─ [E] Approach torii      → SC-03
                 ├─ [E] Enter shack         → SC-04 (+ cave_map)
                 ├─ [E] Fight Salt Crab     → SC-05 COMBAT
                 └─ [E] Enter caves         → tidal_caves [SC-06]
                      ├─ [E] Salt Crab (entrance)     → optional fight
                      ├─ [E] Water gate               → PUZZLE → tide_cut_saber
                      ├─ [E] Optional crabs           → optional
                      ├─ [E] Deep pool                → SC-08 → 2× Tide Wraith
                      ├─ [E] Shore Wraith             → SC-09 → BOSS → wraith_pearl
                      ├─ [E] Shrine alcove            → SC-10 → Yuzu joins
                      ├─ [E] Palace vision            → SC-11
                      └─ [E] To palace gate           → dragon_palace_gate [SC-12]
                           ├─ [E] Palace wraiths      → 2× Tide Wraith (full party)
                           ├─ [E] Mirror chamber       → SC-13
                           ├─ [E] Palace Sentinel      → SC-14 → BOSS
                           ├─ [E] Tide Keeper          → SC-15 → BOSS (3 phases)
                           └─ [E] Face the tide        → SC-16 CHOICE
                                ├─ Path A: Open the box
                                ├─ Path B: Break the box
                                └─ Path C: Walk into the tide
```

### 3.2 Ending path A — Rewind

```
SC-16 → "Open the box" (ending_chosen=rewind)
  → ending_rewind [SC-17a auto]
       → credits.tscn
            → main_menu (any key)
```

**Video chapter markers:** Menu → Act I village → Cave puzzle → Shore Wraith → Yuzu join → Palace → Sentinel → Tide Keeper → Choice → Rewind ending → Credits

### 3.3 Ending path B — Anchor

```
SC-16 → "Break the box" (ending_chosen=anchor)
  → ending_anchor [SC-17b auto]
       → credits → main_menu
```

### 3.4 Ending path C — Drift

```
SC-16 → "Walk into the tide" (ending_chosen=drift)
  → ending_drift [SC-17c auto]
       → credits → main_menu
```

### 3.5 Optional branches (any ending run)

- Read all 8 lore markers (see TC-LORE-01–08)
- Optional crab pack (FloodedChamberCrabs)
- Return village ↔ caves via ToVillage
- Dev Zone Hub direct zone jump (dev only)

### 3.6 Estimated duration

| Path | Target time | Video target |
|------|-------------|--------------|
| Single ending (speed) | 45–90 min | 15–20 min highlight reel |
| Single ending (thorough + lore) | 2–3 h | 30–45 min |
| All 3 endings | 6–9 h | 3 videos or 1 compilation |

---

## 4. Video recording plan

### 4.1 When to record (after plan approval)

| Video ID | Content | Record |
|----------|---------|--------|
| VID-01 | Act I: New Game → cave entrance | `RecordScreen` + GUI play |
| VID-02 | Act II: Caves → Shore Wraith → Yuzu | Same |
| VID-03 | Act III: Palace → Tide Keeper → SC-16 | Same |
| VID-04 | Ending A (Rewind) + credits | Dedicated run |
| VID-05 | Ending B (Anchor) + credits | Dedicated run |
| VID-06 | Ending C (Drift) + credits | Dedicated run |
| VID-07 | Combat showcase (all bosses) | Dev hub or scripted |

### 4.2 Recording checklist

- [ ] Delete `user://saves/` for clean New Game
- [ ] Window focused; click game after each dialogue
- [ ] 1920×1080; `bash tools/run_game.sh`
- [ ] Note commit SHA in video title card
- [ ] **Sound:** expect silence until Phase 7; document as known limitation

### 4.3 Automated capture (no video)

```bash
bash tools/capture_playthrough_screenshots.sh   # 9 PNG milestones
bash tools/run_playtest_smoke.sh                # 9 automated checks
```

---

## 5. Layout & item reasonableness rubric

**Question:** Are environments, item placement, and walk paths *reasonable* for a greybox vertical slice?

Score each **1–5** (1=broken, 3=acceptable greybox, 5=ship-ready).

### 5.1 Zone layout

| Zone | Markers vs geometry | Walk distance | Gating logic | Notes |
|------|---------------------|---------------|--------------|-------|
| beach_shore | Spawn near water; torii silhouette north | Short to ToVillage (z+30) | None | Reasonable |
| ruined_village | Well/torii/shack near props | Hub ≤70m | Cave needs SC-04 | Banner/sandal near puddle — good |
| tidal_caves | Linear tunnel −z | Long corridor | Puzzle before deep pool | Boss at deep pool = same marker as SC-08 — **acceptable but cramped** |
| dragon_palace_gate | Gate → bridge → mirror → throne | Linear | Pearl required | Sentinel/Keeper/Choice share throne area — OK for greybox |
| ending_* | Empty plateau | N/A | Auto dialogue | Minimal — expected pre-art |

### 5.2 Item reasonableness

| Item | Story timing | Placement logic | Verdict |
|------|--------------|-----------------|---------|
| lacquer_box | Prologue | Starting key item | OK |
| cave_map | After Roku | Unlocks cave transition | OK |
| tide_cut_saber | After puzzle | SC-07 grant | OK — puzzle UI abstract |
| wraith_pearl | After Shore Wraith | Gates palace | OK |
| sea_salve ×2 | Start | Combat usable | OK — no shop to buy more |

### 5.3 Known unreasonable / missing (document, don't fail greybox)

- No visible NPCs at Torii/Roku — dialogue at empty markers
- Party members invisible in field after join
- Lore markers invisible (no prop meshes at positions)
- Shop in playtest script but not in game
- XP/level-up in data but not in UI

---

## 6. Proposed AI-agent automation pipeline

### 6.1 Target architecture

```
┌─────────────────────────────────────────────────────────┐
│  Cloud Agent (Cursor)                                    │
│  ├─ Tier 0–1: shell scripts (every commit)              │
│  ├─ Tier 2: Godot headless GDScript tests               │
│  ├─ Tier 3: capture_playthrough_screenshots.sh          │
│  └─ Tier 4: godot-mcp interactive E2E (TO ADOPT)         │
│       ├─ godot_game_time freeze                         │
│       ├─ godot_input (WASD, E, Space)                   │
│       ├─ godot_runtime_state (GameManager flags)        │
│       └─ game_screenshot / RecordScreen                 │
└─────────────────────────────────────────────────────────┘
```

### 6.2 Implementation backlog (for full automation)

| # | Task | Enables |
|---|------|---------|
| A1 | Install **godot-mcp** or **godot-interactive-testing** MCP | Deterministic GUI E2E |
| A2 | Add `GameManager.get_debug_snapshot()` → JSON | State assertions |
| A3 | Add `game/tests/e2e_golden_path.gd` | Autopilot golden path |
| A4 | Add `game/tests/e2e_ending_{rewind,anchor,drift}.gd` | 3 ending tests |
| A5 | Add `tools/run_e2e_suite.sh` | CI agent gate |
| A6 | Add `GameManager.add_xp()` + level-up | TC-CMB-19/20 |
| A7 | Add shop UI | TC-ITEM-10/11 |
| A8 | Add `assets/audio/` + AudioManager | Video with sound |
| A9 | `tools/record_playthrough.sh` | ffmpeg + RecordScreen wrapper |

### 6.3 Agent loop (per feature PR)

1. Read task / milestone from `IMPLEMENTATION_PLAN.md`
2. Implement feature
3. Run Tier 0 + Tier 1 (must pass)
4. Run relevant TC-* subset
5. Capture screenshots or video for PR proof
6. Update this doc if new test cases added
7. File bugs with `QA_AND_BUG_PROCESS.md` template

---

## 7. Test execution schedule (recommended)

| When | Run |
|------|-----|
| Every agent commit | Tier 0 + Tier 1 |
| Movement/dialogue/combat PR | Tier 2 relevant TC-* |
| Milestone demo | Tier 3 screenshots |
| Pre-merge to main | Tier 4 one ending minimum |
| Pre-ship | Tier 4 all 3 endings + Tier 6 l10n |
| Phase 7 art | Tier 5 reasonableness + visual diff |

---

## 8. Current vs planned — honest gap list

Features in `PLAYTEST_SCRIPT.md` that **cannot pass today**:

| Playtest step | Gap |
|---------------|-----|
| Buy 1 salve (step 8) | No shop UI |
| Tab menu regression | Not built |
| Title gallery | Not built |
| Achievement unlock | Steam scaffold only |
| Hard mode Sentinel | Not implemented |
| BGM/SFX | No audio files |
| Portraits in dialogue | Not rendered |
| Level up | XP not applied |

---

## 9. Sign-off criteria (ship-ready)

- [ ] Tier 0–1: 100% pass
- [ ] Tier 4: all 3 endings complete without guide
- [ ] TC-REG-07: zero soft-locks
- [ ] Tier 5: all zones ≥3/5 reasonableness
- [ ] Video: 3 ending recordings (sound when audio lands)
- [ ] `check_asset_compliance.sh` pass
- [ ] Playtest script steps 1–24 pass (after gaps closed)

---

*Next step after approval: execute Tier 1 + Tier 3, then schedule Tier 4 three-ending video runs.*
