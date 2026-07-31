---
id: phase-tools
type: reference
phase: [1, 6]
audience: [qa, pm, builder]
status: active
authority: qa
tokens_est: 479
summary: "Phase gates, tools, remediation relationship"
---
# Acceptance Criteria — Phase gates, tools, remediation relationship

**Hub:** [`ACCEPTANCE_CRITERIA.md`](../ACCEPTANCE_CRITERIA.md)

## When to read

Use **Acceptance Criteria — Phase gates, tools, remediation relationship** (roles: qa, pm, builder) when you need this reference during the current task Jump to a section below instead of reading end-to-end (3 sections).

## Jump to

- [6. Phase gates](#6-phase-gates)
- [7. Tools](#7-tools)
- [8. Relationship to remediation](#8-relationship-to-remediation)


## 6. Phase gates

`acceptance_criteria.json` → `phase_gates`:

| Phase | Required gates |
|-------|----------------|
| `phase_1` | L0 (incl. narrative_density), L1, L2 boot, L2 primitives + conditional art gates when assets exist |
| `phase_6` | L0–L2 + L4 + L5 (E2E not SKIP) |
| `m5_ship` | All art/flow/compliance gates strict (`--ship` flags) |

Conditional art gates: when `urashima.glb` / screenshot / `bgm_village.ogg` **exist**, their gates must **PASS** — not SKIP.

---


## 7. Tools

| Tool | Role |
|------|------|
| `game/data/qa/acceptance_criteria.json` | Thresholds + gate ids |
| `tools/qa_acceptance_lib.py` | Enforce jury rules in Python |
| `tools/validate_acceptance_criteria.py` | Lint catalog + threshold alignment |
| `tools/qa_write_gate_result.py` | Write `artifacts/qa_reports/<gate>.json` |
| `tools/qa_remediation_brief.py` | FAIL → fix actions (links to playbook) |

```bash
python3 tools/validate_acceptance_criteria.py
python3 tools/qa_write_gate_result.py --gate L2_visual_palette --status pass \
  --metric max_avg_anchor_dist=72.4 --evidence artifacts/screenshots/phase1_ruined_village_gameplay.png
```

---


## 8. Relationship to remediation

FAIL without acceptance criteria = noise.
FAIL **with** gate id + measured values + evidence = actionable input to `QA_REMEDIATION_LOOP.md`.

Always chain: **measure → compare to catalog → brief → one lever → re-measure**.
