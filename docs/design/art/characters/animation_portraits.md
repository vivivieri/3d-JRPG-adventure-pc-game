---
id: animation-portraits
type: reference
audience: [visual, builder]
phase: [5]
status: active
authority: art
tokens_est: 406
summary: "[`CHARACTER_BIBLE.md`](../CHARACTER_BIBLE.md)"
---
# Characters — Animation & portraits

**Hub:** [`CHARACTER_BIBLE.md`](../CHARACTER_BIBLE.md)

## 8. Master animation list

**CI whitelist:** Rigged GLB clips must satisfy `required_animations` ⊆ found ⊆ `allowed_animations` in `game/data/models/qa_catalog.json`. Enforced by `L2_animation_whitelist` (`check_animation_whitelist.py --phase m5 --strict`). Update the catalog when adding Mixamo clips.

### Urashima

| Anim | Loop | Priority |
|------|------|----------|
| `idle` | Yes | P0 |
| `walk` | Yes | P0 |
| `run` | Yes | P1 |
| `interact` | No | P0 |
| `attack_light` | No | P0 |
| `attack_heavy` | No | P0 |
| `skill_cast` | No | P0 |
| `hit` | No | P0 |
| `defeat` | No | P1 |
| `ending_dissolve` | No | P1 |
| `ending_stand` | Yes | P1 |
| `ending_row` | Yes | P1 |

### Yuzu

`idle`, `walk` (float), `heal_cast`, `purify_cast`, `hit`, `materialize` (SC-10)

### Roku

`idle`, `walk`, `taunt`, `guard`, `harpoon_strike`, `hit`

### Enemies

Per `game/data/enemies/enemies.json` attack skills — minimum: `idle`, `attack`, `hit`, `death`; bosses add `phase_transition`, `special`

---

## 9. Portrait spec (UI)

| Character | File | Framing |
|-----------|------|---------|
| Urashima | `portraits/urashima.png` | Chest up; box edge visible |
| Yuzu | `portraits/yuzu.png` | Chest up; bell visible |
| Roku | `portraits/roku.png` | Chest up; harpoon strap |
| Otohime | `portraits/otohime.png` | Shadowed half-face |
| Enemies | `portraits/<enemy_id>.png` | Silhouette or bust per boss importance |

Resolution: **512×512** (enemies), **768×768** (party). Ink-wash border per `ART_DIRECTION.md` §4.

---

