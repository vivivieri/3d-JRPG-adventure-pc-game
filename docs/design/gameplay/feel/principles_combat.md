---
id: principles-combat
type: reference
phase: [2, 3]
audience: [builder, visual, qa]
status: active
authority: gameplay
tokens_est: 498
summary: "Principles + combat feedback"
---
# Game Feel — Principles + combat feedback

**Hub:** [`GAME_FEEL.md`](../GAME_FEEL.md)

## 1. Design principles

| Principle | Application |
|-----------|-------------|
| **Restraint** | Melancholy tone — no arcade combo spam |
| **Clarity** | Every hit, reward, and quest update readable in &lt;0.5 s |
| **Weight** | Bosses feel heavy; village feels hollow |
| **Selective VO** | 12 hit clips only (`voice_id` lines) — text+subtitles always; not full script |

---


## 2. Combat feedback

### Hit resolution

| Event | Visual | Audio | Timing |
|-------|--------|-------|--------|
| Player attack hit | Target white flash 0.12 s | `sfx_combat_hit_light` | On damage apply |
| Player heavy / skill | Flash + small forward lunge | Element SFX | 0.15 s |
| Enemy attack hit | Party member flash red | `sfx_combat_hit_heavy` if boss | 0.12 s |
| Defend | Blue tint on actor | `sfx_combat_defend` | Until turn end |
| KO | Collapse anim + desaturate portrait | — | 0.4 s |

**Damage numbers:** Optional v1 — if shown, float up 0.8 s, max 2 per hit. Default **on** for tutorial (SC-05), player can disable in settings (future) or always on for clarity.

**Hitstop:** 0.05 s freeze on crit/limit only — not every basic attack.

### Status & intent

| Element | Feedback |
|---------|----------|
| Intent icon | 1-turn preview above enemy; pulse on change |
| Poison tick | Green drip VFX + small shake |
| Phase banner | 2 s center screen; input locked |
| Limit full | Gauge gold pulse + border shimmer; one SFX chime |

### Victory & defeat

| Event | Sequence |
|-------|----------|
| Win | `sting_victory` (1 s) → XP/coins popup → drops → Confirm or 3 s auto |
| Lose | Desaturate 0.5 s → "The tide claims you" → Load / Title |
| Boss win | Extra 1 s silence before rewards (Shore Wraith: cloth collapse) |

---
