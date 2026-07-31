---
id: scenes-ui
type: reference
phase: [2, 3]
audience: [narrative, builder, flow]
status: active
authority: gameplay
tokens_est: 514
summary: "Scene scripts + prompt UI"
---
# Tutorial Design — Scene scripts + prompt UI

**Hub:** [`TUTORIAL_DESIGN.md`](../TUTORIAL_DESIGN.md)

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
