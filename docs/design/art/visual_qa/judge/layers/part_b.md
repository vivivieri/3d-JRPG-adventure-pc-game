---
id: part-b
type: reference
phase: [1, 5]
audience: [visual, qa]
status: active
authority: art
tokens_est: 653
summary: "Visual QA — Defense Layers (B)"
---
# Visual QA — Defense Layers — Visual QA — Defense Layers (B)

**Hub:** [`defense_layers.md`](../defense_layers.md)

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

**Key-free automated path (recommended in the agent factory):** a QA agent dispatches ≥2 subagents pinned to distinct Cursor models, then `tools/ingest_agent_jury.py --domain visual` scores consensus — no provider keys. See [`AGENT_JURY.md`](../../../../../ops/qa/AGENT_JURY.md).

**Do not** use the same model/session that built the scene as the only judge.

---
