---
id: scene-style
type: reference
phase: [1, 2, 3, 4, 5, 6]
audience: [architect, builder]
status: active
authority: engineering
tokens_est: 786
summary: "**Scope:** `game/scenes/**/*.tscn` (`game/development` only — **no `.tscn` on `main`**)"
---
# Godot Scene Style Guide — Tides of Urashima

**Version:** 1.0
**Scope:** `game/scenes/**/*.tscn` (`game/development` only — **no `.tscn` on `main`**)
**Hub:** [`CODING_STANDARDS_HUB.md`](CODING_STANDARDS_HUB.md)

## When to read

Use **Godot Scene Style Guide — Tides of Urashima** (roles: architect, builder) when you need this reference during the current task Jump to a section below instead of reading end-to-end (7 sections).

## Jump to

- [1. Naming & layout](#1-naming-layout)
- [2. Scene graph rules](#2-scene-graph-rules)
- [3. GDAI verification marker](#3-gdai-verification-marker)
- [4. Static format (`.tscn` text)](#4-static-format-tscn-text)
- [5. Workflow](#5-workflow)
- [6. CI enforcement](#6-ci-enforcement)
- [7. PR checklist (`game/development`)](#7-pr-checklist-gamedevelopment)


## 1. Naming & layout

| Rule | Example |
|------|---------|
| File name | `snake_case.tscn` — `ruined_village.tscn` |
| Greybox | `zone/greybox/` or `*_greybox.tscn` — excluded from ship lint |
| Zone scenes | `game/scenes/zones/<zone_id>.tscn` |
| UI | `game/scenes/ui/<feature>.tscn` |
| Components | `game/scenes/components/<name>.tscn` — instanced by Builder |

---

## 2. Scene graph rules

| Rule | Detail |
|------|--------|
| Base classes | Player → `PlayerController`; interactables → `Interactable` — [`CODE_BASE_CLASS_RULES.md`](CODE_BASE_CLASS_RULES.md) |
| No new `CharacterBody3D` stacks | Extend `PlayerController` only |
| Primitives | No `BoxMesh` / `CapsuleMesh` in ship scenes — NPR meshes (`VISUAL_QA.md`) |
| Lighting | One directional + one fill per zone — [`ENVIRONMENT_KITS.md`](../../design/world/ENVIRONMENT_KITS.md) |
| `WorldEnvironment` | Per-zone fog, tonemap, glow per `RENDERING_GUIDE.md` |

---

## 3. GDAI verification marker

Ship scenes require `game/scenes/.gdai_built` with `verified_f5=true` after editor playtest.

| Check | Gate |
|-------|------|
| No hand-built ship `.tscn` on `main` | `L0_rr_compliance` |
| GDAI marker when scenes change | `L3_gdai_built` |
| Primitive / banned kit scan | `L2_scene_primitives` (`check_scene_visuals.sh`) |
| Static naming & format | `L1_scene_style` (`check_scene_style.sh`) |

---

## 4. Static format (`.tscn` text)

| Rule | Detail |
|------|--------|
| Header | Must start with `[gd_scene` |
| Godot version | `format=3` (Godot 4.x) |
| Paths | `res://` — no absolute filesystem paths |
| IDs | No European/Kenney castle kits in `res://` refs |

---

## 5. Workflow

```
GodotPrompter plan → GDAI MCP build/tune → F5 verify → update .gdai_built
```

Never hand-edit `.tscn` in Cursor when GDAI MCP is connected.

---

## 6. CI enforcement

```bash
bash tools/check_scene_style.sh      # L1_scene_style — SKIP on main
bash tools/check_scene_visuals.sh    # L2_scene_primitives — game/development
bash tools/check_rr_compliance.sh    # L0_rr_compliance
```

---

## 7. PR checklist (`game/development`)

- [ ] Scene built via GDAI MCP; `.gdai_built` updated
- [ ] `bash tools/check_scene_style.sh` green
- [ ] `bash tools/check_scene_visuals.sh` green
- [ ] Zone row in `ENVIRONMENT_KITS.md` applied
- [ ] No primitive placeholders in player-facing paths
