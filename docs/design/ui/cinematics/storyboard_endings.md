---
id: storyboard-endings
type: reference
audience: [builder, visual, narrative]
phase: [5, 6]
status: active
authority: ui
tokens_est: 1062
summary: "Storyboard specs + endings"
---
# Cinematics — Storyboard specs + endings

**Hub:** [`CINEMATICS.md`](../CINEMATICS.md)

## 7. Storyboard scene specs

### SC-00 — Prologue

| Time | Shot |
|------|------|
| 0–2s | Black + surf |
| 2–20s | Spirit-turtle rescue montage |
| 20–40s | Palace silhouette; Otohime; box |
| 40–45s | Fade to SC-01 shore |

See `docs/design/gameplay/TUTORIAL_DESIGN.md` §2.

### SC-01 — Arrival

| Beat | Camera |
|------|--------|
| Open | Wide establishing: shore, grey sky, 3s hold |
| Wake | Cut to Urashima on sand; clutching box |
| Tutorial | Hand off to follow cam |

### SC-11 — Palace flashback

| Beat | Camera |
|------|--------|
| Overlay | Cave wall dissolves to gold palace |
| Dream dolly | Slow push on Otohime silhouette |
| Letterbox | 2.39:1 bars |
| End | Rip back to cave; 0.5s disorienting snap |

**Skippable:** Yes after 3s

### SC-08 — Deep pool vignette (not a full movie)

**Type:** In-scene vignette — **5–8s**; do **not** expand to 15s (horror beat; SC-09 boss intro carries spectacle).

| Time | Shot |
|------|------|
| 0–2s | Close on `cave_deep_pool` surface; drip ambient |
| 2–6s | `cave_face_decal_set` (4 faces) fade in under water; slow push-in |
| 6–8s | Cut to dialogue UI → 2× Tide Wraith encounter |

**Audio:** `sfx_story_whisper_bed` + BGM duck 40% (`AUDIO_PRODUCTION_GUIDE.md` SC-08 row)
**Letterbox:** No
**Skippable:** After 3s
**Assets:** `cave_deep_pool` (2k), face decals — see `ENVIRONMENT_KITS.md` §5
**Flag:** `deep_pool_vignette_seen` (set by `sc08_deep_pool_vignette` hook; encounter win sets separate `deep_pool_seen`)

### SC-12 — Palace gate reveal (mid-game hero cinematic)

**Type:** Optional **12–15s** reveal — the **one** mid-game “movie” worth full camera authorship. Rides on `palace_gate_main` (18k), which the M5 art rebuild must build for the zone anyway.

| Time | Shot |
|------|------|
| 0–3s | Wide from cave exit; party small in frame; void sky `#1A1A3A` |
| 3–10s | Vertigo tilt up `palace_gate_main` above `palace_void_sea` |
| 10–13s | Hold on gate; gold trim catches directional `#FFD890` |
| 13–15s | Ease to gameplay follow cam; `sfx_story_pearl_insert` chime |

**Dialogue:** Roku line *after* cinematic handoff — not inside the 15s block
**Audio:** `bgm_palace` fade in at 3s; `amb_palace_hum` bed
**Letterbox:** No (reserve 2.39:1 for SC-11 + SC-17)
**Skippable:** After 3s on replay; first play — full shot
**Out of scope v1:** FMV, Roku walk-in animation inside shot, reverse-gravity rooms

**Camera markers (author in `dragon_palace_gate.tscn`):**

| Marker | Use |
|--------|-----|
| `CameraMarker_sc12_wide` | Party at cave exit |
| `CameraMarker_sc12_tilt_mid` | Mid vertigo on gate |
| `CameraMarker_sc12_gate_hero` | Hero hold on `palace_gate_main` |

**Director sequence id:** `sc12_gate_reveal` on `CinematicDirector`

### SC-13 — Mirror chamber

| Beat | Camera |
|------|--------|
| Approach | Mirror center frame |
| Reveal | Reflection shows young + old Urashima simultaneously |
| Lighting | Split rim: warm left (young), cool right (old) |

---


## 8. Ending cinematics

### SC-17a — Rewind

| Beat | Camera | Duration |
|------|--------|----------|
| Box opens | Close on box light bloom | 2s |
| Village restore | Time-lapse dissolve: ruin → festival | 4s |
| Crane up | Rising shot over crowd | 6s |
| Urashima fade | Figure dissolves at crowd edge | 3s |
| Credits | Fade to black | — |

**Assets:** `village_restored_kit`, crowd silhouettes

### SC-17b — Anchor

| Beat | Camera | Duration |
|------|--------|----------|
| Box shatters | Medium shot; spirit light scatters | 2s |
| Dawn wide | Shore rebuild; small figures | 5s |
| Sapling | Roku plants tree; hold | 3s |
| Urashima | Older but present; watching | 2s |
| Credits | — | — |

### SC-17c — Drift

| Beat | Camera | Duration |
|------|--------|----------|
| Boat push | Urashima rows away from shore | 3s |
| Pull back | Endless sea; boat shrinks | 8s |
| Underwater glimpse | Camera dips; palace glimmers below | 3s |
| Credits | — | — |

**Assets:** `boat_urashima`, underwater palace silhouette

---
