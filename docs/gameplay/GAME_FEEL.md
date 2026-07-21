# Tides of Urashima — Game Feel & Feedback

**Version:** 1.0 (Pre-build)
**Cross-refs:** `docs/gameplay/COMBAT_SYSTEMS.md`, `docs/ui/UI_UX_FLOW.md`, `docs/ui/CINEMATICS.md`, `docs/vision/PACING_CHART.md`

Defines **moment-to-moment juice** — how the game responds to player actions. Complements systems docs with timing, VFX, and UI feedback rules.

---

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

## 3. Field exploration feedback

### Interaction

| Action | Feedback |
|--------|----------|
| Enter interact range | Prompt "E — Investigate" (localized) |
| Interact | Brief highlight pulse on object |
| Dialogue start | Soft camera nudge toward speaker |
| Zone transition | 1.5 s fade + BGM crossfade |

### Movement

| Surface | Footstep | Notes |
|---------|----------|-------|
| Sand | `sfx_footstep_sand` | Beach, village paths |
| Wood | `sfx_footstep_wood` | Pier, shack |
| Wet | `sfx_footstep_wet` | Puddles, caves |
| Marble | `sfx_footstep_marble` | Palace |

**Camera:** Orbit smooth; no shake in field except optional boss orbit SC-15 (`screen_shake` setting).

### Quest & objectives

| Type | HUD feedback |
|------|--------------|
| Active quest | Top-right compact tracker; stage text updates |
| New quest | Banner 2 s + quest log ping |
| Stage complete | Checkmark + subtle SFX |
| Soft gate (village) | Pointer toward torii after 2 inspects — **not** hard block |

**SC-02:** Player can reach torii without all inspects; Q1 stage 1 encourages 3 points.

---

## 4. Puzzle feedback (SC-07)

| Event | Feedback |
|-------|----------|
| Switch toggle | Stone grind + water rise 2 s |
| HIGH state | Louder drip ambient |
| Latch open | Metallic clang + quest complete |
| Hint 3 min | Quest log text only — **no dialogue** |
| Hint 5 min | Switch glow pulse + chime |

Silence is intentional — see `NARRATIVE_WRITING_GUIDE.md` §4.

---

## 5. UI & menu feedback

| Action | Feedback |
|--------|----------|
| Confirm | `sfx_ui_confirm` |
| Cancel | `sfx_ui_cancel` |
| Item get | `sfx_ui_item_get` + icon fly to HUD |
| Equip | `sfx_ui_equip` + stat delta flash |
| Save | `sfx_ui_save` + "Saved" toast 1.5 s |
| Invalid | `sfx_ui_invalid` + grey flash |
| Tab open | Movement paused; `sfx_ui_menu_open` |

**Typewriter:** 40 CPS Normal (`SETTINGS_ACCESSIBILITY.md`); speaker nameplate always visible.

---

## 6. Story beats

| Beat | Feedback |
|------|----------|
| Box dormant glow | Faint pulse on hip mesh |
| Box awakened (palace) | Stronger pulse + motes |
| SC-10 Yuzu join | `sting_yuzu_join` + materialize VFX 2 s |
| SC-16 choice | Music duck; box bloom; UI cards only |
| Ending | Letterbox where specified; no skip first play |

---

## 7. Screen shake policy

| Context | Shake | Setting |
|---------|-------|---------|
| Boss heavy slam | Light 0.2 s | `screen_shake` on |
| Tide Keeper phase 2 orbit | Camera move, not shake | — |
| Field exploration | None | — |
| Reduced motion | Off all shake | `screen_shake=off` |

---

## 8. Reward pacing

| Reward | When shown | Duration |
|--------|------------|----------|
| XP | Battle end | 2 s banner |
| Shell coins | Battle end | Count-up 0.5 s |
| Key item | Story grant | Full `item_get` fanfare |
| Lore | On read | Journal unlock anim 1 s |
| Level up | Field only | Banner + HP/MP refill VFX |

**Anti-grind:** No XP from inspectables; combat rewards only.

---

## 9. QA checklist

Automated: `bash tools/run_feel_smoke_checks.sh` audits `game/data/qa/feel_thresholds.json` against `player_controller.gd` constants.

Human (L6): `docs/qa/PLAYTEST_SCRIPT.md` §7b feel checklist — avg ≥3.5 across ≥5 testers.

- [ ] SC-05 tutorial prompts sync with combat turns
- [ ] Intent icon matches outcome 100%
- [ ] SC-07 hints fire without dialogue
- [ ] Limit pulse visible at 100%
- [ ] Game Over readable in &lt;2 s
- [ ] No screen shake with `screen_shake=off`
- [ ] Item get SFX not spammed on multi-drop
