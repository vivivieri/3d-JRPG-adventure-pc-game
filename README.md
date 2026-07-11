# Tides of Urashima

A short **3D JRPG adventure** for PC (Steam), adapted from the public-domain Japanese folktale *Urashima Tarō*.

**Engine:** Godot 4.3+ (MIT, no royalties)  
**Languages:** English, 日本語, 简体中文 (Noto Sans fonts bundled)  
**Target audience:** Men 20–30  
**Playtime:** 2–3 hours  

> **`main` is the clean baseline:** design docs, story JSON (`game/data/`), GDAI workflow rules, and a minimal Godot boot shell. Gameplay is **not implemented yet** — rebuild via GodotPrompter + GDAI MCP per `docs/IMPLEMENTATION_PLAN.md`.

---

## Project status

| Milestone | Status |
|-----------|--------|
| M0 — GDD, storyboard, repo scaffold | Done |
| M0b — Multi-language (en / ja / zh) | Done |
| M0c — Art rebuild specs | Done |
| M0d — Gameplay systems specs | Done |
| M0e — Story data on main | Done |
| **Phase 0 — Dev environment + boot shell** | **Done** |
| **Phase 1–6 — Godot implementation** | **Not started** — rebuild on `main` via GDAI MCP |
| M6 — Art rebuild (high-detail Japanese) | Not started |
| M5 — Polish + Steam page | Not started |

---

## Quick start

```bash
bash tools/setup_dev_environment.sh
bash tools/ensure_gdai_mcp.sh          # GDAI MCP + Godot editor HTTP bridge
bash tools/check_dev_environment.sh
bash tools/run_unit_tests.sh
bash tools/run_playtest_smoke.sh       # story data + unit tests + boot load
```

Open `game/project.godot` in Godot 4.3+ (Forward+) and press **F5** — dev boot screen only.

**Workflow:** GodotPrompter (plan/code) + GDAI MCP (editor) **only** — see `.cursorrules` §0, `docs/AI_DEV_WORKFLOW.md`, and `AGENTS.md`. No manual `.tscn` fallback.

**Cloud agents:** `bash tools/install_cloud_dev.sh` via `.cursor/environment.json`. See [`docs/GDAI_CLOUD_SETUP.md`](docs/GDAI_CLOUD_SETUP.md) and [`AGENTS.md`](AGENTS.md).

---

## Pre-build design package

### Art & compliance (M0c)

| Document | Purpose |
|----------|---------|
| [Character Bible](docs/CHARACTER_BIBLE.md) | Models, colors, animations, portraits |
| [Items 3D Model Guide](docs/ITEMS_3D_MODEL_GUIDE.md) | Weapons, props, pickups, attachment rig |
| [Environment Kits](docs/ENVIRONMENT_KITS.md) | Modular assets per zone + lore placements |
| [Boss Designs](docs/BOSS_DESIGNS.md) | Phases, patterns, hard mode |
| [Encounter Table](docs/ENCOUNTER_TABLE.md) | Pacing, XP, shop, equipment |
| [Cinematics](docs/CINEMATICS.md) | Camera, boss intros, endings |
| [Audio Direction](docs/AUDIO_DIRECTION.md) | Music map, SFX, scene cues |
| [Audio Production Guide](docs/AUDIO_PRODUCTION_GUIDE.md) | BGM specs, SFX manifest, scene map |
| [Asset Compliance](docs/ASSET_COMPLIANCE.md) | Copyright-safe policy + verification tools |
| [Art Direction](docs/ART_DIRECTION.md) | Visual pivot + poly budgets |
| [Rendering Guide](docs/RENDERING_GUIDE.md) | Godot 4 Forward+ checklist — tonemap, fog, glow, toon materials |
| [Storyboard Illustrations](docs/STORYBOARD_ILLUSTRATIONS.md) | Pitch art spec + scene briefs |
| [Pitch images](docs/pitch/illustrations/) | P0 concept art (5 images) for presentations |
| [Marketing trailer](steam/trailer.mp4) | ~68s pitch video (EN / JA / ZH) — `python3 tools/generate_marketing_trailer.py --all-locales` |

### Gameplay systems (M0d)

| Document | Purpose |
|----------|---------|
| [Quest & Flags](docs/QUEST_AND_FLAGS.md) | 5 quests, story flags, zone blockers |
| [Tutorial Design](docs/TUTORIAL_DESIGN.md) | Onboarding matrix + SC-00 prologue |
| [Ending Design](docs/ENDING_DESIGN.md) | Choice UI, 3 endings, replay |
| [Items & Economy](docs/ITEMS_AND_ECONOMY.md) | Canonical items, shop, drops |
| [Combat Systems](docs/COMBAT_SYSTEMS.md) | Elements, status, limits |
| [Skills Bible](docs/SKILLS_BIBLE.md) | 15 player skills |
| [UI / UX Flow](docs/UI_UX_FLOW.md) | Menus, HUD, controller |
| [Save & Fail States](docs/SAVE_AND_FAIL_STATES.md) | Autosave, game over |
| [Settings & Accessibility](docs/SETTINGS_ACCESSIBILITY.md) | Options, hard mode, a11y |
| [Puzzle Design](docs/PUZZLE_DESIGN.md) | SC-07 water puzzle |
| [Achievements](docs/ACHIEVEMENTS.md) | 12 Steam achievements |
| [Playtest Script](docs/PLAYTEST_SCRIPT.md) | 2–3h QA path (re-enable after Phase 2+) |
| [QA & Bug Process](docs/QA_AND_BUG_PROCESS.md) | Severity, triage, regression |
| [Narrative Writing Guide](docs/NARRATIVE_WRITING_GUIDE.md) | Voice, silence, no VO, i18n prose |
| [Progression Tuning](docs/PROGRESSION_TUNING.md) | XP, stats, economy, difficulty |
| [Game Feel](docs/GAME_FEEL.md) | Combat juice, feedback, rewards |
| [Lore & Environmental Story](docs/LORE_AND_ENVIRONMENTAL_STORY.md) | 8 lore entries, hub emptiness |
| [World Map & Flow](docs/WORLD_MAP_AND_FLOW.md) | Zones, connections, save points |
| [Replay Design](docs/REPLAY_DESIGN.md) | Endings gallery, second run |
| [Pacing Chart](docs/PACING_CHART.md) | Emotional beat timeline |

### Story data (M0e)

| Document / path | Purpose |
|-----------------|---------|
| [Data Architecture](docs/DATA_ARCHITECTURE.md) | Story-first DB design |
| `game/data/story/scenes.json` | Scene spine SC-00…SC-17c |
| `game/data/story/flags.json` | Flag registry |
| `game/data/quests/main_quests.json` | 5 main quests |
| `game/data/encounters/story_encounters.json` | Scripted fights |
| `game/data/dialogue/chapter_01.json` | All dialogue |
| `game/data/items/items.json` | Full item catalog |
| `game/data/shop/roku_shop.json` | Roku shop |
| `game/data/starting/new_game.json` | New game defaults |

```bash
python3 tools/validate_story_data.py
```

```bash
# Register a new external asset
python3 tools/register_asset.py add \
  --path game/assets/models/characters/urashima/urashima.glb \
  --license ORIGINAL --source "Custom Blender" --author "Project" \
  --used-for "Protagonist model"

# Verify all media + generate audit proof
bash tools/check_asset_compliance.sh
```

---

## Repository layout (`main`)

```
docs/                    # Design docs (source of truth)
game/
  data/                  # Story JSON
  scenes/boot.tscn       # Dev boot shell only
  scripts/core/          # boot_scene.gd, game_bootstrap.gd
  assets/                # Placeholder folders for Phase 1+
  addons/                # GDAI MCP plugin (commercial — see addons/README.md)
  project.godot
tools/
  ensure_gdai_mcp.sh     # Bootstrap GDAI MCP + editor HTTP bridge
  setup_dev_environment.sh
  check_dev_environment.sh
  run_unit_tests.sh
  run_integration_tests.sh
  run_e2e_playthrough.sh   # Phase 6+
  validate_story_data.py
  check_asset_compliance.sh
  install_gdai_plugin.sh # Cloud snapshot: install plugin from zip
.cursorrules             # GDAI-only workflow (§0)
AGENTS.md                # Agent instructions
steam/                   # Store page copy + trailer
```

**Next build step:** Phase 1 — `ruined_village` vertical slice. See [`docs/IMPLEMENTATION_PLAN.md`](docs/IMPLEMENTATION_PLAN.md).

---

## Design highlights

- **Story:** Dark retelling — Urashima returns to a ruined village; the lacquer box holds stolen years
- **Combat:** Turn-based, speed-initiative, data-driven JSON skills/enemies/AI
- **Endings:** Rewind / Anchor / Drift (player choice at final boss)
- **Assets:** Custom high-detail Japanese stylized — **copyright-safe only** (CC0, MIT, OFL, commissioned). See `docs/ASSET_COMPLIANCE.md`

---

## Data-driven content

All combat and narrative content lives in `game/data/`. See `game/data/README.md` for the JSON schema.

Example — load scene data (systems to be built in Phase 2+):

```gdscript
var scenes = JSON.parse_string(FileAccess.get_file_as_string("res://data/story/scenes.json"))
```

---

## Documentation

- [AI Dev Workflow](docs/AI_DEV_WORKFLOW.md) — AI build, unit tests, acceptance criteria
- [Implementation Plan](docs/IMPLEMENTATION_PLAN.md) — rebuild phases
- [GDAI Cloud Setup](docs/GDAI_CLOUD_SETUP.md) — MCP + editor bridge
- [Game Design Document](docs/GDD.md)
- [Storyboard](docs/STORYBOARD.md)
- [Art Direction](docs/ART_DIRECTION.md)
- [Rendering Guide](docs/RENDERING_GUIDE.md)
- [Combat data schema](game/data/README.md)
- [Godot project README](game/README.md)

Full doc index: see tables above.

---

## Steam

Store page copy and capsule placeholders are in [`steam/STORE_PAGE.md`](steam/STORE_PAGE.md).

- Export preset: `game/export_presets.cfg.example` (Windows Desktop)
- GodotSteam integration: planned (see `docs/MILESTONES.md`)
- Target price: $4.99–$9.99

---

## Credits

- Story adapted from *Urashima Tarō* (Japanese folklore, public domain)
- Built with [Godot Engine](https://godotengine.org) (MIT License)
