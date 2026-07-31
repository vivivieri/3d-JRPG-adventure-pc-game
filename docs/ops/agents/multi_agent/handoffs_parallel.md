---
id: handoffs-parallel
type: explanation
phase: [0, 1]
audience: [pm, builder, qa]
status: active
authority: ops
tokens_est: 685
summary: "Handoffs, parallel patterns, env matrix"
---
# Multi-Agent Team — Handoffs, parallel patterns, env matrix

**Hub:** [`MULTI_AGENT_TEAM.md`](../MULTI_AGENT_TEAM.md)

## 4. Handoff contracts

### Architect → Builder

Must include:
- Design doc section (e.g. `ENVIRONMENT_KITS.md` row)
- Node tree outline
- Shader/uniform list
- Properties to set in inspector (GDAI applies)
- Target gate IDs (e.g. `L2_scene_primitives`, `L2_visual_palette`)
- **Component scene** from `LEVEL_DESIGN.md` §1b / `base_classes.json` (if applicable)
- **Base class** to extend — never new `CharacterBody3D` controller (`CODE_BASE_CLASS_RULES.md`)
- **Generation brief** for art assets — `docs/briefs/<id>.md` when present (`GENERATION_READINESS.md`); brief is plan input only — not ship approval

**Core helpers** (`docs/engineering/technical/GDSCRIPT_REGENERATION.md`): Architect delivers ported `.gd` + unit tests; Builder registers **EventBus** autoload only — does not author helper logic.

### Core helper R&R (summary)

| Step | Owner | Deliverable |
|------|-------|-------------|
| Spec + `tools/*_lib.py` on `main` | Architect | `helpers_registry.json`, reference tests PASS |
| `.gd` port on `game/development` | Architect | `game/scripts/core/*.gd`, `game/tests/unit/` |
| `project.godot` autoload | Builder | GDAI MCP — EventBus at minimum in P1-00 |
| Gate verification | QA | `L0_reference_libs`, `L1_unit_tests` |
| When to port | PM | `dispatch_by_phase` in `helpers_registry.json` |

### Builder → QA

Must include:
- `game/scenes/.gdai_built` updated (`verified_f5=true`)
- Commit SHA
- Screenshot paths under `artifacts/screenshots/` if visual
- List of scenes touched

### QA → PM (pass)

```markdown

## 5. Parallel agent patterns

| Situation | Agents in parallel |
|-----------|-------------------|
| Zone art + combat tuning | Architect (combat JSON) ∥ Builder (zone scene) — **different files** |
| Visual jury + integration | QA Agent (jury) ∥ Flow Agent (L4) — after Builder handoff |
| Doc update + implementation | PM (main branch docs) ∥ Builder (`game/development`) |

**Never parallel two agents on the same `.tscn`** — GDAI MCP single-writer.

---


## 6. Environment × agent matrix

| Environment | Lead agent | Supporting agents |
|-------------|------------|-------------------|
| Design (`main`) | PM | Architect (data JSON only) |
| Development | Architect + Builder | Debugger on demand |
| QA | QA Agent | Flow Agent for L4+ |
| UAT | PM + Human | Release Agent (artifact) |
| Preprod | Release Agent | QA Agent (gate verify) |
| Production | Release Agent | PM (sign-off) |

---
