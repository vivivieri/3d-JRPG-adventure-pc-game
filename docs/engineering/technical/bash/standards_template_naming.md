---
id: standards-template-naming
type: reference
phase: [1, 2, 3, 4, 5, 6]
audience: [architect, builder]
status: active
authority: engineering
tokens_est: 573
summary: "Standards, template, naming, quoting"
---
# Bash Style — Standards, template, naming, quoting

**Hub:** [`BASH_STYLE.md`](../BASH_STYLE.md)

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
# See docs/ops/ci-cd/CI.md
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
