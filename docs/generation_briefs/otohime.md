# Generation brief — `otohime`

**Status:** M5 cinematic NPC bust
**Authority:** `CHARACTER_BIBLE.md` §5, `docs/vision/NARRATIVE_WRITING_GUIDE.md`
**Phase:** SC-11 flashback, SC-17c underwater glimpse

## Intent

**Uncanny perfection** — ryūgū court bust, half-face shadowed; porcelain stillness; **not** fanservice or bright anime princess.

## Emotional intent (jury + human rubric)

| Field | Value |
|-------|-------|
| Primary mood | Seductive wrongness, too-perfect mercy |
| Secondary mood | Still water — beauty without warmth |
| Audience read | Men 20–30 — moral mirror, not romance bait |
| Static read (turntable) | Symmetrical collar; shadow hides half-face; kanzashi wave read |
| Motion feel (human L6) | Unnerving stillness if animated; prefer near-static flashback |
| Must avoid | Fanservice, Disney princess, villain cackle, European gown |
| Story anchor | SC-11 "Stay, Urashima…" / SC-17c submerged glimpse |

## Tool chain

Meshy (bust) → Blender (kimono folds, shadow split on face) → GLB static or optional `idle_still`.

**Export:** `game/assets/models/npcs/otohime/otohime_bust.glb`
**Portrait:** `game/assets/ui/portraits/otohime.png` (512×512 shadowed half-face)

## Positive prompts

- Ryūgū-jō court kimono — coral `#C87068`, gold trim `#D4A55A`
- Porcelain skin `#F0E8E0`; **half face in shadow** `#1A1A2A`
- Kanzashi hair ornament — breaking wave silhouette
- Stylized Japanese coastal NPR; muted palace palette

## Negative prompts

anime princess eyes, European ballgown, fanservice pose, chibi, PBR glossy skin, horror gore

## Hard metrics (from qa_catalog.json)

| Field | Value |
|-------|-------|
| Tris | 3,000 – 6,000 (bust only) |
| Textures | ≥1 |
| Rig | None required; optional `idle_still` |

## Acceptance evidence

- [ ] Bust reads uncanny in SC-11 letterbox framing
- [ ] Portrait matches bust face/hair (`portraits/otohime.png`)
- [ ] SC-17c underwater glimpse — desaturated, no dialogue UI
- [ ] Excluded from `hero_jury` — cinematic QA via screenshot + human L6
