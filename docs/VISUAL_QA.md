# Visual QA — How AI Reviews Look & Feel

**Version:** 1.0  
**Problem:** An agent can “succeed” at placing a `BoxMesh`, decide it looks fine in the abstract, and replicate that placeholder across every zone. **Policy text alone does not prevent this.**

**Rule:** AI does **not** pass visual work on log output or node counts alone. It must pass **automated visual gates** + **screenshot review** against `docs/ART_DIRECTION.md`.

**Cross-refs:** `docs/ART_AUTOMATION_PIPELINE.md` §5, `docs/MODEL_QA.md` (asset QA before in-scene), `docs/QA_REMEDIATION_LOOP.md` (FAIL → fix loop), `docs/ACCEPTANCE_CRITERIA.md` (gate `L2_visual_*`)

---

## 1. What AI can and cannot judge

| AI can automate | AI cannot fully replace (needs human L6) |
|---------------|----------------------------------------|
| Detect `BoxMesh` / primitive meshes in `.tscn` | Emotional pacing, “does this feel sad enough?” |
| Sample screenshot pixels vs zone palette hex | Controller comfort |
| Compare screenshot to golden reference PNG | Localization nuance (ja/zh typography) |
| Flag pink missing-font boxes, UI overlap (vision) | Whether combat is fun |
| Verify fog/tonemap nodes exist in scene | Audio mix quality |

**Honest limit:** Without a **viewport screenshot** reviewed by a **multimodal** agent (or human), the AI is blind. `F5 PASS` + `0 errors` is **not** visual approval.

---

## 2. Defense layers (use all — not pick one)

```
L1  check_scene_visuals.sh     → block BoxMesh/primitives in ship .tscn
L3  GDAI screenshot            → artifacts/screenshots/<zone>_<camera>.png
L3b Vision checklist           → agent reads image vs ART_DIRECTION §10
L3c check_screenshot_palette   → muted palette / no candy-bright failure
L3d Multi-LLM vision jury      → 2+ models must PASS (review_screenshot_vision.py)
L4  compare_screenshots (MCP Pro) → diff vs golden master when present
L6  Human playtest             → feel, pacing, fun (after L0–L5)
```

### Layer A — Static scene lint (before commit)

```bash
bash tools/check_scene_visuals.sh
```

Fails if player-facing `.tscn` files contain banned primitive mesh types (`BoxMesh`, `CapsuleMesh`, etc.) or Kenney castle assets. Greybox paths (`greybox/`, `_dev/`, `*.greybox.tscn`) are excluded.

**Run in:** `run_playtest_smoke.sh`, Phase 1+ PRs, M5 gate.

`bash tools/run_visual_smoke_checks.sh` runs palette + multi-LLM jury when `artifacts/screenshots/phase1_<zone>_gameplay.png` exists; **WARNs and skips** until Phase 1 captures screenshots.

### Layer B — Mandatory screenshot (every zone/UI task)

Per `docs/AI_TESTING_SPEC.md` §5.2 step 7:

1. GDAI MCP (or Godotiq / MCP Pro) captures **gameplay camera** viewport at **1920×1080**
2. Save to `artifacts/screenshots/<phase>_<scene>_<view>_<date>.png`
3. Agent **must open and analyze the image** — not only record the path

**Minimum views per zone (Phase 1+):**

| View | Camera |
|------|--------|
| Establishing | Wide — silhouette read (torii, gate, hub layout) |
| Gameplay | Default follow / exploration height |
| Detail | Nearest hero prop (well, box, lantern) |

### Layer C — Vision checklist (agent procedure)

After screenshot, agent answers **in the session report** (yes/no + evidence):

| # | Question | Fail if |
|---|----------|---------|
| V1 | Any obvious grey/brown **axis-aligned boxes** visible? | Primitive placeholder |
| V2 | Palette muted coastal (fog grey, weathered wood) — not candy/sunny anime? | `ART_DIRECTION.md` §1 |
| V3 | Single toon/NPR read — not glossy PBR skin or HDRI sky? | `RENDERING_GUIDE.md` |
| V4 | Japanese coastal motifs — no European castle/medieval read? | `ART_DIRECTION.md` §9 |
| V5 | Hero silhouette readable at gameplay distance? | `CHARACTER_BIBLE.md` |
| V6 | UI: no pink font boxes, no clipped dialogue? | `UI_UX_FLOW.md` |

**If any V1–V6 fails → task is FAIL** even if Godot Output is clean. Replace assets; re-screenshot.

**On FAIL:** `python3 tools/qa_remediation_brief.py --jury <path>.jury.json --log-attempt` — see `docs/QA_REMEDIATION_LOOP.md`.

### Layer D — Palette sampling (automated)

```bash
python3 tools/check_screenshot_palette.py \
  --zone ruined_village \
  --screenshot artifacts/screenshots/phase1_ruined_village_gameplay.png
```

Samples the image grid and checks average color distance to zone anchors in `ART_DIRECTION.md` §1. Catches “everything is default grey” and “neon bright” regressions **after** screenshot exists.

### Layer E — Golden masters (L4, when available)

Store approved reference PNGs:

```
artifacts/golden/ruined_village_gameplay.png
artifacts/golden/ruined_village_establishing.png
```

Godot MCP Pro `compare_screenshots` (or perceptual diff) fails CI if drift exceeds threshold. **First** vertical slice: human + agent approve PNG → commit as golden.

### Layer F — Human L6

Subjective feel, pacing, audio, localization — `docs/PLAYTEST_SCRIPT.md`. Runs **after** L0–L5 on release candidate only.

### Layer G — Multi-LLM vision jury (recommended)

**Why:** A single model (especially the same one that placed the `BoxMesh`) can rationalize bad output. **Independent models reduce blind spots.**

**Rule:** Configure **≥2** vision APIs. **Pass only if ≥2 return `acceptance.valid_pass: true`** (all V1–V6 + confidence ≥ 0.65). See `docs/ACCEPTANCE_CRITERIA.md`.

```bash
python3 tools/review_screenshot_vision.py \
  --zone ruined_village \
  --scene ruined_village.tscn \
  --view gameplay \
  --screenshot artifacts/screenshots/phase1_ruined_village_gameplay.png \
  --min-pass 2
```

**API keys (Cursor Secrets — optional but recommended for M5):**

| Secret | Model used |
|--------|------------|
| `OPENAI_API_KEY` | GPT-4o vision |
| `ANTHROPIC_API_KEY` | Claude Sonnet vision |
| `GEMINI_API_KEY` | Gemini Flash vision |

Output: `artifacts/visual_reviews/<screenshot>.jury.json` with per-model JSON votes.

**No API keys:** script writes `*.manual.json` — paste the embedded prompt into **2+ different** Cursor models manually; same 2-of-N pass rule.

**Do not** use the same model/session that built the scene as the only judge.

---

## 2H. Tools that can judge visuals today (2026)

| Tool | What it judges | Good for | Not good for |
|------|----------------|----------|--------------|
| **Multi-LLM vision jury** (`review_screenshot_vision.py`) | Primitives, palette mood, style rules, UI glitches | Semantic “is this a grey box?” | Fun, pacing, controller feel |
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

## 4. Agent report template (paste every visual task)

```
[VISUAL QA] scene=ruined_village.tscn zone=ruined_village
  check_scene_visuals.sh: PASS
  screenshots:
    - artifacts/screenshots/phase1_ruined_village_establishing.png
    - artifacts/screenshots/phase1_ruined_village_gameplay.png
  palette_check: PASS (avg distance 0.12)
  vision_jury: PASS (2/3 models — see artifacts/visual_reviews/phase1_ruined_village_gameplay.jury.json)
  vision V1 primitives visible: NO
  vision V2 muted palette: YES
  vision V3 NPR not PBR: YES
  vision V4 Japanese coastal: YES
  vision V5 silhouette read: YES
  vision V6 UI clean: N/A (zone only)
  result: PASS
```

---

## 5. Phase gates

| Phase | Visual requirement |
|-------|-------------------|
| 1 — ruined_village | SC-02 §10 checklist + screenshots + `check_scene_visuals.sh` |
| 2–6 | Same per touched zone scene |
| 7 — M5 | Zero primitive lint failures; golden masters for all zones |
| 8 — ship | L6 human + compliance |

---

## 6. Related tools

| Tool | Role |
|------|------|
| `tools/check_scene_visuals.sh` | Static primitive / banned asset scan |
| `tools/check_screenshot_palette.py` | Post-screenshot palette distance |
| `tools/palette_remap.py` | Pre-import texture palette |
| `tools/run_visual_smoke_checks.sh` | L2 smoke: palette + jury (WARN until screenshots) |
| `tools/review_screenshot_vision.py` | Multi-LLM vision jury (2-of-N consensus) |
| `tools/check_asset_compliance.sh` | **License** only — not visual QA |

**Do not confuse** license compliance with look-and-feel approval.
