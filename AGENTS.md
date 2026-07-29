# AGENTS.md — Cloud Agent instructions

**Boot card:** [`docs/ops/BOOT.md`](docs/ops/BOOT.md) · **Router:** [`docs/INDEX.yaml`](docs/INDEX.yaml) · **Rules:** [`.cursorrules`](.cursorrules)

---

## Development environment setup (Setup Agent)

If the task is **Development environment setup**, **update dev environment**, or **snapshot rebuild** and `git branch --show-current` is `main`, you are on the **wrong branch**.

```bash
bash tools/ensure_dev_environment_branch.sh
git fetch origin game/development
git checkout game/development
bash tools/install_cloud_dev.sh
bash tools/ensure_mcp_stack.sh
bash tools/rebuild_cloud_snapshot.sh   # when rebuilding snapshot
```

Do **not** run docs-only `install_main_ci.sh` for this task. Detail: [`CLOUD_SNAPSHOT_LAUNCH.md`](docs/ops/agents/CLOUD_SNAPSHOT_LAUNCH.md).

---

## Branches

| Branch | Contents |
|--------|----------|
| `main` | docs + `game/data/` only — `bash tools/run_docs_ci_checks.sh` |
| `game/development` | full Godot + MCP — docs CI **and** `bash tools/run_ci_checks.sh` |

Docs land on **`main` first**, then sync `main` → `game/development`.
Authority: [`BRANCHING.md`](docs/ops/workflow/BRANCHING.md).

---

## Snapshot / MCP boot (`game/development`)

```bash
git fetch origin game/development
git checkout game/development
bash tools/check_snapshot_boot.sh --report
bash tools/install_cloud_dev.sh
bash tools/ensure_mcp_stack.sh
bash tools/install_extended_toolchain.sh
bash tools/check_extended_toolchain.sh
```

Required MCP: `godot-mcp`, `godotiq`, `godot-mcp-pro`, `gamelab-mcp`. Blender required for M5 turntable.
If stack fails → **STOP and notify** — do not hand-edit `.tscn`.

Editor plugins (JIT): enable GDAI + Godotiq + MCP Pro in `project.godot` `[editor_plugins]` then restart. See [`MCP_STACK.md`](docs/ops/agents/MCP_STACK.md).

---

## Sprint orchestration

| Role | First command |
|------|----------------|
| PM | `bash tools/run_pm_orchestrator.sh` |
| Worker | `bash tools/run_agent_session_gate.sh <role> <issue_id>` |

Close:

```bash
bash tools/run_post_agent_cycle.sh --issue <id> --agent <role> --commit "$(git rev-parse HEAD)"
```

Docs pack for a role: `python3 tools/resolve_docs.py <role>`.

---

## Secrets (day one)

See [`CURSOR_SECRETS_SETUP.md`](docs/ops/agents/CURSOR_SECRETS_SETUP.md) · `bash tools/check_day_one_secrets.sh`
Webhooks: `tools/curl_cursor_webhook.sh {pm|alert|worker}` — never raw-curl automation URLs.

---

## QA (every commit)

| Branch | CI |
|--------|----|
| `main` | `bash tools/run_docs_ci_checks.sh` |
| `game/development` | docs CI + `bash tools/run_ci_checks.sh` |

Acceptance: [`ACCEPTANCE_CRITERIA.md`](docs/ops/qa/ACCEPTANCE_CRITERIA.md).
Cross-cutting factory features → [`WORKFLOW_INTEGRATION.md`](docs/ops/qa/WORKFLOW_INTEGRATION.md) + registry JSON.

---

## Factory ops

| Op | Command / doc |
|----|----------------|
| Secrets | `CURSOR_API_KEY` + [`CURSOR_SECRETS_SETUP.md`](docs/ops/agents/CURSOR_SECRETS_SETUP.md) |
| Watchdog | `bash tools/run_factory_watchdog.sh` · [`FACTORY_WATCHDOG`](docs/ops/agents/FACTORY_WATCHDOG.md) |
| Factory setup | [`FACTORY_SETUP_GUIDE`](docs/ops/agents/FACTORY_SETUP_GUIDE.md) |
| Stakeholder | `bash tools/pm_emit_stakeholder_report.sh` |
| Alignment | `bash tools/run_alignment_audit.sh` · `audit_radar_spec.png` |
| Tournament | [`CANDIDATE_TOURNAMENT`](docs/ops/qa/CANDIDATE_TOURNAMENT.md) |
| Telemetry | [`AGENT_SESSION_TELEMETRY`](docs/ops/qa/AGENT_SESSION_TELEMETRY.md) |

---

## Do not ship

- `game/addons/gdai-mcp-plugin-godot/`, `godotiq/`, `godot_mcp/`
- Disable GDAI before Steam export

Deep runbooks live under `docs/ops/` and `docs/design/` — use the router, not a full-library preload.
