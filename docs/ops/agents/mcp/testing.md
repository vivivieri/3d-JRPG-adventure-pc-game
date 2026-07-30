---
id: testing
type: how-to
audience: [pm, builder]
status: active
authority: agents
tokens_est: 860
---
# MCP — Testing

**Hub:** [`MCP_STACK.md`](../MCP_STACK.md)

## Testing & QA workflow

See `docs/ops/qa/AI_TESTING_SPEC.md` §11 and `docs/ops/qa/ACCEPTANCE_CRITERIA.md` (measurable gates).

| Layer | Tools | MCP role |
|-------|-------|----------|
| L0–L2 | Shell scripts (no MCP) | — |
| L3 | GDAI F5 + screenshot; Godotiq `godotiq_ui_map` for menus | `godot-mcp` |
| L4 | Godot MCP Pro `run_test_scenario`; Godotiq `godotiq_verify_project_runs` | `godot-mcp-pro`, `godotiq` |
| L5 | Godot MCP Pro input replay + `assert_screen_text`; Godotiq `godotiq_trace_flow` on failure | `godot-mcp-pro`, `godotiq` |
| L6 | Human — **after** L5 | — |

### QA stack (every commit + per art/flow task)

**Catalog:** `game/data/qa/acceptance_criteria.json` · **Policy:** `docs/ops/qa/ACCEPTANCE_CRITERIA.md`

```bash
python3 tools/validate_story_data.py          # L0_story_data
python3 tools/validate_acceptance_criteria.py
bash tools/run_playtest_smoke.sh              # L2 bundle
bash tools/run_candidate_tournament.sh      # L2_candidate_select — pre-merge when policy requires
bash tools/run_model_smoke_checks.sh          # when urashima.glb exists
bash tools/run_visual_smoke_checks.sh         # when zone screenshot exists
bash tools/run_audio_smoke_checks.sh          # when bgm_village.ogg and/or P0 VO gate clip exist
bash tools/run_integration_tests.sh           # L4 / INT-*
bash tools/run_e2e_playthrough.sh             # L5 — not SKIP
```

| Domain | Doc | FAIL → |
|--------|-----|--------|
| Thresholds | `ACCEPTANCE_CRITERIA.md` | Cite gate id + measured value |
| 3D | `MODEL_QA.md` | `qa_emit_remediation.sh model-*` |
| Visual | `VISUAL_QA.md` | `qa_emit_remediation.sh visual-*` |
| Tournament | `CANDIDATE_TOURNAMENT.md` | `L2_candidate_select` comparison artifact; one winner per scope |
| Audio (BGM) | `AUDIO_QA.md` | `qa_emit_remediation.sh audio-tech\|audio-jury` |
| Audio (P0 VO) | `AUDIO_QA.md` §A4–A5 | `qa_emit_remediation.sh vo-tech\|vo-jury` |
| Flow | `FLOW_QA.md` | `qa_emit_remediation.sh flow-scenario` |
| Iteration | `QA_REMEDIATION_LOOP.md` | `qa_remediation_brief.py` |

**Rules:** WARN ≠ PASS · SKIP ≠ PASS · jury needs ≥2 models @ confidence ≥ 0.65 · vision keys in Cursor Secrets.

### Example prompts

**Zone albedo (ComfyUI/Material Maker → GDAI):**

```
Generate seamless tileable weathered wood albedo, muted #5C4A3A, Japanese coastal decay, 1024×1024
via Material Maker or ComfyUI locked workflow.
Run: python3 tools/palette_remap.py --zone ruined_village --input game/assets/textures/zones/ruined_village/wood_planks.png
Then using godot-mcp only: assign to pier meshes in ruined_village.tscn. F5 verify.
```

**UI frame (GameLab → GDAI):**

```
Using gamelab-mcp: generate ink-wash menu border, muted palette, 512×128.
palette_remap.py → game/assets/textures/ui/menu_border.png → assign in tab_menu.tscn.
```

**Combat balance (docs → code):**

```
Read docs/design/gameplay/COMBAT_SYSTEMS.md + game/data/skills.json for turn-order and damage formulas.
Update game/data/skills.json and CombatManager.gd to match.
Run bash tools/run_unit_tests.sh.
```

**Debug hung turn (Godotiq):**

```
Use godotiq_signal_map and godotiq_trace_flow on CombatManager.
Read debug console. GDAI only if a .tscn fix is needed.
```

**Automated combat menu (MCP Pro):**

```
Using godot-mcp-pro: run_test_scenario for SC-05 tutorial.
Assert battle menu text visible.
```

---

