---
id: art-automation-pipeline
type: how-to
audience: [visual, builder]
phase: [5]
status: active
authority: art
tokens_est: 393
summary: "Tool tiers and workflows — load the asset class you are generating"
---
# Art Automation Pipeline

**Hub** — load one pack for the zone/workflow you are on.

| Pack | Topic |
|------|-------|
| [`tiers_requirements.md`](automation/tiers_requirements.md) | Tier matrix & MCP requirements |
| [`zone_textures.md`](automation/zone_textures.md) | Zone texture workflow |
| [`ui_art.md`](automation/ui_art.md) | UI art (GameLab) |
| [`characters_props.md`](automation/characters_props.md) | 3D character & prop workflow |
| [`palette_audio_gates.md`](automation/palette_audio_gates.md) | Palette remap, audio, M5 gates |
| [`pay_reject_related.md`](automation/pay_reject_related.md) | Pay vs free, rejected tools, related |
# Art Automation Pipeline — Quality-First, Zero Human Artists

**Version:** 1.1
**Applies to:** M5 art rebuild and all player-facing assets on **`game/development`** (design docs + catalogs stay on `main`)
**Authority:** When this doc conflicts with older “hand-painted / commission” language elsewhere, **this doc wins** for production tooling.

**Principle:** Ship **high-detail stylized Japanese 3D** using the **best automated tool per job**. Quality over cost — paid tools are fine when no free option matches output. **No human artists** in the art or audio production path (modeling, texturing, painting, mixing, VO performance). **Human playtest** (L6) is separate — see `docs/ops/qa/PLAYTEST_SCRIPT.md`.
