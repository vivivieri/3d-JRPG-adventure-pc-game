# AGENTS.md — Cloud Agent pointer

> Full boot card: [`docs/ops/BOOT.md`](docs/ops/BOOT.md) · Router: [`docs/INDEX.yaml`](docs/INDEX.yaml) · Discovery: [`docs/llms.txt`](docs/llms.txt)

**Repo:** Tides of Urashima — stylized 3D JRPG (Godot 4.7).
**Branches:** `main` = docs + design data · `game/development` = Godot implementation (`docs/ops/workflow/BRANCHING.md`).

## Setup Agent (dev environment / snapshot)

You must be on **`game/development`** (not `main`):

```bash
bash tools/ensure_dev_environment_branch.sh
git fetch origin game/development && git checkout game/development
bash tools/install_cloud_dev.sh
bash tools/ensure_mcp_stack.sh
```

## Every implementation session

```bash
bash tools/ensure_mcp_stack.sh
bash tools/check_mcp_ready.sh
bash tools/run_agent_session_gate.sh <role> <issue_id>
```

Load **only** the docs pack printed by the session gate (`tools/resolve_docs.py`). Do not preload the library.
Session gate auto-seeds `must_read` into `artifacts/docs_reads_<id>.log`; post-cycle runs `check_docs_pack_adherence.py --strict` (FAIL = missing/empty/out-of-pack).

## Sprint roles

| Role | First command |
|------|----------------|
| PM | `bash tools/run_pm_orchestrator.sh` |
| Workers | `bash tools/run_agent_session_gate.sh <role> <issue_id>` |
| End session | `bash tools/run_post_agent_cycle.sh --issue <id> --agent <role> --commit "$(git rev-parse HEAD)"` |

## Secrets / QA / factory

- Day-one secrets: `docs/ops/agents/CURSOR_SECRETS_SETUP.md` · `bash tools/check_day_one_secrets.sh`
- Docs CI (`main`): `bash tools/run_docs_ci_checks.sh`
- Game CI (`game/development`): also `bash tools/run_ci_checks.sh`
- Watchdog: `bash tools/run_factory_watchdog.sh --recover`

## Do not ship

Do not ship `game/addons/gdai-mcp-plugin-godot/`, `godotiq/`, or `godot_mcp/`. Disable GDAI before Steam export.

## Cursor Cloud specific instructions

The dev environment is **dashboard/snapshot-managed** (no repo branch picker). Pods may boot on
`main`; the startup script `tools/bootstrap_cloud_environment.sh` auto-checks out `game/development`
(where `game/project.godot` lives) before installing. The dashboard update/install runs with
`SKIP_MCP_BOOTSTRAP=1` so it only refreshes dependencies — the GDAI/MCP stack is started separately
(`bash tools/ensure_mcp_stack.sh`, per the every-session block above), never from the install script.

Verified dev inner loop (run from repo root on `game/development`, `~/.local/bin` on `PATH`):

| Step | Command |
|------|---------|
| Lint (GDScript) | `bash tools/check_gdscript_all.sh` |
| Test (unit, headless) | `bash tools/run_unit_tests.sh` |
| Build (Linux export) | `bash tools/run_linux_export_smoke.sh` |
| Run (headless boot) | `bash tools/with_ci_godot.sh godot4 --headless --rendering-driver opengl3 --path game --quit-after 120` |
| Full CI gates | `bash tools/run_ci_checks.sh` |

Non-obvious gotchas:

- Godot needs the repo-local XDG paths (`XDG_DATA_HOME/CONFIG/CACHE` under `.cache/godot-*`); the
  `run_*`/`check_*` scripts export these themselves, so prefer them over calling `godot4` directly.
- Python lint tools (`gdlint`, `ruff`, `mypy`) come from `tools/requirements-ci.txt`, **not**
  `install_cloud_dev.sh` — the update script pip-installs them so lint gates work after a snapshot rebuild.
- `bash tools/check_dev_environment.sh` reports 3 expected FAILs in cloud (GDAI plugin, Godot MCP Pro,
  GDAI HTTP bridge) because those are commercial/started-on-demand; they do not block lint/test/build/run.

## Factory hooks (registry keywords — keep on this page)

Cross-cutting ops live under `docs/ops/`. This page must keep these strings for `L0_workflow_integration`:

- Secrets / telemetry: `CURSOR_API_KEY`, `docs/ops/agents/FACTORY_SETUP_GUIDE.md`
- Stakeholder: `bash tools/pm_emit_stakeholder_report.sh`
- Alignment: `bash tools/run_alignment_audit.sh` — management visuals `audit_radar_spec.png` + `audit_radar_build.png`
- Tournament: `docs/ops/qa/CANDIDATE_TOURNAMENT.md` · gate `L2_candidate_select` · keyword `CANDIDATE_TOURNAMENT`
- Cycle close: `bash tools/run_post_agent_cycle.sh` · watchdog `bash tools/run_factory_watchdog.sh`
- Portable factory pack: `packages/game-dev-factory/` · `FACTORY_DATA_DIR` · skills `pm-session` / `worker-session` / `factory-bootstrap`

