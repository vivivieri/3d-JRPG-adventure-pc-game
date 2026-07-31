---
id: loop-template
type: reference
phase: [1, 5]
audience: [audio, builder]
status: active
authority: audio
tokens_est: 185
summary: "Store per-track loop documentation in `docs/design/audio/audio_sheets/<track_id>.md`:"
---
# Audio Production — Combat SFX — Loop sheet template

**Hub:** [`combat_sfx.md`](../combat_sfx.md)

## When to read

Use **Audio Production — Combat SFX — Loop sheet template** (roles: audio, builder) when you need this reference during the current task Jump to a section below instead of reading end-to-end (1 sections).



## 7. Loop sheet template

Store per-track loop documentation in `docs/design/audio/audio_sheets/<track_id>.md`:

```markdown
# bgm_village — Loop sheet
- File: game/assets/audio/bgm/bgm_village.ogg
- BPM: 66 | Key: E minor | Length: 3:00
- Loop start: 0:08.000 (bar 5)
- Loop end: 2:58.500 (bar 33)
- Crossfade loop: 0.050 s (DAW export) or seamless bake
- QA: No click at loop point in Godot 10 min play
```

---
