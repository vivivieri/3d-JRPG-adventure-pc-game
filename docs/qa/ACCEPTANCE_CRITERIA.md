# Acceptance Criteria — Measurable QA Pass/Fail

**Version:** 1.3
**Authority:** If a gate is not defined here with a **metric or boolean threshold**, it **cannot block ship**. Vague “looks good” is not QA.

**Machine-readable catalog:** `game/data/qa/acceptance_criteria.json`
**Cross-refs:** `docs/workflow/AI_DEV_WORKFLOW.md` §4, `docs/technical/CODE_BASE_CLASS_RULES.md`, `docs/qa/QA_REMEDIATION_LOOP.md`, `docs/qa/FLOW_QA.md`, `docs/art/MODEL_QA.md`, `docs/art/VISUAL_QA.md`, `docs/audio/AUDIO_QA.md`, `docs/qa/PERFORMANCE_BASELINE.md`

---

## 1. Why QA fails without this

| Useless QA | Valid QA |
|------------|----------|
| “F5 passed, 0 errors” for visuals | Screenshot + palette metrics + 2/3 jury with confidence ≥ 0.65 |
| Agent says “done” with no artifact | Evidence path listed in gate result |
| WARN treated as PASS for M5 | WARN = not ship-ready (`global_rules.warn_is_not_pass`) |
| Jury skipped (no API keys) = pass | SKIP = not PASS |
| Model says `overall_pass: true` alone | Tool recomputes pass from criterion booleans + confidence |
| Re-run same build hoping for different jury | Remediation brief + one lever change |

---

## 2. Global pass rules

From `acceptance_criteria.json` → `global_rules`:

| Rule | Meaning |
|------|---------|
| `warn_is_not_pass` | WARN may exit 0 in dev smoke but **not** M5 ship |
| `skip_is_not_pass` | Missing assets / no API keys = incomplete, not approved — **except** `issue_bootstrap.P1-00` deferred gates during Phase 1 bootstrap |
| `jury_min_pass_models` | **2** models must pass |
| `jury_min_confidence` | **0.65** minimum per model (enforced in `qa_acceptance_lib.py`) |
| `evidence_required_for_pass` | Agent report must cite artifact paths |
| `agent_must_cite_criterion_id` | Reports use gate ids e.g. `L2_visual_palette` |

### Invalid pass patterns (forbidden)

Listed in `acceptance_criteria.json` → `invalid_pass_patterns`. Agents must not use these.

---

## 3. Gate catalog (summary)

### L0 — Data & workflow

| Gate ID | Pass when |
|---------|-----------|
| `L0_rr_compliance` | `check_rr_compliance.sh` exit 0 — ship `.tscn` requires `.gdai_built` with `verified_f5=true`; `main_scene` must match marker |
| `L0_story_data` | `validate_story_data.py` exit 0, **0 errors** |
| `L0_no_secrets` | `check_no_secrets.sh` exit 0 — no live keys in tracked files |
| `L0_ship_build_security` | `check_ship_build_security.sh` exit 0 — dev plugin strip policy |
| `L0_zone_composition` | `validate_zone_composition.py` exit 0 — zone composition contract schema |
| `L0_qa_catalog` | `validate_qa_catalog.py` exit 0 — model catalog + `animation_timing` floor |
| `L0_audio_qa_catalog` | `validate_audio_qa_catalog.py` exit 0 — audio catalog + brief cross-refs |
| `L0_scene_audio_map` | `validate_scene_audio_map.py` exit 0 — scene/zone audio map |
| `L0_base_classes` | `validate_base_classes.py` exit 0 — `base_classes.json` schema valid |
| `L0_base_class_compliance` | `check_base_class_compliance.sh` exit 0 — no rogue native `extends` (game branch) |

### L1 — Unit tests & lint

| Gate ID | Pass when |
|---------|-----------|
| `L1_unit_tests` | All registered tests return `""` (no error string) |
| `L1_gdscript_lint` | `check_gdscript_changed.sh` exit 0 on changed `.gd` files (exit 2 SKIP when no diff — FAIL on game branch) |

### L2 — Smoke

| Gate ID | Pass when |
|---------|-----------|
| `L2_boot_headless` | Godot headless boot exit 0 |
| `L2_scene_primitives` | `check_scene_visuals.sh` exit 0, 0 banned meshes |
| `L2_animation_whitelist` | `check_animation_whitelist.py` exit 0 — required ⊆ clips ⊆ `allowed_animations` |
| `L2_zone_composition` | `run_zone_composition_checks.sh` exit 0 — warn in early phases; `ZONE_COMPOSITION_STRICT=1` at M5 ship (**GR-003**) |
| `L2_feel_smoke` | `run_feel_smoke_checks.sh` exit 0 — `feel_thresholds.json` + player constants |
| `L2_linux_export_smoke` | `run_linux_export_smoke.sh` exit 0 — Linux export + headless run |
| `L2_windows_cross_export` | `run_windows_cross_export.sh` exit 0 — Windows .exe cross-built on Linux CI |
| `L2_windows_export_run` | `run_windows_export_run.sh` exit 0 on **windows-latest** CI — native .exe run |
| `L2_glb_import` | `check_glb_import_scripts.py --strict` exit 0 — post-import toon pipeline |
| `L2_visual_palette` | `avg_anchor_dist ≤ 85`, `bright_ratio ≤ 0.35` |
| `L2_visual_jury` | ≥2 models, all V1–V8 met, confidence ≥ 0.65 |
| `L2_model_technical` | Tris in `qa_catalog.json` range, textures ≥ min, no greybox on ship |
| `L2_model_jury` | ≥2 models, M1–M8 met, confidence ≥ 0.65 |
| `L2_audio_technical` | 44.1 kHz, LUFS/peak per bus table, no procedural on ship |
| `L2_audio_jury` | ≥2 models, A1–A7 met, confidence ≥ 0.65 (hero BGM tracks) |
| `L2_vo_technical` | P0 VO duration ≤ catalog max, voice loudness, locale paths vs dialogue |
| `L2_vo_jury` | ≥2 models, V1–V7 met, confidence ≥ 0.65 (P0 clips, gate locale `en`) |

### L2.5 — Candidate tournament (pre-merge, non-ship)

| Gate ID | Pass when |
|---------|-----------|
| `L2_candidate_select` | `run_candidate_tournament.sh` verdict `promote_challenger` + `comparison_*.json` artifact — **does not block ship**; required when M5 tournament policy applies |

See `docs/qa/CANDIDATE_TOURNAMENT.md`.

### L3 — GDAI Builder handoff

| Gate ID | Pass when |
|---------|-----------|
| `L3_gdai_built` | `check_l3_gdai_built.sh` exit 0 — if ship scenes or `main_scene` changed in diff, `.gdai_built` updated with `verified_f5=true` |
| `L3_gdai_f5` | GDAI MCP F5 in editor — agent-local; not full CI |
| `L3_perf_review` | Godotiq `perf_snapshot` after F5 on **`reference_linux_cloud`** (snapshot) and/or **`reference_pc_gtx1060`** (Windows) — evidence with `baseline_id` — agent-local |

### L4 / L5 — Flow

| Gate ID | Pass when |
|---------|-----------|
| `L4_integration` | All `INT-*` scenarios pass, exit 0 |
| `L5_e2e_three_endings` | Exit 0, **not SKIP** (gate runs use `REQUIRE_L5=1 bash tools/run_e2e_playthrough.sh` — the stub then exits 1), Rewind + Anchor + Drift |

### Ship

| Gate ID | Pass when |
|---------|-----------|
| `M5_asset_compliance` | `check_asset_compliance.sh` exit 0 |
| `L6_human_playtest` | ≥80% `PLAYTEST_SCRIPT.md`, feel checklist avg ≥3.5, ≥5 testers, 0 open S0/S1 — **required ship gate**; **after L5** (Phase 8 prod CD) |

### Required toolchain (not optional)

| Requirement | Check | Notes |
|-------------|-------|-------|
| GameLab MCP | `gamelab-mcp` + `GAMELAB_API_KEY`; `check_extended_toolchain.sh` | Procedural UI fallbacks OK for **asset output** only |
| Blender | `blender` in PATH; `check_extended_toolchain.sh` | M5 turntable QA (`docs/art/MODEL_QA.md` M3) |
| `game/development` CI | `run_ci_checks.sh` exit 0 | Required merge gate; fails until `project.godot` + tests exist |
| L6 human playtest | `L6_human_playtest` gate | Phase 8 only; after L0–L5 — still **required** for ship |

Machine-readable: `acceptance_criteria.json` → `toolchain_requirements`.

Full thresholds: `game/data/qa/acceptance_criteria.json`.

---

## 4. Jury acceptance enforcement

Jury scripts (`review_*_vision.py`) **recompute** pass after each model response:

1. Every criterion boolean must match `expect` in catalog
2. `confidence ≥ 0.65`
3. On fail: `issues[]` must be non-empty
4. Consensus: ≥2 active models with `acceptance.valid_pass`

Jury JSON includes:

```json
"acceptance": {
  "gate_id": "L2_visual_jury",
  "criteria_results": { "v1_primitives_visible": true, ... },
  "confidence_ok": true,
  "valid_pass": true
}
```

**Do not** trust raw `overall_pass` from the LLM without the `acceptance` block.

---

## 5. Agent report template (required fields)

Every QA task ends with this block. **Missing fields = report invalid.**

```markdown
[QA ACCEPTANCE] task=<id> gate=<GATE_ID>
  criterion: L2_model_technical
  measured:
    tris: 14234 (expected 8000–22000)
    textures: 2 (expected >= 1)
  evidence:
    - game/assets/models/characters/urashima/urashima.glb
    - artifacts/model_reviews/urashima.model_jury.json
  jury: L2_model_jury PASS (2/3, conf>=0.65)
  invalid_pass_avoided: no WARN-as-PASS, no SKIP-as-PASS
  remediation: none | attempt N — <lever changed>
  result: VALID PASS | FAIL | WARN (dev only)
```

---

## 6. Phase gates

`acceptance_criteria.json` → `phase_gates`:

| Phase | Required gates |
|-------|----------------|
| `phase_1` | L0 (incl. narrative_density), L1, L2 boot, L2 primitives + conditional art gates when assets exist |
| `phase_6` | L0–L2 + L4 + L5 (E2E not SKIP) |
| `m5_ship` | All art/flow/compliance gates strict (`--ship` flags) |

Conditional art gates: when `urashima.glb` / screenshot / `bgm_village.ogg` **exist**, their gates must **PASS** — not SKIP.

---

## 7. Tools

| Tool | Role |
|------|------|
| `game/data/qa/acceptance_criteria.json` | Thresholds + gate ids |
| `tools/qa_acceptance_lib.py` | Enforce jury rules in Python |
| `tools/validate_acceptance_criteria.py` | Lint catalog + threshold alignment |
| `tools/qa_write_gate_result.py` | Write `artifacts/qa_reports/<gate>.json` |
| `tools/qa_remediation_brief.py` | FAIL → fix actions (links to playbook) |

```bash
python3 tools/validate_acceptance_criteria.py
python3 tools/qa_write_gate_result.py --gate L2_visual_palette --status pass \
  --metric max_avg_anchor_dist=72.4 --evidence artifacts/screenshots/phase1_ruined_village_gameplay.png
```

---

## 8. Relationship to remediation

FAIL without acceptance criteria = noise.
FAIL **with** gate id + measured values + evidence = actionable input to `QA_REMEDIATION_LOOP.md`.

Always chain: **measure → compare to catalog → brief → one lever → re-measure**.
