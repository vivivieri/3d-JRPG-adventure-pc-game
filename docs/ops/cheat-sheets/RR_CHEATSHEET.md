---
id: rr-cheatsheet
type: reference
audience: [pm, builder, qa]
status: active
authority: ops
tokens_est: 3025
summary: "**Print this:** One-page reference for every agent session"
---
# R&R Cheat Sheet — Roles & Responsibilities

**Version:** 1.5
**Print this:** One-page reference for every agent session
**Companion:** `docs/ops/cheat-sheets/CONTROLS_CHEATSHEET.md` — how each role is **enforced** (CI, PR, branch protection)
**Authority:** `.cursorrules` §0–§1 · `docs/ops/agents/MCP_STACK.md` · `docs/ops/agents/MULTI_AGENT_TEAM.md` · `docs/ops/workflow/AGILE_WITHIN_PHASES.md` §11

---
## Golden rules

1. **GodotPrompter writes code** → **GDAI MCP builds scenes** → **QA proves gates** — never skip a handoff.
2. **Only GDAI MCP** may create/edit `.tscn`, nodes, materials, lights, inspector values.
3. **Never hand-edit `.tscn` in Cursor** when GDAI is available (`L0_rr_compliance`).
4. **Scene diff → update `.gdai_built`** in the same PR (`L3_gdai_built` in CI).
5. **P0 MCP required:** `godot-mcp`, `godotiq`, `godot-mcp-pro` — if missing, **STOP and notify user**.
6. **One writer per `.tscn`** — never parallel two agents on the same scene file.
7. **`docs/` + `game/data/`** are design truth — not sprint backlog reprioritization.
8. **Cross-cutting factory features** — register in `workflow_integration_registry.json`; run `bash tools/check_feature_integration.sh --remind` before merge (`docs/ops/qa/WORKFLOW_INTEGRATION.md`).
9. **Open PRs with the role template** — `game_development` or `docs_main` checklist (`docs/ops/cheat-sheets/CONTROLS_CHEATSHEET.md`).
10. **Extend base classes only** — no new `CharacterBody3D` stacks (`docs/engineering/technical/CODE_BASE_CLASS_RULES.md`).

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

## Session startup (every run)

> Full detail: [`rr/session.md`](rr/session.md) — load only when needed.

## How to pick work (dev & QA)

> Full detail: [`rr/pick_work.md`](rr/pick_work.md) — load only when needed.

## Performance review (required — not code review)

> Full detail: [`rr/performance_review.md`](rr/performance_review.md) — load only when needed.

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
| Spec refinement (design time) | **`main` only** — docs + data + `tools/*_lib.py`; **never** `.gd`/`.tscn` (`SPEC_FIRST_DEVELOPMENT.md` §10) |
| Core helper spec / Python ref | **Architect** PR to `main` — `docs/engineering/technical/GDSCRIPT_REGENERATION.md` |
| Phase 1 visuals port (P1-01) | **Architect** on `game/development` — `GDSCRIPT_REGENERATION.md` §10 · `bash tools/regenerate_phase1_visuals.sh` |
| Core helper `.gd` port | **Architect** on `game/development` — PM dispatch by phase |
| EventBus autoload registration | **Builder** (GDAI MCP) — after Architect `event_bus.gd` |
| RC / beta / prod tag | **Release Agent** + `run_cd_gates.sh` |

---

## Handoff minimums

**Architect → Builder:** design doc row, node tree, shader/uniform list, inspector targets, gate IDs, **component scene** to instance (`LEVEL_DESIGN.md` §1b); for art assets, link or attach `docs/briefs/<id>.md` when present (`GENERATION_READINESS.md`). On-direction = bible + brief; feel polish = human L6 feedback loop (`MODEL_QA.md` §9).

**Architect → Builder (core helpers):** `helpers_registry.json` entry + Python reference path; GDScript file at `gdscript_path` committed on `game/development`; for **EventBus** only — Builder registers autoload in `project.godot` via GDAI MCP (`docs/engineering/technical/GDSCRIPT_REGENERATION.md` §2).

**Builder → QA:** commit SHA, `game/scenes/.gdai_built` (`verified_f5=true`), scenes touched, screenshots if visual.

**QA → PM (pass):** gate report in **PR body** (template block) with commit + gate IDs + evidence paths.

**QA → Architect (fail):** `bash tools/qa_emit_remediation.sh <brief-id>` + gate ID in issue.

**PM → all:** ensure linked issue + correct **PR template** before review.

---

## Escalation ladder (no infinite dev↔QA loops)

`docs/ops/qa/ESCALATION_POLICY.md` · `game/data/qa/escalation_policy.json` · `tools/pm_escalate.py`

| Tier | Owner | Cap → next |
|------|-------|-----------|
| 1 · dev ↔ QA loop | dev + QA | **max 3 reopens** → arbitration |
| 2 · Arbitration | **Architect (Design Authority / SA)** | classify root cause; resolve or (needs business decision) → Product Owner |
| 3 · Product Owner | Human (Telegram) | final — `amend_requirement`/`descope`/`wont_fix`/`approve_as_is`/`reprioritize` |

Only the arbiter (Architect/SA) or the Product Owner may change a requirement — that is what breaks the loop. Every tier is capped; escalation goes **up**, never sideways.

## QA gate layers

> Full detail: [`rr/qa_gates.md`](rr/qa_gates.md) — load only when needed.

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
- Config: `game/data/qa/sprint_phases.json` · Policy: `docs/ops/workflow/AGILE_WITHIN_PHASES.md` §12.1.

---

## Forbidden without user override

- Hand-editing ship `.tscn` in Cursor
- Gameplay/visual work with GDAI disconnected
- MCP Pro / Godotiq for scene mutations
- Kenney kits, unknown-license web assets
- Summer Engine, Fennara (fourth scene editor)
- Skipping phase gates via sprint reprioritization
- **Cross-cutting factory feature merged without `workflow_integration_registry.json` entry** — run `bash tools/check_feature_integration.sh --remind`

---

## Quick commands

```bash
bash tools/run_ci_checks.sh              # game/development full CI
bash tools/run_docs_ci_checks.sh         # main docs/data CI
bash tools/check_rr_compliance.sh        # L0 — Builder R&R
bash tools/check_l3_gdai_built.sh        # L3 — scene diff needs .gdai_built
bash tools/run_cd_gates.sh --channel rc  # pre-export
bash tools/check_asset_compliance.sh     # before commit with assets
bash tools/run_perf_review_checks.sh     # L2 — perf thresholds catalog
python3 tools/validate_story_data.py     # L0_story_data
```

---


## Factory hooks (names for L0_workflow_integration)

| Hook | Command / artifact |
|------|--------------------|
| Close session | `bash tools/run_post_agent_cycle.sh` |
| Watchdog | `bash tools/run_factory_watchdog.sh` |
| Factory setup | `FACTORY_SETUP_GUIDE` · `docs/ops/agents/FACTORY_SETUP_GUIDE.md` |
| Stakeholder | `bash tools/pm_emit_stakeholder_report.sh` |
| Alignment | `bash tools/run_alignment_audit.sh` · `audit_radar_spec.png` |
| Tournament | `bash tools/run_candidate_tournament.sh` |

## Related docs (full detail)

| Doc | Contents |
|-----|----------|
| `.cursorrules` §0–§1 | Hard rules, combined workflow |
| **`docs/engineering/technical/CODE_BASE_CLASS_RULES.md`** | **Extend-only code bases** + license-safe 3D sources |
| **`docs/ops/cheat-sheets/CONTROLS_CHEATSHEET.md`** | **Enforcement** — CI, PR templates, branch protection |
| `docs/ops/agents/MCP_STACK.md` | Full toolchain, install, troubleshooting |
| `docs/ops/agents/MULTI_AGENT_TEAM.md` | Handoffs, parallel patterns, definition of done |
| `docs/ops/workflow/AGILE_WITHIN_PHASES.md` | Sprint facilitator, AI-native cadence |
| **`docs/ops/agents/SPRINT_ORCHESTRATION.md`** | **Enforced dispatch** — no self-assign |
| **`docs/ops/agents/PM_AGENT_RUNBOOK.md`** | PM session steps, stale escalation |
| **`docs/ops/qa/AGENT_SESSION_TELEMETRY.md`** | **Auto token/duration logging** — factory integration §9 |
| `docs/ops/sprints/Phase1-Sprint1-issues.md` | Active sprint issue bodies |
| `docs/ops/qa/ACCEPTANCE_CRITERIA.md` | Gate thresholds |
| **`docs/ops/qa/PERFORMANCE_BASELINE.md`** | **Hardware + environment baseline for perf evidence** |
| **`docs/ops/qa/AI_TESTING_SPEC.md`** | **L0–L6 test layers, screenshots, E2E video** |
| **`docs/design/art/VISUAL_QA.md`** | **Screenshot + vision jury procedure** |
| `docs/ops/ci-cd/CI.md` | GitHub Actions gate matrix |
| `docs/ops/ci-cd/GITHUB_SETUP.md` | PAT + `setup_github_project.sh` |
| `docs/ops/workflow/AI_DEV_WORKFLOW.md` | Extended command reference |
