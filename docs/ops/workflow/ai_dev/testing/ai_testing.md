---
id: ai-testing
type: how-to
phase: [0, 1, 8]
audience: [pm, qa, architect, builder]
status: active
authority: workflow
tokens_est: 995
summary: "Testing is **layered**. Higher layers run after lower layers pass."
---
# AI Dev — Testing Policy — AI testing policy

**Hub:** [`testing_policy.md`](../testing_policy.md)

## When to read

Use **AI Dev — Testing Policy — AI testing policy** (roles: pm, qa, architect, builder) when executing this procedure Jump to a section below instead of reading end-to-end (4 sections).

## Jump to

- [2. AI testing policy](#2-ai-testing-policy)
- [2.1 AI agent obligations](#21-ai-agent-obligations)
- [2.2 Headless vs editor](#22-headless-vs-editor)
- [2.3 Test artifacts](#23-test-artifacts)


## 2. AI testing policy

Testing is **layered**. Higher layers run after lower layers pass.

**Golden rule:** **Human QA (L6) runs only after all AI playthrough layers (L0–L5) pass** on the same release-candidate commit. See `docs/ops/qa/AI_TESTING_SPEC.md` §0.

**L2.5 (optional):** Champion/challenger zone tournaments run **before merge** when policy requires — `docs/ops/qa/CANDIDATE_TOURNAMENT.md`. Non-ship; does not replace L0–L5.

| Layer | Runner | Who runs it | Purpose |
|-------|--------|-------------|---------|
| **L0 — Data validation** | `python3 tools/validate_story_data.py` + base-class validators | AI agent (every commit) | JSON schema, cross-refs, scene IDs, `base_classes.json` |
| **L1 — Unit tests + lint** | `bash tools/run_unit_tests.sh` + `check_gdscript_changed.sh` | AI agent (every commit) | Pure logic, parsers, calculators, flags; `gdlint` on changed `.gd` |
| **L2 — Smoke tests** | `bash tools/run_playtest_smoke.sh` | AI agent (every commit) | Boot, lint; primitives, animation whitelist, feel smoke, GLB import, visual/audio/model smoke when assets exist |
| **L2.5 — Candidate tournament** | `bash tools/run_candidate_tournament.sh` | Builder / Visual (when policy requires) | Champion/challenger golden harness compare — pre-merge only (`CANDIDATE_TOURNAMENT.md`) |
| **L3 — GDAI editor verify** | GDAI MCP F5 + viewport | AI agent (per scene task) | Visual layout, materials, runtime errors in editor |
| **L4 — AI integration tests** | `bash tools/run_integration_tests.sh` | AI agent (phase gate) | Multi-scene flows, combat round, save/load |
| **L5 — AI E2E playthrough** | `REQUIRE_L5=1 bash tools/run_e2e_playthrough.sh` | AI agent (Phase 6 gate + every RC) | Full story + 3 endings (headless or recorded) |
| **L6 — Human QA** | `docs/ops/qa/PLAYTEST_SCRIPT.md` | Human (**after L0–L5 pass**) | Feel, pacing, localization — **ship gate only** |

**GitHub CI** (`.github/workflows/ci.yml`): runs headless subset via `bash tools/run_docs_ci_checks.sh` on `main`.
**Game CI** (`game-ci.yml` on `game/development`): `bash tools/run_ci_checks.sh`.
**Environments & multi-agent:** `docs/ops/ci-cd/ENVIRONMENTS.md`, `docs/ops/agents/MULTI_AGENT_TEAM.md`, `docs/ops/agents/PROJECT_MANAGEMENT.md`.

### 2.1 AI agent obligations

Before marking **any** implementation task done, the agent must:

1. Run L0 + L1 + L2 (always)
2. Run L3 for any scene/visual change
3. Run L4 when the phase acceptance criteria require it
4. Run L5 when Phase 6 is complete and on every release candidate
5. **Do not request human QA until L0–L5 all pass**
6. Report pass/fail counts in the PR or session summary (template: `docs/ops/qa/AI_TESTING_SPEC.md` §10)
7. **Never** claim “tested” based only on code review

### 2.2 Headless vs editor

| Concern | Tool |
|---------|------|
| Scene tree, materials, lighting | **GDAI MCP** (editor) — headless cannot replace |
| JSON loading, damage math, flag logic | **Unit tests** (headless) |
| Scene loads without crash | **Smoke / integration** (headless) |
| Art checklist (palette, fog, silhouettes) | **GDAI MCP** screenshot + `ART_DIRECTION.md` checklist (AI); human art sign-off post-L5 / Phase 7 |

### 2.3 Test artifacts

Agents should save evidence for phase gates:

```
artifacts/
  screenshots/     # GDAI viewport captures at acceptance checkpoints
  videos/            # E2E playthrough recordings (Phase 6+)
  test-reports/      # Optional junit-style logs from run_unit_tests.sh
```

---
