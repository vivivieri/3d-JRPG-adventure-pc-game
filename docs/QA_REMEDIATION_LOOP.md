# QA Remediation Loop — Industry Polish + Anti-Infinite-Retry

**Version:** 1.0  
**Problem:** QA gates catch bad assets, but agents often **re-run the same generator with the same prompt** and expect a different result. That loop never ends.

**Rule:** Every FAIL produces a **structured remediation brief** with a **changed lever** before the next build. Same pipeline + same prompt = **blocked** after 2 attempts.

**Cross-refs:** `docs/MODEL_QA.md`, `docs/VISUAL_QA.md`, `docs/AUDIO_QA.md`, `docs/FLOW_QA.md`, `docs/ACCEPTANCE_CRITERIA.md`, `docs/ART_AUTOMATION_PIPELINE.md`, `game/data/qa/remediation_playbook.json`

---

## 1. Industry standards we map to

We do not ship a AAA art/audio department. These are the **industry practices** our automated gates approximate — use them when arguing *what* to fix, not *whether* to skip QA.

### 3D models & environment art

| Industry practice | What it means | Our equivalent |
|-------------------|---------------|----------------|
| **Production phases** (blockout → greybox → beauty → polish) | Each phase has different DoD; you do not polish a blockout | `MODEL_QA.md` rejects blockouts at beauty phase; Kenney = greybox only |
| **Technical art review (TAR) gate** | Mesh budget, UVs, pivots, naming before engine import | `check_model_technical.py` + `qa_catalog.json` tri budgets |
| **Art bible / silhouette sign-off** | Readable shape at gameplay distance before texture | Turntable jury M4 + `CHARACTER_BIBLE.md` |
| **glTF 2.0 interchange** (Khronos) | Engine-neutral asset validation | GLB parse in `model_qa_lib.py` |
| **LOD authoring** (when applicable) | Distance-based mesh swap | Future; v1 uses single hero LOD per `CHARACTER_BIBLE.md` budgets |

**References:** GDC art pipeline talks (phase gating); Khronos [glTF 2.0 spec](https://registry.khronos.org/glTF/specs/2.0/glTF-2.0.html); standard game art DoD checklists (poly count, texel density, pivot at feet).

### Visual polish & look-dev

| Industry practice | What it means | Our equivalent |
|-------------------|---------------|----------------|
| **Golden master / visual regression** | Committed reference image; CI fails on drift | `compare_screenshots` + `artifacts/screenshots/*_golden.png` (`VISUAL_QA.md` §2F) |
| **Color script / palette lock** | Zone mood locked before final lighting | `ART_DIRECTION.md` §1 + `palette_remap.py` + `check_screenshot_palette.py` |
| **Art direction compliance review** | Bible checklist, not “looks fine to me” | Vision jury V1–V6 + zone rows in `ENVIRONMENT_KITS.md` |
| **Look-dev iteration** | Change **one** lighting/material variable per pass | Remediation lever `lighting` vs `albedo` vs `mesh` — never all at once |

**References:** Visual regression tools (Percy, Chromatic, Applitools — same *golden diff* pattern); film color-script workflow adapted to games.

### Audio polish & mastering

| Industry practice | What it means | Our equivalent |
|-------------------|---------------|----------------|
| **ITU-R BS.1770 / EBU R128** loudness metering | Integrated LUFS + true peak limits | `check_audio_technical.py` per-bus targets |
| **Platform loudness guidance** | Music ~−14 to −20 LUFS integrated (streaming/game) | BGM target −16 ± 4 LU (`AUDIO_QA.md`) |
| **Stem / bus mastering** | Music, SFX, VO on separate buses before final mix | `AUDIO_PRODUCTION_GUIDE.md` bus layout |
| **Loop seam QA** | 10+ min in-engine listen for clicks | Human L6; technical duration/range in A2 |
| **Reference track A/B** | Compare mood against locked brief | ACE-Step prompts in `ace_step_prompts.json` + audio jury |

**References:** [EBU R 128](https://tech.ebu.ch/loudness); ITU-R BS.1770; AES game audio loudness guidance; iZotope/FFmpeg `loudnorm` workflow.

### General QA iteration (any medium)

| Practice | Application here |
|----------|------------------|
| **PDCA / build-measure-learn** | FAIL → brief → one lever change → re-measure |
| **Root cause vs symptom** | “Too dark” may be exposure, not albedo — classify before regenerating |
| **Versioned artifacts** | `revision_log.json` per asset; never overwrite without attempt number |
| **Escalation tier** | Attempt 3+ → different tool tier or human L6, not attempt 4 of same prompt |

---

## 2. The remediation loop (required on every FAIL)

```
┌─────────┐    ┌──────────────┐    ┌─────────────────┐    ┌────────────┐
│ QA FAIL │───▶│ Brief script │───▶│ Pick ONE lever  │───▶│ Rebuild vN │
└─────────┘    │ + playbook   │    │ log revision    │    └─────┬──────┘
               └──────────────┘    └─────────────────┘          │
                                                                 ▼
                                                          ┌────────────┐
                                                          │ Re-run QA  │
                                                          └─────┬──────┘
                                                                │
                    ┌───────────────────────────────────────────┘
                    ▼
         PASS ──▶ ship asset
         FAIL ──▶ attempt < max? ──yes──▶ loop (must change different lever)
                    │
                    no ──▶ ESCALATE (tool tier ↑ or human L6)
```

### Step-by-step (agent mandatory)

1. **Capture** — jury JSON (`*.jury.json`), technical stderr, or lint output. Do not delete on FAIL.
2. **Brief** — `python3 tools/qa_remediation_brief.py --jury <path>` (or `--technical-model`, `--technical-audio`).
3. **Log** — append attempt to `artifacts/<domain>_reviews/<asset>/revision_log.json` via `--log-attempt`.
4. **Change ONE lever** from the brief (see §3). Document in commit message: `fix(urashima): attempt 2 — Tripo prompt + added coat folds (m5 fail)`.
5. **Do NOT repeat** anything listed under `do_not_repeat` in the playbook for that failure code.
6. **Re-QA** full layer (not just the step that failed — downstream may have masked issues).
7. **Escalate** after **2 failed attempts with the same lever class** (e.g. two `meshy_prompt` tweaks) → switch tool tier per `ART_AUTOMATION_PIPELINE.md` §1.

---

## 3. Lever taxonomy (change one per attempt)

| Lever class | Examples | When to use |
|-------------|----------|-------------|
| `prompt` | Meshy/Tripo/ACE-Step text, negative prompts, reference image | Style/silhouette/mood wrong; jury M2/M6 or audio A3 fail |
| `tool_tier` | Meshy → Tripo → Rodin; procedural → ACE-Step | Same prompt failed twice |
| `mesh_ops` | Blender decimate ratio, subdiv, manual edge loop | Technical tris fail; M5 detail fail |
| `texture` | ComfyUI workflow, Material Maker, `palette_remap.py` zone | Muted palette fail; untextured kit |
| `shader_scene` | Toon ramp, emission, fog, light angle | In-scene visual fail but turntable PASS |
| `placement_camera` | GDAI reposition, gameplay camera screenshot | V5 silhouette in-scene only |
| `mastering` | ffmpeg `loudnorm`, loop points, trim tail | A2 LUFS/peak fail |

**Forbidden:** “Run jury again” without rebuilding. “Tweak jury min-pass.” “Mark WARN as PASS.”

---

## 4. Commands

```bash
# After vision jury FAIL
python3 tools/qa_remediation_brief.py \
  --jury artifacts/visual_reviews/phase1_ruined_village_gameplay.jury.json \
  --log-attempt

# After model jury FAIL
python3 tools/qa_remediation_brief.py \
  --jury artifacts/model_reviews/urashima.jury.json \
  --log-attempt

# After audio jury FAIL
python3 tools/qa_remediation_brief.py \
  --jury artifacts/audio_reviews/bgm_village.jury.json \
  --log-attempt

# After technical lint FAIL (no jury yet)
python3 tools/qa_remediation_brief.py --technical-model urashima
python3 tools/qa_remediation_brief.py --technical-audio bgm_village
```

---

## 5. Agent report template (after FAIL)

```markdown
[QA REMEDIATION] asset=urashima attempt=2
  failed_criteria: m5_sufficient_detail (2/3 models)
  root_cause_class: mesh_ops + prompt
  lever_changed: tool_tier (Meshy → Tripo) + coat fold keywords in prompt
  do_not_repeat: same Meshy prompt; decimate 0.5 ratio (attempt 1)
  next_qa: check_model_technical.py → render_model_turntable.py → review_model_vision.py
  escalation_if_fail: manual Blender sculpt pass on coat; then human L6
```

---

## 6. Stop rules (prevents never-ending loops)

| Rule | Limit |
|------|-------|
| Same lever class twice | **Block** — must switch lever class or tool tier |
| Total automated attempts per asset | **3** — then escalate to human L6 or different primary tool |
| Same jury failure code 3× | **Escalate** — symptom may be wrong pipeline stage (e.g. blockout treated as beauty) |
| Re-screenshot without mesh change | **Invalid** if V1 primitives failed |

---

## 7. Medium-specific quick maps

### Model FAIL → typical fix order

1. Technical tris/textures → `mesh_ops` / `texture` (not new AI gen)
2. M1 block primitive → **regenerate** with `tool_tier` bump; do not texture a cube
3. M3 chibi → prompt proportions + negative “chibi, big head”
4. M5 low detail → lower decimate **or** higher-quality gen tier
5. Turntable PASS, in-scene FAIL → `shader_scene` + `VISUAL_QA.md` (not re-export GLB)

### Visual FAIL → typical fix order

1. V1 primitives → replace mesh (MODEL_QA path); lint before screenshot
2. V2 palette → `palette_remap.py` + zone fog/sky (`RENDERING_GUIDE.md`)
3. V3 PBR look → toon shader assignment (GDAI), not HDRI swap
4. V4 wrong culture motif → art swap per `ENVIRONMENT_KITS.md`, not lighting
5. V5 silhouette → camera distance or mesh scale, not bloom

### Audio FAIL → typical fix order

1. Placeholder source → ACE-Step (`generate_ai_bgm.sh`); never re-run procedural
2. LUFS/peak → `mastering` ffmpeg; do not re-compose
3. Wrong mood (jury) → `prompt` in `ace_step_prompts.json`; A/B one variable
4. Loop click → edit loop points (human or DAW); technical pass first

---

## 8. Tools

| Tool | Role |
|------|------|
| `game/data/qa/remediation_playbook.json` | Failure code → actions, do-not-repeat, lever class |
| `tools/qa_remediation_brief.py` | Generate brief from jury JSON or technical check |
| `artifacts/*/revision_log.json` | Per-asset attempt history (gitignored outputs; log structure committed as example) |

---

## 9. Related docs

| Doc | Role |
|-----|------|
| `docs/FLOW_QA.md` | **Game flow** — L0/L4/L5 progression + flow levers |
| `docs/QA_AND_BUG_PROCESS.md` | Gameplay bugs (S0–S3) — separate from art QA loop |
| `docs/AI_TESTING_SPEC.md` | L0–L6 test layers |
| `docs/PLAYTEST_SCRIPT.md` | Human L6 after automated pass |

---

## 10. Unified iterative improvement (all domains)

Everything in the project improves the same way:

```
BUILD → MEASURE (automated QA) → BRIEF on FAIL → change ONE lever → REBUILD
```

| Domain | Measure | Brief command |
|--------|---------|---------------|
| Story data | `validate_story_data.py` | `qa_emit_remediation.sh data-story` |
| Game flow | `run_integration_tests.sh` / E2E | `qa_emit_remediation.sh flow-scenario INT-*` |
| 3D model | model smoke / MODEL_QA | `qa_emit_remediation.sh model-tech\|model-jury` |
| Visual | visual smoke / VISUAL_QA | `qa_emit_remediation.sh visual-palette\|visual-jury` |
| Audio | audio smoke / AUDIO_QA | `qa_emit_remediation.sh audio-tech\|audio-jury` |

Smoke and integration scripts **auto-emit** briefs on FAIL via `tools/qa_emit_remediation.sh`.

**Game flow detail:** `docs/FLOW_QA.md` — critical path testing, INT-* scenarios, flow lever taxonomy (`data_fix`, `trigger_wiring`, `flag_logic`, `godotiq_trace`, …).

**Stop rules apply to all domains:** max 3 attempts per asset/scenario; same lever class twice → blocked; then escalate (tool tier ↑ or human L6).
