---
id: dragon-palace
type: reference
audience: [builder, builder_zone, architect]
phase: [5, 6]
status: active
authority: world
tokens_est: 691
summary: "`res://scenes/world/dragon_palace_gate.tscn`"
---
# Level Design — Palace + endings

**Hub:** [`LEVEL_DESIGN.md`](../LEVEL_DESIGN.md)

## 5. Zone: `dragon_palace_gate` (SC-12–16)

**Scene:** `res://scenes/world/dragon_palace_gate.tscn`
**Act:** II–III · **BGM:** `bgm_palace` · **Sky:** void `#1A1A3A`

### Blockout

| Metric | Target |
|--------|--------|
| Hero mesh | `palace_gate_main` ~18k tris (M5) |
| Interior | Mirror hall → sentinel arena → throne |
| SC-12 cinematic | 12–15s gate reveal (`CINEMATICS.md`) |

### Layout

```
[Exterior gate SC-12] — SavePoint_gate
      ↓ (wraith_pearl insert)
[Mirror chamber SC-13]
      ↓
[Sentinel hall SC-14]
      ↓
[Throne arena SC-15 → SC-16 choice]
```

### Interactables & triggers

| Node | Scene ID / hook | Sets flag | Requirement |
|------|-----------------|-----------|-------------|
| `CinematicTrigger_sc12_gate_reveal` | hook `sc12_gate_reveal` | `sc12_gate_reveal_seen` | First visit; markers `CameraMarker_sc12_*` |
| `SavePoint_gate` | — | — | Manual save |
| `EncounterTrigger_enc_sc12_palace_wraiths` | SC-12 | `roku_combat_active` | Gate approach |
| `Interactable_SC-13` | SC-13 | `knows_box_truth` | Mirror |
| `CinematicTrigger_sc14_sentinel_breather` | hook `sc14_sentinel_breather` | `sc14_breather_seen` | Requires `knows_box_truth`; breather before sentinel boss |
| `EncounterTrigger_enc_sc14_sentinel` | SC-14 | `sentinel_defeated` | Boss |
| `EncounterTrigger_enc_sc15_tide_keeper` | SC-15 | — | Requires `sentinel_defeated`; sets `tide_keeper_defeated` via `sc16_last_mercy_resolution` after SC-16 |
| `Interactable_SC-16` | SC-16 | `ending_chosen` | Three-way choice UI |
| `CinematicTrigger_sc16_last_mercy` | hook `sc16_last_mercy_resolution` | `sc16_last_mercy_seen`, `tide_keeper_defeated` | After ending choice; `load_ending` per `ending_chosen` |

### Camera markers (SC-12)

| Marker | Beat |
|--------|------|
| `CameraMarker_sc12_wide` | Party at cave exit 0–3s |
| `CameraMarker_sc12_tilt_mid` | Mid vertigo 3–10s |
| `CameraMarker_sc12_gate_hero` | Hero hold 10–15s |

---


## 6. Ending zones (SC-17a/b/c)

| Zone ID | Scene | Ending | BGM |
|---------|-------|--------|-----|
| `ending_rewind` | SC-17a | Rewind | `bgm_ending_rewind` + `cine_ending_rewind_hero` |
| `ending_anchor` | SC-17b | Anchor | `bgm_ending_anchor` + `cine_ending_anchor_hero` |
| `ending_drift` | SC-17c | Drift | `bgm_ending_drift` + `cine_ending_drift_hero` |

Each: single authored space, no combat, cinematic camera only, credits handoff.

**Entry:** `GameManager.load_ending(ending_id)` from SC-16 choice — not walk-back from palace.

---
