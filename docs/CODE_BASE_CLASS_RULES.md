# Code Base Classes — Agent R&R (Not 3D Meshes)

**Version:** 1.0  
**Machine-readable:** `game/data/code/base_classes.json`  
**Cross-refs:** `docs/TECHNICAL_DESIGN.md`, `docs/RR_CHEATSHEET.md`, `docs/ASSET_COMPLIANCE.md`, `docs/ART_AUTOMATION_PIPELINE.md`

---

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

- `extends CharacterBody3D` on player rig in a zone scene
- New autoload singletons
- Rewriting `InputMap` actions (canonical list: `UI_UX_FLOW.md`)
- Parallel combat stack “for one boss”

---

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

## 5. Verification

```bash
python3 tools/validate_base_classes.py
bash tools/check_rr_compliance.sh          # no rogue ship scene scripts
bash tools/check_animation_whitelist.py    # when GLB present
bash tools/install_glb_import_pipeline.sh  # once per dev env (game/development)
```

On `game/development` CI: `L0_base_classes`, `L2_animation_whitelist` (conditional), `L1_gdscript_lint` (changed files).

---

## 6. Cross-refs

- `docs/CHARACTER_BIBLE.md` — rig + animation names  
- `docs/MODEL_QA.md` — GLB import + post-import  
- `docs/CONTROLS_CHEATSHEET.md` — gate enforcement  
