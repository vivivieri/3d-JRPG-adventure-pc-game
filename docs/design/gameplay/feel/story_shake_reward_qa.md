---
id: story-shake-reward-qa
type: reference
phase: [2, 3]
audience: [builder, visual, qa]
status: active
authority: gameplay
tokens_est: 460
summary: "Story, shake, rewards, QA"
---
# Game Feel — Story, shake, rewards, QA

**Hub:** [`GAME_FEEL.md`](../GAME_FEEL.md)

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

Human (L6): `docs/ops/qa/PLAYTEST_SCRIPT.md` §7b feel checklist — avg ≥3.5 across ≥5 testers.

- [ ] SC-05 tutorial prompts sync with combat turns
- [ ] Intent icon matches outcome 100%
- [ ] SC-07 hints fire without dialogue
- [ ] Limit pulse visible at 100%
- [ ] Game Over readable in &lt;2 s
- [ ] No screen shake with `screen_shake=off`
- [ ] Item get SFX not spammed on multi-drop
