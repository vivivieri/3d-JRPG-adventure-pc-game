---
id: when-ci-forbidden
type: how-to
phase: [1, 6]
audience: [pm, visual, builder]
status: active
authority: qa
tokens_est: 400
summary: "When required, CI, forbidden, related"
---
# Candidate Tournament — When required, CI, forbidden, related

**Hub:** [`CANDIDATE_TOURNAMENT.md`](../CANDIDATE_TOURNAMENT.md)

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

- `docs/design/art/VISUAL_QA.md` — screenshot + jury layers
- `docs/ops/qa/QA_REMEDIATION_LOOP.md` — one lever per retry (tournament OR remediation, not both loops blindly)
- `docs/ops/qa/WORKFLOW_INTEGRATION.md` — register hooks if extending tournament
