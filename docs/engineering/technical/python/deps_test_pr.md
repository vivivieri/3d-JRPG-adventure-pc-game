---
id: deps-test-pr
type: reference
phase: [1, 2, 3, 4, 5, 6]
audience: [architect, builder]
status: active
authority: engineering
tokens_est: 721
summary: "Deps, testing, anti-patterns, PR, links"
---
# Python Style — Deps, testing, anti-patterns, PR, links

**Hub:** [`PYTHON_STYLE.md`](../PYTHON_STYLE.md)

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
| `except:` bare | Always catch specific exceptions — `L1_error_handling` (ruff `E722`) |
| `except Exception: pass` | **Forbidden** — log `WARN` to stderr or re-raise (`L1_error_handling`) |
| `return None` after failure | Log first — `print(..., file=sys.stderr)` with context |
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
- Project hub: [`CODING_STANDARDS_HUB.md`](../CODING_STANDARDS_HUB.md)
- Data JSON rules: [`JSON_DATA_STYLE.md`](../JSON_DATA_STYLE.md)
