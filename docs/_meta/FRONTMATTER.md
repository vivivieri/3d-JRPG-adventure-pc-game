# Doc frontmatter schema

Optional YAML frontmatter on `docs/**/*.md` (except `archive/`, auto-generated reports).

```yaml
---
id: rendering-guide
type: reference          # tutorial | how-to | reference | explanation
audience: [builder, visual]
phase: [1, 5]
status: active           # active | draft | deprecated
authority: art           # conflict domain tip
tokens_est: 3500         # optional soft budget
---
```

| Field | Required | Notes |
|-------|----------|-------|
| `id` | recommended | kebab-case stable id |
| `type` | recommended | Diátaxis type |
| `audience` | optional | Matches `docs/INDEX.yaml` roles |
| `phase` | optional | Implementation phases 0–8 |
| `status` | optional | `deprecated` docs belong under `archive/` |
| `authority` | optional | Hint when prose conflicts with JSON |
| `tokens_est` | optional | Helps pack budgeting |

**Hub files** (`README.md`, `BOOT.md`, `llms.txt`, `INDEX.yaml`) skip frontmatter.

**CI:** `L0_docs_index` warns on missing `type` for indexed active docs (non-blocking until coverage ≥ 80%).
