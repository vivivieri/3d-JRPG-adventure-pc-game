---
id: tools-antipattern
type: how-to
audience: [visual, builder, qa]
phase: [1, 5]
status: active
authority: art
tokens_est: 608
summary: "Visual QA — Tools + black-box anti-pattern — Recommendation: Use L1 + L3c + L3d (2-of-3 LLM jury) + L4 golden diff together. No single tool replaces human playt"
---
# Visual QA — Tools + black-box anti-pattern

**Hub:** [`VISUAL_QA.md`](../VISUAL_QA.md)

## When to read

Use **Visual QA — Tools + black-box anti-pattern** (roles: visual, builder, qa) when executing this procedure Jump to a section below instead of reading end-to-end (2 sections).

## Jump to

- [2H. Tools that can judge visuals today (2026)](#2h-tools-that-can-judge-visuals-today-2026)
- [3. The black-box scenario (explicit anti-pattern)](#3-the-black-box-scenario-explicit-anti-pattern)


## 2H. Tools that can judge visuals today (2026)

| Tool | What it judges | Good for | Not good for |
|------|----------------|----------|--------------|
| **Multi-LLM vision jury** (`review_screenshot_vision.py`) | Primitives, palette mood, style rules, UI glitches, **emotional mood (V7–V8)** | Semantic “is this a grey box?” | Fun, pacing, controller feel |
| **Cursor agent (multimodal)** | Same as above when screenshot attached | Interactive iteration | Unbiased if same agent built scene |
| **Godot MCP Pro `compare_screenshots`** | Pixel diff vs golden PNG | Regression “did art change?” | New scenes, style compliance |
| **`check_screenshot_palette.py`** | Average color vs zone hex | Muted palette drift | Composition, silhouettes |
| **`check_scene_visuals.sh`** | BoxMesh in `.tscn` | Block placeholders before render | Materials, lighting |
| **LAION Aesthetic / ImageReward** | Generic “pretty” score | Ranking variants | JRPG-specific style rules |
| **Dedicated “game art QA” SaaS** | — | **None mature for stylized JRPG** | — |
| **Human L6 playtest** | Feel, emotion, fun | Ship gate | Slow, subjective |

**Recommendation:** Use **L1 + L3c + L3d (2-of-3 LLM jury) + L4 golden diff** together. No single tool replaces human playtest.

---


## 3. The black-box scenario (explicit anti-pattern)

**Bad workflow (forbidden):**

```
Agent: "Placed MeshInstance3D for shack — done"
Agent: marks task complete without screenshot
Agent: copies same BoxMesh pattern to pier, well, palace
```

**Required workflow:**

```
1. GodotPrompter plans NPR mesh or imports GLB (not BoxMesh)
2. GDAI places mesh + toon material
3. bash tools/check_scene_visuals.sh  → must PASS
4. GDAI F5 + screenshot gameplay view
5. Agent vision review V1–V6 (or multi-LLM jury L3d)
6. python3 tools/check_screenshot_palette.py --zone ...
7. python3 tools/review_screenshot_vision.py --min-pass 2 ...
8. Only then: mark task done / commit
```

---
