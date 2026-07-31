---
id: part-a
type: reference
phase: [1, 5]
audience: [visual, qa]
status: active
authority: art
tokens_est: 642
summary: "Model QA — Who Directs Feel (A)"
---
# Model QA — Who Directs Feel — Model QA — Who Directs Feel (A)

**Hub:** [`who_directs.md`](../who_directs.md)

### 9.1 Two questions

| Question | Meaning | Who **sets** direction | Who **judges** pass/fail |
|----------|---------|------------------------|--------------------------|
| **Are we on-direction?** | Correct brand, culture, silhouette, palette, story read | Design docs on `main` | L2 automated gates + vision jury |
| **Does it feel right?** | Weight, motion, attachment, combat telegraph in play | Human playtest feedback | **Human QA (L6)** after L0–L5 green |

Agents **execute and measure** — they do **not** own taste or redefine the art bible.


### 9.2 Direction authority chain (on-direction)

When in doubt, resolve in this order:

| Priority | Source | Owner role | What it defines |
|----------|--------|------------|-----------------|
| 1 | `docs/design/vision/GDD.md`, `docs/design/vision/STORYBOARD.md` | **PM** (facilitates) | Mood, audience, scene intent |
| 2 | `docs/design/art/ART_DIRECTION.md`, `docs/design/art/CHARACTER_BIBLE.md`, `docs/design/world/ENVIRONMENT_KITS.md` | **PM + design docs** | Palette, silhouettes, zone kits |
| 3 | `docs/briefs/<id>.md` | **Architect + Visual** | Per-asset prompt recipe (plan input) |
| 4 | `game/data/models/qa_catalog.json` | **Architect** | Tris, paths, animation contracts |
| 5 | `game/data/qa/acceptance_criteria.json` | **QA + Architect** | Measurable thresholds (M1–M6, L2 gates) |
| 6 | `game/data/qa/remediation_playbook.json` | **QA** | FAIL code → **one** lever to try next |

**Visual Agent** does not invent direction — it runs jury evidence against rows 2–5.

**Builder (GDAI)** applies meshes in scenes; it does not change prompts or bible rows without Architect handoff.


### 9.3 Who knows “feels right” (in motion)

| Signal | Owner | When |
|--------|-------|------|
| Turntable M4/M5 (static silhouette, detail) | Vision jury (2-of-N LLM) | Before / during import |
| Gameplay screenshot V5 (silhouette in zone) | Vision jury + `VISUAL_QA.md` | After GDAI placement |
| Walk cycle, cloth weight, combat read, attachment | **Human testers** | **L6 only** — `PLAYTEST_SCRIPT.md` §7b |
| Input latency, camera spring | `GAME_FEEL.md` + `feel_thresholds.json` | L2 feel smoke + human F1–F2 |

**Human QA Lead** is the **final arbiter** for subjective enjoyment. No agent may mark M5 art ship-ready on “vibes” alone.
