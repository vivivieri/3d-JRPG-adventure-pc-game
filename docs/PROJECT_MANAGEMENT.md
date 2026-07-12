# Project Management — Issues, Logs & MCP Integrations

**Version:** 1.0  
**Primary tracker:** **GitHub Issues** (repo-native, PR-linked, Actions-aware)  
**Optional MCP:** Linear (sprints) · Notion (docs/tasks)  
**Cross-refs:** `docs/QA_AND_BUG_PROCESS.md`, `docs/ENVIRONMENTS.md`, `docs/MULTI_AGENT_TEAM.md`

---

## 1. Tool choice

| Tool | Tier | Use for | Status |
|------|------|---------|--------|
| **GitHub Issues** | **P0 required** | Bugs, gate failures, features, env labels | ✅ Use now |
| **GitHub Actions** | **P0** | CI/CD logs, artifact retention | ✅ Live |
| **GitHub Projects** | P1 | Kanban by milestone / env | Optional board |
| **Linear MCP** | P1 optional | Sprint cycles inside each phase | Needs auth — see `AGILE_WITHIN_PHASES.md` |
| **Notion MCP** | P2 optional | Design notes, meeting notes | Needs auth; **not** design authority (`docs/` wins) |
| **Datadog MCP** | N/A ship | Not needed for Godot indie | Skip |

**Rule:** `docs/` + `game/data/` remain authoritative for game design. PM tools track **work**, not **spec**.

**One-time GitHub config:** `bash tools/setup_github_project.sh` — see `docs/GITHUB_SETUP.md`.

---

## 2. GitHub Issues — label taxonomy

### Environment

| Label | Meaning |
|-------|---------|
| `env/development` | Active implementation |
| `env/qa` | Automated gate failure or CI |
| `env/uat` | Human playtest / RC build |
| `env/preprod` | Steam beta |
| `env/production` | Ship blocker |

### Severity (bugs)

| Label | Meaning |
|-------|---------|
| `severity/S0` | Blocker |
| `severity/S1` | Major |
| `severity/S2` | Minor |
| `severity/S3` | Polish |

### Gate / domain

| Label | Example |
|-------|---------|
| `gate/L0_story_data` | Validator fail |
| `gate/L1_unit_tests` | Unit test fail |
| `gate/L4_integration` | Flow scenario fail |
| `gate/L5_e2e` | Ending path fail |
| `domain/visual` | Art jury |
| `domain/audio` | LUFS / jury |
| `domain/flow` | Soft-lock |

### Agent / status

| Label | Meaning |
|-------|---------|
| `agent/architect` | Needs GodotPrompter |
| `agent/builder` | Needs GDAI MCP |
| `agent/qa` | Needs gate run |
| `agent/release` | Needs tag/CD |
| `status/blocked` | Waiting on MCP/secrets/human |
| `status/in-progress` | Active agent |
| `status/done` | Verified fixed |

### Milestone

Link issues to GitHub Milestones matching `docs/MILESTONES.md`: `M1-core`, `M5-art`, `M6-steam`.

---

## 3. Issue templates

Use `.github/ISSUE_TEMPLATE/`:

| Template | When |
|----------|------|
| **Bug report** | Human or agent-found defect |
| **Gate failure** | CI/CD or `run_*_checks.sh` fail |
| **Feature / task** | Phase work from implementation plan |

**Pull request templates:** `.github/PULL_REQUEST_TEMPLATE/` — role handoff checklists + gate report (`docs/CONTROLS_CHEATSHEET.md`).

Title convention: `[ENV][Severity?][Gate?] Summary`

---

## 4. Traceability flow

```
GitHub Issue (#123)
    ├── linked PR (game/development)
    │     └── CI run → logs + gate ID in check name
    ├── commit SHA in issue body
    ├── artifacts/screenshots/*.png
    ├── artifacts/test-reports/ (optional)
    └── remediation: tools/qa_emit_remediation.sh output pasted in comment
```

### Agent obligation on FAIL

1. Run failing gate locally or read Actions log
2. `bash tools/qa_emit_remediation.sh <brief-id>` when available
3. Open or update issue with: gate ID, SHA, log excerpt, remediation lever
4. Label `env/qa` or `env/development`
5. **Do not close** until gate re-run PASS on same issue thread

---

## 5. Log sources by environment

| Source | Dev | QA | UAT | Preprod |
|--------|-----|----|----|---------|
| Godot Output (GDAI F5) | ✅ | — | — | — |
| Godotiq debug console | ✅ | ✅ | — | — |
| `run_ci_checks.sh` stdout | ✅ | ✅ | — | — |
| GitHub Actions log | — | ✅ | ✅ | ✅ |
| GitHub Release assets | — | — | ✅ | ✅ |
| Human playtest notes | — | — | ✅ | ✅ |
| Steam beta feedback | — | — | — | ✅ |

**Retention:** GitHub Actions logs ~90 days; attach critical logs to issues for long-term trace.

---

## 6. Optional MCP integrations

### Linear (P1 — sprint board)

**When:** Multiple parallel agents executing the **current implementation phase**.

**Model:** Phase-gated Agile — waterfall phases 0–8, 2-week cycles **inside** each phase. See `docs/AGILE_WITHIN_PHASES.md`.

| Action | Linear MCP |
|--------|------------|
| Create tasks from phase | `spec-to-implementation` or `create-task` skill |
| Query open blockers | `database-query` |
| Active phase + gates | Read `game/data/qa/sprint_phases.json` |

**Setup:** Team `Tides of Urashima` · Projects `M1-core`, `M5-art`, `M6-steam` · Cycles named `Phase{N}-Sprint{K}`.

Do not duplicate `game/data/` into Linear — link to repo paths in issue descriptions.

### Notion (P2 — narrative / planning notes)

**When:** External stakeholders need non-git visibility.

| Action | Notion MCP |
|--------|------------|
| Playtest summary | `knowledge-capture` skill |
| Phase plan | `spec-to-implementation` skill |

**Not for:** Runtime stats, scene IDs, or gate thresholds — keep in repo.

### GitHub (P0 — no extra MCP)

Agents use `ManagePullRequest` + Issues via cloud task tools. Labels and templates provide structure.

---

## 7. GitHub Projects board (recommended columns)

| Column | WIP limit | Entry criteria |
|--------|-----------|----------------|
| Backlog | — | Issue created |
| Ready | 10 | Spec + gate IDs defined |
| In Progress | 3 | Agent assigned (`status/in-progress`) |
| QA | 5 | PR open, CI running |
| UAT | 2 | RC tagged |
| Done | — | Gates PASS + issue closed |

---

## 8. PM Agent checklist (start of sprint)

- [ ] Sync `docs/MILESTONES.md` with open issues
- [ ] No open `severity/S0` on `env/uat` or `env/preprod`
- [ ] RC tag planned with gate list
- [ ] Human UAT scheduled only if L5 PASS on RC commit

---

## 9. Cross-refs

- `docs/QA_AND_BUG_PROCESS.md` §3 — bug body template
- `docs/MULTI_AGENT_TEAM.md` — role handoffs
- `docs/ENVIRONMENTS.md` — promotion rules
- `tools/qa_emit_remediation.sh` — structured failure briefs
