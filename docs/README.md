# Tides of Urashima — Documentation Index

**Start here (humans).** Agents: load [`ops/BOOT.md`](ops/BOOT.md) + [`INDEX.yaml`](INDEX.yaml) — not this whole page.

| Resource | Purpose |
|----------|---------|
| [ops/BOOT.md](ops/BOOT.md) | Thin always-on boot card |
| [INDEX.yaml](INDEX.yaml) | Role → must_read router |
| [llms.txt](llms.txt) | LLM discovery map |
| [_meta/DOC_LIBRARY_ADR.md](_meta/DOC_LIBRARY_ADR.md) | Why this layout |
| [_meta/FRONTMATTER.md](_meta/FRONTMATTER.md) | Required YAML frontmatter |
| [_meta/redirects.yaml](_meta/redirects.yaml) | Legacy path → new path |

Large bibles are split into packs (load hub + one pack):

| Hub | Packs |
|-----|-------|
| [AI_TESTING_SPEC.md](ops/qa/AI_TESTING_SPEC.md) | [ops/qa/testing/](ops/qa/testing/) |
| [MCP_STACK.md](ops/agents/MCP_STACK.md) | [ops/agents/mcp/](ops/agents/mcp/) |
| [AI_DEV_WORKFLOW.md](ops/workflow/AI_DEV_WORKFLOW.md) | [ops/workflow/ai_dev/](ops/workflow/ai_dev/) |
| [RR_CHEATSHEET.md](ops/cheat-sheets/RR_CHEATSHEET.md) | [ops/cheat-sheets/rr/](ops/cheat-sheets/rr/) |
| [CHARACTER_BIBLE.md](design/art/CHARACTER_BIBLE.md) | [design/art/characters/](design/art/characters/) |
| [AUDIO_PRODUCTION_GUIDE.md](design/audio/AUDIO_PRODUCTION_GUIDE.md) | [design/audio/production/](design/audio/production/) |
| [DATA_ARCHITECTURE.md](engineering/technical/DATA_ARCHITECTURE.md) | [engineering/technical/data/](engineering/technical/data/) |

```bash
python3 tools/resolve_docs.py --list-roles
python3 tools/resolve_docs.py builder_zone
python3 tools/resolve_docs.py architect --issue P1-01 --budget 12000
python3 tools/refresh_docs_catalogs.py   # after adding docs
```

---

## Folder map

| Bucket | Path | Contents |
|--------|------|----------|
| **Design** | [design/](design/) | vision · world · gameplay · art · audio · ui |
| **Engineering** | [engineering/](engineering/) | TDD · data · coding standards |
| **Ops** | [ops/](ops/) | agents · workflow · ci-cd · qa · cheat-sheets · sprints |
| **Briefs** | [briefs/](briefs/) | AI generation briefs (task-scoped) |
| **Archive** | [archive/](archive/) | deprecated · compliance reports · pitch |

### Design

| Doc | Purpose |
|-----|---------|
| [GDD.md](design/vision/GDD.md) | Master game design |
| [STORYBOARD.md](design/vision/STORYBOARD.md) | 20-scene narrative bible |
| [LEVEL_DESIGN.md](design/world/LEVEL_DESIGN.md) | Zones, interactables |
| [ENVIRONMENT_KITS.md](design/world/ENVIRONMENT_KITS.md) | Per-zone lighting kits |
| [COMBAT_SYSTEMS.md](design/gameplay/COMBAT_SYSTEMS.md) | Turn combat |
| [ART_DIRECTION.md](design/art/ART_DIRECTION.md) | Palette, silhouettes |
| [RENDERING_GUIDE.md](design/art/RENDERING_GUIDE.md) | Tonemap, fog, glow |
| [ART_AUTOMATION_PIPELINE.md](design/art/ART_AUTOMATION_PIPELINE.md) | Art/audio gen tiers |
| [AUDIO_PRODUCTION_GUIDE.md](design/audio/AUDIO_PRODUCTION_GUIDE.md) | Buses, loudness |
| [UI_UX_FLOW.md](design/ui/UI_UX_FLOW.md) | Menus, HUD |

### Engineering

| Doc | Purpose |
|-----|---------|
| [CODING_STANDARDS_HUB.md](engineering/technical/CODING_STANDARDS_HUB.md) | Languages + CI gates |
| [TECHNICAL_DESIGN.md](engineering/technical/TECHNICAL_DESIGN.md) | Runtime architecture |
| [DATA_ARCHITECTURE.md](engineering/technical/DATA_ARCHITECTURE.md) | JSON spine |
| [CODE_BASE_CLASS_RULES.md](engineering/technical/CODE_BASE_CLASS_RULES.md) | Extend-only bases |

### Ops

| Doc | Purpose |
|-----|---------|
| [RR_CHEATSHEET.md](ops/cheat-sheets/RR_CHEATSHEET.md) | Roles & handoffs |
| [CONTROLS_CHEATSHEET.md](ops/cheat-sheets/CONTROLS_CHEATSHEET.md) | CI / PR controls |
| [MCP_STACK.md](ops/agents/MCP_STACK.md) | MCP toolchain |
| [IMPLEMENTATION_PLAN.md](ops/workflow/IMPLEMENTATION_PLAN.md) | Phases 0–8 |
| [ACCEPTANCE_CRITERIA.md](ops/qa/ACCEPTANCE_CRITERIA.md) | Measurable gates |
| [CI.md](ops/ci-cd/CI.md) | GitHub Actions |

Full catalogs live in each folder; use `INDEX.yaml` for role packs.

---

## Authority chain

| Priority | Document |
|----------|----------|
| 1 | [IMPLEMENTATION_PLAN.md](ops/workflow/IMPLEMENTATION_PLAN.md) |
| 1b | [DEVELOPMENT_LIFECYCLE.md](ops/workflow/DEVELOPMENT_LIFECYCLE.md) · [BRANCHING.md](ops/workflow/BRANCHING.md) |
| 2 | [MILESTONES.md](ops/workflow/MILESTONES.md) |
| 3 | [TECHNICAL_DESIGN.md](engineering/technical/TECHNICAL_DESIGN.md) |
| 4 | [DATA_ARCHITECTURE.md](engineering/technical/DATA_ARCHITECTURE.md) + `game/data/` |
| 5 | [MCP_STACK.md](ops/agents/MCP_STACK.md) · [ART_AUTOMATION_PIPELINE.md](design/art/ART_AUTOMATION_PIPELINE.md) · [`.cursorrules`](../.cursorrules) |

**Numeric values:** `game/data/*.json` wins over prose.

---

## Quick links by need

| I need to… | Read |
|------------|------|
| Boot an agent | [BOOT.md](ops/BOOT.md) · `python3 tools/resolve_docs.py <role>` |
| Understand the game | [GDD.md](design/vision/GDD.md) → [STORYBOARD.md](design/vision/STORYBOARD.md) |
| Build next phase | [IMPLEMENTATION_PLAN.md](ops/workflow/IMPLEMENTATION_PLAN.md) |
| Coding standards | [CODING_STANDARDS_HUB.md](engineering/technical/CODING_STANDARDS_HUB.md) |
| Zone lighting | [RENDERING_GUIDE.md](design/art/RENDERING_GUIDE.md) + [ENVIRONMENT_KITS.md](design/world/ENVIRONMENT_KITS.md) |
| QA pass/fail | [ACCEPTANCE_CRITERIA.md](ops/qa/ACCEPTANCE_CRITERIA.md) |
| Cloud factory | [FACTORY_SETUP_GUIDE.md](ops/agents/FACTORY_SETUP_GUIDE.md) |

---

## Data layer

| Path | Purpose |
|------|---------|
| [game/data/README.md](../game/data/README.md) | Load API, schema |
| `game/data/story/scenes.json` | Scene spine |

```bash
python3 tools/validate_story_data.py
```

---

## Deprecated / archive

| Old | New |
|-----|-----|
| `docs/art/…` | `docs/design/art/…` |
| `docs/qa/…` | `docs/ops/qa/…` |
| `docs/agents/…` | `docs/ops/agents/…` |
| `docs/technical/…` | `docs/engineering/technical/…` |
| `docs/generation_briefs/…` | `docs/briefs/…` |
| [GDAI_REGEN_PLAN.md](archive/deprecated/GDAI_REGEN_PLAN.md) | [IMPLEMENTATION_PLAN.md](ops/workflow/IMPLEMENTATION_PLAN.md) |

See [`_meta/redirects.yaml`](_meta/redirects.yaml) for the full map.
