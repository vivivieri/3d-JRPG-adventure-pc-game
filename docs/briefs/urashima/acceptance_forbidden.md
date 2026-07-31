---
id: acceptance-forbidden
type: how-to
audience: [visual, builder]
phase: [1, 5]
status: active
authority: briefs
tokens_est: 208
summary: "Acceptance + forbidden"
---
# Urashima Generation Brief — Acceptance + forbidden

**Hub:** [`urashima.md`](../urashima.md)

## Acceptance evidence

- [ ] Turntable 4-view PNG (`artifacts/models/urashima_turntable.png`)
- [ ] Gameplay-distance screenshot — Urashima on village path at 8 m
- [ ] `python3 tools/check_model_technical.py --model urashima` — PASS
- [ ] `python3 tools/check_animation_whitelist.py --phase 1 --strict` — PASS (required floor)
- [ ] `L2_model_jury` — PASS (2-of-3 when API keys set)
- [ ] `L2_visual_jury` — PASS in `ruined_village` placement
- [ ] Portrait `game/assets/ui/portraits/urashima.png` — chest up, box edge visible (512×512 min)
- [ ] Registered: `python3 tools/register_asset.py add ...` + `LICENSES.md` entry

---


## Forbidden

- `CapsuleMesh` / `BoxMesh` placeholder in ship build
- T-pose in any shipped scene
- Clip names outside `allowed_animations` in catalog
- PBR glossy skin or metallic workflow materials
