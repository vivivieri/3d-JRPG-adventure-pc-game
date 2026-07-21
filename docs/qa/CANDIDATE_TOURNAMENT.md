# Candidate Tournament — Champion/Challenger + Golden Harness

**Version:** 1.0
**Layer:** **L2.5** (pre-merge, **non-ship**)
**Authority:** `game/data/qa/candidate_tournament_policy.json`
**Cross-refs:** `docs/qa/ACCEPTANCE_CRITERIA.md`, `docs/qa/AI_TESTING_SPEC.md`, `docs/art/VISUAL_QA.md`

---

## 1. What this is (and is not)

| This **is** | This **is not** |
|-------------|-----------------|
| Industry **champion/challenger** for generation | A second ship QA stack |
| **Golden harness** — same screenshots, palette, gates every compare | Building the game N times and Frankenstein-merging |
| Optional **upstream picker** before merge | Replacement for L0–L6 |
| One **canonical winner** per scope (zone/issue) | Multiple living forks on `game/development` |

**Ship truth stays L0–L6.** `L2_candidate_select` never blocks `main` docs CI or M6 ship by itself.

---

## 2. Stack position

```
Spec + sprint issue
        │
        ▼
┌───────────────────────────┐
│  L2.5 Candidate tournament │  ← THIS (optional, max 3 tries/issue)
│  golden harness + rubric   │
└─────────────┬─────────────┘
              │ ONE winner commit
              ▼
┌───────────────────────────┐
│  L0 → L1 → L2 → L3 → L4 → L5 │  ← unchanged mandatory spine
└─────────────┬─────────────┘
              ▼
         L6 human (RC only)
```

---

## 3. Data files

| File | Role |
|------|------|
| `game/data/qa/golden_harness.json` | Per-scope capture paths, palette zone keys, hard gate veto list |
| `game/data/qa/evaluation_rubrics.json` | Soft rubric axes (tie-break only) mapped to jury criteria |
| `game/data/qa/candidate_tournament_policy.json` | Max candidates, non-ship flag, registry paths |
| `artifacts/candidates/champion_registry.json` | Current champion per scope (runtime, gitignored except samples) |
| `artifacts/candidates/<issue>/comparison_*.json` | Comparison evidence for PM / stakeholder |

---

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

## 7. When tournament is required

| Phase / tag | Policy |
|-------------|--------|
| Phase 1 vertical slice (`ruined_village`) | **Recommended** — max 2 challengers |
| M5 hero art / zone NPR | **Required** per `generation_readiness_backlog.json` |
| Docs/data-only `main` | **Skip** — no harness captures |
| Bug fix, no visual change | **Skip** |

---

## 8. CI gates

| Gate | Blocks ship? | Command |
|------|--------------|---------|
| `L0_candidate_tournament` | No (schema) | `python3 tools/validate_candidate_tournament.py` |
| `L2_candidate_select` | No (pre-merge evidence) | `bash tools/run_candidate_tournament.sh` |

Both registered in `acceptance_criteria.json`. Only `L0_*` runs on `main` docs CI.

---

## 9. Forbidden patterns

Listed in `acceptance_criteria.json` → `invalid_pass_patterns`:

- Promoting challenger without comparison artifact
- Challenger promoted when hard gate FAIL
- Merging assets from multiple challengers into one scene
- Using soft score to override `L2_visual_palette` FAIL

---

## 10. Related docs

- `docs/art/VISUAL_QA.md` — screenshot + jury layers
- `docs/qa/QA_REMEDIATION_LOOP.md` — one lever per retry (tournament OR remediation, not both loops blindly)
- `docs/qa/WORKFLOW_INTEGRATION.md` — register hooks if extending tournament
