# Tides of Urashima — Implementation Plan

**Version:** 1.1 (Fresh rebuild)  
**Branch:** `main` (clean baseline)  
**Source of truth:** `main` design docs + `game/data/` JSON  
**Workflow:** GodotPrompter + full MCP toolchain — see `docs/MCP_STACK.md`.  
**Milestone checklist:** `docs/MILESTONES.md` (M5 art → M6 Steam).

Previous full implementation on `main` was **stripped** (boot shell + data only). Phases 1–6 rebuild from documentation via GDAI MCP.

### Phase ↔ milestone map

| Phase | Milestone | Focus |
|-------|-----------|-------|
| 0 | M0, M0c–M0h | Dev environment + design/data baseline ✅ |
| 1 | — | Environment foundation + SC-02 vertical slice gate |
| 2–3 | M1 | Core systems + narrative exploration |
| 4 | M2 | Combat vertical slice |
| 5 | M3 | Chapter 1 dungeons |
| 6 | M4 | Full story + three endings |
| 7 | **M5** | Art rebuild (NPR zones, hero meshes, curated audio) |
| 8 | **M6** | Steam export, compliance, playtest |

---

## Phase 0 — Dev environment ✅ (current)

| Task | Status |
|------|--------|
| `game/project.godot` (Godot 4.7 Forward+) | Done |
| Folder structure (`tools/setup_dev_environment.sh`) | Done |
| `tools/check_dev_environment.sh` | Done |
| `.cursor/mcp.json.example` (GDAI MCP) | Done |
| `game/addons/README.md` | Done |
| Boot scene validates `game/data/` paths | Done |
| Cloud install (`tools/install_cloud_dev.sh`, `.cursor/environment.json`) | Done |
| Story data validator (`tools/validate_story_data.py`) | Done |
| GDAI MCP workflow rules (`.cursorrules`, `tools/ensure_gdai_mcp.sh`) | Done |
| Fresh-rebuild smoke (`tools/run_playtest_smoke.sh`) | Done |
| AI dev workflow doc (`docs/AI_DEV_WORKFLOW.md`) | Done |
| AI testing spec (`docs/AI_TESTING_SPEC.md`) | Done |
| Unit tests (`tools/run_unit_tests.sh`, `game/tests/unit/`) | Done |

**Verify:**

```bash
bash tools/setup_dev_environment.sh
bash tools/ensure_gdai_mcp.sh
bash tools/check_dev_environment.sh
bash tools/run_unit_tests.sh
bash tools/run_playtest_smoke.sh
# Open game/project.godot in Godot 4.7 → F5
```

---

## Phase 1 — Environment foundation (NEXT)

**Read first:** `docs/LEVEL_DESIGN.md` (zone `ruined_village`), `docs/RENDERING_GUIDE.md`

Build stylized zone rendering before gameplay systems. Follow `docs/RENDERING_GUIDE.md`.

| # | Task | Docs |
|---|------|------|
| 1.1 | `environments/*.tres` — WorldEnvironment per zone (tonemap, fog, glow) | RENDERING_GUIDE §3–6 |
| 1.2 | `scripts/world/zone_visuals.gd` — apply palette, sky, lights at runtime | ENVIRONMENT_KITS §1 |
| 1.3 | `shaders/toon_base.gdshader` — single ramp family | ART_DIRECTION §7 |
| 1.4 | `shaders/water_stylized.gdshader` — foam + gentle displacement | ART_DIRECTION §3.6 |
| 1.5 | Greybox zone scenes: `beach_shore`, `ruined_village`, `tidal_caves`, `dragon_palace_gate` | STORYBOARD, ENVIRONMENT_KITS |
| 1.6 | DirectionalLight3D + fog per zone table | RENDERING_GUIDE §5 |
| 1.7 | ProceduralSky per zone (no HDRI) | RENDERING_GUIDE §4 |
| 1.8 | **Vertical slice gate:** SC-02 Ruined Village passes art checklist | ART_DIRECTION §10 |

**GDAI workflow:** GodotPrompter drafts shaders/`zone_visuals.gd` → GDAI MCP places nodes in `.tscn` → F5 verify. **Acceptance criteria:** `docs/AI_DEV_WORKFLOW.md` §4 Phase 1.

---

## Phase 2 — Core systems shell

**Read first:** `docs/TECHNICAL_DESIGN.md`, `docs/CODE_STYLE.md`

| # | Task | Docs |
|---|------|------|
| 2.1 | Autoloads: `GameManager`, `EventBus`, `SaveSystem`, `DialogueRunner`, `CombatManager` | GDD, DATA_ARCHITECTURE |
| 2.2 | `GameManager.load_json("res://data/...")` API | game/data/README.md |
| 2.3 | `LocalizationManager` + Noto fonts | LOCALIZATION.md |
| 2.4 | Main menu → New Game → beach_shore | UI_UX_FLOW.md |
| 2.5 | Player controller + camera orbit | GAME_FEEL.md |
| 2.6 | Scene transitions between zones | WORLD_MAP_AND_FLOW.md |

---

## Phase 3 — Narrative & exploration

| # | Task | Docs |
|---|------|------|
| 3.1 | Dialogue box UI + `DialogueRunner` wired to `game/data/dialogue/` | NARRATIVE_WRITING_GUIDE |
| 3.2 | Interactables + interaction prompt HUD | UI_UX_FLOW.md |
| 3.3 | Quest tracker + flag system from `story/flags.json` | QUEST_AND_FLAGS.md |
| 3.4 | SC-01 through SC-05 field content (village hub) | STORYBOARD.md |
| 3.5 | Lore collectibles | LORE_AND_ENVIRONMENTAL_STORY.md |

---

## Phase 4 — Combat vertical slice

| # | Task | Docs |
|---|------|------|
| 4.1 | Combat UI (HP/MP, intent icons, battle log) | COMBAT_SYSTEMS.md |
| 4.2 | Turn order, skills from `skills.json` | SKILLS_BIBLE.md |
| 4.3 | SC-05 Salt Crab tutorial encounter | TUTORIAL_DESIGN.md |
| 4.4 | Boss framework (phases, intent UI) | BOSS_DESIGNS.md |

---

## Phase 5 — Chapter 1 dungeons

| # | Task | Docs |
|---|------|------|
| 5.1 | Tidal caves greybox → art pass | ENVIRONMENT_KITS §5 |
| 5.2 | Water level puzzle SC-07 (silent — no VO) | PUZZLE_DESIGN.md |
| 5.3 | Shore Wraith boss SC-09 | BOSS_DESIGNS.md |
| 5.4 | Yuzu joins SC-10 | CHARACTER_BIBLE.md |

---

## Phase 6 — Full story & endings

| # | Task | Docs |
|---|------|------|
| 6.1 | Dragon Palace Gate zone | ENVIRONMENT_KITS §6 |
| 6.2 | Palace Sentinel + Tide Keeper | BOSS_DESIGNS.md |
| 6.3 | SC-16 choice UI + three endings | ENDING_DESIGN.md |
| 6.4 | Ending environment variants | ENVIRONMENT_KITS §7 |
| 6.5 | Credits sequence | CINEMATICS.md |

---

## Phase 7 — M5 art rebuild

Replace greybox with authored assets per `docs/ART_DIRECTION.md`:

- Urashima, Yuzu, Roku models
- Hero set-pieces (torii, palace gate)
- Hand-painted zone textures
- Painted portraits
- Curated BGM (`docs/AUDIO_PRODUCTION_GUIDE.md`)

---

## Phase 8 — M6 Steam & ship prep

| # | Task |
|---|------|
| 8.1 | GodotSteam + `tools/export_windows.sh` |
| 8.2 | `bash tools/check_asset_compliance.sh` |
| 8.3 | Graphics quality presets (Low/Med/High) |
| 8.4 | Playtest script (`docs/PLAYTEST_SCRIPT.md`) |
| 8.5 | Disable/remove GDAI MCP before export |

---

## Zone build order (environment)

1. **ruined_village** — vertical slice gate (SC-02)
2. **beach_shore** — SC-01 arrival
3. **tidal_caves** — biolume + puzzle
4. **dragon_palace_gate** — void sky + glow
5. **ending_*** — per ending doc

---

## Validation commands

```bash
python3 tools/validate_story_data.py
bash tools/ensure_gdai_mcp.sh
bash tools/run_unit_tests.sh
bash tools/check_dev_environment.sh
bash tools/run_playtest_smoke.sh
bash tools/run_integration_tests.sh   # Phase 2+ gates
bash tools/run_e2e_playthrough.sh     # Phase 6 gate
bash tools/check_asset_compliance.sh  # when assets exist
```

---

## Deprecated

- `docs/GDAI_REGEN_PLAN.md` — superseded by this plan (old `gdai-regen-dc91` branch deleted)
- All `*-dc91` implementation branches — deleted; do not restore old code
