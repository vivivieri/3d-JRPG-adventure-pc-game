# Bash / Shell Style Guide — Tides of Urashima

**Version:** 1.0  
**Scope:** `tools/*.sh` — CI runners, bootstrap, QA orchestration  
**Hub:** [`CODING_STANDARDS_HUB.md`](CODING_STANDARDS_HUB.md)

---

## 1. Industry standards (authoritative externals)

| Standard | Reference | What it governs |
|----------|-----------|-----------------|
| **Shell style** | [Google Shell Style Guide](https://google.github.io/styleguide/shellguide.html) | Structure, quoting, functions |
| **POSIX** | IEEE 1003.1 | Portable builtins where possible |
| **Defensive bash** | [BashFAQ](https://mywiki.wooledge.org/BashFAQ) | Pitfalls, `set` options |

**Project shell:** `bash` 5.x (Linux CI and Cloud Agents). Scripts may use bashisms when `#!/usr/bin/env bash` is declared.

---

## 2. File template

```bash
#!/usr/bin/env bash
# One-line purpose — authority doc link if non-obvious.
# See docs/ci-cd/CI.md
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

# ... script body ...
```

| Line | Purpose |
|------|---------|
| `set -e` | Exit on first command failure |
| `set -u` | Error on unset variables |
| `set -o pipefail` | Pipeline fails if any stage fails |
| `ROOT` | Repo root — same pattern in every `tools/*.sh` |

---

## 3. Naming

| Kind | Pattern | Example |
|------|---------|---------|
| CI runner | `run_<domain>_<action>.sh` | `run_docs_ci_checks.sh` |
| Gate check | `check_<domain>.sh` | `check_no_secrets.sh` |
| Install / bootstrap | `install_<thing>.sh` | `install_cloud_dev.sh` |
| Ensure / daemon | `ensure_<thing>.sh` | `ensure_mcp_stack.sh` |
| Functions | `snake_case` | `run_gate()`, `log_info()` |
| Env vars | `UPPER_SNAKE` | `PHASE1_BOOTSTRAP_CI`, `REQUIRE_L5` |

---

## 4. Quoting & variables

```bash
# Good — always quote expansions
echo "Branch: ${BRANCH}"
python3 "${ROOT}/tools/validate_story_data.py"

# Good — arrays (rare)
files=("game/data/story/scenes.json" "game/data/story/flags.json")

# Bad
python3 $ROOT/tools/validate_story_data.py   # word-split risk
rm -rf $dir/*                                # glob / empty var risk
```

Use `[[ ]]` for bash conditionals; `$(...)` for command substitution — not backticks.

---

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

## 8. Anti-patterns

| Don't | Why |
|-------|-----|
| `set +e` without comment | Hides failures |
| Unquoted `$var` | Word splitting / glob bugs |
| `eval` on user input | Injection risk |
| Hardcoded `/workspace` only paths | Use `ROOT` |
| Duplicate gate IDs in runner | `check_doc_sync.py` fails CI |
| Long business logic in bash | Implement in `tools/*.py` |

---

## 9. PR checklist (shell)

- [ ] `#!/usr/bin/env bash` + `set -euo pipefail`
- [ ] `ROOT` resolution matches other scripts
- [ ] Quoted variable expansions
- [ ] New gate ID registered in `acceptance_criteria.json`
- [ ] `python3 tools/check_doc_sync.py` if runner changed
- [ ] `bash tools/run_docs_ci_checks.sh` green
