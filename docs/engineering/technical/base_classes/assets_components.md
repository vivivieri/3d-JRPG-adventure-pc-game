---
id: assets-components
type: reference
phase: [1, 2, 3, 4, 5, 6]
audience: [architect, builder]
status: active
authority: engineering
tokens_est: 529
summary: "Code Base Class Rules — 3D asset sources + component scenes — Code base classes ≠ 3D base mesh. For models, use this pipeline only:"
---
# Code Base Class Rules — 3D asset sources + component scenes

**Hub:** [`CODE_BASE_CLASS_RULES.md`](../CODE_BASE_CLASS_RULES.md)

## When to read

Use **Code Base Class Rules — 3D asset sources + component scenes** (roles: architect, builder) when you need this reference during the current task Jump to a section below instead of reading end-to-end (3 sections).

## Jump to

- [3. 3D assets — license-safe sources (separate from code bases)](#3-3d-assets-license-safe-sources-separate-from-code-bases)
- [Optional proportion reference (not shipped)](#optional-proportion-reference-not-shipped)
- [4. Component scenes (Builder catalog)](#4-component-scenes-builder-catalog)


## 3. 3D assets — license-safe sources (separate from code bases)

**Code base classes ≠ 3D base mesh.** For **models**, use this pipeline only:

| Source | License | Use for | Ship? |
|--------|---------|---------|-------|
| **Repo procedural** (`tools/generate_*`) | ORIGINAL | Placeholders, audio, portraits | ✅ |
| **Meshy / Tripo / Rodin** + Blender | Service ToS → `LICENSES.md` | Hero/enemy meshes | ✅ when logged |
| **Mixamo** rig + clips | Adobe ToS | Humanoid walk/combat animations | ✅ document |
| **Poly Haven** | CC0 | Rocks, trees — **greybox/nature props only** | ✅ not hero look |
| **ComfyUI / Material Maker** | Workflow doc | Tileable NPR albedos | ✅ |
| **Kenney / random Sketchfab** | Varies | **Greybox only** — banned ship | ❌ player-facing |
| **Copyrighted anime / Ghibli refs** | AR | Style reference only | ❌ |

**There is no “download one free human base body and reskin” hero path** — heroes are **AI-generated to `CHARACTER_BIBLE.md`**, rigged **Mixamo humanoid**, animations from **whitelist** (`qa_catalog.json`).

### Optional proportion reference (not shipped)

- CC0 mannequin or blockout mesh in `game/assets/_dev/` for scale checks only — **never** in `qa_catalog.json` ship paths.

---


## 4. Component scenes (Builder catalog)

See `LEVEL_DESIGN.md` §1b and `base_classes.json` → `component_scenes`.

Builder **instances** these in zones; does not author new trigger types without Architect.

---
