---
id: judge-layers
type: how-to
audience: [visual, builder, qa]
phase: [1, 5]
status: active
authority: art
tokens_est: 1521
summary: "What AI can judge + defense layers"
---
# Visual QA — What AI can judge + defense layers

**Hub:** [`VISUAL_QA.md`](../VISUAL_QA.md)

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
L2.5 run_candidate_tournament.sh → champion/challenger (`golden_harness.json` — CANDIDATE_TOURNAMENT.md)
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

Per `docs/ops/qa/AI_TESTING_SPEC.md` §5.2 step 7:

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

**On FAIL:** `python3 tools/qa_remediation_brief.py --jury <path>.jury.json --log-attempt` — see `docs/ops/qa/QA_REMEDIATION_LOOP.md`.

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

Subjective feel, pacing, audio, localization — `docs/ops/qa/PLAYTEST_SCRIPT.md`. Runs **after** L0–L5 on release candidate only.

### Layer G — Multi-LLM vision jury (recommended)

**Why:** A single model (especially the same one that placed the `BoxMesh`) can rationalize bad output. **Independent models reduce blind spots.**

**Rule:** Configure **≥2** vision APIs. **Pass only if ≥2 return `acceptance.valid_pass: true`** (all V1–V6 + confidence ≥ 0.65). See `docs/ops/qa/ACCEPTANCE_CRITERIA.md`.

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

**Key-free automated path (recommended in the agent factory):** a QA agent dispatches ≥2 subagents pinned to distinct Cursor models, then `tools/ingest_agent_jury.py --domain visual` scores consensus — no provider keys. See [`AGENT_JURY.md`](../../../ops/qa/AGENT_JURY.md).

**Do not** use the same model/session that built the scene as the only judge.

---
