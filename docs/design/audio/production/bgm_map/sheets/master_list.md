---
id: master-list
type: reference
phase: [1, 5]
audience: [audio, builder]
status: active
authority: audio
tokens_est: 416
summary: "Shore Wraith and Palace Sentinel share `bgm_boss`. Tide Keeper uses `bgm_boss` in phase 1, then crossfades to phase-specific tracks at thresholds (see §5)."
---
# BGM Track Sheets — Master BGM list

**Hub:** [`bgm_sheets.md`](../bgm_sheets.md)

### Master BGM list

| Track ID | File | Duration target | Loop | Used when |
|----------|------|-----------------|------|-----------|
| `bgm_menu` | `bgm/bgm_menu.ogg` | 2:30 | Yes | Title screen |
| `bgm_prologue` | `bgm/bgm_prologue.ogg` | 1:45 | No | SC-00 only |
| `bgm_village` | `bgm/bgm_village.ogg` | 3:00 | Yes | `ruined_village`, `beach_shore` field |
| `bgm_caves` | `bgm/bgm_caves.ogg` | 3:30 | Yes | `tidal_caves` field |
| `bgm_palace` | `bgm/bgm_palace.ogg` | 3:00 | Yes | `dragon_palace_gate` field |
| `bgm_combat` | `bgm/bgm_combat.ogg` | 2:00 | Yes | Standard encounters |
| `bgm_boss` | `bgm/bgm_boss.ogg` | 2:30 | Yes | Shore Wraith, Palace Sentinel |
| `bgm_boss_tide_keeper_p2` | `bgm/bgm_boss_tide_keeper_p2.ogg` | 2:00 | Yes | Tide Keeper phase 2 |
| `bgm_boss_tide_keeper_p3` | `bgm/bgm_boss_tide_keeper_p3.ogg` | 1:30 | Yes | Tide Keeper phase 3 + choice gate |
| `bgm_ending_rewind` | `bgm/bgm_ending_rewind.ogg` | 2:00 | No | SC-17a |
| `bgm_ending_anchor` | `bgm/bgm_ending_anchor.ogg` | 2:00 | No | SC-17b |
| `bgm_ending_drift` | `bgm/bgm_ending_drift.ogg` | 2:30 | No | SC-17c |

**v1 boss music rule:** Shore Wraith and Palace Sentinel share `bgm_boss`. Tide Keeper uses `bgm_boss` in phase 1, then crossfades to phase-specific tracks at thresholds (see §5).

---
