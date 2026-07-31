---
id: project-profile
type: reference
audience: [architect, builder]
status: active
authority: engineering
tokens_est: 860
summary: "Python — PEP 8 Standards — Project PEP 8 profile — def load_catalog() -> dict[str, Any]:"
---
# Python — PEP 8 Standards — Project PEP 8 profile

**Hub:** [`standards_pep8.md`](../standards_pep8.md)

## When to read

Use **Python — PEP 8 Standards — Project PEP 8 profile** (roles: architect, builder) when you need this reference during the current task Jump to a section below instead of reading end-to-end (6 sections).

## Jump to

- [2. PEP 8 essentials (project profile)](#2-pep-8-essentials-project-profile)
- [2.1 Code layout](#21-code-layout)
- [2.2 Imports (PEP 8 §Imports)](#22-imports-pep-8-imports)
- [2.3 Naming (PEP 8 §Naming conventions)](#23-naming-pep-8-naming-conventions)
- [2.4 Whitespace (PEP 8 §Whitespace)](#24-whitespace-pep-8-whitespace)
- [2.5 Strings & files](#25-strings-files)


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
