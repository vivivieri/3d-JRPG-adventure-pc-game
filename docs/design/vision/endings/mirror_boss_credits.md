---
id: mirror-boss-credits
type: reference
phase: [1, 6]
audience: [narrative, flow]
status: active
authority: vision
tokens_est: 385
summary: "Mirror choice, boss resolution, credits"
---
# Ending Design — Mirror choice, boss resolution, credits

**Hub:** [`ENDING_DESIGN.md`](../ENDING_DESIGN.md)

## 4. SC-13 mirror choice (recorded, low branch)

**Scene:** Roku reveals box truth
**Dialogue choice:** "I would open it" / "I would break it" / "I don't know yet"

| Choice | Flag | Effect |
|--------|------|--------|
| Open | `mirror_choice=open` | SC-16 Rewind subtext slightly warmer (1 line variant) |
| Break | `mirror_choice=break` | SC-16 Anchor subtext slightly warmer |
| Don't know | `mirror_choice=unknown` | Default subtext |

**Does NOT lock or disable any ending.** Flavor only.

---


## 5. Post-choice boss resolution

After choice confirmed:
1. Tide Keeper speaks 1 line reacting to choice
2. Urashima uses scripted `Last Mercy` (cosmetic, 1 turn)
3. Keeper dissolves; no additional combat
4. Fade to ending scene (SC-17a/b/c)

---


## 6. Credits

**All endings:** Roll credits after cinematic (60–90s)

| Section | Content |
|---------|---------|
| Dedicated to | "Those who returned too late." |
| Story | Adapted from Urashima Tarō (public domain) |
| Engine | Godot MIT |
| Fonts | Noto OFL |
| Audio/Art | Per `docs/archive/compliance/COMPLIANCE_REPORT.md` |
| Ending tag | "You chose: [Rewind/Anchor/Drift]" — small text |

**After credits:** Return to title. `game_completed` set. Save slot shows ending icon.

---
