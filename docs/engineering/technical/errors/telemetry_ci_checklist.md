---
id: telemetry-ci-checklist
type: reference
phase: [1, 2, 3, 4, 5, 6]
audience: [architect, builder]
status: active
authority: engineering
tokens_est: 651
summary: "Logging, anti-patterns, CI, PR, links"
---
# Error Handling — Logging, anti-patterns, CI, PR, links

**Hub:** [`ERROR_HANDLING.md`](../ERROR_HANDLING.md)

## 5. Logging & telemetry

| Channel | Content |
|---------|---------|
| Godot Output panel | `push_error` / `push_warning` during F5 |
| CI logs | `[PASS]`/`[FAIL]` gate lines — cite gate id in PR |
| `artifacts/agent_session_telemetry/` | Agent cycle events — no player PII |
| Stakeholder Telegram | Summaries only — link to `COMPLIANCE_REPORT.md` |

Do not log: API keys, webhook URLs, save file contents.

---


## 6. Anti-patterns

| Don't | Do instead |
|-------|------------|
| Swallow errors in boot autoloads | `push_error` + early return |
| `print("error")` in validators | `print(..., file=sys.stderr)` + exit `1` |
| Player UI shows `L0_story_data` | Localized "Something went wrong" + log internally |
| Infinite retry on bad JSON | Fix data; re-run validator |
| `assert` for content bugs in ship | Data gates + `GameManager` guards |

---


## 7. CI enforcement

| Concern | Gate |
|---------|------|
| Python bare/silent except | `L1_error_handling` — ruff `E722`/`S110`/`S112` + AST (no silent handlers) |
| Bash `&& … \|\| fail` | `L1_error_handling` |
| GDScript `push_error` + boot `return` | `L1_error_handling` (when `game/scripts` exists) |
| Python style (imports, unused) | `L1_python_lint` (ruff) |
| Shell failure patterns | `L1_shellcheck` |
| JSON format | `L1_json_style` |
| Story cross-refs | `L0_story_data` |
| Runtime unhandled exceptions | L3 F5 + L4/L5 MCP scenarios (`AI_TESTING_SPEC.md` §5) |

```bash
bash tools/check_error_handling.sh   # L1_error_handling
```

---


## 8. PR checklist

- [ ] New failure paths include *what* + *fix hint*
- [ ] No secrets or absolute cloud paths in messages
- [ ] Validators collect all errors before exit
- [ ] GDScript: `push_error` on boot failures; `is_instance_valid` after `await`
- [ ] Bash: no `A && B || C` for pass/fail (use `if`/`else`)
- [ ] `bash tools/check_error_handling.sh` (`L1_error_handling`)
- [ ] Matching `L0_*` / `L1_*` gate green after change

---


## 9. Quick reference links

- [`PYTHON_STYLE.md`](../PYTHON_STYLE.md) · [`BASH_STYLE.md`](../BASH_STYLE.md) · [`GDSCRIPT_STYLE.md`](../GDSCRIPT_STYLE.md)
- [`JSON_DATA_STYLE.md`](../JSON_DATA_STYLE.md) · [`TYPESCRIPT_STYLE.md`](../TYPESCRIPT_STYLE.md)
- [`SAVE_AND_FAIL_STATES.md`](../SAVE_AND_FAIL_STATES.md) · [`QA_AND_BUG_PROCESS.md`](../../../ops/qa/QA_AND_BUG_PROCESS.md)
