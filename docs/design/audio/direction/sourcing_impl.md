---
id: sourcing-impl
type: reference
phase: [1, 5]
audience: [audio, builder]
status: active
authority: audio
tokens_est: 257
summary: "Sourcing, implementation, production order"
---
# Audio Direction — Sourcing, implementation, production order

**Hub:** [`AUDIO_DIRECTION.md`](../AUDIO_DIRECTION.md)

## 6. Sourcing

| Type | Source options |
|------|----------------|
| Music | ACE-Step 1.5 curated prompts, OpenGameArt (CC-BY log), Freesound CC0 layers |
| SFX | Freesound CC0, Sonniss GDC packs (check license) |
| **Rule** | Log in `docs/design/art/LICENSES.md`; register with `tools/register_asset.py`; verify with `tools/check_asset_compliance.sh` |

---


## 7. Implementation

- `AudioManager` crossfade 1.5s between zone BGM
- Boss music overrides field; restore on exit
- `user://settings.json`: `music_volume`, `sfx_volume` (0–1)

---


## 8. Production order

1. Village + beach ambient (vertical slice)
2. Combat + boss stems
3. Palace + caves
4. Ending tracks (3)
5. Full SFX pass per `ENCOUNTER_TABLE` fights
