---
id: setup-ceremony
type: how-to
phase: [0, 1, 8]
audience: [pm]
status: active
authority: workflow
tokens_est: 789
summary: "Full machine-readable rows: `game/data/qa/sprint_phases.json`."
---
# Agile — Linear Sprints — Setup + ceremony

**Hub:** [`linear_sprints.md`](../linear_sprints.md)

## 3. Linear setup (when MCP authenticated)

### 3.1 Linear hierarchy

| Linear entity | Maps to |
|---------------|---------|
| **Workspace** | Your studio / personal workspace |
| **Team** | `Tides of Urashima` |
| **Projects** | `M1-core`, `M5-art`, `M6-steam` (+ optional `M0-foundation`) |
| **Cycles** | 1-week batches **inside** current phase (close on gates, not calendar) |
| **Issues** | GitHub Issues (mirror or primary in Linear, link both ways) |
| **Labels** | Mirror `env/*`, `agent/*`, `gate/*` from `PROJECT_MANAGEMENT.md` |

### 3.2 Linear ↔ implementation phase map

| Impl phase | Linear project | Milestone | Sprint focus (examples) | Phase exit (must PASS) |
|------------|----------------|-----------|-------------------------|-------------------------|
| **0** ✅ | — | M0 | Done — docs/data baseline | `run_docs_ci_checks.sh` |
| **1** ← now | `M1-core` | — | ruined_village slice, toon shader, zone_visuals | `phase_1` gates in `acceptance_criteria.json` |
| **2** | `M1-core` | M1 | boot, LocalizationManager, settings UI | Phase 2 criteria §`AI_DEV_WORKFLOW` |
| **3** | `M1-core` | M1 | dialogue, quests, exploration, shop | L4 integration scenarios |
| **4** | `M1-core` | M2 | combat vertical slice, boss framework | Combat INT-* pass |
| **5** | `M1-core` | M3 | Chapter 1 dungeons, SC-08/11/12 | Zone flow L4 |
| **6** | `M1-core` | M4 | full story, 3 endings, cinematics | **L5 E2E** three endings |
| **7** | `M5-art` | M5 | NPR zones, hero meshes, VO clips | L2 jury + model/audio technical |
| **8** | `M6-steam` | M6 | GodotSteam, export, store, playtest | L6 + `STEAM_RELEASE_CHECKLIST` |

Full machine-readable rows: `game/data/qa/sprint_phases.json`.

### 3.3 Cycle naming convention

```
Phase{N}-Sprint{K}   e.g. Phase1-Sprint1, Phase1-Sprint2
```

Or date-based: `2026-W28` with description `Phase 1 — ruined village`.

**One active implementation phase at a time** on `game/development`. Cycle goals must cite phase task IDs from `IMPLEMENTATION_PLAN.md` (e.g. 1.3, 1.8).

---



## 4. Sprint ceremony (lightweight — AI team)

| Ceremony | When | Owner | Output |
|----------|------|-------|--------|
| **Phase kickoff** | Start of phase N | PM Agent (sprint facilitator) | Linear project/cycle + issues from IMPLEMENTATION_PLAN §Phase N table |
| **Sprint planning** | Cycle start | PM Agent (sprint facilitator) | 5–10 issues max; each has gate IDs + `agent/*` label |
| **Daily** | Each agent session | Active agent | Commit + CI; update issue status |
| **Sprint review** | Cycle end | QA Agent | Gate report pasted in issue/PR |
| **Phase review** | All phase tasks done | QA + Flow Agent | Phase exit gates; optional `v*-rc*` tag → UAT |
| **Retro** | After UAT or phase exit | PM + Human | Update `sprint_phases.json` notes; adjust next cycle WIP |

No standups required — agent session logs + GitHub Actions replace them.

---
