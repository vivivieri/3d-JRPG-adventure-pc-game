# 3D Model QA — Technical Gates + Turntable Vision Jury

**Version:** 1.0  
**Problem:** An agent can import a **low-poly blockout**, **Kenney greybox**, or **chibi AI mesh** and call it “Urashima done” — then reuse that quality bar everywhere.

**Rule:** Models pass **catalog + GLB technical lint + turntable vision jury** (hero/set-pieces) before ship. In-game screenshot QA (`docs/VISUAL_QA.md`) catches placement; this doc catches **the asset itself**.

**Cross-refs:** `docs/CHARACTER_BIBLE.md`, `docs/ITEMS_3D_MODEL_GUIDE.md`, `docs/ART_AUTOMATION_PIPELINE.md` §5, `docs/QA_REMEDIATION_LOOP.md`, `docs/ACCEPTANCE_CRITERIA.md`, `game/data/models/qa_catalog.json`

---

## 1. What to automate vs human

| Automate | Human L6 |
|----------|----------|
| GLB exists, path correct | Walk cycle feels natural |
| Triangle count in budget | Coat cloth weight |
| Embedded textures present | Combat hit readability |
| Not Kenney/greybox path | Emotional attachment to character |
| Turntable: not block primitive | Zone composition at gameplay camera |
| Turntable: silhouette + style jury | |

---

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

**Pass:** ≥2 models `acceptance.valid_pass: true` (confidence ≥ 0.65, all M1–M6 met). See `docs/ACCEPTANCE_CRITERIA.md` gate `L2_model_jury`.

### Why turntable + in-game screenshot?

| Layer | Catches |
|-------|---------|
| Turntable jury | Bad mesh **before** Godot import |
| `VISUAL_QA.md` | Wrong material, lighting, zone palette **in context** |

Use **both**.

---

## 3. Agent workflow (3D model task)

```
1. Meshy/Tripo/Rodin → Blender decimate/UV → export GLB
2. ComfyUI/Material Maker albedo + palette_remap.py
3. python3 tools/register_asset.py
4. python3 tools/check_model_catalog.py --phase 1
5. python3 tools/check_model_technical.py --model urashima
6. python3 tools/render_model_turntable.py --model urashima
7. python3 tools/review_model_vision.py --model urashima
8. GDAI MCP — import, toon shader, F5 + VISUAL_QA screenshot
```

---

## 4. L2 smoke

```bash
bash tools/run_model_smoke_checks.sh
```

| State | Behavior |
|-------|----------|
| No `urashima.glb` | **WARN** skip |
| GLB exists | catalog + technical; turntable + jury if Blender + API keys |
| Jury fail | **FAIL** → run `qa_remediation_brief.py` before rebuild |

Wired into `run_playtest_smoke.sh`.

---

## 5. Agent report template

```
[MODEL QA] model=urashima
  catalog phase1: PASS
  technical: PASS (14234 tris, 2 textures)
  turntable: artifacts/model_reviews/urashima/
  jury: PASS (2/3)
  in_game_visual: pending GDAI screenshot
  result: PASS (asset); PENDING (in-scene)
```

---

## 6. Tools

| Tool | Role |
|------|------|
| `game/data/models/qa_catalog.json` | Paths, tri budgets, jury list |
| `tools/check_model_catalog.py` | Phase required models |
| `tools/check_model_technical.py` | GLB lint |
| `tools/render_model_turntable.py` | Blender 4-view render |
| `tools/review_model_vision.py` | Multi-LLM turntable jury |
| `tools/run_model_smoke_checks.sh` | L2 smoke wrapper |

---

## 7. vs Visual / Audio QA

| | Visual | Audio | **3D Model** |
|--|--------|-------|----------------|
| Static lint | `.tscn` primitives | LUFS/format | **GLB tris/textures** |
| Render for jury | Game screenshot | Listen to Ogg | **Blender turntable** |
| LLM scope | Every zone shot | 8 hero BGMs | **hero_jury list only** |
| In-engine verify | Required | GDAI wire | **Required (VISUAL_QA)** |
