---
id: docs-types-patterns
type: reference
phase: [1, 2, 3, 4, 5, 6]
audience: [architect, builder]
status: active
authority: engineering
tokens_est: 1059
summary: "Python Style — Docstrings, types, project patterns — Every module, public function, and public class gets a docstring."
---
# Python Style — Docstrings, types, project patterns

**Hub:** [`PYTHON_STYLE.md`](../PYTHON_STYLE.md)

## When to read

Use **Python Style — Docstrings, types, project patterns** (roles: architect, builder) when you need this reference during the current task Jump to a section below instead of reading end-to-end (9 sections).

## Jump to

- [3. Docstrings (PEP 257)](#3-docstrings-pep-257)
- [4. Type hints (PEP 484 / 585)](#4-type-hints-pep-484-585)
- [5. Project patterns (validators & libs)](#5-project-patterns-validators-libs)
- [5.1 Repo root resolution](#51-repo-root-resolution)
- [5.2 CLI entrypoint (gate scripts)](#52-cli-entrypoint-gate-scripts)
- [5.3 Reference libraries (`*_lib.py`)](#53-reference-libraries-_libpy)
- [5.4 Error collection vs fail-fast](#54-error-collection-vs-fail-fast)
- [5.5 Subprocess & paths](#55-subprocess-paths)
- [5.6 Secrets](#56-secrets)


## 3. Docstrings (PEP 257)

Every **module**, **public function**, and **public class** gets a docstring.

```python
"""Validate story-driven game data integrity.

Checks cross-references between story/scenes.json, flags.json, quests,
encounters, items, and dialogue scene IDs.

Authority: docs/engineering/technical/DATA_ARCHITECTURE.md
"""
```

| Level | Style |
|-------|-------|
| Module | One-line summary; optional paragraph + `Authority:` link |
| Function | Imperative one-liner: `"""Load catalog JSON from disk."""` |
| Class | Summary line; methods documented if non-obvious |

Do **not** duplicate type info in docstrings when type hints are present.

---


## 4. Type hints (PEP 484 / 585)

Required on **new** public functions and all reference-lib APIs.

```python
from __future__ import annotations

from pathlib import Path
from typing import Any

def load_json(path: Path) -> dict[str, Any]:
    if not path.is_file():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def main(argv: list[str] | None = None) -> int:
    ...
    return 0
```

| Use | Avoid |
|-----|-------|
| `list[str]`, `dict[str, Any]` | Bare `list`, `dict` without params (in new code) |
| `X \| None` | `Optional[X]` in new code |
| `-> int` on `main()` | Missing return type on CLI entrypoints |

---


## 5. Project patterns (validators & libs)

### 5.1 Repo root resolution

```python
ROOT = Path(__file__).resolve().parents[1]   # tools/*.py → repo root
DATA = ROOT / "game" / "data"
```

For scripts in subfolders, adjust `.parents[N]` — never hardcode `/workspace`.

### 5.2 CLI entrypoint (gate scripts)

All `validate_*.py` and `check_*.py` scripts exposed to CI:

```python
def main() -> int:
    errors: list[str] = []
    # ... collect errors ...
    if errors:
        print("VALIDATION FAILED:")
        for e in errors:
            print(f"  - {e}")
        return 1
    print("OK — summary line for humans")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

| Exit code | Meaning |
|-----------|---------|
| `0` | PASS |
| `1` | FAIL |
| `2` | SKIP (only when gate is intentionally N/A — document in script header) |

### 5.3 Reference libraries (`*_lib.py`)

- Pure functions where possible — no global mutable state
- Behavior must match `game/data/code/helpers_registry.json` contracts
- Covered by `python3 tools/test_reference_libs.py` (`L0_reference_libs`)
- GDScript ports on `game/development` must preserve semantics — see [`GDSCRIPT_REGENERATION.md`](../GDSCRIPT_REGENERATION.md)

### 5.4 Error collection vs fail-fast

| Pattern | When |
|---------|------|
| Collect `errors: list[str]`, print all, exit 1 | Validators (show full report) |
| Raise `ValueError` / `FileNotFoundError` | Library code called by tests |
| `push_error` equivalent | N/A — use `print(..., file=sys.stderr)` |

### 5.5 Subprocess & paths

```python
subprocess.run(
    ["python3", str(ROOT / "tools/validate_story_data.py")],
    check=False,
    cwd=ROOT,
    capture_output=True,
    text=True,
)
```

- Prefer `pathlib` over `os.path`
- Quote paths as `str(path)` in subprocess argv — no `shell=True` unless required

### 5.6 Secrets

- Never embed API keys, tokens, or webhook URLs in `.py`
- Read from environment / Cursor Secrets at runtime
- `bash tools/check_no_secrets.sh` (`L0_no_secrets`)

---
