# AGENTS.md — Cloud Agent instructions

## Cursor Cloud specific instructions

**Repo:** Tides of Urashima — stylized 3D JRPG (Godot 4.7 Forward+)  
**Platforms (v1):** **Linux + Windows** (Steam) — Linux required because Cursor Cloud Agents run Linux; see `docs/qa/PLATFORM_SUPPORT.md`. macOS v1.1+.  
**Branches:** `main` = **docs + design data only** · `game/development` = **full Godot implementation** (no merge to `main` until M6 ship) — see `docs/workflow/BRANCHING.md`  
**Environments:** dev → qa → uat → preprod (optional) → prod — see `docs/ci-cd/ENVIRONMENTS.md`  
**Delivery model:** Phase-gated Agile — see `docs/workflow/AGILE_WITHIN_PHASES.md`  
**Multi-agent team:** `docs/agents/MULTI_AGENT_TEAM.md` · **R&R cheat sheet:** `docs/cheat-sheets/RR_CHEATSHEET.md` · **Controls cheat sheet:** `docs/cheat-sheets/CONTROLS_CHEATSHEET.md` · **Issues:** `docs/agents/PROJECT_MANAGEMENT.md` (GitHub Issues P0)  
**Design source of truth:** `docs/` on `main` + `game/data/` JSON  
**Code base classes:** `docs/technical/CODE_BASE_CLASS_RULES.md` · `game/data/code/base_classes.json`  
**Documentation index:** `docs/README.md`  
**Build order:** `docs/workflow/IMPLEMENTATION_PLAN.md` (M5 art → M6 Steam) — checklist in `docs/workflow/MILESTONES.md`  
**Implementation plan:** `docs/workflow/IMPLEMENTATION_PLAN.md`  
**Workflow:** **GodotPrompter + full MCP toolchain** — see `.cursorrules` §0, `docs/agents/MCP_STACK.md`, `docs/workflow/AI_DEV_WORKFLOW.md`

| Tool / MCP server | Role |
|-------------------|------|
| GodotPrompter | Plan, GDScript, shaders, tests |
| `godot-mcp` (GDAI) | **Build** scenes |
| `godotiq` | **Analyze** signals/debug |
| `godot-mcp-pro` | **Test** scenarios/asserts (L4/L5) |
| `gamelab-mcp` | **UI art** — frames, icon sheets **(required)** |
| ComfyUI / Material Maker | **Zone NPR albedos** — offline |
| Meshy / Tripo / Rodin + **Blender** | **3D hero pipeline + M5 turntable QA** — required offline |
| `generate_game_audio.py` + ACE-Step 1.5 | **Audio** placeholders + zone/opening/boss/ending hero BGM |
| `generate_ai_vo.py` + ElevenLabs | **Selective VO** — 12 emotional clips only (`docs/vision/VO_HIT_LIST.md`) |

**All MCP servers required** (`godot-mcp`, `godotiq`, `godot-mcp-pro`, `gamelab-mcp`). **Blender** required for M5 turntable QA. Procedural UI fallbacks OK for asset output only — see `docs/art/ART_AUTOMATION_PIPELINE.md`. If any required piece missing → STOP and notify user.

### Cloud environment: which branch you are on matters

The Godot editor + MCP stack (`godot-mcp`, `godotiq`, `godot-mcp-pro`, `gamelab-mcp`) and the commercial GDAI plugin only exist / matter on `game/development`. **On `main` they are neither present nor needed** — `main` has no `project.godot`, no `.gd` gameplay code, and no `game/addons/`.

- **`main` (default cloud checkout):** docs + design data + Python tooling only. The committed `.cursor/environment.json` `install` here only runs `pip3 install --user -r tools/requirements-ci.txt numpy` (installs `gdtoolkit` → `gdlint`/`gdformat` into `~/.local/bin`; `python3`/`numpy` ship in the base image). Do **not** boot the MCP/Godot stack on `main`.
  - **Tests:** `bash tools/run_docs_ci_checks.sh` (L0 docs+data gates, pure `python3`).
  - **Lint:** `bash tools/check_gdscript_changed.sh` (SKIPs on `main` — no `.gd`); `gdlint <file>` directly for any `.gd` (project scripts add `~/.local/bin` to PATH themselves).
  - **Run the content pipeline (the runnable "app" on `main`):** e.g. `python3 tools/generate_game_audio.py --track bgm_village` writes a real `.ogg` under `game/assets/audio/bgm/` (untracked — do not commit demo output). `tools/generate_procedural_portraits.py` currently has a syntax error and is not runnable.
- **`game/development`:** run the full bootstrap below. That heavy stack (Godot download, commercial plugins, MCP bridges) is intentionally **not** wired into `main`'s `environment.json`.

### Cloud snapshot launch (`game/development` only)

**Before implementation work:** read `docs/agents/CLOUD_SNAPSHOT_LAUNCH.md` — active snapshot id, launch checklist, and JIT-vs-snapshot troubleshooting. Launch from [Cloud Agents → Environments](https://cursor.com/dashboard/cloud-agents/environments/r/github.com/vivivieri/3d-jrpg-adventure-pc-game) on branch **`game/development`**, not ad-hoc on `main`. **Linux ship is required** for cloud dev parity — `docs/qa/PLATFORM_SUPPORT.md`.

### Environment bootstrap

On every cloud agent start:

```bash
bash tools/install_cloud_dev.sh      # Godot, uv, Godotiq, MCP Pro, Blender
bash tools/ensure_mcp_stack.sh       # Editor + MCP bridges — REQUIRED
bash tools/install_extended_toolchain.sh  # Blender, audio placeholders, GameLab config
bash tools/check_extended_toolchain.sh    # Full toolchain status
```

Installed components:
- **Godot 4.7** editor → `godot4` in `~/.local/bin`
- **uv / uvx** → GDAI + Godotiq MCP bridges
- **Node.js** → Godot MCP Pro server (if installed)
- **GDAI MCP** → `game/addons/gdai-mcp-plugin-godot/` (commercial)
- **Godotiq** → `game/addons/godotiq/` (`bash tools/install_godotiq.sh`)
- **Godot MCP Pro** → `game/addons/godot_mcp/` + `tools/godot-mcp-pro-server/` (commercial)

### MCP workflow (mandatory — all tools)

**First commands every implementation session (before any `game/scenes/` work):**

```bash
bash tools/ensure_mcp_stack.sh
bash tools/check_mcp_ready.sh
bash tools/check_rr_compliance.sh
bash tools/check_extended_toolchain.sh
```

If `ensure_mcp_stack.sh`, `check_mcp_ready.sh`, or `check_extended_toolchain.sh` fails → **STOP scene/editor work** and notify the user.  
Docs/data/JSON tasks may continue. **Do not** hand-edit `.tscn` as a fallback.

```
0. bash tools/ensure_mcp_stack.sh
1. GodotPrompter — plan GDScript, shaders, tests
2. docs/ + game/data/ — design context before data/combat edits
3. ComfyUI/Material Maker or gamelab-mcp — art gen → palette_remap.py → game/assets/
4. godot-mcp (GDAI) — build scenes, materials, F5 verify
5. godotiq — trace_flow / signal_map when debugging systems
6. godot-mcp-pro — run_test_scenario for L4/L5 playthrough asserts
7. Meshy/Blender offline — hero GLB meshes when 3D art task requires it
```

**Scene edits:** GDAI only. Do not hand-edit `.tscn`.

### Sprint orchestration (mandatory — no honor system)

| Role | First command every session |
|------|----------------------------|
| **PM / Sprint Master** | `bash tools/run_pm_orchestrator.sh` — FAIL blocks all dispatch |
| **Architect, Builder, QA, Flow, Release, Visual** | `bash tools/run_agent_session_gate.sh <role> <issue_id>` before work |

Authority: `docs/agents/PM_AGENT_RUNBOOK.md`, `docs/agents/SPRINT_ORCHESTRATION.md`, `game/data/qa/sprint_board.json`

**End every completed issue with** (triggers PM via webhook — not cron):

```bash
python3 tools/pm_update_issue.py <issue_id> --status done --commit "$(git rev-parse HEAD)"
bash tools/pm_emit_cycle_event.sh agent_cycle_complete --issue <issue_id> --agent <role> --commit "$(git rev-parse HEAD)"
```

See `docs/agents/CLOUD_AGENT_SETUP_RUNBOOK.md`.

### If MCP unavailable — NOTIFY USER, DO NOT FALL BACK

| Server | Check |
|--------|-------|
| GDAI | `curl -sf http://127.0.0.1:3571/tools`; plugin + `godot-mcp` in Cursor |
| Godotiq | `game/addons/godotiq/`; `godotiq` in Cursor MCP |
| MCP Pro | `tools/godot-mcp-pro-server/build/index.js`; `godot-mcp-pro` in Cursor |
| GameLab | `gamelab-mcp` in Cursor MCP; `GAMELAB_API_KEY` in Secrets **(required)** |
| Blender | `blender` in PATH — `bash tools/install_extended_toolchain.sh` **(required for M5 turntable)** |
| ComfyUI / Material Maker | Local install for zone albedos |

Register all installed servers in Cursor (desktop Settings or cloud dashboard). See `docs/agents/MCP_STACK.md`.

### Copyright-safe procedural assets

| Type | Generator |
|------|-----------|
| Zone NPR albedos | ComfyUI / Material Maker + `palette_remap.py` |
| UI art | GameLab MCP (required; procedural placeholders OK until gen ships) |
| BGM / SFX | `python3 tools/generate_game_audio.py --all` + ACE-Step ship path |
| Selective VO | `bash tools/generate_ai_vo.sh --tier p0` (needs `ELEVENLABS_API_KEY`) |
| Portrait placeholders | `python3 tools/generate_procedural_portraits.py --all` |
| Manifest | `python3 tools/register_asset.py add --help` |

No web-scraped art/audio. See `docs/art/ASSET_COMPLIANCE.md`.

### Automated testing & QA (required every commit)

See `docs/workflow/AI_DEV_WORKFLOW.md` for policy, `docs/qa/ACCEPTANCE_CRITERIA.md` for **measurable** pass/fail, and **`docs/ci-cd/CI.md`** for GitHub Actions gates.

| Branch | CI script |
|--------|-----------|
| `main` | `bash tools/run_docs_ci_checks.sh` — data + docs only |
| `game/development` | `bash tools/run_ci_checks.sh` — **required** full L0–L4 game gates (green before PR merge) |

```bash
export PATH="$HOME/.local/bin:$PATH"
export XDG_DATA_HOME="/workspace/.cache/godot-data"
export XDG_CONFIG_HOME="/workspace/.cache/godot-config"
export XDG_CACHE_HOME="/workspace/.cache/godot-cache"

python3 tools/validate_story_data.py          # L0
python3 tools/validate_acceptance_criteria.py # catalog lint
python3 tools/validate_base_classes.py        # L0 base class registry
bash tools/check_rr_compliance.sh             # L0 — GDAI-verified scenes only
bash tools/check_base_class_compliance.sh     # L0 — native extends audit
bash tools/run_unit_tests.sh                  # L1
bash tools/check_gdscript_changed.sh          # L1 — gdlint on changed .gd
bash tools/run_playtest_smoke.sh              # L2 (incl. animation, feel, art smokes)
python3 tools/check_animation_whitelist.py --phase m5 --strict  # L2 when GLBs exist
bash tools/run_feel_smoke_checks.sh           # L2 feel
python3 tools/check_glb_import_scripts.py --strict  # L2 GLB import
bash tools/run_integration_tests.sh           # L4 phase gates (Phase 2+)
REQUIRE_L5=1 bash tools/run_e2e_playthrough.sh  # L5 (Phase 6+; blocks human QA)
bash tools/check_asset_compliance.sh
```

| QA domain | Policy doc | On FAIL |
|-----------|------------|---------|
| Acceptance thresholds | `docs/qa/ACCEPTANCE_CRITERIA.md` | Fix metric; cite gate id in report |
| 3D models | `docs/art/MODEL_QA.md` | `qa_emit_remediation.sh model-tech\|model-jury` |
| Visuals | `docs/art/VISUAL_QA.md` | `qa_emit_remediation.sh visual-palette\|visual-jury` |
| Audio (BGM) | `docs/audio/AUDIO_QA.md` | `qa_emit_remediation.sh audio-tech\|audio-jury` |
| Audio (P0 VO) | `docs/audio/AUDIO_QA.md` §A4–A5 | `qa_emit_remediation.sh vo-tech\|vo-jury` |
| Game flow | `docs/qa/FLOW_QA.md` | `qa_emit_remediation.sh flow-scenario INT-*` |
| Iteration | `docs/qa/QA_REMEDIATION_LOOP.md` | One lever per attempt; max 3 |

GDAI MCP F5 = **L3**; Godotiq = debug/trace; Godot MCP Pro = L4/L5 scenarios (`docs/qa/AI_TESTING_SPEC.md`, `docs/agents/MCP_STACK.md`).

**Human QA:** Only after L0–L5 pass — `docs/qa/PLAYTEST_SCRIPT.md` (`docs/qa/AI_TESTING_SPEC.md` §8).

### Cross-cutting factory features (agents MUST register)

If your task adds or changes anything that touches **PM dispatch, agent sessions, secrets, cycle events, orchestrator steps, watchdog, or stakeholder reports**:

1. Read `docs/qa/WORKFLOW_INTEGRATION.md`
2. Register the feature in `game/data/qa/workflow_integration_registry.json` (hooks + doc refs + secrets)
3. Wire all script hooks before updating docs alone
4. **Before commit/PR:** `bash tools/check_feature_integration.sh --remind` — must PASS
5. Run `bash tools/run_docs_ci_checks.sh` (includes `L0_workflow_integration`)

**Do not** ship a cross-cutting feature in one script only — CI will fail and PM dispatch docs will drift.

### Rendering & environment (Phase 1)

Before building zones, read:
- `docs/art/RENDERING_GUIDE.md`
- `docs/world/ENVIRONMENT_KITS.md`
- `docs/art/ART_DIRECTION.md`

Build order: **ruined_village** vertical slice → beach → caves → palace.  
All scene work via **GDAI MCP** after GodotPrompter plans.

### Secrets (day one — all compulsory)

**How to obtain each key:** `docs/agents/CURSOR_SECRETS_SETUP.md` · verify: `bash tools/check_day_one_secrets.sh`

| Secret | Purpose |
|--------|---------|
| `CURSOR_PM_CYCLE_WEBHOOK_URL` | PM Automation A webhook |
| `CURSOR_FACTORY_ALERT_WEBHOOK_URL` | Factory alert Automation D webhook |
| `GAMELAB_API_KEY` | GameLab MCP |
| `GH_TOKEN` | `gh` CLI, issue sync, GitHub dispatch |
| `TELEGRAM_BOT_TOKEN` / `TELEGRAM_CHAT_ID` | Stakeholder status |
| `ELEVENLABS_API_KEY` | Selective VO |
| `CURSOR_API_KEY` | Auto agent token telemetry (Cloud Agents usage API) |

Also in GitHub repo Secrets: both webhook URLs (Actions workflows). Scope: **Personal + Runtime Secret**.

**Later phases:** GDAI license, `OPENAI_API_KEY` / `GEMINI_API_KEY` (M5+ jury), Steam keys (Phase 8).

### Do not ship

- Do not ship: `game/addons/gdai-mcp-plugin-godot/`, `game/addons/godotiq/`, `game/addons/godot_mcp/`
- Disable GDAI before Steam export
