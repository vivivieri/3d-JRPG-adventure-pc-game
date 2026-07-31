---
id: art-direction
type: reference
audience: [visual, builder]
phase: [1, 5]
status: active
authority: art
tokens_est: 700
summary: "Palette, silhouettes, style rules — load the section for your pass"
---
# Art Direction

**Hub** — load one pack for the zone/workflow you are on.

| Pack | Topic |
|------|-------|
| [`palette.md`](direction/palette.md) | Color palette |
| [`characters_env_ui.md`](direction/characters_env_ui.md) | Silhouettes, environment, UI style |
| [`budgets_sourcing.md`](direction/budgets_sourcing.md) | Poly budgets & asset sourcing |
| [`pipeline_mood_avoid.md`](direction/pipeline_mood_avoid.md) | AI→Godot pipeline, mood, avoid list |
| [`vertical_slice_gate.md`](direction/vertical_slice_gate.md) | Vertical slice gate |
# Tides of Urashima — Art Direction Bible

**Version:** 1.1 (Pre-build pivot)
**Visual target:** **High-detail stylized Japanese 3D** — automated stylized albedo, readable silhouettes, authored environments. Not anime-realistic or photoreal PBR — closer to *Ni no Kuni* environmental richness and *Eastward* clarity with Japanese coastal motifs.

**Production policy:** Quality-first **automated** pipeline — no human artists in art/audio production. See `docs/design/art/ART_AUTOMATION_PIPELINE.md`.

**Audience note (men 20–30):** Muted palette, emotional weight, no chibi comedy. Beauty with decay.

**Related docs:** `docs/design/art/CHARACTER_BIBLE.md`, `docs/design/world/ENVIRONMENT_KITS.md`, `docs/design/ui/CINEMATICS.md`, `docs/design/art/ITEMS_3D_MODEL_GUIDE.md`, `docs/design/art/RENDERING_GUIDE.md`

### Ship rule (v1)

**No primitive placeholders** (`BoxMesh`, `CapsuleMesh`, Kenney knight, procedural spheres) in player-facing builds. Greybox may exist in editor-only layers during development.

---
