---
id: multi-agent-branch-strategy
type: how-to
phase: [0, 1]
audience: [pm, builder]
status: active
authority: agents
tokens_est: 867
summary: "One issue → one feature branch → one PR → merge → cycle event."
---
# Multi-Agent Branch Strategy

## When to read

Use **Multi-Agent Branch Strategy** (roles: pm, builder) when executing this procedure Jump to a section below instead of reading end-to-end (8 sections).

## Jump to

- [1. Branch naming](#1-branch-naming)
- [2. Per-issue workflow](#2-per-issue-workflow)
- [3. Definition of done](#3-definition-of-done)
- [4. Strict role policy](#4-strict-role-policy)
- [5. Parallel issues](#5-parallel-issues)
- [6. Evidence](#6-evidence)
- [7. Failure path](#7-failure-path)
- [8. Cross-refs](#8-cross-refs)


## 1. Branch naming

| Scope | Pattern | Example |
|-------|---------|---------|
| Cloud agent feature work | `cursor/<issue-id-lowercase>-a091` | `cursor/p1-01-a091` |
| Sprint integration branch | `game/development` | long-lived implementation trunk |
| Design / orchestration | `main` | docs, `game/data/`, tools |

Issue field: `branch_name_pattern` in `sprint_board.json` (default `cursor/{issue_id}-a091`).

**Cursor Cloud agents:** session instructions may use suffix `-ec08` instead of `-a091` — same issue ID, same PR target (`game/development`). Factory dispatch uses the board pattern; cloud agents follow their session suffix when creating branches.

---

## 2. Per-issue workflow

```mermaid
sequenceDiagram
  participant PM as PM Agent
  participant W as Worker Agent
  participant GH as GitHub

  PM->>W: pm_dispatch_packet.json
  W->>W: run_agent_session_gate.sh
  W->>GH: branch cursor/p1-02-a091
  W->>W: work + gates + evidence bundle
  W->>GH: PR → game/development
  GH->>GH: Game CI
  W->>PM: agent_cycle_complete (after merge)
```

---

## 3. Definition of done

| `done_requires` | When to use |
|-----------------|-------------|
| `pr_merged` | Default — gameplay, scenes, shaders |
| `ci_green_on_branch` | Bootstrap (P1-00), docs-only on trunk |
| `push_only` | PM review / meta tasks (P1-06) |

Enforced by `python3 tools/pm_check_done_criteria.py <issue_id>` before `pm_update_issue.py --status done`.

---

## 4. Strict role policy

One agent role per session. `run_agent_session_gate.sh` rejects when:

- Agent not in `next_dispatch`
- Agent ≠ `agent_owner` and ≠ `co_agent` (`AGENT_SESSION_STRICT_ROLE=1` default)

Do **not** combine Architect + Builder in one session.

---

## 5. Parallel issues

When `parallel_with` is set and WIP caps allow, orchestrator may dispatch two starts (e.g. P1-01 Architect toon + P1-03 Architect water, then P1-02 Builder + P1-03). Each still gets its own branch and PR. Board peers are validated by `validate_sprint_board.py` (unknown `parallel_with` ids FAIL).

---

## 6. Evidence

Before marking done (or use the enforced single command):

```bash
bash tools/run_post_agent_cycle.sh --issue P1-02 --agent builder --commit <sha> \
  --gate L2_scene_primitives --artifact artifacts/qa_reports/...
```

Manual steps (same order as `run_post_agent_cycle.sh`):

```bash
python3 tools/check_docs_pack_adherence.py --issue P1-02 --strict   # before board/webhook
python3 tools/pm_check_done_criteria.py P1-02 --commit <sha>
python3 tools/pm_update_issue.py P1-02 --status done --commit <sha>
bash tools/pm_emit_cycle_event.sh agent_cycle_complete --issue P1-02 --agent builder --commit <sha>
python3 tools/pm_bundle_evidence.py P1-02 --gate L2_scene_primitives --artifact artifacts/qa_reports/...
```

---

## 7. Failure path

```bash
bash tools/run_post_agent_cycle.sh --issue P1-02 --agent builder --outcome failed --failed-check L2_scene_primitives
```

PM re-dispatches **same issue** for remediation — does not skip to next issue.

---

## 8. Cross-refs

- `docs/ops/agents/CLOUD_AGENT_SETUP_RUNBOOK.md`
- `docs/ops/agents/FACTORY_WATCHDOG.md`
- `game/data/qa/sprint_board.json`
