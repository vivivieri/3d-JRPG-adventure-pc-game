---
id: puzzle-design
type: reference
phase: [1, 5]
audience: [builder, architect]
status: active
authority: world
tokens_est: 768
summary: "Tides of Urashima — Puzzle Design (SC-07) — Version: 1.0 (Pre-build)"
---
# Tides of Urashima — Puzzle Design (SC-07)

## When to read

Use **Tides of Urashima — Puzzle Design (SC-07)** (roles: builder, architect) when you need this reference during the current task Jump to a section below instead of reading end-to-end (9 sections).

## Jump to

- [1. Overview](#1-overview)
- [2. Layout](#2-layout)
- [3. States](#3-states)
- [4. Solution path](#4-solution-path)
- [5. Hint system](#5-hint-system)
- [6. Soft-lock checks](#6-soft-lock-checks)
- [7. Assets](#7-assets)
- [8. Audio / feedback](#8-audio-feedback)
- [9. QA checklist](#9-qa-checklist)


## 1. Overview

| Field | Value |
|-------|-------|
| **Location** | Tidal Caves — flooded chamber |
| **Type** | 2-state water level switch |
| **Duration target** | 2–5 minutes |
| **Fail state** | None — cannot die |
| **Blocks** | Deep pool (SC-08) until solved |
| **Dialogue** | **None** — intentional quiet beat (`NARRATIVE_WRITING_GUIDE.md` §4) |

---

## 2. Layout

```
[SOUTH - entrance]
     |
  [Switch A] ---- [Basin - water plane]
     |
  [Platform - latch] (reachable HIGH only)
     |
  [Optional chest] (LOW path side chamber)
     |
[NORTH - deep pool exit]
```

---

## 3. States

| State | Water Y | Switch A | Access |
|-------|---------|----------|--------|
| **LOW** | -0.5m | Off | Chest chamber dry; latch blocked |
| **HIGH** | +0.8m | On | Latch reachable; chest flooded |

**Single switch** toggles LOW ↔ HIGH. Animation 2s water rise/fall.

---

## 4. Solution path

1. Enter chamber (LOW default)
2. Optional: loot chest in side alcove (LOW) — contains `tide_cut_saber` (`scenes.json` `grants_items`)
3. Flip Switch A → HIGH
4. Cross platform to **Ancient Latch** (interact E)
5. Latch opens north gate → SC-08 deep pool
6. Flag: `water_puzzle_solved`

**No reverse required** for main path after latch.

---

## 5. Hint system

| Time stuck | Hint delivery |
|------------|---------------|
| 0–3 min | None |
| 3 min | Quest log: *"The tide remembers two heights."* |
| 5 min | Switch glow pulse + audio chime |
| 8 min | Quest log + Urashima thought: *"Raise the water. The lock floats."* (optional ghost subtitle if `met_roku`) |

Requires `hints_enabled` in settings (default on).

---

## 6. Soft-lock checks

| Risk | Mitigation |
|------|------------|
| Player leaves HIGH, can't reach latch | Switch visible from all paths |
| Chest missable | Optional; `tide_cut_saber` is a bonus weapon, never required (Normal clear possible on `fisher_katana`) |
| Water animation interrupt | Player can move; no lock-in |

---

## 7. Assets

- `cave_switch_stone` — interactable
- `cave_flood_basin` — water mesh
- `WaterPuzzle` node — state machine
- `cave_chest_ancient` — optional chest: `tide_cut_saber` (canonical, `scenes.json` SC-07 `grants_items`)

---

## 8. Audio / feedback

- Switch: stone grind + water rush
- Latch open: metallic clang + quest complete ping
- HIGH state: drip ambient louder

---

## 9. QA checklist

- [ ] Solvable in 2 toggles
- [ ] Hints fire at 3 min
- [ ] `water_puzzle_solved` gates SC-08
- [ ] No sequence break via jump clipping
