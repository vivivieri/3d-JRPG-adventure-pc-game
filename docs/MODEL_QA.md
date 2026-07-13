# 3D Model QA — Technical Gates + Turntable Vision Jury

**Version:** 1.2  
**Problem:** An agent can import a **low-poly blockout**, **Kenney greybox**, or **chibi AI mesh** and call it “Urashima done” — then reuse that quality bar everywhere.

**Rule:** Models pass **catalog + GLB technical lint + turntable vision jury** (hero/set-pieces) before ship. In-game screenshot QA (`docs/VISUAL_QA.md`) catches placement; this doc catches **the asset itself**.

**Cross-refs:** `docs/CHARACTER_BIBLE.md`, `docs/ITEMS_3D_MODEL_GUIDE.md`, `docs/ART_AUTOMATION_PIPELINE.md` §5, `docs/QA_REMEDIATION_LOOP.md`, `docs/ACCEPTANCE_CRITERIA.md`, `docs/GENERATION_READINESS.md`, `docs/generation_briefs/`, `game/data/models/qa_catalog.json`

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
3. python3 tools/register_asset.py add --path <path> --license <id> --source <name> --author <name> --used-for <desc>
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

---

## 8. Model polish cadence (structured iteration)

**Problem:** “Keep tweaking until it feels right” without a ladder produces infinite retries or random prompt changes.

**Rule:** Polish is **gate-driven**. Each attempt changes **one lever** (`docs/QA_REMEDIATION_LOOP.md` §3), logs to `revision_log.json`, and re-runs the **full** model layer — not jury-only reruns.

### 8.1 Attempt ladder (default per asset)

| Attempt | Goal | Primary levers | Exit when |
|---------|------|----------------|-----------|
| **0 — Gen** | First shippable candidate | `prompt` + `tool_tier` (Meshy/Tripo/Rodin) | Technical PASS |
| **1 — Read** | On-brand silhouette | `mesh_ops` (Blender sculpt/decimate) or `prompt` if M2/M3/M6 fail | Turntable jury PASS (M1–M6) |
| **2 — Context** | Reads in zone + motion | `texture` + `shader_scene` + GDAI placement | `VISUAL_QA` gameplay screenshot PASS |
| **3 — Feel** | Human enjoyment | Human L6 feedback → brief/doc update → **one** rebuild lever | `PLAYTEST_SCRIPT.md` §7b avg ≥3.5 (≥5 testers) |

After **3 automated attempts** with no PASS → **escalate** (tool tier ↑, manual Blender pass, or human L6 waiver with evidence). Same lever class twice → **blocked** (`QA_REMEDIATION_LOOP.md` §6).

### 8.2 Polish commands (one full pass)

```bash
MODEL=urashima
python3 tools/check_model_technical.py --model "$MODEL" --ship
python3 tools/render_model_turntable.py --model "$MODEL"
python3 tools/review_model_vision.py --model "$MODEL" --min-pass 2
# GDAI: import, zone placement, gameplay screenshot
python3 tools/check_screenshot_palette.py --zone ruined_village --screenshot artifacts/screenshots/phase1_ruined_village_gameplay.png
bash tools/run_model_smoke_checks.sh
```

On FAIL: `bash tools/qa_emit_remediation.sh model-tech|model-jury <args>` — apply **one** action from the brief before the next attempt.

### 8.3 What “polish” is not

| Invalid | Why |
|---------|-----|
| Re-run jury without rebuilding GLB | Symptom unchanged |
| Tweaking `min-pass` or marking WARN as PASS | Gate shopping |
| Agent “looks fine to me” without jury + screenshot | No measurable evidence |
| More than 3 automated loops on same failure code | Escalate per stop rules |
| Builder changes mesh without Architect brief / failed criterion | R&R violation — direction must be traceable |

---

## 9. Who gives direction vs who knows “feels right”

Polish has **two different questions**. The project answers them with **different owners**.

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
| 1 | `docs/GDD.md`, `docs/STORYBOARD.md` | **PM** (facilitates) | Mood, audience, scene intent |
| 2 | `docs/ART_DIRECTION.md`, `docs/CHARACTER_BIBLE.md`, `docs/ENVIRONMENT_KITS.md` | **PM + design docs** | Palette, silhouettes, zone kits |
| 3 | `docs/generation_briefs/<id>.md` | **Architect + Visual** | Per-asset prompt recipe (plan input) |
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

### 9.4 How “keep tweaking” works legally

```
FAIL (automated) ──▶ remediation brief ──▶ ONE lever ──▶ rebuild ──▶ re-measure
                              │
                              ▼
                    cite: gate ID + bible/brief row

L0–L5 PASS ──▶ Human L6 ──▶ feedback ("coat too stiff")
                              │
                              ▼
                    PM/Architect updates brief or bible row
                              │
                              ▼
                    Builder regen/import ──▶ full QA stack again
```

**Traceability rule:** Every polish commit message must cite **what failed** (gate ID or human F#) and **which lever changed**. Example: `fix(urashima): attempt 2 — m4_silhouette, mesh_ops coat hem exaggeration`.

### 9.5 Role cheat sheet

| Role | Gives direction? | Knows “feels right”? |
|------|------------------|----------------------|
| **PM** | Prioritizes *which* asset/zone; does not override palette/bible | Facilitates L6; accepts ship with gate evidence |
| **Architect** | Writes briefs, plans, shaders; extends bible via PR to `main` | No — proposes against docs |
| **Visual Agent** | No — measures vs bible/brief | No — jury is compliance, not enjoyment |
| **Builder** | No | No — F5 verify only |
| **QA Agent** | No — enforces gates | No — proves PASS/FAIL |
| **Vision jury (LLM)** | No — reads bible/brief as rubric | Partial — style/silhouette only, not fun |
| **Human QA** | **Yes** for feel gaps not in automation | **Yes** — L6 sign-off |

### 9.6 Gaps (honest limits)

| Gap | Mitigation today |
|-----|------------------|
| Jury cannot score “fun” or emotional attachment | Human L6 + `PLAYTEST_SCRIPT.md` §7b F6–F8 |
| `animation_timing` not in CI yet | Brief targets + manual review until P1 catalog field |
| No standing “polish sprint” without FAIL | M5 milestone + per-asset production order (`CHARACTER_BIBLE.md` §11) |

See `docs/GENERATION_READINESS.md` for per-row ⚠️ Partial items that still need human judgment after gates pass.
