---
id: combat-endings
type: reference
audience: [audio, builder]
status: active
authority: audio
tokens_est: 625
summary: "BGM — Per-track Specs — Combat + boss + endings — See `AUDIO_DIRECTION.md` §2 for instrument notes. Each ending track must not loop; tail fade ≥ 4 s."
---
# BGM — Per-track Specs — Combat + boss + endings

**Hub:** [`per_track_specs.md`](../per_track_specs.md)

## When to read

Use **BGM — Per-track Specs — Combat + boss + endings** (roles: audio, builder) when you need this reference during the current task Jump to a section below instead of reading end-to-end (5 sections).

## Jump to

- [`bgm_combat`](#bgm_combat)
- [`bgm_boss`](#bgm_boss)
- [`bgm_boss_tide_keeper_p2`](#bgm_boss_tide_keeper_p2)
- [`bgm_boss_tide_keeper_p3`](#bgm_boss_tide_keeper_p3)
- [`bgm_ending_rewind` / `bgm_ending_anchor` / `bgm_ending_drift`](#bgm_ending_rewind-bgm_ending_anchor-bgm_ending_drift)


## `bgm_combat`

| Field | Value |
|-------|-------|
| **BPM** | 108 |
| **Key** | C minor |
| **Mood** | Tension, mid tempo |
| **Instruments** | Light taiko, staccato strings, no choir |
| **Loop point** | Bar 17 |
| **Enter** | `sting_combat_start` (0.8 s) then crossfade 0.5 s |
| **Exit** | Crossfade 1.5 s back to zone BGM on victory |


## `bgm_boss`

| Field | Value |
|-------|-------|
| **BPM** | 120 |
| **Key** | D minor |
| **Mood** | Escalation |
| **Instruments** | Full taiko, low brass, choir hits on bar 1 of each 8-bar phrase |
| **Loop point** | Bar 33 |
| **Enter** | `sting_boss_intro` (1.2 s) after cinematic skip window |
| **Bosses** | `shore_wraith` (SC-09), `palace_sentinel` (SC-14), Tide Keeper **phase 1** (SC-15) |


## `bgm_boss_tide_keeper_p2`

| Field | Value |
|-------|-------|
| **BPM** | 132 |
| **Key** | D minor → modal lift on relative F |
| **Mood** | Surge, cosmic |
| **Trigger** | Tide Keeper HP ≤ 66%; banner "Then let the sea decide!" |
| **Crossfade** | 2.0 s from `bgm_boss` |
| **Sync** | Camera orbit phase 2 (`CINEMATICS.md`) |


## `bgm_boss_tide_keeper_p3`

| Field | Value |
|-------|-------|
| **BPM** | 72 |
| **Key** | A minor |
| **Mood** | Ebb, tragic stillness |
| **Trigger** | Tide Keeper HP ≤ 25%; banner "Even mercy... tires." |
| **Crossfade** | 3.0 s |
| **Choice gate** | At 10% HP → `sting_choice_silence` ducks music to -24 dBFS; hold until choice confirmed |


## `bgm_ending_rewind` / `bgm_ending_anchor` / `bgm_ending_drift`

| Track | BPM | Key | Length | Loop |
|-------|-----|-----|--------|------|
| `bgm_ending_rewind` | 96 | G major | 1:45 | No — credits roll |
| `bgm_ending_anchor` | 80 | C major | 1:30 | No |
| `bgm_ending_drift` | 54 | E minor | 2:00 | No — fade to surf only |

See `AUDIO_DIRECTION.md` §2 for instrument notes. Each ending track **must not** loop; tail fade ≥ 4 s.

---
