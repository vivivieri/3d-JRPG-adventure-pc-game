---
id: defense-layers
type: how-to
phase: [1, 5]
audience: [visual, qa]
status: active
authority: art
tokens_est: 1049
summary: "M1 check_model_catalog.py → required GLBs for phase"
---
# Model QA — Layers & Workflow — Defense layers

**Hub:** [`layers_workflow.md`](../layers_workflow.md)

## 2. Defense layers

```
M1  check_model_catalog.py       → required GLBs for phase
M2  check_model_technical.py     → tris, textures, banned sources
M3  blender_render_turntable.py  → 4-view PNG turntable
M3b review_model_vision.py       → 2-of-N LLM on turntable (hero/set-pieces)
L3  in-game screenshot           → VISUAL_QA.md (placement + zone)
L6  human playtest               → feel
```

### M1 — Catalog

```bash
python3 tools/check_model_catalog.py --phase 1
python3 tools/check_model_catalog.py --phase m5
```

Phase 1 minimum: `urashima`, `village_torii_damaged`, `village_well_stone`, `village_shack_roku` (SC-02 vertical slice).

### M2 — Technical GLB lint

```bash
python3 tools/check_model_technical.py --model urashima
python3 tools/check_model_technical.py --all-present
python3 tools/check_model_technical.py --model urashima --ship  # M5: fail greybox
```

| Check | Fail if |
|-------|---------|
| Triangles | Outside `qa_catalog.json` min/max |
| Textures | Fewer than `texture_min` embedded images |
| Source | Path under `models/nature/`, `models/castle/`, or manifest Kenney greybox (`--ship`) |
| File size | Hero < 100 KB (likely empty/blockout) |

### M2b — GLB import sanitizer (EditorScenePostImport)

```bash
bash tools/install_glb_import_pipeline.sh   # copies script + toon shader; patches .import sidecars
python3 tools/check_glb_import_scripts.py --strict
```

Templates:
- `tools/godot_templates/editor/glb_toon_post_import.gd` — assigns `toon_base.gdshader` ShaderMaterial; handles `StandardMaterial3D` + `ORMMaterial3D`
- `tools/godot_templates/shaders/toon_base.gdshader` — project NPR ramp family

**Godot (manual fallback):** `.glb` → Import → Scene → Advanced → Post Import Script → `res://scripts/editor/glb_toon_post_import.gd`

### M2c — Animation whitelist

```bash
python3 tools/check_animation_whitelist.py --phase m5 --strict
```

For each rigged model: `required_animations` ⊆ GLB clips ⊆ `allowed_animations` (see `CHARACTER_BIBLE.md` §8). Bosses `palace_sentinel` and `tide_keeper_p1` must have full animation contracts in `qa_catalog.json`.

### M3 — Turntable render (Blender)

```bash
python3 tools/render_model_turntable.py --model urashima
# → artifacts/model_reviews/urashima/{front,side,back,three_quarter}.png
```

Requires **Blender** (`install_extended_toolchain.sh`). Neutral grey studio + 4 orthographic-style views.

### M3b — Multi-LLM vision jury (hero + set-pieces)

```bash
python3 tools/review_model_vision.py --model urashima --min-pass 2
```

Sends **4 turntable PNGs** to vision models with `CHARACTER_BIBLE` / catalog brief.

**Hero jury scope** (`qa_catalog.json` → `hero_jury`): Urashima, Yuzu, Roku, torii, palace gate, lacquer box, Shore Wraith, Tide Keeper.

**Criteria (M1–M6):**

| # | Question |
|---|----------|
| M1 | Obvious **axis-aligned block** or untextured primitive? |
| M2 | **Stylized Japanese coastal** — not European castle / generic fantasy? |
| M3 | **Adult 1:5 proportions** — not chibi? |
| M4 | **Readable silhouette** at game distance (3/4 view)? |
| M5 | **Sufficient detail** for high-detail NPR target — not low-poly kitbash? |
| M6 | Matches model brief (coat, box, torii, etc.)? |
| M7 | **Emotional mood matches** generation brief (`docs/briefs/<id>.md`)? |
| M8 | **No forbidden tone** (comedy cheer, horror gore, bright Ghibli swagger)? |

**Pass:** ≥2 models `acceptance.valid_pass: true` (confidence ≥ 0.65, all M1–M8 met). Jury loads **Emotional intent** from generation brief when present. See `tools/generation_brief_lib.py`. Gate `L2_model_jury`.

**Note:** M7/M8 judge **art-direction emotional register** from stills — not animation feel or player enjoyment (human L6).

### Why turntable + in-game screenshot?

| Layer | Catches |
|-------|---------|
| Turntable jury | Bad mesh **before** Godot import |
| `VISUAL_QA.md` | Wrong material, lighting, zone palette **in context** |

Use **both**.

---
