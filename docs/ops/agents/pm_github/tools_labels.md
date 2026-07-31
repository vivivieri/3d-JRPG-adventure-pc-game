---
id: tools-labels
type: how-to
phase: [0, 1]
audience: [pm]
status: active
authority: ops
tokens_est: 690
summary: "Tool choice + label taxonomy"
---
# Project Management — Tool choice + label taxonomy

**Hub:** [`PROJECT_MANAGEMENT.md`](../PROJECT_MANAGEMENT.md)

## 1. Tool choice

| Tool | Tier | Use for | Status |
|------|------|---------|--------|
| **GitHub Issues** | **P0 required** | Bugs, gate failures, features, env labels | ✅ Use now |
| **GitHub Actions** | **P0** | CI/CD logs, artifact retention | ✅ Live |
| **GitHub Projects** | P1 | Kanban by milestone / env | Optional board |
| **Linear MCP** | P1 optional | Sprint cycles inside each phase | Needs auth — see `AGILE_WITHIN_PHASES.md` |
| **Notion MCP** | P2 optional | Design notes, meeting notes | Needs auth; **not** design authority (`docs/` wins) |
| **Datadog MCP** | N/A ship | Not needed for Godot indie | Skip |

**Rule:** `docs/` + `game/data/` remain authoritative for game design. PM tools track **work**, not **spec**.

**One-time GitHub config:** `bash tools/setup_github_project.sh` — see `docs/ops/ci-cd/GITHUB_SETUP.md`.

---


## 2. GitHub Issues — label taxonomy

### Environment

| Label | Meaning |
|-------|---------|
| `env/development` | Active implementation |
| `env/qa` | Automated gate failure or CI |
| `env/uat` | Human playtest / RC build |
| `env/preprod` | Steam beta |
| `env/production` | Ship blocker |

### Severity (bugs)

| Label | Meaning |
|-------|---------|
| `severity/S0` | Blocker |
| `severity/S1` | Major |
| `severity/S2` | Minor |
| `severity/S3` | Polish |

### Gate / domain

| Label | Example |
|-------|---------|
| `gate/L0_story_data` | Validator fail |
| `gate/L0_base_classes` | Base class registry fail |
| `gate/L0_base_class_compliance` | Rogue controller fail |
| `gate/L1_unit_tests` | Unit test fail |
| `gate/L1_gdscript_lint` | GDScript lint fail |
| `gate/L2_animation_whitelist` | Animation name / required floor fail |
| `gate/L2_feel_smoke` | Feel constant fail |
| `gate/L2_glb_import` | GLB post-import fail |
| `gate/L4_integration` | Flow scenario fail |
| `gate/L5_e2e` | Ending path fail |
| `domain/visual` | Art jury |
| `domain/audio` | LUFS / jury |
| `domain/flow` | Soft-lock |

### Agent / status

| Label | Meaning |
|-------|---------|
| `agent/architect` | Needs GodotPrompter |
| `agent/builder` | Needs GDAI MCP |
| `agent/qa` | Needs gate run |
| `agent/analyst` | Factory efficiency rollup (telemetry) |
| `agent/release` | Needs tag/CD |
| `status/blocked` | Waiting on MCP/secrets/human |
| `status/in-progress` | Active agent |
| `status/done` | Verified fixed |

### Milestone

Link issues to GitHub Milestones matching `docs/ops/workflow/MILESTONES.md`: `M1-core`, `M5-art`, `M6-steam`.

---
