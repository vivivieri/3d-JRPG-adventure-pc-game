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

- **`docs/INDEX.yaml`** — role → `must_read` / `optional` / `never_autoload` + **`tasks:`** packs
- **`docs/llms.txt`** — [llmstxt.org](https://llmstxt.org/) discovery map
- **`docs/ops/BOOT.md`** — single thin always-on boot card
- **`docs/_meta/redirects.yaml`** — legacy path → new path
- **Diátaxis types** tagged in `INDEX.yaml` (tutorial / how-to / reference / explanation)
- **YAML frontmatter** optional on docs (`docs/_meta/FRONTMATTER.md`); enforced gradually via `L0_docs_index`
- **`resolve_docs.py`** — `--issue` / `--task` / `--phase` / `--budget` / `--report`; briefs auto-attach; `L0_handoff_refs` lint

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

---

## Amendment — Docs pack thinning / fragmentation (2026-07-31)

**Status:** Accepted  
**Context:** After packs rounds 4–8, active leaves ≥1.0k were cleared, but arbitrary `part_a`/`part_b` halves and hub-of-hub nests raised navigation cost. Defrag merged those halves ([#180](https://github.com/vivivieri/3d-JRPG-adventure-pc-game/pull/180)).

### Standing policy (do not reopen bulk thinning)

1. **No more bulk thinning rounds** chasing token bands (e.g. 900–999). Done bar: active leaves generally &lt;1.0k; thin hubs with pack TOCs.
2. **Named topic packs only** — pack filenames and TOC labels must name the topic (`weapons.md`, `field.md`). Never ship opaque `part_a` / `part_b` or `(A)`/`(B)` labels unless the names are real topics.
3. **Nest depth** — prefer **hub → leaf** or **hub → named packs**. Avoid hub-of-hub (a pack that is only another TOC). Cap practical depth; deep `../` chains are a smell.
4. **Clarity over sub-1k** — a coherent ~1.2–1.4k leaf beats another arbitrary split. Re-split only when a must_read/task pack blows budget, or one file mixes two jobs for different roles.
5. **Skim aids on fat leaves** — prefer sharp frontmatter `summary:` (for `resolve_docs` deferred tips) plus in-doc **When to read** / **Jump to** over new pack files. Sweep tool: `python3 tools/apply_docs_skim_aids.py` (idempotent; covers all active leaves by default; skips hubs/archive/briefs).
6. **Opportunistic only** — further splits happen when already editing that topic, not as dedicated thinning sprints.
7. **Next effort** — use packs (`resolve_docs` task packs, adherence), not more file splits. Tooling reference: `tools/consolidate_docs_part_ab.py` (defrag), not new `split_docs_roundN.py` by default.
8. **Pack budget headroom** — keep role/task `optional` lists lean so typical `resolve_docs --budget 12000` packs retain ≥~800 tok headroom. Prefer task packs for deep leaves (L3/L4, playtest act sheets, language style). When a task pack provides optionals, those replace generic role optionals (specialty remaps still merge). Remap CI work: `architect` + `acceptance_ci` → `qa`; skip zone/brief auto-attach on process tasks (`acceptance_ci`, `factory_bootstrap`, …). Re-measure: `python3 tools/audit_docs_read_efficiency.py`.

Authority: this ADR · pointer: [`docs/README.md`](../README.md) § Docs pack enhance.
