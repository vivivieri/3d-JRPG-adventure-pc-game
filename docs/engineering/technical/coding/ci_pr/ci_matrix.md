---
id: ci-matrix
type: reference
phase: [1, 2, 3, 4, 5, 6]
audience: [architect, builder]
status: active
authority: engineering
tokens_est: 460
summary: "Coding — CI & PR — CI enforcement matrix — Policy: WARN ≠ PASS · SKIP ≠ PASS · F5 alone ≠ visual PASS."
---
# Coding — CI & PR — CI enforcement matrix

**Hub:** [`ci_pr_commands.md`](../ci_pr_commands.md)

## When to read

Use **Coding — CI & PR — CI enforcement matrix** (roles: architect, builder) when you need this reference during the current task Jump to a section below instead of reading end-to-end (1 sections).



## 9. CI enforcement matrix

| Change type | Minimum gates | Branch |
|-------------|---------------|--------|
| Story / combat JSON | `L0_story_data`, `L1_json_style` | `main` |
| Python tooling | `L1_python_lint` | both |
| Shell scripts | `L1_shellcheck` | both |
| JSON format / naming | `L1_json_style` | both |
| Documentation (`.md`) | `L1_markdown_style` | `main` |
| Shaders (`.gdshader`) | `L1_gdshader_style` | both (templates on `main`) |
| Scenes (`.tscn`) | `L1_scene_style`, `L2_scene_primitives`, `L3_gdai_built` | `game/development` |
| TypeScript (MCP Pro) | `L1_typescript_lint` | `game/development` (SKIP when vendor not installed) |
| Error / exception style | [`ERROR_HANDLING.md`](../../ERROR_HANDLING.md) | `L1_error_handling` — all languages |
| GitHub Actions YAML | `L1_workflow_yaml` | both |
| Python reference libs | `L1_mypy_libs` | both |
| New QA catalog | matching `L0_*` + `L0_doc_sync` | `main` |
| GDScript logic | `L1_unit_tests`, `L1_gdscript_lint`, `L1_gdscript_lint_all` | `game/development` |
| Base class / extends | `L0_base_class_compliance` | both |
| Scenes / materials | `L2_boot_headless`, `L3_gdai_built`, perf if applicable | `game/development` |
| Phase gate | `L4_integration` (INT-*) | `game/development` |
| Full ship path | `L5_e2e_three_endings` | `game/development` |

**Policy:** WARN ≠ PASS · SKIP ≠ PASS · F5 alone ≠ visual PASS.

```bash
# main — docs + data
bash tools/run_docs_ci_checks.sh

# game/development — full game CI
bash tools/run_ci_checks.sh
```

---
