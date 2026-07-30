---
id: pick-work
type: reference
audience: [pm, builder, qa]
status: active
authority: ops
tokens_est: 837
---
# R&R — how-to-pick-work-dev-qa

**Hub:** [`RR_CHEATSHEET.md`](../RR_CHEATSHEET.md)

## How to pick work (dev & QA)

**Rule:** Do **not** self-pick from the backlog. PM dispatches via orchestrator; workers pass session gate first.

### Where work is defined

| Question | Answer | Source |
|----------|--------|--------|
| What phase are we in? | **Phase 1** — ruined_village vertical slice | `game/data/qa/sprint_phases.json` → `active_phase` |
| What sprint is active? | **Phase1-Sprint1** (7 issues) | `game/data/qa/sprint_board.json` |
| What are the tasks? | P1-00 … P1-06 bodies + handoffs | `docs/ops/sprints/Phase1-Sprint1-issues.md` |
| What is the long-term order? | Phases 0→8 (do not reorder) | `docs/ops/workflow/IMPLEMENTATION_PLAN.md` |
| Story points? | **No** — use `sequence`, `depends_on`, gate IDs, severity | — |

### Who picks the next item?

| Role | Action |
|------|--------|
| **PM Agent** | `bash tools/run_pm_orchestrator.sh` → `python3 tools/pm_dispatch_workers.py` → read `artifacts/pm_orchestrator_report.json` → `next_dispatch` |

**Full factory setup:** `docs/ops/agents/FACTORY_SETUP_GUIDE.md`
| **Dev / QA** | Wait for dispatch → `bash tools/run_agent_session_gate.sh <role> <issue_id>` → read issue section in sprint pack |

### Phase 1 dependency chain (current sprint)

```
P1-00 (pm)     bootstrap project.godot + CI
  ├─→ P1-01 (architect)  toon shader + zone_visuals
  │     └─→ P1-02 (builder)  ruined_village.tscn
  │           ├─→ P1-04 (qa)  CI + L0–L2 gate report
  │           │     └─→ P1-06 (pm)  sprint review
  │           └─→ P1-05 (qa)  golden screenshot + zone composition
  └─→ P1-03 (architect)  water shader  [parallel with P1-02 after P1-00]
```

### Priority (no story points)

| Kind | Scale | Use |
|------|-------|-----|
| **Phase order** | 0→8 waterfall | PM cannot skip phases via sprint |
| **Sprint sequence** | `sequence` 1–7 on board | Orchestrator dispatch order |
| **Blockers** | `depends_on` / `blocks` | QA waits until builder issue `done` |
| **Bug severity** | S0–S3 | `severity/S0` … in GitHub Issues |
| **Asset tier** | P0 / P1 | Art/audio docs (e.g. P0 VO clips) |
| **Gate layers** | L0→L6 | Definition of done per issue |

### How QA knows dev is done

1. **Board:** QA issues list `depends_on` (e.g. P1-04 depends on P1-02).
2. **Status:** Upstream issue set to `done` via `python3 tools/pm_update_issue.py`.
3. **Event:** `bash tools/run_post_agent_cycle.sh --issue <id> --agent <role> --commit <sha>` → closes session telemetry + PM re-runs orchestrator → dispatches QA.
4. **Handoff:** Builder posts **Builder → QA** block in PR/issue (`docs/ops/sprints/Phase*-Sprint*-issues.md`).
5. **CI:** PR on `game/development` must pass listed `acceptance_gate_ids` before QA closes issue.

### Definition of done (sprint issue)

- [ ] Gate IDs PASS on PR commit
- [ ] `bash tools/run_ci_checks.sh` green (game branch)
- [ ] `L3_gdai_built` if scenes touched
- [ ] **`L3_perf_review`** if scenes, shaders, materials, meshes, lights, or fog changed
- [ ] Evidence paths in PR / issue
- [ ] Board status `done` + GitHub issue closed

**Full policy:** `docs/ops/agents/SPRINT_ORCHESTRATION.md` · `docs/ops/agents/PM_AGENT_RUNBOOK.md` · `docs/ops/workflow/AGILE_WITHIN_PHASES.md`

---

