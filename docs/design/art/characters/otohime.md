---
id: otohime
type: reference
audience: [visual, builder]
phase: [5]
status: active
authority: art
tokens_est: 509
---
# Character — Otohime

**Hub:** [`CHARACTER_BIBLE.md`](../CHARACTER_BIBLE.md)

## 5. Otohime (NPC — flashback / glimpse)

**ID:** `otohime`
**Role:** Moral mirror; not playable
**Appearances:** SC-11 (flashback), SC-17c (underwater glimpse — no dialogue)

**Cross-refs:** `docs/design/vision/NARRATIVE_WRITING_GUIDE.md` §Otohime, `docs/design/ui/CINEMATICS.md` SC-11, `docs/briefs/otohime.md`

### Design direction

- **Too perfect** — porcelain skin, no flaws, symmetrical; uncanny stillness (not fanservice)
- **Ryūgū-jō court dress** — layered kimono, coral gold trim, elongated sleeves
- Face **partially shadowed** in flashback; never full idle in field
- SC-17c: submerged silhouette only — palace tempts again; no VO

### Silhouette

- Tall, elongated sleeves; **kanzashi** ornament reads as breaking wave
- Ship mesh: **bust only** (chest-up) — sufficient for mirror chamber + flashback letterbox

| Spec | Detail |
|------|--------|
| **Height (bust)** | ~0.65 m mesh (implies ~1.75 m full figure scale) |
| **Silhouette** | Symmetrical collar; sleeves frame face; half-face in shadow |
| **Tris** | ~3k–6k (bust); no locomotion rig |
| **Mesh breakdown** | (1) Face + hair + kanzashi 1.5k; (2) Kimono collar + sleeve sculpt 1.5k–3k — folds baked, no cloth sim |
| **Palette** | Skin porcelain `#F0E8E0`; kimono coral `#C87068`; gold trim `#D4A55A`; shadow `#1A1A2A` on obscured half |
| **Materials** | Skin slightly glossy (unsettling); kimono matte NPR toon — **not** bright Ghibli |
| **VFX** | SC-11: restrained trim bloom; SC-17c: underwater caustic pass, desaturated |
| **Animations** | None required v1; optional `idle_still` 4s loop (hands folded) for flashback hold |
| **GLB** | `game/assets/models/npcs/otohime/otohime_bust.glb` |
| **Portrait** | `portraits/otohime.png` — 512×512 shadowed half-face (`portraits/otohime_ethereal` variant for SC-11 UI) |

### Voice tone (writing ref)

Seductive stillness; short lines; no villain monologue. See `VO_HIT_LIST.md` `sc11_otohime_01`.

---

