---
id: roles-rules
type: reference
phase: [0, 1, 8]
audience: [pm, architect, builder, release]
status: active
authority: workflow
tokens_est: 566
summary: "Branch roles + rules"
---
# Branching Policy — Branch roles + rules

**Hub:** [`BRANCHING.md`](../BRANCHING.md)

## 1. Branch roles

| Branch | Purpose | What it contains | Merge policy |
|--------|---------|------------------|--------------|
| **`main`** | Design & **complete specifications** | `docs/`, `game/data/` (incl. `code/spec_registry.json`), `game/locale/`, `tools/`, validators | Docs/data updates anytime via PR |
| **`game/development`** | Full game implementation | Everything on `main` **plus** `game/project.godot`, scripts, scenes, assets, tests, addons | **No merge to `main` until the game is ship-ready (M6)** |

---


## 2. Rules

### On `main`

- ✅ Design docs, GDD, art direction, implementation plan
- ✅ Story/combat JSON (`game/data/`)
- ✅ i18n string table (`game/locale/translations.csv`)
- ✅ Spec registries (`game/data/code/spec_registry.json`, `autoload_registry.json`, `scene_registry.json`)
- ✅ Validators, CI for data + docs (`tools/run_docs_ci_checks.sh`)
- ✅ Steam store copy and marketing trailers (`steam/`)
- ❌ Godot project file, GDScript gameplay code, `.tscn` scenes, ship assets (`tools/check_main_no_ship_code.sh`)
- ❌ Game implementation PRs

### On `game/development`

- ✅ All Godot implementation (Phases 1–8) — **only after `SPEC_DEV_START` gate** (`docs/engineering/technical/SPEC_FIRST_DEVELOPMENT.md`)
- ✅ GDAI MCP–built scenes, shaders, assets
- ✅ Unit/integration/E2E tests
- ✅ Full game CI (`tools/run_ci_checks.sh`, `.github/workflows/game-ci.yml`) — **required green before PR merge**
- ⚠️ Work in progress is expected — this branch is **not** public-facing documentation

### Merge to `main` (game complete only)

Merge `game/development` → `main` **once**, when:

1. All phase gates L0–L5 pass on a release-candidate commit
2. L6 human playtest sign-off (`docs/ops/qa/PLAYTEST_SCRIPT.md`)
3. `M5_asset_compliance` and Steam export ready (Phase 8 / M6)
4. Production Steam release complete (or RC approved for doc merge)

Until then: **do not merge game implementation to `main`**.

**CD:** Tag releases on `game/development` only — see `docs/ops/ci-cd/CD.md`.

---
