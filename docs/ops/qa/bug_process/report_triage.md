---
id: report-triage
type: how-to
phase: [1, 6]
audience: [qa, pm, builder]
status: active
authority: qa
tokens_est: 464
summary: "QA and Bug Process — Bug report template + triage — Copy into GitHub issue (template: Gate failure / Bug report), Discord, or playtest spreadsheet."
---
# QA and Bug Process — Bug report template + triage

**Hub:** [`QA_AND_BUG_PROCESS.md`](../QA_AND_BUG_PROCESS.md)

## When to read

Use **QA and Bug Process — Bug report template + triage** (roles: qa, pm, builder) when executing this procedure Jump to a section below instead of reading end-to-end (4 sections).

## Jump to

- [3. Bug report template](#3-bug-report-template)
- [4. Triage workflow](#4-triage-workflow)
- [Triage checklist (maintainer)](#triage-checklist-maintainer)
- [GitHub labels (recommended)](#github-labels-recommended)


## 3. Bug report template

Copy into GitHub issue (**template: Gate failure / Bug report**), Discord, or playtest spreadsheet.
See `docs/ops/agents/PROJECT_MANAGEMENT.md` for labels and `bash tools/report_gate_failure.sh` for gate failures.

```markdown

## 4. Triage workflow

```
Report filed
    ↓
Triage (within 1 session)
    ├─ Reproduce? → No → Need info → back to reporter
    ├─ Duplicate? → Link primary issue; close duplicate
    ├─ Assign severity (§2)
    └─ Assign owner + milestone (M4/M5/M6)
    ↓
Fix on feature branch
    ↓
Verify (§5)
    ↓
Close issue + note commit/PR
```

### Triage checklist (maintainer)

- [ ] Reproduced on clean `user://` save (or provided save)
- [ ] Severity matches §2 (escalate if main-path blocked)
- [ ] Scene ID and flags documented
- [ ] Not a duplicate of open issue
- [ ] Linked to milestone if S0–S1

### GitHub labels (recommended)

| Label | Use |
|-------|-----|
| `bug` | All defects |
| `severity/s0-blocker` | Ship stop |
| `severity/s1-major` | Milestone gate |
| `severity/s2-minor` | Polish queue |
| `severity/s3-polish` | Backlog |
| `area/combat` | Combat, bosses, skills |
| `area/story` | Scenes, dialogue, flags |
| `area/ui` | Menus, HUD |
| `area/audio` | BGM, SFX |
| `area/l10n` | Translations |
| `area/save` | Save/load, game over |

---
