---
id: vfx-impl-checklist
type: reference
audience: [builder, visual, narrative]
phase: [5]
status: active
authority: ui
tokens_est: 670
summary: "VFX, Godot hooks, skip, M5 priority, checklist"
---
# Cinematics — VFX, Godot hooks, skip, M5 priority, checklist

**Hub:** [`CINEMATICS.md`](../CINEMATICS.md)

## 9. VFX language (camera-adjacent)

| VFX | Usage | Style |
|-----|-------|-------|
| Ink ripple | Combat transition | 2D screen shader |
| Spirit particles | Yuzu, torii | Cyan motes, soft |
| Box glow | Palace, choice | Red-gold pulse |
| Tide surge | Boss phases | Water mesh + foam |
| Dissolve | Rewind ending | Vertical wipe up |

**Avoid:** Lens flare spam, shaky cam, anime speed lines

---


## 10. Implementation hooks (Godot)

```gdscript
# Suggested signals on EventBus
EventBus.cinematic_started(scene_id: String)
EventBus.cinematic_finished(scene_id: String)
EventBus.combat_intro_requested(boss_id: String)
```

**Scene nodes:**

- `CinematicDirector` (autoload or per-zone) — owns camera override stack
- `CombatCamera` — child of combat root
- Markers: `CameraMarker_establishing`, `CameraMarker_boss_intro` in boss arenas
- SC-12: `CameraMarker_sc12_wide`, `_tilt_mid`, `_gate_hero` (see §7 SC-12)

---


## 11. Skip policy

| Cinematic | Skip after |
|-----------|------------|
| SC-02 hub pan | Immediate |
| SC-08 pool vignette | 3s |
| SC-11 flashback | 3s |
| SC-12 gate reveal | 3s (replay only; first play full) |
| Boss intros | 2s |
| Endings | Never (first play) |
| Endings replay | After first clear — skip to credits OK |

Store `seen_cinematics: []` in save data.

---


## 12. Mid-game cinematic priority (M5 art rebuild)

Ship in this order — emotional ROI over runtime:

| Priority | Scene | Treatment | Duration |
|----------|-------|-----------|----------|
| P0 | SC-02 | Hub pan | 4s |
| P0 | SC-00 | Opening montage | ~45s |
| P0 | SC-17a/b/c | Ending crane + hero BGM | 60–120s each |
| P1 | SC-09 / 14 / 15 | Boss intros | 3–6s |
| P1 | **SC-12** | Palace gate reveal | 12–15s |
| P2 | SC-08 | Deep pool vignette | 5–8s |
| P2 | SC-11 | Palace flashback | skippable |

**Rule:** One 15s mid-game movie only (SC-12). SC-08 stays a vignette to avoid water/guilt overlap with SC-09.

---


## 13. Production checklist

- [ ] Every storyboard scene has camera row in this doc or STORYBOARD
- [ ] Boss arenas have `CameraMarker_boss_intro` placed
- [ ] SC-12 gate markers + `sc12_gate_reveal` sequence authored
- [ ] SC-08 face decals + pool vignette trigger at `DeepPoolEncounter`
- [ ] Combat transition shader works at 1080p60
- [ ] Ending crane paths authored in `ending_*.tscn`
- [ ] No camera clip through palace gate hero mesh
