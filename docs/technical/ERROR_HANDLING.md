# Error Handling & Messages — Tides of Urashima

**Version:** 1.1
**Scope:** All languages in the factory — Python CI, Bash gates, GDScript runtime, TypeScript MCP, JSON validators
**Hub:** [`CODING_STANDARDS_HUB.md`](CODING_STANDARDS_HUB.md)

---

## 1. Principles

| Principle | Detail |
|-----------|--------|
| **Fail loud in dev** | Missing boot data, broken cross-refs, and invalid saves must surface immediately — not at ship |
| **Fail quiet for players** | In-game: no stack traces, no raw file paths, no internal gate IDs |
| **No silent exceptions** | Every `except` must **log**, **raise**, **errors.append**, **return an error tuple/message**, or be an documented optional-import / parse-fallback — **never** `pass` or bare `return None` without logging |
| **Actionable text** | Every `[FAIL]` / `push_error` includes *what* broke and *how to fix* |
| **Minimal surface** | Linear single-player JRPG — not a multi-tenant service; avoid over-engineered retry frameworks |

**Policy:** WARN ≠ PASS · SKIP ≠ PASS — same tri-state rules as QA gates (`docs/qa/ACCEPTANCE_CRITERIA.md`).

---

## 2. Message format conventions

### 2.1 CI / tooling (Python, Bash)

| Prefix | Meaning | Exit code |
|--------|---------|-----------|
| `[PASS] <gate_id>` | Gate succeeded | `0` |
| `[FAIL] <gate_id>` | Gate failed — blocks merge | `1` |
| `[SKIP] …` | Gate not applicable | `0` on `main` runners; `2` on tri-state game CI |
| `[WARN] …` | Advisory only — **does not pass a gate** | — |
| `[OK]` / `[FAIL]` | Sub-step inside a script | — |

**Python validator errors** — include file path and field:

```text
story/scenes.json: scene SC-02-WELL references missing flag: shore_key_found
```

**Bash** — use `fail()` / `ok()` helpers; never `echo` success and failure on the same line without `if`.

### 2.2 GDScript runtime

| API | When |
|-----|------|
| `push_error("…")` | Recoverable dev error — missing JSON key, invalid scene hook |
| `push_warning("…")` | Degraded path — fallback texture, optional VO clip missing |
| `assert(condition, "…")` | Impossible state in debug; ship builds use data validators instead |
| `printerr("…")` | Rare — prefer `push_error` for editor visibility |

**Player-facing** — use i18n dialogue or UI copy from JSON; never show `res://` paths or flag IDs.

### 2.3 TypeScript (MCP Pro)

| Pattern | When |
|---------|------|
| `console.error` + structured JSON | Tool handler failure |
| `process.exit(1)` | Server boot failure only |
| Return MCP error object | Per-tool failure — do not crash the server |

---

## 3. Language-specific patterns

### 3.1 Python (`tools/*.py`)

Authority: [`PYTHON_STYLE.md`](PYTHON_STYLE.md) §5.4

| Situation | Pattern |
|-----------|---------|
| Validator | Collect `errors: list[str]`, print all, `return 1` |
| Library (`*_lib.py`) | Raise `ValueError` / `FileNotFoundError`; tests catch |
| CLI `main()` | `return 0` / `1` / `2` (SKIP documented in header) |
| Subprocess failure | Capture stdout/stderr; include command in message |

```python
errors.append(f"{rel}: unknown encounter id {enc_id!r}")
# …
if errors:
    for err in errors:
        print(err, file=sys.stderr)
    return 1
```

**Never:** bare `except:` · `except Exception: pass` · `return None` without logging · swallowing without `WARN`/`[FAIL]` to stderr.

```bash
bash tools/check_error_handling.sh   # L1_error_handling — AST scan, no silent handlers
```

### 3.2 Bash (`tools/*.sh`)

Authority: [`BASH_STYLE.md`](BASH_STYLE.md)

| Situation | Pattern |
|-----------|---------|
| Gate script | `set -euo pipefail`; `fail()` sets `FAIL=1`; exit `1` at end |
| Optional step | Explicit `if` — not `cmd && ok || fail` (SC2015) |
| Best-effort swallow | `# swallow-ok` comment when `|| true` or `2>/dev/null` is intentional |
| Missing dependency | `[FAIL] <tool> not installed — <install command>` |

```bash
fail() { echo "[FAIL] $*"; FAIL=1; }
```

### 3.3 GDScript (`game/scripts/`, `game/tests/`)

Authority: [`GDSCRIPT_STYLE.md`](GDSCRIPT_STYLE.md) §12 · [`CODE_STYLE.md`](CODE_STYLE.md) §9

| Situation | Pattern |
|-----------|---------|
| Missing JSON at boot | `push_error()` + `return` — boot must not continue with half data |
| Unknown story flag | Return default `false`; `push_warning` once in debug |
| After `await` | `if not is_instance_valid(self): return` |
| Missing ship asset | No silent fallback — `check_asset_compliance.sh` catches |
| Combat invariant break | `push_error` + end turn safely — never soft-lock |

```gdscript
var data := GameManager.load_json(path)
if data.is_empty():
    push_error("GameManager: failed to load %s" % path)
    return
```

### 3.4 JSON validators (semantic errors)

Authority: [`JSON_DATA_STYLE.md`](JSON_DATA_STYLE.md)

Format errors → `L1_json_style` (`check_json_style.py`).
Cross-ref / schema errors → matching `L0_*` validator (`validate_story_data.py`, etc.).

### 3.5 TypeScript MCP tools

Authority: [`TYPESCRIPT_STYLE.md`](TYPESCRIPT_STYLE.md) §7

Return tool errors to the agent; log stack traces to stderr only. Never expose Godot scene paths in user-facing MCP responses without `--minimal` test context.

---

## 4. Exit code matrix

| Code | Meaning | Used by |
|------|---------|---------|
| `0` | PASS (or SKIP on `main` simple runners) | All gates |
| `1` | FAIL | All gates |
| `2` | SKIP (tri-state — game CI via `gate_lib.sh`) | `check_gdscript_all.sh`, `run_unit_tests.sh`, etc. |

---

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

- [`PYTHON_STYLE.md`](PYTHON_STYLE.md) · [`BASH_STYLE.md`](BASH_STYLE.md) · [`GDSCRIPT_STYLE.md`](GDSCRIPT_STYLE.md)
- [`JSON_DATA_STYLE.md`](JSON_DATA_STYLE.md) · [`TYPESCRIPT_STYLE.md`](TYPESCRIPT_STYLE.md)
- [`SAVE_AND_FAIL_STATES.md`](SAVE_AND_FAIL_STATES.md) · [`QA_AND_BUG_PROCESS.md`](../qa/QA_AND_BUG_PROCESS.md)
