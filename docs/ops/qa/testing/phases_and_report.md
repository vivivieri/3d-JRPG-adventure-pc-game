---
id: phases-and-report
type: reference
audience: [qa, flow]
status: active
authority: qa
tokens_est: 444
summary: "Copy into PR or session summary:"
---
# Phase map, report template & related

**Hub:** [`AI_TESTING_SPEC.md`](../AI_TESTING_SPEC.md)

## 9. Phase → required test layers

| Phase | Layers required before phase sign-off |
|-------|--------------------------------------|
| 0 | L0, L1, L2, L3 (boot) |
| 1 | L0–L3 |
| 2 | L0–L4 |
| 3 | L0–L4 |
| 4 | L0–L4 |
| 5 | L0–L4 |
| 6 | L0–L5 |
| 7 | L0–L5 (+ asset compliance) |
| 8 | L0–L5 on RC → **then L6 human** → export |

**Human QA never runs before Phase 6 L5 is implemented and passing.**

---

## 10. Agent session report template

Copy into PR or session summary:

```markdown
## 12. Optional: GUT unit tests (Phase 4+)

If `game/tests/unit/` becomes crowded, adopt **[GUT](https://github.com/bitwes/Gut)** (Godot Unit Test):

- GodotPrompter writes GUT test scripts per `COMBAT_SYSTEMS.md` worked examples.
- Run headless: `godot4 --headless -s addons/gut/gut_cmdln.gd` (after plugin install).
- Wire into `tools/run_unit_tests.sh`.

**Until then:** keep the lightweight `test_runner.gd` scaffold on `main`.

---

## 13. Related files

| Path | Role |
|------|------|
| `tools/run_unit_tests.sh` | L1 |
| `tools/run_playtest_smoke.sh` | L2 |
| `tools/run_integration_tests.sh` | L4 |
| `tools/run_e2e_playthrough.sh` | L5 |
| `game/tests/unit/` | L1 tests |
| `game/tests/integration/` | L4 tests (to add) |
| `game/tests/e2e/` | L5 tests (to add) |
| `docs/ops/qa/PLAYTEST_SCRIPT.md` | L6 human script |
| `docs/ops/workflow/AI_DEV_WORKFLOW.md` | Build policy + acceptance criteria |
| `docs/ops/qa/ACCEPTANCE_CRITERIA.md` | Measurable QA gates |
| `docs/ops/qa/QA_REMEDIATION_LOOP.md` | FAIL iteration |
