# R&R Cheat Sheet — Roles & Responsibilities

**Version:** 1.0  
**Print this:** One-page reference for every agent session  
**Authority:** `.cursorrules` §0–§1 · `docs/MCP_STACK.md` · `docs/MULTI_AGENT_TEAM.md` · `docs/AGILE_WITHIN_PHASES.md` §11

---

## Golden rules

1. **GodotPrompter writes code** → **GDAI MCP builds scenes** → **QA proves gates** — never skip a handoff.
2. **Only GDAI MCP** may create/edit `.tscn`, nodes, materials, lights, inspector values.
3. **Never hand-edit `.tscn` in Cursor** when GDAI is available (`L0_rr_compliance`).
4. **P0 MCP required:** `godot-mcp`, `godotiq`, `godot-mcp-pro` — if missing, **STOP and notify user**.
5. **One writer per `.tscn`** — never parallel two agents on the same scene file.
6. **`docs/` + `game/data/`** are design truth — not sprint backlog reprioritization.

---

## Tool R&R (what owns what)

| Layer | Tool | Owns | Must NOT |
|-------|------|------|----------|
| Plan & code | **GodotPrompter** | `.gd`, `.gdshader`, tests, architecture | Hand-edit scenes |
| Build | **GDAI MCP** (`godot-mcp`) | `.tscn`, materials, lights, F5 | System design |
| Analyze | **Godotiq** (`godotiq`) | Signals, `trace_flow`, debug console | Scene mutations |
| Test | **MCP Pro** (`godot-mcp-pro`, `--minimal`) | L4/L5 scenarios, asserts | Build/edit scenes |
| UI art | **GameLab MCP** *(P1)* | UI PNG/WebP → `game/assets/textures/ui/` | Place nodes / `.tscn` |
| Zone albedo | **ComfyUI / Material Maker** | Tileables → `palette_remap.py` | Assign in editor (→ GDAI) |
| Hero 3D | **Meshy/Tripo/Rodin + Blender** | GLB import | Scene placement (→ GDAI) |
| Audio | **ACE-Step / generate_game_audio.py** | BGM/SFX prototypes | — |
| Design data | **`docs/` + `game/data/`** | Story, flags, skills, gates | — |

---

## Agent roster

| Role | Agent | Owns | Must NOT |
|------|-------|------|----------|
| **PM / Sprint facilitator** | PM Agent | Issues, milestones, env promotion, batch planning | Write code or `.tscn` |
| **Architect** | GodotPrompter | Plans, `.gd`, shaders, unit tests | Hand-edit scenes |
| **Builder** | GDAI Builder | Scenes, materials, F5, `.gdai_built` | Replace architect |
| **QA** | QA Agent | L0–L2 gates, evidence, bugs | Mark ship without gates |
| **Integration** | Flow Agent | L4/L5 integration/E2E | Build scenes |
| **Debugger** | Analyze Agent | Godotiq diagnosis | Scene mutations |
| **Release** | Release Agent | Tags, `run_cd_gates.sh`, export | Features |
| **Visual** | Visual Agent | L2 jury evidence (palette/model/audio) | Bypass jury |
| **Human QA** | Human | L6 UAT sign-off | Before L0–L5 pass |

**Sprint Master:** none — **PM Agent** facilitates; **QA Agent** owns sprint review evidence.

---

## Session startup (every run)

```bash
bash tools/ensure_mcp_stack.sh
bash tools/check_mcp_ready.sh          # Builder, Flow, Debugger
bash tools/check_rr_compliance.sh      # All roles touching game/
```

**PM-only (`main` docs/issues):**
```bash
bash tools/run_docs_ci_checks.sh
```

---

## Default workflow (one feature)

```
READ  → zone row in ENVIRONMENT_KITS.md + RENDERING_GUIDE.md
PLAN  → GodotPrompter: shaders, scripts, node tree, gate IDs
BUILD → GDAI MCP: scenes, materials, lights, F5
DEBUG → Godotiq (on failure only)
TEST  → QA L0–L2; Flow L4/L5 if flows/scenes changed
SHIP  → commit; gates PASS; check_asset_compliance.sh
```

---

## Situation → tool (conflict resolver)

| Situation | Use |
|-----------|-----|
| Edit `.tscn` / reparent nodes | **GDAI MCP only** |
| Combat/signal hang | **Godotiq** `signal_map`, `trace_flow` |
| Menu/combat automated test | **MCP Pro** `run_test_scenario` |
| Zone wood/stone texture | ComfyUI/Material Maker → **GDAI** assign |
| UI ink frame / icons | GameLab → **GDAI** assign |
| Balance / dialogue / flags | **`game/data/`** PR to `main` |
| RC / beta / prod tag | **Release Agent** + `run_cd_gates.sh` |

---

## Handoff minimums

**Architect → Builder:** design doc row, node tree, shader/uniform list, inspector targets, gate IDs.

**Builder → QA:** commit SHA, `game/scenes/.gdai_built` (`verified_f5=true`), scenes touched, screenshots if visual.

**QA → PM (pass):** gate report with commit + gate IDs + evidence paths.

**QA → Architect (fail):** `bash tools/qa_emit_remediation.sh <brief-id>` + gate ID in issue.

---

## QA gate layers

| Layer | Who | Examples |
|-------|-----|----------|
| L0 | Shell / QA | `L0_story_data`, `L0_rr_compliance` |
| L1 | QA | `L1_unit_tests` |
| L2 | QA + Visual | `L2_scene_primitives`, `L2_visual_palette`, jury |
| L3 | Builder + QA | GDAI F5 + `.gdai_built` |
| L4 | Flow | `L4_integration` |
| L5 | Flow | `L5_e2e_three_endings` |
| L6 | Human | Playtest sign-off — **after** L0–L5 |

**Policy:** WARN ≠ PASS · SKIP ≠ PASS · F5 alone ≠ visual PASS.

---

## Branch & environment

| Target | Branch | Lead agent | Contents |
|--------|--------|------------|----------|
| Design | `main` | PM | `docs/`, `game/data/`, `tools/` |
| Implementation | `game/development` | Architect + Builder | Godot project, scenes, assets |
| UAT artifact | tag on `game/development` | Release | `v*-rc*`, `v*-beta*` |
| Ship | tag + Steam | Release + Human | `v1.0.*` after M6 checklist |

---

## Sprint batches (AI-native)

- Close cycle when **gate evidence is on PR** — not when calendar week ends.
- **Micro:** 1–3 issues · **Standard:** ≤10 issues · **Integration:** L4/L5 green.
- Config: `game/data/qa/sprint_phases.json` · Policy: `docs/AGILE_WITHIN_PHASES.md` §12.1.

---

## Forbidden without user override

- Hand-editing ship `.tscn` in Cursor  
- Gameplay/visual work with GDAI disconnected  
- MCP Pro / Godotiq for scene mutations  
- Kenney kits, unknown-license web assets  
- Summer Engine, Fennara (fourth scene editor)  
- Skipping phase gates via sprint reprioritization  

---

## Quick commands

```bash
bash tools/run_ci_checks.sh              # game/development full CI
bash tools/run_docs_ci_checks.sh         # main docs/data CI
bash tools/run_cd_gates.sh --channel rc  # pre-export
bash tools/check_asset_compliance.sh     # before commit with assets
python3 tools/validate_story_data.py     # L0_story_data
```

---

## Related docs (full detail)

| Doc | Contents |
|-----|----------|
| `.cursorrules` §0–§1 | Hard rules, combined workflow |
| `docs/MCP_STACK.md` | Full toolchain, install, troubleshooting |
| `docs/MULTI_AGENT_TEAM.md` | Handoffs, parallel patterns, definition of done |
| `docs/AGILE_WITHIN_PHASES.md` | Sprint facilitator, AI-native cadence |
| `docs/ACCEPTANCE_CRITERIA.md` | Gate thresholds |
| `docs/AI_DEV_WORKFLOW.md` | Extended command reference |
