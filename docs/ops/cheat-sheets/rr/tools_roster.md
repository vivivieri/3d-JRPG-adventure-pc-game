---
id: tools-roster
type: reference
audience: [pm, builder, qa]
status: active
authority: ops
tokens_est: 915
summary: "Controls, tools, agent roster"
---
# R&R Cheat Sheet — Controls, tools, agent roster

**Hub:** [`RR_CHEATSHEET.md`](../RR_CHEATSHEET.md)

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
| UI art | **GameLab MCP** | UI PNG/WebP → `game/assets/textures/ui/` | Place nodes / `.tscn` |
| Zone albedo | **ComfyUI / Material Maker** | Tileables → `palette_remap.py` | Assign in editor (→ GDAI) |
| Hero 3D | **Meshy/Tripo/Rodin + Blender** | GLB import | Scene placement (→ GDAI) |
| Audio | **ACE-Step / ElevenLabs** + `audio_qa_catalog.json` | BGM hero jury + P0 VO jury (`docs/design/audio/AUDIO_QA.md`) | — |
| Design data | **`docs/` + `game/data/`** | Story, flags, skills, gates | — |
| Core helper spec + Python ref | **Architect** (`main`) | `helpers_registry.json`, `tools/*_lib.py` | Ship `.gd` on `main` |
| Core helper GDScript port | **Architect** (`game/development`) | `game/scripts/core/*.gd`, unit tests | Autoload registration |
| Core helper autoload wire-up | **Builder** (GDAI MCP) | `project.godot` autoloads | Author helper `.gd` logic |

---


## Agent roster

| Role | Agent | Owns | Must NOT | Control hook |
|------|-------|------|----------|--------------|
| **PM / Sprint facilitator** | PM Agent | Issues, milestones, orchestrator dispatch, escalations | Write code or `.tscn` | **`run_pm_orchestrator.sh` PASS**; `L0_sprint_board` |
| **Architect** | GodotPrompter | Plans, `.gd`, shaders, unit tests; **Design Authority (SA)** for arbitration | Hand-edit scenes | `L1`, `L1_gdscript_lint`, `L0_base_class_compliance`; **owns base classes** |
| **Builder** | GDAI Builder | Scenes, materials, F5, `.gdai_built` | Replace architect | `L0_rr`, **`L3_gdai_built`**, **component `.tscn` catalog** |
| **QA** | QA Agent | L0–L3 gates, evidence, bugs | Mark ship without gates | CI green + **gate report in PR** |
| **Integration** | Flow Agent | L4/L5 integration/E2E | Build scenes | `L4_integration`; L5 in CD beta/prod |
| **Debugger** | Analyze Agent | Godotiq diagnosis | Scene mutations | Policy only (read-only tools) |
| **Release** | Release Agent | Tags, `run_cd_gates.sh`, export | Features | `run_cd_gates.sh`; CD workflows |
| **Visual** | Visual Agent | L2 jury evidence (palette/model/audio/vo) | Bypass jury | L2 jury scripts + thresholds |
| **Factory Analyst** | Analyst Agent | Token/duration rollups, sprint efficiency reports | Write game code or scenes | `analyze_agent_session_telemetry.py` |
| **Human QA** | Human | L6 UAT sign-off | Before L0–L5 pass | `STEAM_RELEASE_CHECKLIST`; CD prod |

**Sprint Master:** none — **PM Agent** facilitates; **QA Agent** owns sprint review evidence.

---
