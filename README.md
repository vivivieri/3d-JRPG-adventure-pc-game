# Tides of Urashima

A short **3D JRPG adventure** for PC (Steam), adapted from the public-domain Japanese folktale *Urashima Tarō*.

**Engine:** Godot 4.7 stable (MIT, no royalties)  
**Languages:** English, 日本語, 简体中文 (Noto Sans — bundled at ship)  
**Target audience:** Men 20–30  
**Playtime:** 2–3 hours  

> **`main` is the clean baseline:** design docs, story JSON (`game/data/`), workflow rules, and a minimal Godot boot shell. **Gameplay is not implemented yet** — rebuild via GodotPrompter + full MCP stack per [`docs/IMPLEMENTATION_PLAN.md`](docs/IMPLEMENTATION_PLAN.md).

---

## Project status

| Stage | Status |
|-------|--------|
| **M0** — GDD, storyboard, specs | Done |
| **M0b** — i18n (en / ja / zh) | Spec done — `LocalizationManager` Phase 2+ |
| **M0c–M0h** — Art, gameplay, narrative, data, AI workflow docs | Done |
| **Phase 0** — Dev environment + boot shell | **Done** |
| **Phases 1–6** — Zones, systems, combat, full story | **Not started** |
| **M5 / Phase 7** — Art rebuild (NPR zones, hero meshes, curated audio) | Not started |
| **M6 / Phase 8** — Steam export, compliance, Windows playtest | Not started |

**Next build step:** Phase 1 — `ruined_village` vertical slice (SC-02). Checklist: [`docs/MILESTONES.md`](docs/MILESTONES.md).

### Implementation phases (build order)

| Phase | Milestone | Focus |
|-------|-----------|-------|
| 1 | — | Environment + SC-02 vertical slice gate |
| 2–3 | M1 | Core systems + narrative exploration |
| 4 | M2 | Combat vertical slice |
| 5 | M3 | Chapter 1 (caves, puzzle, Shore Wraith) |
| 6 | M4 | Full story + three endings |
| 7 | **M5** | Art rebuild — replace greybox/Kenney placeholders |
| 8 | **M6** | Steam ship — GodotSteam 4.20+, export, playtest |

---

## Documentation authority

When docs disagree, use this order:

1. [`docs/IMPLEMENTATION_PLAN.md`](docs/IMPLEMENTATION_PLAN.md) — **what to build, in what order**
2. [`docs/MILESTONES.md`](docs/MILESTONES.md) — deliverable checklist
3. [`docs/MCP_STACK.md`](docs/MCP_STACK.md) — which tool owns which task
4. [`.cursorrules`](.cursorrules) — agent hard rules
5. [`game/data/`](game/data/) — runtime content source of truth

---

## Quick start

```bash
bash tools/setup_dev_environment.sh
bash tools/ensure_mcp_stack.sh          # GDAI + Godotiq + MCP Pro bridges
bash tools/check_dev_environment.sh
bash tools/run_unit_tests.sh
bash tools/run_playtest_smoke.sh       # story data + unit tests + boot load
python3 tools/validate_story_data.py
```

Open `game/project.godot` in Godot 4.7 (Forward+) and press **F5** — dev boot screen only.

### Agent workflow

| Tool | Role |
|------|------|
| **GodotPrompter** (Cursor) | Plan + write `.gd`, `.gdshader`, tests |
| **GDAI MCP** | Build scenes in editor — no manual `.tscn` edits |
| **Godotiq** | Debug signals, trace flows, read Output |
| **Godot MCP Pro** | L4/L5 automated test scenarios (`--minimal`) |
| **GameLab MCP** | Generate zone textures, UI sheets |
| **Notion MCP** | Design context (formulas, lore index) |

Full map: [`docs/MCP_STACK.md`](docs/MCP_STACK.md) · Rules: [`.cursorrules`](.cursorrules) §0

**Cloud agents:** [`AGENTS.md`](AGENTS.md) · [`docs/GDAI_CLOUD_SETUP.md`](docs/GDAI_CLOUD_SETUP.md)

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
| [Cinematics](docs/CINEMATICS.md) | In-engine cameras — **no FMV** |
| [Audio Direction](docs/AUDIO_DIRECTION.md) | Music map, SFX, selective VO policy |
| [Audio Production Guide](docs/AUDIO_PRODUCTION_GUIDE.md) | BGM/SFX specs, buses, scene map |
| [Asset Compliance](docs/ASSET_COMPLIANCE.md) | Copyright-safe policy + verification |
| [Art Direction](docs/ART_DIRECTION.md) | Muted Japanese coastal stylized 3D |
| [Rendering Guide](docs/RENDERING_GUIDE.md) | Forward+ tonemap, fog, glow, zone presets |
| [Storyboard Illustrations](docs/STORYBOARD_ILLUSTRATIONS.md) | Pitch art spec + scene briefs |
| [Pitch images](docs/pitch/illustrations/) | 25 images (20 scenes + 5 characters) |
| [Marketing trailer](steam/trailer.mp4) | ~75s EN / JA / ZH — `python3 tools/generate_marketing_trailer.py --all-locales` |

### Gameplay systems (M0d)

| Document | Purpose |
|----------|---------|
| [Quest & Flags](docs/QUEST_AND_FLAGS.md) | 5 quests, story flags, zone blockers |
| [Tutorial Design](docs/TUTORIAL_DESIGN.md) | Onboarding + SC-00 prologue |
| [Ending Design](docs/ENDING_DESIGN.md) | Choice UI, 3 endings, replay |
| [Items & Economy](docs/ITEMS_AND_ECONOMY.md) | 20 items, shop, drops |
| [Combat Systems](docs/COMBAT_SYSTEMS.md) | Turn order, elements, intent UI |
| [Skills Bible](docs/SKILLS_BIBLE.md) | 15 player + 6 enemy skills |
| [UI / UX Flow](docs/UI_UX_FLOW.md) | Menus, HUD, controller |
| [Save & Fail States](docs/SAVE_AND_FAIL_STATES.md) | Autosave, game over |
| [Settings & Accessibility](docs/SETTINGS_ACCESSIBILITY.md) | Options, hard mode, a11y |
| [Puzzle Design](docs/PUZZLE_DESIGN.md) | SC-07 water puzzle (silent) |
| [Achievements](docs/ACHIEVEMENTS.md) | 12 Steam achievements |
| [Playtest Script](docs/PLAYTEST_SCRIPT.md) | 2–3h QA path (after Phase 2+) |
| [QA & Bug Process](docs/QA_AND_BUG_PROCESS.md) | Severity, triage, milestone gates |
| [Narrative Writing Guide](docs/NARRATIVE_WRITING_GUIDE.md) | Voice, silence, i18n prose |
| [VO Hit List](docs/VO_HIT_LIST.md) | 12 selective ElevenLabs clips |
| [Progression Tuning](docs/PROGRESSION_TUNING.md) | XP, stats, economy |
| [Game Feel](docs/GAME_FEEL.md) | Combat juice, feedback |
| [Lore & Environmental Story](docs/LORE_AND_ENVIRONMENTAL_STORY.md) | 8 lore entries |
| [World Map & Flow](docs/WORLD_MAP_AND_FLOW.md) | Zones, transitions, save points |
| [Replay Design](docs/REPLAY_DESIGN.md) | Endings gallery, second run |
| [Pacing Chart](docs/PACING_CHART.md) | Emotional beat timeline |

### Story data (M0e)

| Path | Purpose |
|------|---------|
| [Data Architecture](docs/DATA_ARCHITECTURE.md) | Story-first DB design + schema versions |
| `game/data/story/scenes.json` | 23 scene rows (SC-00…SC-17c) |
| `game/data/story/flags.json` | Flag registry |
| `game/data/dialogue/chapter_01.json` | 22 dialogue scenes, 12 `voice_id` VO lines |
| `game/data/quests/main_quests.json` | 5 main quests |
| `game/data/encounters/story_encounters.json` | 8 scripted fights |
| `game/data/skills/skills.json` | Player + enemy skills |
| `game/data/items/items.json` | Full item catalog |

```bash
python3 tools/validate_story_data.py
bash tools/check_asset_compliance.sh   # when assets exist
```

---

## Repository layout (`main`)

```
docs/                    # Design docs (source of truth)
game/
  data/                  # Story JSON spine
  scenes/boot.tscn       # Dev boot shell only
  scripts/
    core/                # boot_scene.gd, game_bootstrap.gd
    story/               # CinematicDirector, VoiceLinePlayer, story_data.gd
  assets/                # Placeholder tree for Phase 1+
  addons/                # GDAI MCP, Godotiq (commercial/gitignored — see addons/README.md)
  project.godot          # Godot 4.7 Forward+
tools/
  ensure_mcp_stack.sh
  validate_story_data.py
  generate_marketing_trailer.py
  generate_ai_bgm.py / generate_ai_vo.py
.cursorrules             # GodotPrompter + MCP workflow
AGENTS.md                # Cloud agent instructions
steam/                   # Store copy + trailer (EN / JA / ZH)
```

---

## Design highlights

- **Story:** Dark retelling — Urashima returns to a ruined village; the lacquer box holds stolen years
- **Combat:** Turn-based, speed-initiative, data-driven JSON skills/enemies
- **Endings:** Rewind / Anchor / Drift (player choice at final boss)
- **Cinematics:** Godot cameras + `CinematicDirector` — no FMV in-game
- **VO:** 12 selective emotional clips (ElevenLabs) — not full dialogue
- **Visuals:** Muted Japanese coastal stylized 3D — Kenney/primitives greybox only until M5 art pass
- **Assets:** Copyright-safe only (CC0, MIT, OFL, commissioned). See [`docs/ASSET_COMPLIANCE.md`](docs/ASSET_COMPLIANCE.md)

---

## Data-driven content

All combat and narrative content lives in `game/data/`. See [`game/data/README.md`](game/data/README.md).

```gdscript
# Phase 2+ — GameManager.load_json API (planned)
var scenes = StoryData.load_json("res://data/story/scenes.json")
```

---

## Key documentation

| Doc | Purpose |
|-----|---------|
| [Implementation Plan](docs/IMPLEMENTATION_PLAN.md) | Rebuild phases 0–8 |
| [Milestones](docs/MILESTONES.md) | Feature checklist |
| [MCP Stack](docs/MCP_STACK.md) | Full toolchain R&R |
| [AI Dev Workflow](docs/AI_DEV_WORKFLOW.md) | Build policy + acceptance criteria |
| [AI Testing Spec](docs/AI_TESTING_SPEC.md) | L0–L6 test layers |
| [Tech Stack](docs/TECH_STACK.md) | Godot 4.7 + plugin versions |
| [GDD](docs/GDD.md) | Game design document |
| [Storyboard](docs/STORYBOARD.md) | 19-scene narrative bible |
| [Licenses](docs/LICENSES.md) | Attribution log |

---

## Steam (M6 / Phase 8)

- Store copy: [`steam/STORE_PAGE.md`](steam/STORE_PAGE.md)
- Trailer: `steam/trailer.mp4` (+ `_ja`, `_zh`)
- GodotSteam **4.20+** required for Godot 4.7 — [`steam/GODOTSTEAM_SETUP.md`](steam/GODOTSTEAM_SETUP.md)
- Export: `tools/export_windows.sh` · Target price: $4.99–$9.99

---

## Credits

- Story adapted from *Urashima Tarō* (Japanese folklore, public domain)
- Built with [Godot Engine](https://godotengine.org) (MIT License)
