---
id: controls-tech-ship
type: explanation
phase: [1, 6]
audience: [narrative, pm, architect]
status: active
authority: vision
tokens_est: 894
summary: "Controls, tech, milestones, Steam, i18n, risks"
---
# Game Design Document — Controls, tech, milestones, Steam, i18n, risks

**Hub:** [`GDD.md`](../GDD.md)

## 11. Controls (PC)

| Action | Default |
|--------|---------|
| Move | WASD |
| Interact | E |
| Menu | Tab |
| Confirm | Enter / Space |
| Cancel | Esc |

**Gamepad:** Full main-path playable on Xbox-layout controller (M5 polish). See `docs/design/gameplay/PLAYER_CONTROLS.md` and `docs/design/ui/UI_UX_FLOW.md` §11. No remapping v1.

---


## 12. Technical architecture

```
game/
  scripts/core/       GameManager, SaveSystem, EventBus
  scripts/combat/     TurnManager, Combatant, SkillResolver
  scripts/narrative/  DialogueRunner, QuestTracker
  scripts/exploration/     PlayerController, Interactable, zone triggers
  data/               JSON — skills, enemies, dialogue, quests
  scenes/             Godot scenes (world, combat, UI)
```

**Data-driven design:** All combat and dialogue content in JSON (`game/data/` — no YAML) for fast AI-assisted iteration.

---


## 13. Milestones

**Build order:** `docs/ops/workflow/IMPLEMENTATION_PLAN.md` Phases 0–8 are authoritative. **M5 = art rebuild** (Phase 7) before **M6 = Steam ship** (Phase 8).

| ID | Deliverable | Done when |
|----|-------------|-----------|
| M0 | GDD + storyboard + repo | ✓ This doc |
| M0b | i18n (en / ja / zh / zh-Hant + dialect VO) | ✓ Written data in `game/data/` + `translations.csv`; runtime `LocalizationManager` Phase 2+; VO clips Phase 7 |
| M0c | Pre-build art specs | ✓ CHARACTER_BIBLE, ENVIRONMENT_KITS, BOSS_DESIGNS, ENCOUNTER_TABLE, CINEMATICS |
| M0d | Pre-build game design specs | ✓ QUEST_AND_FLAGS, TUTORIAL, ENDING, COMBAT, UI, etc. |
| M0e | Story data layer (`game/data/`) | ✓ DATA_ARCHITECTURE, validate_story_data.py |
| M1 | Greybox movement + dialogue | Walk village, talk to NPC (Phases 2–3) |
| M2 | Combat vertical slice | 1 fight feels good (Phase 4) |
| M3 | Chapter 1 playable | Tidal Caves complete (Phase 5) |
| M4 | Full story | All 3 endings (Phase 6) |
| M5 | Art rebuild (high-detail Japanese) | Vertical slice SC-02 → full NPR production per ART_DIRECTION v1.1 (Phase 7) |
| M6 | Steam & ship prep | Export, store page, compliance, Windows playtest (Phase 8) |

---


## 14. Steam positioning

- **Tags:** JRPG, Story Rich, Short, Atmospheric, Turn-Based Combat
- **Price band:** $4.99–$9.99 (short narrative game)
- **USP:** "A 2–3 hour emotional folktale — Dark Urashima Tarō"

---


## 15. Localization

Supported languages at launch: **English**, **Japanese**, **Simplified Chinese**, **Traditional Chinese** (粵語 or 國語 VO).

- **Ship data:** `en`, `ja`, `zh`, `zh-Hant` in dialogue, items, lore, quests, shop JSON + `game/locale/translations.csv` (core UI keys)
- Traditional Chinese VO: player picks **Cantonese** or **Mandarin** in settings (`vo_dialect`) — clips generated Phase 7
- Language selector on main menu; preference saved to `user://settings.json`
- See `docs/engineering/technical/LOCALIZATION.md` for translator workflow

---


## 16. Risk register

| Risk | Mitigation |
|------|------------|
| Scope creep | Lock 3 locations until post-launch |
| Asset inconsistency | Single style bible + vertical slice gate (`docs/design/art/ART_DIRECTION.md` §10) |
| License violations | `docs/design/art/ASSET_COMPLIANCE.md` + `tools/check_asset_compliance.sh` before ship |
| Combat feel | Vertical slice before content production |
