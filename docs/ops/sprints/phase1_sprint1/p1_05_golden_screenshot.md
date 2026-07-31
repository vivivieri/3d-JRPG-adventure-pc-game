---
id: p1-05-golden-screenshot
type: how-to
audience: [pm, architect, builder, qa]
phase: [1]
status: active
authority: ops
tokens_est: 431
summary: "P1-05 golden screenshot"
---
# Phase1-Sprint1 — P1-05 golden screenshot

**Hub:** [`Phase1-Sprint1-issues.md`](../Phase1-Sprint1-issues.md)

## P1-05 — QA + Builder: golden screenshot + zone composition (GR-001, GR-003)

**Title:** `[DEV][P1-05] Phase 1.10–1.11 — ruined_village golden screenshot + zone composition smoke`

**Labels:** `agent/qa`, `agent/builder`, `domain/visual`, `gate/L2_zone_composition`

| Field | Value |
|-------|-------|
| Phase | 1 |
| Implementation plan | **1.10**, **1.11** |
| Generation readiness | **GR-001**, **GR-003** |
| Lead agent | **qa** (Builder captures via GDAI) |
| Depends on | P1-02 merged (P1-04 gate report recommended but not blocking) |

### Acceptance gate IDs

```
L2_visual_palette
L2_zone_composition     # warn mode — strict at M5
```

### Spec summary

1. **GDAI capture** gameplay camera screenshot at 1.6 m height, gameplay FOV, torii vista readable.
2. Save to `artifacts/screenshots/phase1_ruined_village_gameplay.png` (path from `zone_composition.json`).
3. Run zone composition smoke:

```bash
bash tools/run_zone_composition_checks.sh
# M5 strict: ZONE_COMPOSITION_STRICT=1 bash tools/run_zone_composition_checks.sh
```

4. Optional palette smoke when screenshot exists:

```bash
bash tools/run_visual_smoke_checks.sh
```

### Evidence

- `artifacts/screenshots/phase1_ruined_village_gameplay.png`
- `artifacts/visual_reviews/` if jury keys available (conditional — SKIP ≠ PASS for M5 ship)

### Design refs

- `docs/design/art/GENERATION_READINESS.md` §X-02
- `game/data/qa/generation_readiness_backlog.json` → GR-001, GR-003
- `game/data/qa/zone_composition.json` → `ruined_village`

### Definition of done

- [ ] Golden screenshot committed under `artifacts/screenshots/`
- [ ] Zone composition smoke exit 0 (warn OK for Phase 1)
- [ ] GR-001 / GR-003 status updated in backlog PR if closing items

---
