---
id: language-exit
type: reference
phase: [1, 2, 3, 4, 5, 6]
audience: [architect, builder]
status: active
authority: engineering
tokens_est: 912
summary: "Error Handling — Language patterns + exit codes — Authority: `PYTHON_STYLE.md` §5.4"
---
# Error Handling — Language patterns + exit codes

**Hub:** [`ERROR_HANDLING.md`](../ERROR_HANDLING.md)

## When to read

Use **Error Handling — Language patterns + exit codes** (roles: architect, builder) when you need this reference during the current task Jump to a section below instead of reading end-to-end (7 sections).

## Jump to

- [3. Language-specific patterns](#3-language-specific-patterns)
- [3.1 Python (`tools/*.py`)](#31-python-toolspy)
- [3.2 Bash (`tools/*.sh`)](#32-bash-toolssh)
- [3.3 GDScript (`game/scripts/`, `game/tests/`)](#33-gdscript-gamescripts-gametests)
- [3.4 JSON validators (semantic errors)](#34-json-validators-semantic-errors)
- [3.5 TypeScript MCP tools](#35-typescript-mcp-tools)
- [4. Exit code matrix](#4-exit-code-matrix)


## 3. Language-specific patterns

### 3.1 Python (`tools/*.py`)

Authority: [`PYTHON_STYLE.md`](../PYTHON_STYLE.md) §5.4

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

Authority: [`BASH_STYLE.md`](../BASH_STYLE.md)

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

Authority: [`GDSCRIPT_STYLE.md`](../GDSCRIPT_STYLE.md) §12 · [`CODE_STYLE.md`](../CODE_STYLE.md) §9

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

Authority: [`JSON_DATA_STYLE.md`](../JSON_DATA_STYLE.md)

Format errors → `L1_json_style` (`check_json_style.py`).
Cross-ref / schema errors → matching `L0_*` validator (`validate_story_data.py`, etc.).

### 3.5 TypeScript MCP tools

Authority: [`TYPESCRIPT_STYLE.md`](../TYPESCRIPT_STYLE.md) §7

Return tool errors to the agent; log stack traces to stderr only. Never expose Godot scene paths in user-facing MCP responses without `--minimal` test context.

---


## 4. Exit code matrix

| Code | Meaning | Used by |
|------|---------|---------|
| `0` | PASS (or SKIP on `main` simple runners) | All gates |
| `1` | FAIL | All gates |
| `2` | SKIP (tri-state — game CI via `gate_lib.sh`) | `check_gdscript_all.sh`, `run_unit_tests.sh`, etc. |

---
