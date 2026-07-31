---
id: pr-checklist
type: reference
phase: [1, 2, 3, 4, 5, 6]
audience: [architect, builder]
status: active
authority: engineering
tokens_est: 617
summary: "PR checklist by change type"
---
# Coding — CI & PR — PR checklist by change type

**Hub:** [`ci_pr_commands.md`](../ci_pr_commands.md)

## 10. PR checklist by change type

### Python PR (`main`)

- [ ] [PEP 8](https://peps.python.org/pep-0008/) naming, 4-space indent, quoted UTF-8 I/O
- [ ] Module docstring + `from __future__ import annotations`
- [ ] `main() -> int` with correct exit codes
- [ ] `bash tools/check_python_lint.sh`
- [ ] `bash tools/check_error_handling.sh` when error paths change
- [ ] `python3 tools/test_reference_libs.py` if `*_lib.py` changed
- [ ] `bash tools/run_docs_ci_checks.sh` green

### Documentation PR (`main`)

- [ ] [MARKDOWN_STYLE.md](../../MARKDOWN_STYLE.md) — ATX headings, no tabs in prose, trailing newline
- [ ] `python3 tools/check_markdown_style.py` (`L1_markdown_style`)
- [ ] Relative links resolve from file location
- [ ] `bash tools/run_docs_ci_checks.sh` green

### Data-only PR (`main`)

- [ ] [JSON_DATA_STYLE.md](../../JSON_DATA_STYLE.md) — 2-space indent, `snake_case`, RFC 8259 valid
- [ ] Edited upstream files before downstream references (§5.5)
- [ ] IDs are `snake_case`; scene IDs match `SC-*` pattern
- [ ] i18n objects include `en`, `ja`, `zh`, `zh-Hant` where user-facing
- [ ] `python3 tools/validate_story_data.py` (and domain validator if applicable)
- [ ] `bash tools/run_docs_ci_checks.sh` green
- [ ] Updated authority doc if schema version bumped

### GDScript PR (`game/development`)

- [ ] [GDSCRIPT_STYLE.md](../../GDSCRIPT_STYLE.md) — typed GDScript, declaration order, base classes
- [ ] No hardcoded story numbers or dialogue strings
- [ ] Typed signals; no `yield()` or string connects
- [ ] `bash tools/run_unit_tests.sh`
- [ ] `bash tools/check_gdscript_changed.sh` + `bash tools/check_gdscript_all.sh`
- [ ] Scenes built via GDAI MCP (not hand-edited `.tscn`)

### TypeScript / MCP PR (`game/development`)

- [ ] [TYPESCRIPT_STYLE.md](../../TYPESCRIPT_STYLE.md) — strict TS, `--minimal` preserved
- [ ] `npm run build` in `tools/godot-mcp-pro-server/`
- [ ] No new scene-editing MCP tools
- [ ] `bash tools/check_mcp_ready.sh` passes

### New factory / QA feature

- [ ] Entry in `game/data/qa/workflow_integration_registry.json` if cross-cutting
- [ ] Validator + CI gate wired
- [ ] [`WORKFLOW_INTEGRATION.md`](../../../../ops/qa/WORKFLOW_INTEGRATION.md) updated

---
