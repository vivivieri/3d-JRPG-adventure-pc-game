# Python 3 Style Guide — Tides of Urashima

**Version:** 1.0  
**Scope:** `tools/*.py` on `main` — validators, CI, procedural generators, reference libs  
**Hub:** [`CODING_STANDARDS_HUB.md`](CODING_STANDARDS_HUB.md)

---

## 1. Industry standards (authoritative externals)

Follow these unless this doc or a project validator explicitly overrides them.

| Standard | PEP / doc | What it governs |
|----------|-----------|-----------------|
| **Style** | [PEP 8](https://peps.python.org/pep-0008/) | Layout, naming, whitespace, imports |
| **Docstrings** | [PEP 257](https://peps.python.org/pep-0257/) | Module / class / function docstrings |
| **Type hints** | [PEP 484](https://peps.python.org/pep-0484/) · [PEP 585](https://peps.python.org/pep-0585/) | `list[str]`, `dict[str, Any]`, return types |
| **Annotations future** | [PEP 563](https://peps.python.org/pep-0563/) via `from __future__ import annotations` | Postpone evaluation — use in all new modules |
| **Zen** | [PEP 20](https://peps.python.org/pep-0020/) | Readability counts; explicit is better than implicit |
| **JSON in Python** | [PEP 8 §Programming Recommendations](https://peps.python.org/pep-0008/#programming-recommendations) | `with open(..., encoding="utf-8")` |

**Python version:** 3.10+ (stdlib features like `list[str]` without `from __future__` are OK when `annotations` import is present).

---

## 2. PEP 8 essentials (project profile)

### 2.1 Code layout

| Rule | Project default |
|------|-----------------|
| Indentation | **4 spaces** — never tabs |
| Line length | **100 characters** soft limit (PEP 8 allows 99; match surrounding file if older) |
| Blank lines | 2 between top-level defs; 1 between methods |
| Trailing whitespace | None |
| Final newline | Required on every `.py` file |

```python
# Good — vertical breathing room
def load_catalog() -> dict[str, Any]:
    return load_json(CATALOG_PATH)


def save_catalog(data: dict[str, Any]) -> None:
    save_json(CATALOG_PATH, data)
```

### 2.2 Imports (PEP 8 §Imports)

Order: **stdlib → third-party → local**. One import per line for `import x`. Group with blank lines.

```python
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from pm_orchestrator_lib import parse_issue_pack  # noqa: E402  — after sys.path tweak only
```

| Do | Don't |
|----|-------|
| `from pathlib import Path` | `from pathlib import *` |
| `import json` | `import json, sys` on one line |
| Absolute imports within `tools/` after path setup | Circular imports without lazy import |

### 2.3 Naming (PEP 8 §Naming conventions)

| Kind | Style | Example |
|------|-------|---------|
| Modules | `snake_case` | `validate_story_data.py` |
| Functions / variables | `snake_case` | `load_catalog()`, `scene_ids` |
| Constants | `UPPER_SNAKE` | `ROOT`, `REQUIRED_LOCALES` |
| Classes | `CapWords` | `class AlignmentAuditError(Exception)` |
| Private | `_leading_underscore` | `_hidden_domain_ids()` |
| “Internal use” module | `_leading_underscore` prefix (rare) | `_legacy_parser.py` |

**Avoid:** single-letter names except `i`, `j`, `k` in loops, `e` in `except`, `_` for unused.

### 2.4 Whitespace (PEP 8 §Whitespace)

```python
# Good
spam(ham[1], {eggs: 2})
x = 1
y = 2
long_variable = function(one, two, three, four)

# Bad
spam( ham[ 1 ], { eggs : 2 } )
x             = 1
y             = 2
```

- No space inside `()`, `[]`, `{}` for indexing/calls (except slicing `a[i : j]`)
- Space after `,` in argument lists
- No space before `:` in dict literals / slices

### 2.5 Strings & files

```python
# UTF-8 always for game data and docs
data = json.loads(path.read_text(encoding="utf-8"))
path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
```

- Prefer **double quotes** for docstrings and user-facing strings; single quotes OK for short internal strings — **be consistent within a file**
- Use f-strings (PEP 498) for formatting: `f"Unknown flag: {flag_id}"`

---

## 3. Docstrings (PEP 257)

Every **module**, **public function**, and **public class** gets a docstring.

```python
"""Validate story-driven game data integrity.

Checks cross-references between story/scenes.json, flags.json, quests,
encounters, items, and dialogue scene IDs.

Authority: docs/technical/DATA_ARCHITECTURE.md
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
- GDScript ports on `game/development` must preserve semantics — see [`GDSCRIPT_REGENERATION.md`](GDSCRIPT_REGENERATION.md)

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

## 6. Dependencies

Declared in `tools/requirements-ci.txt`:

```
gdtoolkit>=4.3.0
matplotlib>=3.8
```

Install: `bash tools/install_ci_deps.sh` or `pip3 install --user -r tools/requirements-ci.txt`

Pin new dependencies in `requirements-ci.txt` with a minimum version comment in the PR.

---

## 7. Testing

| Kind | Location | Command |
|------|----------|---------|
| Reference lib unit tests | `tools/test_reference_libs.py` | `python3 tools/test_reference_libs.py` |
| Validator smoke | each `validate_*.py` | `python3 tools/validate_story_data.py` |
| Full docs CI | runner | `bash tools/run_docs_ci_checks.sh` |

Use `unittest` (stdlib) — no pytest requirement on `main`.

```python
class SaveIntegrityLibTests(unittest.TestCase):
    def test_round_trip(self) -> None:
        ...
```

---

## 8. Anti-patterns (do not ship)

| Don't | Why |
|-------|-----|
| `except:` bare | Always catch specific exceptions |
| Mutable default args `def f(x=[])` | Use `None` sentinel |
| `from module import *` | Namespace pollution |
| Hardcoded absolute paths | Breaks CI and other machines |
| `print()` as only logging in long pipelines | Use structured messages; gate scripts may print summary |
| Duplicate JSON load logic | Use shared `load_json()` helper in lib modules |
| Gameplay balance in Python | Belongs in `game/data/*.json` |

---

## 9. PR checklist (Python)

- [ ] `from __future__ import annotations` on new modules
- [ ] PEP 8 naming and 4-space indent
- [ ] Module docstring with authority doc link
- [ ] Public functions typed; `main() -> int`
- [ ] UTF-8 `encoding=` on all text file I/O
- [ ] `bash tools/check_python_lint.sh` if `tools/*.py` changed
- [ ] `python3 tools/test_reference_libs.py` if `*_lib.py` changed
- [ ] Matching validator run if `game/data/` schema checked
- [ ] `bash tools/check_no_secrets.sh` if new strings added
- [ ] `bash tools/run_docs_ci_checks.sh` green

---

## 10. Quick reference links

- [PEP 8 — Style Guide](https://peps.python.org/pep-0008/)
- [PEP 257 — Docstring Conventions](https://peps.python.org/pep-0257/)
- [PEP 484 — Type Hints](https://peps.python.org/pep-0484/)
- [Real Python PEP 8 summary](https://realpython.com/python-pep8/) (tutorial)
- Project hub: [`CODING_STANDARDS_HUB.md`](CODING_STANDARDS_HUB.md)
- Data JSON rules: [`JSON_DATA_STYLE.md`](JSON_DATA_STYLE.md)
