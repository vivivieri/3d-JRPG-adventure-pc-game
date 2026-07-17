# Tides of Urashima — Tutorial & Onboarding Design

**Version:** 1.0 (Pre-build)  
**Cross-refs:** `docs/vision/STORYBOARD.md`, `docs/ui/UI_UX_FLOW.md`, `docs/world/QUEST_AND_FLAGS.md`

**Design goal:** Teach every system within the first 45 minutes. No manual required. Prompts dismiss permanently once flag set.

---

## 1. Teaching philosophy

| Rule | Detail |
|------|--------|
| One new system per scene | Never stack 3 tutorials at once |
| Diegetic first | Roku / Yuzu explain; minimal meta text |
| Skippable prompts | Confirm dismisses; flag prevents repeat |
| Fail-forward | Tutorial crab cannot kill player |
| Hard mode | Does not disable tutorials on first play |

---

## 2. Prologue — SC-00 (new)

**Duration:** 45–60s (skippable after first play via `prologue_seen`)

| Beat | Visual | Teach |
|------|--------|-------|
| 1 | Black + surf SFX | Tone |
| 2 | Urashima nets wounded spirit-turtle | Story setup (GDD §2) |
| 3 | Brief palace montage (silhouette) | Dragon Palace exists |
| 4 | Otohime hands lacquer box | Box origin |
| 5 | Cut to SC-01 shore | "I thought it was three days." |

**Skip:** Hold Confirm 1s on "Skip prologue" after 3s

---

## 3. Tutorial matrix

| System | Scene | Trigger | Prompt text (EN) | Flag |
|--------|-------|---------|------------------|------|
| **Movement** | SC-01 | Spawn | "WASD to move" | `tutorial_movement_done` |
| **Camera** | SC-01 | After 5s walk | "Right-mouse drag to look · Scroll to zoom" | `tutorial_camera_done` |
| **Interact** | SC-02 | Near banner | "E — Investigate" | `tutorial_interact_done` |
| **Inspect** | SC-02 | 1st inspect | "Examine objects for clues and lore" | — |
| **Save point** | SC-02 | Near well | "Save points — interact to record progress" | `tutorial_save_done` |
| **Dialogue** | SC-03 | Torii scene start | "Space — advance dialogue" | `tutorial_dialogue_done` |
| **Shop** | SC-04 | Roku shack exit | "Roku's cache — buy supplies here (Tab → Shop)" | `tutorial_shop_done` |
| **Attack** | SC-05 | Combat turn 1 | "Attack — basic strike" | part of `tutorial_combat_done` |
| **Skill** | SC-05 | Combat turn 2 | "Skill — costs MP; stronger" | part of `tutorial_combat_done` |
| **Defend** | SC-05 | Combat turn 3 | "Defend — reduce damage this turn" | `tutorial_combat_done` |
| **Intent UI** | SC-09 | Boss turn 2 | "Enemy intent — plan around telegraphed attacks" | `tutorial_intent_done` |
| **Phase change** | SC-09 | Boss 50% HP | "Boss phase — pattern may change" | — |
| **Party heal** | SC-10 | Post-join dialogue (mandatory) | "Yuzu — Spirit Light heals allies" | `tutorial_heal_done` |
| **Limit gauge** | SC-09 or SC-15 | Gauge full | "Limit ready — devastating once-per-fight skill" | `tutorial_limit_done` |
| **Equipment** | SC-07 chest or SC-04 | First item obtained | "Tab → Equipment — arm yourself" | `tutorial_equip_done` |
| **Lore journal** | SC-02 | First lore read | "Tab → Lore — collected memories" | `tutorial_lore_done` |
| **Field menu** | SC-04 | First Tab press | "Tab — menu (items, equipment, quests, lore)" | `tutorial_menu_done` |

**Flag storage:** all `tutorial_*` flags in the table above are registered in
`game/data/story/flags.json` (set by scene spine / encounters; usable in conditions and
quest gates). The save slot's `tutorial_seen[]` array (`SAVE_AND_FAIL_STATES.md` §2) is an
optional **UI dedupe** list (suppress re-showing the same prompt text within a run) — it does
not replace story flags.

---

## 4. Scene-by-scene script

### SC-01 — Movement only
- Lock interact until player reaches gate marker (8m)
- Max 2 prompt lines

### SC-02 — Explore & save
- 3 inspectables required for Q1 but **not** gated with hard block — soft quest pointer on HUD
- Well save: heal to full on first save (one-time treat)

### SC-03 — Dialogue
- No combat; 6–8 lines max before player control

### SC-04 — Shop intro
- Roku gives `cave_map` (key item, flavor) + unlocks cave
- Shop UI opens once automatically; player must close to proceed
- **No combat yet** — crab is after shack exit on path

### SC-05 — Combat tutorial
Scripted 3-turn win:

| Turn | Player forced option | Enemy |
|------|---------------------|-------|
| 1 | Attack only | Pinch (low damage) |
| 2 | Skill (`tidal_slash`) only | Pinch |
| 3 | Defend encouraged; Attack OK | Pinch (blocked) |
| 4+ | Free | Crab HP scripted low → auto win |

Urashima cannot die; HP floor at 1.

### SC-09 — Boss tutorial
- Intent UI highlighted turn 2 (pulse border)
- Solo Urashima — no party menu swap
- See `BOSS_DESIGNS.md` solo HP tune (~320)

### SC-10 — Heal tutorial (mandatory)
- **Required path:** SC-10 dialogue always runs after SC-09; Yuzu demonstrates `spirit_light` in dialogue (sets `tutorial_heal_done`)
- Optional micro-fight vs 1 Tide Wraith (`enc_sc10_optional_wraith`) reinforces heal UI for players who skip prompts

### SC-12 — Full party
- If 3 members: prompt "Protect Yuzu — Spirit beats the Sentinel's lacquer"

---

## 5. Prompt UI spec

- **Position:** Above action bar (field) or below top bar (combat)
- **Style:** Semi-transparent ink panel; white text; no blocking input except forced tutorial turns
- **Duration:** Until action completed or Confirm dismiss
- **i18n:** Keys `TUTORIAL_*` in `translations.csv`

---

## 6. What we deliberately do NOT tutorialize

- Speed initiative order math
- Status effect stacking (see `COMBAT_SYSTEMS.md` — learn by play)
- Hard mode (menu description only)
- Ending choice (SC-16 — no timer, no hint toward "correct" ending)

---

## 7. Replay behavior

| Flag | Where stored | Replay behavior |
|------|--------------|-----------------|
| `prologue_seen` | `profile_meta.json` (cross-run) | Skip prologue offered on every later run |
| `tutorial_*` | run save slot | Suppressed within a run; **reset on New Game** (prompts reshow) |
| `game_completed_once` | `profile_meta.json` (cross-run) | All tutorials auto-skipped on later runs; optional "Hints" in settings |

---

## 8. QA checklist

- [ ] New player reaches SC-05 combat without reading a manual
- [ ] Intent UI understood by 90% playtesters without extra text
- [ ] Shop tutorial does not trap player in UI
- [ ] All tutorial strings exist in en / ja / zh / zh-Hant
- [ ] No tutorial prompt during SC-16 choice
