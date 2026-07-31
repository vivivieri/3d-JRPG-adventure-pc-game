# Schema notes (MVP)

Templates under `../templates/` are the practical schema. Validators in a host
repo should require at least:

## sprint_board.json
- `version`, `active_sprint`, `orchestration`, `issues[]`
- Issue fields: `id`, `title`, `sequence`, `phase`, `agent_owner`,
  `acceptance_gate_ids`, `status`, `depends_on`

## sprint_phases.json
- `active_phase`, `phases[]` with `phase` + `name` (+ optional `exit_gates`)

## pm_orchestrator_steps.json
- `session_steps[]` with `step`, `id`, `command`, `block_on_fail`
- `post_agent_cycle.command` pointing at enforced close script

## workflow_integration_registry.json
- `features[]` with `script_hooks` and `required_doc_refs`

Path resolution is **not** part of JSON schema — use `FACTORY_DATA_DIR`.
