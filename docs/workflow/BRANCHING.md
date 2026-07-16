# Branching policy — documentation vs game development

**Version:** 1.1  
**Authority:** This document defines which branches hold what, and when code may land on `main`.  
**Spec-first policy:** `docs/technical/SPEC_FIRST_DEVELOPMENT.md` — **complete specs on `main`; zero ship code until `SPEC_DEV_START` gate.**

---

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

- ✅ All Godot implementation (Phases 1–8) — **only after `SPEC_DEV_START` gate** (`docs/technical/SPEC_FIRST_DEVELOPMENT.md`)
- ✅ GDAI MCP–built scenes, shaders, assets
- ✅ Unit/integration/E2E tests
- ✅ Full game CI (`tools/run_ci_checks.sh`, `.github/workflows/game-ci.yml`) — **required green before PR merge**
- ⚠️ Work in progress is expected — this branch is **not** public-facing documentation

### Merge to `main` (game complete only)

Merge `game/development` → `main` **once**, when:

1. All phase gates L0–L5 pass on a release-candidate commit
2. L6 human playtest sign-off (`docs/qa/PLAYTEST_SCRIPT.md`)
3. `M5_asset_compliance` and Steam export ready (Phase 8 / M6)
4. Production Steam release complete (or RC approved for doc merge)

Until then: **do not merge game implementation to `main`**.

**CD:** Tag releases on `game/development` only — see `docs/ci-cd/CD.md`.

---

## 3. Workflow for developers & agents

```bash
# Documentation or story data change
git checkout main
# edit docs/ or game/data/
bash tools/run_docs_ci_checks.sh
git commit && git push && open PR → main

# Game implementation
git checkout game/development
bash tools/ensure_mcp_stack.sh          # before scene work
# GodotPrompter + GDAI MCP build loop
bash tools/run_ci_checks.sh             # full game CI
git commit && git push                  # to game/development only
```

---

## 4. CI per branch

| Branch | CI workflow | CD workflow | Environment |
|--------|-------------|-------------|-------------|
| `main` | `ci.yml` | — | **design** |
| `game/development` | `game-ci.yml` + `qa-nightly.yml` | `cd-artifact.yml` · `cd-steam.yml` | **dev** / **qa** / **uat** / **preprod** / **prod** |

See `docs/ci-cd/ENVIRONMENTS.md` for promotion rules (dev → qa → uat → preprod → prod).

---

## 5. Creating the game branch (one-time)

Already done:

```bash
git checkout -b game/development   # from last main snapshot with full game tree
git push -u origin game/development
```

New clones:

```bash
git clone <repo>
git checkout game/development   # for implementation
git checkout main               # for docs/data only
```

---

## 6. Cross-refs

- `docs/workflow/IMPLEMENTATION_PLAN.md` — build phases (executed on `game/development`)
- `docs/ci-cd/CI.md` — full game CI gate catalog
- `AGENTS.md` — agent bootstrap; design source on `main`, build on `game/development`
- `.cursorrules` §0 — GDAI MCP scene policy (applies on `game/development`)
