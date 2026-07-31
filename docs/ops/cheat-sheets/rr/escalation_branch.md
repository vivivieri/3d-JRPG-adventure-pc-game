---
id: escalation-branch
type: reference
phase: [0, 1]
audience: [pm, builder, qa]
status: active
authority: ops
tokens_est: 627
summary: "R&R Cheat Sheet — Escalation, branch, sprint, forbidden — docs/ops/qa/ESCALATION_POLICY.md` · `game/data/qa/escalation_policy.json` · `tools/pm_escalate.py"
---
# R&R Cheat Sheet — Escalation, branch, sprint, forbidden

**Hub:** [`RR_CHEATSHEET.md`](../RR_CHEATSHEET.md)

## When to read

Use **R&R Cheat Sheet — Escalation, branch, sprint, forbidden** (roles: pm, builder, qa) when you need this reference during the current task Jump to a section below instead of reading end-to-end (4 sections).

## Jump to

- [Escalation ladder (no infinite dev↔QA loops)](#escalation-ladder-no-infinite-devqa-loops)
- [Branch & environment](#branch-environment)
- [Sprint batches (AI-native)](#sprint-batches-ai-native)
- [Forbidden without user override](#forbidden-without-user-override)


## Escalation ladder (no infinite dev↔QA loops)

`docs/ops/qa/ESCALATION_POLICY.md` · `game/data/qa/escalation_policy.json` · `tools/pm_escalate.py`

| Tier | Owner | Cap → next |
|------|-------|-----------|
| 1 · dev ↔ QA loop | dev + QA | **max 3 reopens** → arbitration |
| 2 · Arbitration | **Architect (Design Authority / SA)** | classify root cause; resolve or (needs business decision) → Product Owner |
| 3 · Product Owner | Human (Telegram) | final — `amend_requirement`/`descope`/`wont_fix`/`approve_as_is`/`reprioritize` |

Only the arbiter (Architect/SA) or the Product Owner may change a requirement — that is what breaks the loop. Every tier is capped; escalation goes **up**, never sideways.


## Branch & environment

| Target | Branch | Lead agent | Contents |
|--------|--------|------------|----------|
| Design | `main` | PM | `docs/`, `game/data/`, `tools/` |
| Implementation | `game/development` | Architect + Builder | Godot project, scenes, assets |
| UAT artifact | tag on `game/development` | Release | `v*-rc*`, `v*-beta*` |
| Ship | tag + Steam | Release + Human | `v1.0.*` after M6 checklist |

---


## Sprint batches (AI-native)

- Close cycle when **gate evidence is on PR** — not when calendar week ends.
- **Micro:** 1–3 issues · **Standard:** ≤10 issues · **Integration:** L4/L5 green.
- Config: `game/data/qa/sprint_phases.json` · Policy: `docs/ops/workflow/AGILE_WITHIN_PHASES.md` §12.1.

---


## Forbidden without user override

- Hand-editing ship `.tscn` in Cursor
- Gameplay/visual work with GDAI disconnected
- MCP Pro / Godotiq for scene mutations
- Kenney kits, unknown-license web assets
- Summer Engine, Fennara (fourth scene editor)
- Skipping phase gates via sprint reprioritization
- **Cross-cutting factory feature merged without `workflow_integration_registry.json` entry** — run `bash tools/check_feature_integration.sh --remind`

---
