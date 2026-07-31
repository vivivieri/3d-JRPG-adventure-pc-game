---
id: meaning-rules
type: reference
phase: [1, 2, 3, 4, 5, 6]
audience: [architect, builder]
status: active
authority: engineering
tokens_est: 586
summary: "Analogy: Human-made skeleton code (classes). AI fills instances (scenes, data, materials) — not a new skeleton per feature."
---
# Code Base Class Rules — What inherit means + hard R&R

**Hub:** [`CODE_BASE_CLASS_RULES.md`](../CODE_BASE_CLASS_RULES.md)

## When to read

Use **Code Base Class Rules — What inherit means + hard R&R** (roles: architect, builder) when you need this reference during the current task Jump to a section below instead of reading end-to-end (5 sections).

## Jump to

- [1. What “inherit human base classes” means](#1-what-inherit-human-base-classes-means)
- [2. Hard R&R rules](#2-hard-rr-rules)
- [Architect (GodotPrompter) — owns bases](#architect-godotprompter-owns-bases)
- [Builder (GDAI MCP) — instances only](#builder-gdai-mcp-instances-only)
- [Forbidden without Architect PR + TDD update](#forbidden-without-architect-pr-tdd-update)


## 1. What “inherit human base classes” means

| Means | Does **not** mean |
|-------|-------------------|
| **GDScript** classes authored by **Architect (GodotPrompter)** on `game/development` | Downloading a human-sculpted **3D character mesh** and “modifying” it |
| Agents **extend** `PlayerController`, `Combatant`, `Interactable` | Agents write new `CharacterBody3D` movement from scratch |
| Combat math lives in **autoloads + `game/data/`** | AI rewrites damage formulas in zone scenes |
| **GDAI MCP** instances **component `.tscn`** files | AI hand-builds one-off node trees per chest/NPC |

**Analogy:** Human-made **skeleton code** (classes). AI fills **instances** (scenes, data, materials) — not a new skeleton per feature.

---


## 2. Hard R&R rules

### Architect (GodotPrompter) — owns bases

- Create/update files listed in `base_classes.json` → `architect_owns`
- Define **state machines** (`TurnManager`, puzzle FSM) — not free-form `_process` spaghetti
- Unit tests for formulas and flag wiring (`L1_unit_tests`)

### Builder (GDAI MCP) — instances only

- Place **component scenes** from `LEVEL_DESIGN.md` §1b catalog
- Assign meshes/materials; **do not** add new gameplay scripts on zone roots
- Subclass scripts only when Architect adds an approved `extends Interactable` variant in a **named** file

### Forbidden without Architect PR + TDD update

- Native `extends CharacterBody3D` / `Area3D` / `Node` outside registered base class files
- New autoload singletons
- Rewriting `InputMap` actions (canonical list: `UI_UX_FLOW.md`)
- Parallel combat stack “for one boss”

---
