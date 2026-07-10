# Tides of Urashima — Cinematics & Camera Spec

**Version:** 1.0 (Pre-build)  
**Engine:** Godot 4 — `Camera3D`, `AnimationPlayer`, optional `Tween`  
**Cross-refs:** `docs/STORYBOARD.md`, `docs/CHARACTER_BIBLE.md`

---

## 1. Global camera rules

| Context | Mode | FOV | Notes |
|---------|------|-----|-------|
| Field exploration | Third-person orbit | 65° | Right-mouse orbit; scroll zoom 3–8m |
| Dialogue (field) | Soft lock on speaker | 55° | Cut between speakers; no handheld shake |
| Combat | Fixed side-view JRPG | 50° | Party left, enemies right |
| Boss intro | Cinematic override | 45–60° | 3–6s; skippable after 2s |
| Ending | Scripted dolly/crane | 40–55° | Not skippable first play |

**Letterboxing:** Optional 2.39:1 bars during SC-11 flashback and SC-17 endings only.

---

## 2. Field camera — exploration

### Default follow (`OrbitCamera`)

- **Offset:** Behind-player 4.5m, height 1.6m, look-at chest
- **Collision:** Camera pulls in when clipping walls
- **Zone overrides:**

| Zone | Fog | Max zoom | Special |
|------|-----|----------|---------|
| beach_shore | Light | 7m | Slight dutch avoided |
| ruined_village | Heavy | 6m | Slow pan on first enter (SC-02) |
| tidal_caves | None | 5m | Lower height 1.4m |
| dragon_palace_gate | Medium void | 8m | Vertigo OK on gate shot |

### SC-02 first hub enter

- **Duration:** 4s
- **Move:** Pan from spawn to torii silhouette, return to follow
- **Input:** Movement disabled during pan; skippable with Confirm

---

## 3. Dialogue camera

| Shot type | When | Framing |
|-----------|------|---------|
| Wide | Scene start, mood beats | Both characters + environment |
| Over-shoulder | Back-and-forth | Speaker 1/3 frame, listener bokeh |
| Close | SC-03 spirit voice, SC-13 mirror | Face + box or mirror edge |
| Low angle | SC-03 torii | Looking up at cracked torii |

**Portrait UI:** Lower third dialogue box; 2D portrait left of text (see `ART_DIRECTION.md` §4).

---

## 4. Combat transitions

### Enter combat (all fights)

1. Screen ripple (ink-wash radial, 0.4s)
2. Fade to combat camera (0.3s)
3. Enemy slide-in from right (0.5s)
4. Intent UI hidden turn 1 tutorial only

### Exit combat (victory)

1. Victory sting + flash on enemies (0.3s)
2. Ripple out (0.4s)
3. Return to field camera at trigger position

### Exit combat (defeat)

1. Desaturate 0.5s → Game Over menu

---

## 5. Boss intros

### Shore Wraith (SC-09) — 5s

| Time | Shot |
|------|------|
| 0–2s | Low angle pool; water churn |
| 2–4s | Wraith rises; camera pulls back |
| 4–5s | Snap to combat framing; boss name banner |

**Audio:** Water surge + choir stab

### Palace Sentinel (SC-14) — 3s

| Time | Shot |
|------|------|
| 0–1s | Hall depth; footsteps |
| 1–2s | Sentinel turns; eye slit glow |
| 2–3s | Combat framing |

### Tide Keeper (SC-15) — 6s

| Time | Shot |
|------|------|
| 0–2s | Wide throne; void sea below |
| 2–4s | Tide Keeper materializes from water |
| 4–5s | Close on Urashima reaction |
| 5–6s | Combat framing; name banner |

---

## 6. Boss phase cameras

### Shore Wraith phase 2

- Brief zoom 10% on boss (0.5s) at 50% HP
- No orbit

### Tide Keeper phase 2 — Surge

- **Slow orbit** 30° over 8s during phase (combat continues)
- Orbit pauses on player turn for readability
- Reset on phase 3

### Choice gate (SC-16)

- Combat freeze; camera dolly to Urashima close-up (1.5m)
- Box glow intensifies; UI choice overlay
- Background desaturate 20%

---

## 7. Storyboard scene specs

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

---

## 11. Skip policy

| Cinematic | Skip after |
|-----------|------------|
| SC-02 hub pan | Immediate |
| SC-11 flashback | 3s |
| Boss intros | 2s |
| Endings | Never (first play) |
| Endings replay | After first clear — skip to credits OK |

Store `seen_cinematics: []` in save data.

---

## 12. Production checklist

- [ ] Every storyboard scene has camera row in this doc or STORYBOARD
- [ ] Boss arenas have `CameraMarker_boss_intro` placed
- [ ] Combat transition shader works at 1080p60
- [ ] Ending crane paths authored in `ending_*.tscn`
- [ ] No camera clip through palace gate hero mesh
