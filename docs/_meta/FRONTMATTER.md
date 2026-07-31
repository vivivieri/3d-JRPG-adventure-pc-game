---
id: frontmatter-schema
type: reference
audience: [pm, architect, builder, qa]
phase: [0]
status: active
authority: meta
tokens_est: 494
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
| `phase` | **required on INDEX-listed active docs** | Phases 0–8 for `resolve_docs --phase`. Heuristics: art/world/ui/audio→`[1,5]`; gameplay→`[2,3]`; vision→`[1,6]`; engineering/technical→`[1–6]`; ops/qa→`[1,6]`; ops/ci-cd→`[6,8]`; ops/workflow→`[0,1,8]`; ops/agents + cheat-sheets→`[0,1]`; else `[1]` |
| `status` | recommended | `deprecated` docs belong under `archive/` |
| `authority` | recommended | Hint when prose conflicts with JSON |
| `tokens_est` | **required on INDEX-listed active docs** | Helps pack budgeting (`--budget`) |
| `summary` | **required on INDEX-listed active docs** | One-line TL;DR printed when the doc is deferred over budget/phase |

**Skip frontmatter:** `README.md`, `BOOT.md`, `llms.txt`, `INDEX.yaml`, `archive/**`, `_meta/**`, `briefs/**`, `audio_sheets/**`, `sprints/**`, `automation_prompts/**`.

**CI:**
- `L0_docs_index` — ≥80% of active docs have `type:`; INDEX paths + redirects
- `L0_docs_pack_policy` — INDEX active docs must have `type`/`phase`/`summary`/`tokens_est`; no opaque `part_a`/`part_b` packs; completed split/stamp/reorg one-shots must stay deleted
- `L0_handoff_refs` — sprint `handoff_refs` + `docs_task`
