---
id: externals
type: reference
audience: [architect, builder]
status: active
authority: engineering
tokens_est: 372
summary: "Python — PEP 8 Standards — Authoritative externals — Follow these unless this doc or a project validator explicitly overrides them."
---
# Python — PEP 8 Standards — Authoritative externals

**Hub:** [`standards_pep8.md`](../standards_pep8.md)

## When to read

Use **Python — PEP 8 Standards — Authoritative externals** (roles: architect, builder) when you need this reference during the current task Jump to a section below instead of reading end-to-end (1 sections).



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
