---
id: stakeholder-visuals
type: how-to
phase: [1, 6]
audience: [pm, qa]
status: active
authority: qa
tokens_est: 520
summary: "Stakeholder audit visuals: latest/ + style/ + per-run visuals/ snapshots"
---
# Alignment — Visuals / History / Integration — Stakeholder visuals

**Hub:** [`visuals_history_integration.md`](../visuals_history_integration.md)

## When to read

Use when placing or regenerating alignment audit PNGs for stakeholder updates.

## Storage layout

| Path | Role |
|------|------|
| `docs/archive/compliance/alignment_audit_visuals/latest/` | Current management set (regen target) |
| `docs/archive/compliance/alignment_audit_visuals/style/` | `tides_*` style kit + concept/roadmap packs |
| `docs/archive/compliance/alignment_audit_reports/<audit_id>/visuals/` | **Versioned** per-run snapshot (Git LFS) |

**Do not** dump versioned runs only into the shared root — that overwrites history.

## Auto-generated management set (`latest/`)

| File | Content |
|------|---------|
| `audit_exec_summary.png` | Primary illustrated exec slide |
| `audit_radar_report.png` | Spec + build two-stream |
| `audit_radar_spec.png` | Spec stream radar |
| `audit_radar_spec_breakdown.png` | Spec domain grid |
| `audit_radar_build.png` | Build radar or AWAITING TIDE |
| `audit_radar_*_<domain>.png` | Technical sub-radars (matplotlib OK if unlocked) |

Illustrated locks: `visual_policy.illustrated_locked_filenames` — preserved unless `generate_audit_radar_images.py --force`.

**Style authority:** `style/tides_audit_radar_updated.png` (navy/gold/teal ornate JRPG).

## Commands

```bash
bash tools/run_alignment_audit.sh \
  --visuals-from docs/archive/compliance/alignment_audit_visuals/latest
```

Regenerate matplotlib fallbacks into `latest/` (skips locks):

```bash
python3 tools/generate_audit_radar_images.py \
  --report artifacts/alignment_audits/latest.json \
  --output-dir docs/archive/compliance/alignment_audit_visuals/latest
```

Legacy mega dashboard / 6-axis art live under `style/` and are **not** management status.
