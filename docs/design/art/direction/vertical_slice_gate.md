---
id: vertical-slice-gate
type: reference
audience: [visual, builder]
phase: [1]
status: active
authority: art
tokens_est: 326
summary: "is gated twice — greybox first, final art later:"
---
# Art Direction — Vertical slice gate

**Hub:** [`ART_DIRECTION.md`](../ART_DIRECTION.md)

## When to read

Use **Art Direction — Vertical slice gate** (roles: visual, builder) when you need this reference during the current task Jump to a section below instead of reading end-to-end (3 sections).

## Jump to

- [10. Vertical slice gate](#10-vertical-slice-gate)
- [Phase 1 gate (greybox slice — rendering foundation)](#phase-1-gate-greybox-slice-rendering-foundation)
- [M5 / Phase 7 gate (final art — before ship)](#m5-phase-7-gate-final-art-before-ship)

## 10. Vertical slice gate

**SC-02 Ruined Village** is gated twice — greybox first, final art later:

### Phase 1 gate (greybox slice — rendering foundation)

- [ ] Palette matches §1 hex values at gameplay camera distance (lights, fog, sky)
- [ ] Filmic/ACES tonemap + zone fog per `RENDERING_GUIDE.md` (no default grey)
- [ ] Toon ramp shader on ground/blockout meshes
- [ ] 60 FPS @ 1080p on target hardware
- Greybox/primitive meshes **allowed** at this gate (dev only — `LEVEL_DESIGN.md` §1)

### M5 / Phase 7 gate (final art — before ship)

- [ ] Urashima authored model + walk/idle
- [ ] Hero torii + shack + well (no primitives)
- [ ] Zero primitive/greybox meshes in player-facing scenes
- [ ] 60 FPS @ 1080p maintained after art pass
