# Tides of Urashima — Documentation Index

**Start here (humans).** Agents: load [`ops/BOOT.md`](ops/BOOT.md) + [`INDEX.yaml`](INDEX.yaml) — not this whole page.

| Resource | Purpose |
|----------|---------|
| [ops/BOOT.md](ops/BOOT.md) | Thin always-on boot card |
| [INDEX.yaml](INDEX.yaml) | Role + task → must_read router |
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
| [RENDERING_GUIDE.md](design/art/RENDERING_GUIDE.md) | [design/art/rendering/](design/art/rendering/) |
| [MODEL_QA.md](design/art/MODEL_QA.md) | [design/art/model_qa/](design/art/model_qa/) |
| [ITEMS_3D_MODEL_GUIDE.md](design/art/ITEMS_3D_MODEL_GUIDE.md) | [design/art/items/](design/art/items/) |
| [NARRATIVE_WRITING_GUIDE.md](design/vision/NARRATIVE_WRITING_GUIDE.md) | [design/vision/narrative/](design/vision/narrative/) |
| [IMPLEMENTATION_PLAN.md](ops/workflow/IMPLEMENTATION_PLAN.md) | [ops/workflow/implementation/](ops/workflow/implementation/) |
| [CLOUD_AGENT_SETUP_RUNBOOK.md](ops/agents/CLOUD_AGENT_SETUP_RUNBOOK.md) | [ops/agents/cloud_setup/](ops/agents/cloud_setup/) |
| [AGILE_WITHIN_PHASES.md](ops/workflow/AGILE_WITHIN_PHASES.md) | [ops/workflow/agile/](ops/workflow/agile/) |
| [CURSOR_SECRETS_SETUP.md](ops/agents/CURSOR_SECRETS_SETUP.md) | [ops/agents/secrets/](ops/agents/secrets/) |
| [LEVEL_DESIGN.md](design/world/LEVEL_DESIGN.md) | [design/world/levels/](design/world/levels/) |
| [ENVIRONMENT_KITS.md](design/world/ENVIRONMENT_KITS.md) | [design/world/env_kits/](design/world/env_kits/) |
| [ART_DIRECTION.md](design/art/ART_DIRECTION.md) | [design/art/direction/](design/art/direction/) |
| [ART_AUTOMATION_PIPELINE.md](design/art/ART_AUTOMATION_PIPELINE.md) | [design/art/automation/](design/art/automation/) |
| [CI.md](ops/ci-cd/CI.md) | [ops/ci-cd/ci/](ops/ci-cd/ci/) |
| [DEVELOPMENT_LIFECYCLE.md](ops/workflow/DEVELOPMENT_LIFECYCLE.md) | [ops/workflow/lifecycle/](ops/workflow/lifecycle/) |
| [game-dev-factory](../packages/game-dev-factory/README.md) | Portable PM/lifecycle control plane + Cursor skills |
| [GDSCRIPT_REGENERATION.md](engineering/technical/GDSCRIPT_REGENERATION.md) | [engineering/technical/gdscript_regen/](engineering/technical/gdscript_regen/) |

```bash
python3 tools/resolve_docs.py --list-roles
python3 tools/resolve_docs.py --list-tasks
python3 tools/resolve_docs.py builder_zone
python3 tools/resolve_docs.py visual --issue P1-01 --budget 12000 --report artifacts/docs_pack_P1-01.txt
python3 tools/resolve_docs.py builder --task zone_lighting --phase 1
python3 tools/docs_pack_impact.py --base origin/main
python3 tools/pm_docs_preflight.py
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

## Docs pack enhance (progressive disclosure)

Agent packs are resolved by `tools/resolve_docs.py` (see `docs/INDEX.yaml`).

Recent efficiency work:

1. Specialty role remap (`tools/docs_role_map.py`) — `builder` + `zone_lighting` → `builder_zone`
2. Real deferred TL;DRs + calibrated `tokens_est` (`tools/fix_docs_frontmatter.py`)
3. Tasks: `visual_qa`, `acceptance_ci`, `audio_bgm`, `ui_cinematics`
4. Split hubs: `VISUAL_QA`, `GENERATION_READINESS`, `TECHNICAL_DESIGN`, `CODING_STANDARDS_HUB`, `RR`/`CONTROLS`, `QA_REMEDIATION`, `ACCEPTANCE_CRITERIA`
5. Zone-aware `env_kits/` + `levels/` attach from issue title
6. Machine `artifacts/docs_pack_<issue>.json`; session gate FAILs if resolve fails
7. Briefs/zones/characters are **budget-trimable** (boot + handoff stay protected)
8. Remaining splits: `STORYBOARD`, `GDD`, `MILESTONES`, `BOSS_DESIGNS`, `GDAI_CLOUD_SETUP`, `QA_AND_BUG_PROCESS`, `FLOW_QA`, thin `briefs/ruined_village`
9. Character pack auto-attach; `check_docs_pack_adherence.py` on post-cycle (**strict** — session gate auto-seeds `must_read` via `log_docs_read.py`)
10. Round 4: release/security/steam + language/factory/cinematics splits; `pack_catalog` in INDEX; phase tags ~100%; session gate inits `artifacts/docs_reads_<issue>.log`; thinner AGENTS/BOOT
11. Rounds 5–8: remaining fat hubs/leaves; then **pause** bulk thinning
12. Defrag: collapse arbitrary `part_a`/`part_b` halves + hub-of-hub nests ([#180](https://github.com/vivivieri/3d-JRPG-adventure-pc-game/pull/180))
13. Adherence enforced (no honor system): gate seeds reads; post-cycle `--strict` FAIL; P1-03 `parallel_with` P1-01+P1-02; audit `--out` absolute-path safe

### Standing policy (pack splits)

**Authority:** [`_meta/DOC_LIBRARY_ADR.md`](_meta/DOC_LIBRARY_ADR.md) § Amendment — Docs pack thinning.

- Do **not** run another bulk thinning round.
- Packs must be **named topics** — no opaque `part_a`/`part_b` or `(A)`/`(B)`.
- Prefer **hub → leaf** (or hub → named packs); avoid hub-of-hub.
- A coherent ~1.2–1.4k leaf is fine; clarity beats sub-1k chasing.
- Prefer sharp `summary:` + **When to read** / **Jump to** on fat leaves over new splits (`python3 tools/apply_docs_skim_aids.py`).
- Keep role/task `optional` packs lean (≥~800 tok headroom at budget 12000); deep leaves live on task packs. When a task provides optionals, they replace generic role optionals (specialty remaps still merge). Audit: `python3 tools/audit_docs_read_efficiency.py`.
- Next work: **use** packs (`resolve_docs`, adherence), not more splits.
- **CI:** `L0_docs_pack_policy` locks standing policy (no opaque packs; INDEX docs have phase/summary/tokens; completed `split_docs_*` / stamp / reorg one-shots must stay deleted). Operator tools kept: `form_docs_frontmatter.py`, `consolidate_docs_part_ab.py`, `apply_docs_skim_aids.py`.
