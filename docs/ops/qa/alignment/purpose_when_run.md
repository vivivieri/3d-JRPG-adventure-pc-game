---
id: purpose-when-run
type: how-to
phase: [1, 6]
audience: [pm, qa]
status: active
authority: qa
tokens_est: 922
summary: "Alignment Audit — Purpose, when, how to run — Produces a repeatable alignment audit with:"
---
# Alignment Audit — Purpose, when, how to run

**Hub:** [`ALIGNMENT_AUDIT.md`](../ALIGNMENT_AUDIT.md)

## When to read

Use **Alignment Audit — Purpose, when, how to run** (roles: pm, qa) when executing this procedure Jump to a section below instead of reading end-to-end (4 sections).

## Jump to

- [1. Purpose](#1-purpose)
- [1b. Two streams (management view)](#1b-two-streams-management-view)
- [2. When to run](#2-when-to-run)
- [3. How to run](#3-how-to-run)


## 1. Purpose

Produces a **repeatable alignment audit** with:

| Output | Path |
|--------|------|
| JSON report (latest) | `artifacts/alignment_audits/latest.json` |
| Markdown report | `artifacts/alignment_audits/latest.md` |
| HTML stakeholder dashboard | `artifacts/alignment_dashboard.html` |
| **Committed history (GitHub)** | `docs/archive/compliance/alignment_audit_reports/<audit_id>/` |
| History index | `docs/archive/compliance/alignment_audit_history.json` |
| Timestamped artifact folder | `artifacts/alignment_audits/<audit_id>/` |

Each audit includes:

1. **Verdict** — `ALIGNED` · `AT_RISK` · `FAIL` (CI + applicable streams)
2. **Two streams** — **Spec readiness** (design & prep) and **Build readiness** (dev & ship)
3. **Domain radar scores** (0–10) — grouped by stream, not one merged mega-radar
4. **CI summary** — gate PASS/FAIL counts
5. **Data parity** — encounters, hooks, tutorial flags, sprint board ↔ sprint pack IDs
6. **Full recommendation checklist** — P0–P3 by category
7. **Visual manifest** — stakeholder PNG packs (when bundled)

### 1b. Two streams (management view)

**Do not show one merged radar to management** — it makes spec work look incomplete when build has not started.

| Stream | ID | Primary branch | Question |
|--------|-----|----------------|----------|
| **Design & preparation** | `spec_readiness` | `main` | Can we dispatch builders? Is design truth complete? |
| **Development & shipping** | `build_readiness` | `game/development` | Does the game run, pass gates, and approach Steam? |

On **`main`**, build stream is **N/A** (no `project.godot` by design). Headline: `Spec 9.8/10 · Build N/A`.

On **`game/development`**, both streams score independently. Verdict = worst applicable stream after CI pass.

**GitHub:** `report.md` § Streams. **Local:** `dashboard.html` — two stream cards at top.

---


## 2. When to run

| Trigger | Command |
|---------|---------|
| After alignment PR merge | `bash tools/run_alignment_audit.sh --trigger post_merge --note "PR #N"` |
| End of agent session | `bash tools/run_alignment_audit.sh --trigger agent_session` |
| Before P1-00 dispatch | `bash tools/run_alignment_audit.sh --trigger pre_dispatch` |
| Phase exit | `bash tools/run_alignment_audit.sh --trigger phase_exit` |
| Manual | `bash tools/run_alignment_audit.sh` |

**PM orchestrator:** add as optional post-step alongside stakeholder report when alignment work lands.

**Workflow integration:** After adding cross-cutting factory features, register in `game/data/qa/workflow_integration_registry.json` and verify `L0_workflow_integration` PASS — see `docs/ops/qa/WORKFLOW_INTEGRATION.md`.

---


## 3. How to run

```bash
# Full audit (runs docs CI or game CI based on branch)
bash tools/run_alignment_audit.sh

# With stakeholder visuals bundled from a directory
bash tools/run_alignment_audit.sh --visuals-from docs/archive/compliance/alignment_audit_visuals

# Fast check without re-running CI (uses skip — scores approximate)
bash tools/run_alignment_audit.sh --skip-ci --trigger quick_check
```

Open dashboard for product owner:

```bash
xdg-open artifacts/alignment_dashboard.html   # Linux
open artifacts/alignment_dashboard.html       # macOS
```

---
