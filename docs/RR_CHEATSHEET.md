# R&R Cheat Sheet — Roles & Responsibilities

**Version:** 1.1  
**Print this:** One-page reference for every agent session  
**Companion:** `docs/CONTROLS_CHEATSHEET.md` — how each role is **enforced** (CI, PR, branch protection)  
**Authority:** `.cursorrules` §0–§1 · `docs/MCP_STACK.md` · `docs/MULTI_AGENT_TEAM.md` · `docs/AGILE_WITHIN_PHASES.md` §11

---

## Golden rules

1. **GodotPrompter writes code** → **GDAI MCP builds scenes** → **QA proves gates** — never skip a handoff.
2. **Only GDAI MCP** may create/edit `.tscn`, nodes, materials, lights, inspector values.
3. **Never hand-edit `.tscn` in Cursor** when GDAI is available (`L0_rr_compliance`).
4. **Scene diff → update `.gdai_built`** in the same PR (`L3_gdai_built` in CI).
5. **P0 MCP required:** `godot-mcp`, `godotiq`, `godot-mcp-pro` — if missing, **STOP and notify user**.
6. **One writer per `.tscn`** — never parallel two agents on the same scene file.
7. **`docs/` + `game/data/`** are design truth — not sprint backlog reprioritization.
8. **Open PRs with the role template** — `game_development` or `docs_main` checklist (`docs/CONTROLS_CHEATSHEET.md`).

---

## Controls at a glance

| What | Where |
|------|-------|
| Who owns what | **This doc** — roster + handoffs |
| What blocks merge | **`CONTROLS_CHEATSHEET.md`** — CI gates, PR checklists, branch protection |
| PR role checkboxes | `.github/PULL_REQUEST_TEMPLATE/game_development.md` |
| Builder scene proof | `L0_rr_compliance` + **`L3_gdai_built`** (`check_l3_gdai_built.sh`) |
| Apply branch protection | `bash tools/setup_github_project.sh` (+ `GH_TOKEN`) |

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

| Role | Agent | Owns | Must NOT | Control hook |
|------|-------|------|----------|--------------|
| **PM / Sprint facilitator** | PM Agent | Issues, milestones, env promotion, batch planning | Write code or `.tscn` | Issue template: phase + gates; PR template opened |
| **Architect** | GodotPrompter | Plans, `.gd`, shaders, unit tests | Hand-edit scenes | `L1_unit_tests`; handoff in PR/issue |
| **Builder** | GDAI Builder | Scenes, materials, F5, `.gdai_built` | Replace architect | `L0_rr_compliance`, **`L3_gdai_built`**, `L2_*` |
| **QA** | QA Agent | L0–L3 gates, evidence, bugs | Mark ship without gates | CI green + **gate report in PR** |
| **Integration** | Flow Agent | L4/L5 integration/E2E | Build scenes | `L4_integration`; L5 in CD beta/prod |
| **Debugger** | Analyze Agent | Godotiq diagnosis | Scene mutations | Policy only (read-only tools) |
| **Release** | Release Agent | Tags, `run_cd_gates.sh`, export | Features | `run_cd_gates.sh`; CD workflows |
| **Visual** | Visual Agent | L2 jury evidence (palette/model/audio) | Bypass jury | L2 jury scripts + thresholds |
| **Human QA** | Human | L6 UAT sign-off | Before L0–L5 pass | `STEAM_RELEASE_CHECKLIST`; CD prod |

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
TEST  → QA L0–L3; Flow L4/L5 if flows/scenes changed
MERGE → PR template checkboxes + CI green (see CONTROLS_CHEATSHEET)
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

**QA → PM (pass):** gate report in **PR body** (template block) with commit + gate IDs + evidence paths.

**QA → Architect (fail):** `bash tools/qa_emit_remediation.sh <brief-id>` + gate ID in issue.

**PM → all:** ensure linked issue + correct **PR template** before review.

---

## QA gate layers

| Layer | Who | Examples |
|-------|-----|----------|
| L0 | Shell / QA | `L0_story_data`, `L0_rr_compliance` |
| L1 | QA | `L1_unit_tests` |
| L2 | QA + Visual | `L2_scene_primitives`, `L2_visual_palette`, jury |
| L3 | Builder + QA | **`L3_gdai_built`** (CI — marker in scene diff) · **`L3_gdai_f5`** (editor F5) |
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
bash tools/check_rr_compliance.sh        # L0 — Builder R&R
bash tools/check_l3_gdai_built.sh        # L3 — scene diff needs .gdai_built
bash tools/run_cd_gates.sh --channel rc  # pre-export
bash tools/check_asset_compliance.sh     # before commit with assets
python3 tools/validate_story_data.py     # L0_story_data
```

---

## Related docs (full detail)

| Doc | Contents |
|-----|----------|
| `.cursorrules` §0–§1 | Hard rules, combined workflow |
| **`docs/CONTROLS_CHEATSHEET.md`** | **Enforcement** — CI, PR templates, branch protection |
| `docs/MCP_STACK.md` | Full toolchain, install, troubleshooting |
| `docs/MULTI_AGENT_TEAM.md` | Handoffs, parallel patterns, definition of done |
| `docs/AGILE_WITHIN_PHASES.md` | Sprint facilitator, AI-native cadence |
| `docs/ACCEPTANCE_CRITERIA.md` | Gate thresholds |
| `docs/CI.md` | GitHub Actions gate matrix |
| `docs/GITHUB_SETUP.md` | PAT + `setup_github_project.sh` |
| `docs/AI_DEV_WORKFLOW.md` | Extended command reference |
