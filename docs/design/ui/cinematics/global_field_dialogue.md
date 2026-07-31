---
id: global-field-dialogue
type: reference
audience: [builder, visual, narrative]
phase: [1, 5]
status: active
authority: ui
tokens_est: 504
summary: "Global, field, dialogue cameras"
---
# Cinematics — Global, field, dialogue cameras

**Hub:** [`CINEMATICS.md`](../CINEMATICS.md)

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
