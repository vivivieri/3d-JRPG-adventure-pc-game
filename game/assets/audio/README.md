# Audio assets

Original procedural BGM and SFX for Tides of Urashima — Japanese coastal JRPG mood (pentatonic melodies, ocean ambience, taiko combat, temple bells). MIT license (this repo).

Regenerate all audio:

```bash
./tools/generate_assets.sh
# or
python3 tools/generate_game_audio.py
```

## Tracks

| File | Mood |
|------|------|
| `bgm/menu.ogg` | Foggy coast, shakuhachi-like lead |
| `bgm/village.ogg` | Ruined village, waves + koto phrases |
| `bgm/caves.ogg` | Deep teal caves, biolume tension |
| `bgm/palace.ogg` | Ethereal palace bells |
| `bgm/combat.ogg` | Taiko rhythm + tension pads |
| `bgm/boss.ogg` | Heavier drums, darker scale |

## SFX

`ui_confirm`, `ui_cancel`, `interact`, `hit`, `heal`, `victory`, `defeat`, `footstep`, `item`, `equip`
