# ADR — Documentation library reorg (agent-first)

**Status:** Accepted
**Date:** 2026-07-29
**Deciders:** Factory / docs maintainers

---

## Context

The docs library (~186 markdown files) was already grouped by domain (`art/`, `qa/`, …), but agents paid a high token cost because:

1. Boot rules were triplicated (`.cursorrules`, `AGENTS.md`, MCP/cheat-sheet prose).
2. `docs/README.md` was a 300-line human catalog, not a machine router.
3. Domain folders mixed tutorials, how-tos, reference, and archive reports.
4. No role-scoped load list — agents opened large bibles for narrow tasks.

## Decision

Reorganize under five top-level buckets + a machine index:

| Bucket | Path | Purpose |
|--------|------|---------|
| Design | `docs/design/` | Product truth (vision, world, gameplay, art, audio, ui) |
| Engineering | `docs/engineering/` | TDD, data architecture, coding standards |
| Ops | `docs/ops/` | Agents, workflow, CI/CD, QA process, cheat sheets |
| Briefs | `docs/briefs/` | Generation briefs (task-scoped only) |
| Archive | `docs/archive/` | Deprecated, compliance reports, pitch |

Also:

- **`docs/INDEX.yaml`** — role → `must_read` / `optional` / `never_autoload`
- **`docs/llms.txt`** — [llmstxt.org](https://llmstxt.org/) discovery map
- **`docs/ops/BOOT.md`** — single thin always-on boot card
- **`docs/_meta/redirects.yaml`** — legacy path → new path
- **Diátaxis types** tagged in `INDEX.yaml` (tutorial / how-to / reference / explanation)
- **YAML frontmatter** optional on docs (`docs/_meta/FRONTMATTER.md`); enforced gradually via `L0_docs_index`

`docs/build/` was rejected as a folder name because root `.gitignore` ignores `build/`.

## Consequences

- All `docs/<domain>/` references updated to new paths; redirects kept for grepping.
- `.cursorrules` and `AGENTS.md` slim to pointers + hard rules; detail lives in `BOOT.md` / domain docs.
- `python3 tools/resolve_docs.py <role>` prints the pack for a role.
- `L0_docs_index` validates INDEX paths exist and redirects are consistent.
- Generation briefs and archive never enter agent boot context.

## Alternatives considered

| Option | Why rejected |
|--------|--------------|
| Flat Diátaxis-only tree (`tutorials/`, `how-to/`, …) | Breaks domain mental model for game design |
| Keep old paths + INDEX only | Misses navigability; archive still pollutes listings |
| One mega-doc | Worse for tokens and git blame |
