# Agent-driven jury (key-free vision/audio QA)

**Authority:** Alternative to the external-API vision/audio jury (`docs/art/VISUAL_QA.md`, `docs/art/MODEL_QA.md`, `docs/audio/AUDIO_QA.md`) that uses **Cursor's own LLMs via agent subagents** instead of `OPENAI_API_KEY` / `ANTHROPIC_API_KEY` / `GEMINI_API_KEY`.

**Cross-refs:** `docs/qa/ACCEPTANCE_CRITERIA.md` (consensus rules) · `tools/ingest_agent_jury.py` · `tools/qa_acceptance_lib.py`

---

## 1. Why this exists

The external-API jury (`tools/review_*_vision.py`) calls `api.openai.com` / `api.anthropic.com` / Gemini directly, which needs provider API keys. Those calls are made by a **headless Python script**, and Cursor exposes no general inference API a script can use — so the script cannot reach Cursor's subscription models.

A **Cursor agent can**, by dispatching subagents pinned to distinct models. This doc defines a jury where the review verdicts are produced by the agent's LLMs and then validated by a pure script. No provider keys required.

**Integrity is identical to the API path.** Verdicts are ingested through the same `qa_acceptance_lib` functions: `overall_pass` is recomputed from the measurable criteria (not the model's self-report), the confidence floor is enforced, and consensus still requires `jury_min_pass_models` (2) **distinct** models to pass. `WARN`/`SKIP` are still not `PASS`.

## 2. Hard limitation (read this)

This path requires a **Cursor agent runtime** (a cloud/PM-factory agent or the editor). It is **not** available in headless GitHub Actions, which has no Cursor LLM access. That is acceptable because the vision/audio jury is already **agent/editor-only** — it is explicitly listed under "Not run in CI" in `tools/run_ci_checks.sh` and is executed via `tools/run_*_smoke_checks.sh` by a QA agent, not by the game-ci workflow.

So: use provider keys if you need a fully headless (no-agent) jury; use this agent jury if the QA step always runs inside a Cursor agent (the sprint factory model).

## 3. Protocol

For each asset (screenshot / GLB turntable render / audio-spectrogram-or-clip):

1. **Confirm the asset exists** (e.g. `artifacts/screenshots/phase1_ruined_village_gameplay.png`).
2. **Dispatch >= 2 subagents pinned to DISTINCT Cursor models** (e.g. one `gpt-*`, one `claude-*`, optionally one `gemini-*`). Each subagent must:
   - open the asset with the Read tool (Read supports images),
   - apply the domain checklist for that gate (fields in §4),
   - return **only** a JSON object with every criterion field, a numeric `confidence` (0-1), `issues`, `summary`, and a `model` field naming the model used.
3. **Save each verdict** to `artifacts/<domain>_reviews/<stem>.agent/<model>.json` (one file per model).
4. **Ingest + score consensus:**

   ```bash
   python3 tools/ingest_agent_jury.py \
     --domain visual \
     --asset artifacts/screenshots/phase1_ruined_village_gameplay.png \
     --reviews-dir artifacts/visual_reviews/phase1_ruined_village_gameplay.agent
   ```

   This writes the canonical `artifacts/visual_reviews/<stem>.jury.json` (`mode: agent_jury`) and exits `0` (consensus pass), `1` (fail), or `2` (fewer than 2 distinct models — SKIP).
5. The smoke gate (`tools/run_visual_smoke_checks.sh`) picks up that `jury.json` as a real PASS/FAIL — no API keys involved.

## 4. Domain checklist fields

Each verdict JSON must include these boolean fields plus `confidence`, `issues`, `summary`, `model`:

| Domain | `--domain` | Criterion fields |
|--------|-----------|------------------|
| Screenshots | `visual` | `v1_primitives_visible` (expect false), `v2_muted_palette`, `v3_npr_not_pbr`, `v4_japanese_coastal`, `v5_silhouette_readable`, `v6_ui_clean`, `v7_emotional_mood_matches`, `v8_no_forbidden_tone` |
| 3D models | `model` | `m1_not_block_primitive`, `m2_japanese_coastal_style`, `m3_adult_not_chibi`, `m4_silhouette_readable`, `m5_sufficient_detail`, `m6_matches_brief`, `m7_emotional_mood_matches`, `m8_no_forbidden_tone` |
| Audio (BGM) | `audio` | `a1_not_cheap_procedural`, `a2_melancholy_coastal`, `a3_not_upbeat_pop`, `a4_instrumental_no_vocals`, `a5_fits_scene_mood`, `a6_emotional_mood_matches`, `a7_no_forbidden_tone` |
| VO | `vo` | `v1_not_robotic_placeholder`, `v2_script_semantics_match`, `v3_matches_direction`, `v4_not_anime_exaggeration`, `v5_fits_scene_mood`, `v6_emotional_mood_matches`, `v7_no_forbidden_tone` |

Except `v1_primitives_visible` / `m1_not_block_primitive` polarity, "good" is `true`. `confidence` must be `>= 0.65` (`jury_min_confidence`) for a verdict to count as a pass. The exact expected polarity per field lives in `game/data/qa/acceptance_criteria.json → jury.<domain>.criteria`.

## 5. Relationship to the external-API jury

Both paths converge on the same `<stem>.jury.json` and the same consensus gate ids (`L2_visual_jury`, `L2_model_jury`, `L2_audio_jury`, `L2_vo_jury`). The agent path sets `mode: agent_jury`; the API path sets per-model provider ids. You can use either — or the API path as an unattended fallback where no agent runs.
