---
id: frontmatter-schema
type: reference
audience: [pm, architect, builder, qa]
phase: [0]
status: active
authority: meta
tokens_est: 320
summary: "YAML frontmatter schema for docs/**/*.md"
---
# Doc frontmatter schema

YAML frontmatter is **required** on active `docs/**/*.md` (except hubs/archive listed below).

```yaml
---
id: rendering-guide
type: reference          # tutorial | how-to | reference | explanation
audience: [builder, visual]
phase: [1, 5]
status: active           # active | draft | deprecated
authority: art           # conflict domain tip
tokens_est: 450          # optional soft budget
---
```

| Field | Required | Notes |
|-------|----------|-------|
| `id` | yes | kebab-case stable id |
| `type` | yes | Diátaxis type |
| `audience` | recommended | Matches `docs/INDEX.yaml` roles |
| `phase` | optional | Implementation phases 0–8 — `resolve_docs.py --phase N` drops optionals whose list excludes N |
| `status` | recommended | `deprecated` docs belong under `archive/` |
| `authority` | recommended | Hint when prose conflicts with JSON |
| `tokens_est` | optional | Helps pack budgeting (`--budget`) |
| `summary` | optional | One-line TL;DR printed when the doc is deferred over budget/phase |

**Skip frontmatter:** `README.md`, `BOOT.md`, `llms.txt`, `INDEX.yaml`, `archive/**`, `_meta/**`, `briefs/**`, `audio_sheets/**`, `sprints/**`, `automation_prompts/**`.

**CI:** `L0_docs_index` requires ≥80% of active docs to have `type:` frontmatter. `L0_handoff_refs` validates sprint `handoff_refs` + `docs_task`.
