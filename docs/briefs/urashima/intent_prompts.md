---
id: intent-prompts
type: how-to
audience: [visual, builder]
phase: [1, 5]
status: active
authority: briefs
tokens_est: 711
summary: "Intent + prompts"
---
# Urashima Generation Brief — Intent + prompts

**Hub:** [`urashima.md`](../urashima.md)

## Intent (one sentence)

Weathered late-20s Japanese fisherman, adult **1:5** proportions (~1.7 m), dark indigo coat and cream tunic — **lacquer box on left hip readable at 8 m gameplay camera** in `ruined_village`.


## Emotional intent (jury + human rubric)

| Field | Value |
|-------|-------|
| Primary mood | Quiet guilt, exhaustion |
| Secondary mood | Weathered dignity — not self-pity or heroism |
| Audience read | Men 20–30 — melancholy coastal; emotional weight |
| Static read (turntable) | Slightly hunched posture; worn clothes; box visible — reads alone and tired |
| Motion feel (human L6) | Heavy tired walk; not bouncy anime gait |
| Must avoid | Chibi comedy, heroic swagger, bright hope, horror gore |
| Story anchor | SC-01 — clutching box on grey beach |

---


## Tool chain

| Step | Tool | Output |
|------|------|--------|
| 1 | **Meshy** or **Tripo** | Base mesh + albedo (stylized, not PBR glossy) |
| 2 | **Blender** | Decimate to tri budget, UV unwrap, separate lacquer box mesh, export GLB |
| 3 | **ComfyUI** or **Material Maker** | Stylized albedo touch-up / projection if needed |
| 4 | `palette_remap.py` | Zone-neutral character palette compliance |
| 5 | **Mixamo** | Humanoid rig + animation clips (rename to whitelist) |
| 6 | `install_glb_import_pipeline.sh` | NPR post-import + toon shader on import |
| 7 | **GDAI MCP** | Place in `ruined_village.tscn`, F5 verify |

**Export path:** `game/assets/models/characters/urashima/urashima.glb`

---


## Positive prompt anchors

### Style
- Stylized Japanese coastal NPR — muted, emotional weight, beauty with decay
- Reference mood: *Eastward* clarity + *Ni no Kuni* material richness — **not** bright Ghibli fantasy, not photoreal PBR, not chibi

### Silhouette (must read at distance)
- Long **dark indigo coat** (`#2A3A4A`) open at front, wind-reactive hem (2 bone chains max)
- **Cream fisherman tunic** (`#D8C8A8`) with salt stains, rolled trousers
- **Straw sandals**, rope belt / obi
- **Lacquer box** on **left hip** — separate mesh; dormant red seam glow (`#8B2A3A` at 15%)
- Hair tied back (`#1A1A1A`); weathered face; slightly hunched Act I posture

### Palette (hard hex)

| Part | Hex |
|------|-----|
| Coat | `#2A3A4A` |
| Tunic | `#D8C8A8` |
| Skin | `#C8A888` |
| Hair | `#1A1A1A` |
| Box lacquer | `#6B1A1A` |
| Box clasp | `#C8A040` |

### Proportions & scale
- Head-to-body **1:5** (adult — no oversized anime head)
- **Height:** 1.7 m in Godot (1 unit = 1 m)
- Shoulder width ~0.45 m; coat hem ~mid-calf

---


## Negative prompt (required)

```
chibi, big anime eyes, cel-shaded glossy skin, PBR metallic, European medieval,
Kenney, low-poly blockout, T-pose shipped, cape superhero, fantasy armor,
bright saturated Ghibli colors, photoreal face, beard, western cowboy,
floating accessories, symmetrical perfect clean clothes
```

---
