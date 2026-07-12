# Generation brief — `palace_gate_main`

**Status:** M5 hero set-piece (hero jury)  
**Authority:** `ENVIRONMENT_KITS.md` §6, `qa_catalog.json`  
**Phase:** SC-12 vertigo shot

## Intent

Impossible floating ryūgū gate **~12–15 m** tall — coral gold trim, void sky `#1A1A3A` behind; gold emission **capped** to avoid bloom clip; pearl socket for `wraith_pearl`.

## Tool chain

Meshy/Blender hero sculpt → ComfyUI gold trim albedo → `palette_remap.py --zone dragon_palace_gate` → GLB.

**Export:** `game/assets/models/environment/dragon_palace_gate/palace_gate_main.glb`

## Positive prompts

- Karahafu-inspired curves; crimson lacquer `#8B2A3A`; coral gold `#D4A55A` trim
- Floats over void — no ground contact
- Scale: party reads small at gate base (vertigo)
- Pearl socket at center — 6 cm diameter recess

## Negative prompts

European castle gate, Roman arch, medieval portcullis, stars in void sky, neon gold

## Hard metrics

| Field | Value |
|-------|-------|
| Tris | 8,000 – 30,000 |
| Height | 12–15 m arch |

## Lighting pairing

- Directional gold `#FFD890` from above
- Void sky `#1A1A3A` — **no stars**
- Emissive trim: intensity ≤0.4 per `RENDERING_GUIDE.md`

## Acceptance

- [ ] SC-12 vertigo establishing screenshot
- [ ] `wraith_pearl` fits socket without Z-fight
- [ ] `L2_model_jury` PASS
- [ ] Party scale reference: 3 characters at base for scale shot
