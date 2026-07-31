---
id: prompts-pitch-qa
type: how-to
phase: [1, 6]
audience: [visual, narrative, pm]
status: active
authority: vision
tokens_est: 729
summary: "Prompts, regen, pitch deck, 3D relationship, QA"
---
# Storyboard Illustrations — Prompts, regen, pitch deck, 3D relationship, QA

**Hub:** [`STORYBOARD_ILLUSTRATIONS.md`](../STORYBOARD_ILLUSTRATIONS.md)

## 6. AI generation prompt template

```
[Subject from §5], Tides of Urashima stylized Japanese game concept art,
hand-painted illustration style, muted melancholy coastal JRPG mood,
adult proportions head-to-body 1:5, palette [hex list from zone],
high detail environment, readable silhouette, fog and decay,
no chibi, no text, no watermark, 16:9 cinematic composition
```

**Example (SC-02):**
```
Ruined Japanese fishing village overtaken by sea, rotting festival banners,
submerged wooden houses, grey fog sky #8B9AF, moss and rust accents,
lonely fisherman silhouette with red lacquer box on hip, wide establishing shot,
stylized NPR game concept art, melancholy, no people, no text
```

---


## 7. Automated regeneration brief

| Deliverable | Format | Tool |
|-------------|--------|------|
| Key scenes P0 | PNG 1920×1080 | ComfyUI / Cursor image gen |
| Full storyboard P1 | PNG 1920×1080 | ComfyUI batch |
| Character portraits | PNG 1024×1024 | ComfyUI + `palette_remap.py` |
| Contact sheet | PNG 3840×2160 | ComfyUI batch (optional) |

**Rights:** Log AI tool + prompt in `docs/design/art/LICENSES.md` + `tools/register_asset.py`.

**Pitch art:** Tool-generated illustrations are acceptable for **marketing/pitch** until 3D replaces for ship (`ASSET_COMPLIANCE.md`).

---


## 8. Pitch deck assembly

Suggested slide order for a 10-minute presentation:

1. Title — `party_lineup.png`
2. Elevator pitch (text)
3. SC-00 → SC-01 — prologue + arrival
4. SC-02 hub — exploration loop
5. SC-05 / SC-09 — combat + boss
6. SC-12 palace — Act III scale
7. SC-16 + three ending thumbs
8. Scope slide (2–3 h, 3 endings, en/ja/zh)
9. Vertical slice gate — SC-02 3D target

---


## 9. Relationship to 3D production

| Illustration | 3D target |
|--------------|-----------|
| `SC-02_ruined_village.png` | `ENVIRONMENT_KITS.md` village kit + vertical slice |
| Character portraits | `CHARACTER_BIBLE.md` portrait spec |
| `SC-09_shore_wraith.png` | `shore_wraith.glb` mesh breakdown |
| Box in all shots | `ITEMS_3D_MODEL_GUIDE.md` lacquer box |

Illustrations are **reference** for modelers — not traced 1:1 if composition differs.

---


## 10. QA checklist (pitch package)

- [x] P0 five images exist under `docs/archive/pitch/illustrations/`
- [x] P1 full scene pass (SC-00 through SC-17c)
- [x] P2 character portraits (party + 4 busts)
- [ ] Palettes match zone hex values at a glance
- [ ] No chibi / European castle motifs
- [x] SC-07 image has no dialogue text
- [x] All images logged in `LICENSES.md`
- [x] `README.md` links pitch folder for collaborators
