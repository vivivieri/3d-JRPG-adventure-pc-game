---
id: workflow-promotion
type: how-to
phase: [1, 6]
audience: [pm, visual, builder]
status: active
authority: qa
tokens_est: 631
summary: "Workflow, promotion, PM involvement"
---
# Candidate Tournament — Workflow, promotion, PM involvement

**Hub:** [`CANDIDATE_TOURNAMENT.md`](../CANDIDATE_TOURNAMENT.md)

## 4. Workflow (Builder / Visual)

### Step A — Produce challenger (after L2 passes on candidate commit)

1. Capture golden harness screenshots (GDAI / MCP Pro) to paths in `golden_harness.json`
2. Run required L2 gates on **this commit**
3. Write challenger manifest:

```bash
# artifacts/candidates/P1-02/challenger_run2.json
# See game/data/qa/examples/challenger_manifest_sample.json
```

### Step B — Compare

```bash
bash tools/run_candidate_tournament.sh \
  --challenger artifacts/candidates/P1-02/challenger_run2.json
```

Outputs:
- `verdict`: `promote_challenger` | `keep_champion` | `reject_challenger`
- `comparison_*.json` under `artifacts/candidates/<issue_id>/`

### Step C — Promote (if verdict wins)

```bash
bash tools/run_candidate_tournament.sh \
  --challenger artifacts/candidates/P1-02/challenger_run2.json \
  --promote
```

Updates `artifacts/candidates/champion_registry.json` — **one row per scope**.

### Step D — Merge winner only

Merge **one** PR/commit to `game/development`. Run full `bash tools/run_ci_checks.sh`.

Attach comparison artifact in sprint evidence:

```bash
python3 tools/pm_bundle_evidence.py P1-02 \
  --gate L2_candidate_select \
  --artifact artifacts/candidates/P1-02/comparison_<ts>.json
```

---


## 5. Promotion rules (enforced in code)

1. **Hard gate veto** — challenger must PASS every `hard_gates` row in `golden_harness.json` for the scope
2. **Golden harness** — required captures exist; palette check via `check_screenshot_palette.py`
3. **No incumbent** — first PASS challenger becomes champion
4. **Incumbent exists** — challenger must beat champion **soft_score** (rubric axes from jury JSON)
5. **Tie** — keep champion (stability)
6. **Never** merge two challengers into one scene

Soft scores **cannot** override hard FAIL.

---


## 6. PM / PO involvement

| Role | Action |
|------|--------|
| **Builder** | Run tournament before opening PR when issue tag includes `tournament` or phase ≥ M5 art |
| **QA** | Verify comparison artifact + gate IDs on PR |
| **PM** | Reject PR without `L2_candidate_select` evidence when tournament required |
| **Product owner** | Approve rubric once per phase; read stakeholder dashboard — not daily PRs |

---
