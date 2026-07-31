---
id: ci-logging
type: reference
phase: [1, 2, 3, 4, 5, 6]
audience: [architect, builder]
status: active
authority: engineering
tokens_est: 398
summary: "CI gate pattern, logging, Python invoke"
---
# Bash Style — CI gate pattern, logging, Python invoke

**Hub:** [`BASH_STYLE.md`](../BASH_STYLE.md)

## 5. CI gate pattern

Authoritative runner: `tools/run_docs_ci_checks.sh` / `tools/run_ci_checks.sh`

```bash
run_gate() {
  local gate_id="$1"
  shift
  echo ""
  echo "── ${gate_id}"
  if "$@"; then
    echo "[PASS] ${gate_id}"
    PASS=$((PASS + 1))
  else
    echo "[FAIL] ${gate_id}"
    FAIL=$((FAIL + 1))
  fi
}

run_gate "L0_story_data" python3 tools/validate_story_data.py
```

| Exit code | Meaning |
|-----------|---------|
| `0` | PASS |
| `1` | FAIL |
| `2` | SKIP (document when gate is N/A) |

Gate IDs must match `game/data/qa/acceptance_criteria.json` — enforced by `L0_doc_sync`.

---


## 6. Logging & errors

```bash
echo "==> Starting alignment audit"
echo "[FAIL] ${gate_id}"   # human-visible in CI logs
echo "[SKIP] no .gd on main"
```

- Use `echo` for CI-visible status — not silent failure
- Send recoverable hints to stderr when appropriate: `echo "..." >&2`
- Do not `exit` without a message when `set -e` triggers unexpectedly — prefer explicit `if ! cmd; then echo ...; exit 1; fi` for complex flows

---


## 7. Python invocation

```bash
python3 tools/validate_story_data.py
bash tools/run_docs_ci_checks.sh
```

- Use `python3` explicitly — not `python`
- Prefer running from `ROOT` after `cd "$ROOT"`
- Do not rely on user-site PATH in CI — `install_ci_deps.sh` documents deps

---
