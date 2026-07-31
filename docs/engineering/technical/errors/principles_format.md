---
id: principles-format
type: reference
phase: [1, 2, 3, 4, 5, 6]
audience: [architect, builder]
status: active
authority: engineering
tokens_est: 652
summary: "Principles + message format"
---
# Error Handling — Principles + message format

**Hub:** [`ERROR_HANDLING.md`](../ERROR_HANDLING.md)

## 1. Principles

| Principle | Detail |
|-----------|--------|
| **Fail loud in dev** | Missing boot data, broken cross-refs, and invalid saves must surface immediately — not at ship |
| **Fail quiet for players** | In-game: no stack traces, no raw file paths, no internal gate IDs |
| **No silent exceptions** | Every `except` must **log**, **raise**, **errors.append**, **return an error tuple/message**, or be an documented optional-import / parse-fallback — **never** `pass` or bare `return None` without logging |
| **Actionable text** | Every `[FAIL]` / `push_error` includes *what* broke and *how to fix* |
| **Minimal surface** | Linear single-player JRPG — not a multi-tenant service; avoid over-engineered retry frameworks |

**Policy:** WARN ≠ PASS · SKIP ≠ PASS — same tri-state rules as QA gates (`docs/ops/qa/ACCEPTANCE_CRITERIA.md`).

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
