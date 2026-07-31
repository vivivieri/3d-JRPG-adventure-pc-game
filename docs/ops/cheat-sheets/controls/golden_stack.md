---
id: golden-stack
type: reference
audience: [pm, builder, qa, release]
status: active
authority: ops
tokens_est: 402
summary: "Golden rules + control stack"
---
# Controls Cheat Sheet — Golden rules + control stack

**Hub:** [`CONTROLS_CHEATSHEET.md`](../CONTROLS_CHEATSHEET.md)

## Golden rules

1. **Enforce outputs, not intentions** — gates PASS with evidence, or merge/tag is blocked.
2. **CI is the hard floor** — agent honor system fills gaps CI cannot see.
3. **WARN ≠ PASS · SKIP ≠ PASS** — on `game/development`, CI maps SKIP → FAIL via `tools/gate_lib.sh`.
4. **Builder proof** — scene changes require `.gdai_built` in the same PR (`L3_gdai_built`).
5. **Human L6** — only after L0–L5 pass.
6. **Cross-cutting factory features** — register in `workflow_integration_registry.json`; `bash tools/check_feature_integration.sh --remind` before merge (`docs/ops/qa/WORKFLOW_INTEGRATION.md`).

---


## Control stack (strong → weak)

| # | Control | Blocks merge? | Blocks ship/tag? |
|---|---------|---------------|------------------|
| 1 | **GitHub Actions CI** | ✅ PR/push fail | ✅ via `run_cd_gates.sh` |
| 2 | **Branch protection** | ✅ when configured | — |
| 3 | **PR role checklist** | ⚠️ Review discipline | — |
| 4 | **Issue templates** | ⚠️ Required fields | — |
| 5 | **R&R scripts** | ✅ in CI | ✅ |
| 6 | **Remediation loop** | ⚠️ Process | ✅ anti-infinite-retry |
| 7 | **Phase exit gates** | — | ✅ phase promotion |
| 8 | **Pre-delivery control** | — | ✅ blocks outbound delivery until automated checks pass (`docs/ops/workflow/DELIVERY_CONTROL.md`) |
| 9 | **Agent rules** | — | — |

---
