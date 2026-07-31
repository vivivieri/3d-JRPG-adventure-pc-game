---
id: verify-handoff
type: how-to
audience: [architect, builder]
phase: [1]
status: active
authority: engineering
tokens_est: 394
summary: "Verify, handoff, recover, checklist"
---
# Phase 1 Visuals Regen — Verify, handoff, recover, checklist

**Hub:** [`phase1_visuals.md`](../phase1_visuals.md)

### 10.4 Verify

```bash
# On main specs (any branch)
bash tools/regenerate_phase1_visuals.sh --test

# On game/development after ports
bash tools/run_unit_tests.sh
bash tools/run_ci_checks.sh
```

**Gates:** `L1_unit_tests`, `L1_gdscript_lint`, `L0_base_class_compliance`


### 10.5 Builder handoff (P1-02)

After Architect PR merges, Builder uses GDAI MCP — **do not hand-edit `.tscn` in Cursor**:

- Node tree: P1-01 handoff in `docs/ops/sprints/phase1_sprint1/p1_01_architect_toon.md`
- Scene catalog: `scene_registry.json` → `ruined_village.required_nodes`
- Materials: assign `toon_base.gdshader` on greybox meshes
- Gates: `L3_gdai_built`, `L2_scene_primitives`


### 10.6 Recovering prior ports (diff hints)

```bash
git show 87a5ace:game/scripts/exploration/zone_visuals.gd
git show 87a5ace:game/shaders/toon_base.gdshader
git show 87a5ace:game/environments/ruined_village.tres
git show 87a5ace:game/tests/unit/test_zone_visuals.gd
```

Registry + Python reference win on conflicts.


### 10.7 One-command checklist

```bash
bash tools/regenerate_phase1_visuals.sh          # checklist + validate + reference tests
bash tools/regenerate_phase1_visuals.sh --check   # spec artifacts only
bash tools/regenerate_phase1_visuals.sh --test    # ZoneVisualsLibTests only
```
