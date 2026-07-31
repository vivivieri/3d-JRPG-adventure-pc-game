---
id: playback-ship
type: reference
phase: [1, 6]
audience: [audio, narrative]
status: active
authority: vision
tokens_est: 289
summary: "Selective VO Hit List — Godot playback + ship checklist — VoiceLinePlayer` resolves paths; `DialogueRunner` plays VO when `voice_id` is set:"
---
# Selective VO Hit List — Godot playback + ship checklist

**Hub:** [`VO_HIT_LIST.md`](../VO_HIT_LIST.md)

## When to read

Use **Selective VO Hit List — Godot playback + ship checklist** (roles: audio, narrative) when you need this reference during the current task Jump to a section below instead of reading end-to-end (2 sections).

## Jump to

- [Godot playback (Phase 2+)](#godot-playback-phase-2)
- [Ship checklist](#ship-checklist)

## Godot playback (Phase 2+)

`VoiceLinePlayer` resolves paths; `DialogueRunner` plays VO when `voice_id` is set:

- Duck BGM per clip `duck_bgm_db` in `vo_prompts.json`
- Player can advance before VO ends (clip fades)
- Settings: Voice volume; voice language follows text locale

---


## Ship checklist

- [ ] Replace all `PLACEHOLDER_*` voice IDs
- [ ] P0 clips: `L2_vo_technical` PASS **all locales** (`en`, `ja`, `zh`, `zh-Hant` `cant` + `cmn`); `L2_vo_jury` PASS on `en` gate per clip
- [ ] Generation briefs satisfied — `docs/briefs/vo/*.md`
- [ ] No VO on tutorial / inspectable / puzzle scenes
- [ ] `python3 tools/validate_story_data.py` passes
- [ ] Log ElevenLabs license in `docs/design/art/LICENSES.md`
