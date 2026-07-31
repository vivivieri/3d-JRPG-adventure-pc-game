---
id: combat-boss
type: reference
audience: [builder, visual, narrative]
phase: [2, 5]
status: active
authority: ui
tokens_est: 442
summary: "Combat transitions + boss cameras"
---
# Cinematics — Combat transitions + boss cameras

**Hub:** [`CINEMATICS.md`](../CINEMATICS.md)

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
