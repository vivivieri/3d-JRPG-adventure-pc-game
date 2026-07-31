---
id: scum-qa
type: reference
phase: [1, 2, 3, 4, 5, 6]
audience: [architect, builder, qa]
status: active
authority: engineering
tokens_est: 188
summary: "Single slot reduces abuse; players may backup `user://` file. No anti-scum for v1."
---
# Save & Fail States — Save scumming + QA

**Hub:** [`SAVE_AND_FAIL_STATES.md`](../SAVE_AND_FAIL_STATES.md)

## 7. Save scumming

**Allowed.** Single slot reduces abuse; players may backup `user://` file. No anti-scum for v1.

**Ending gallery** encourages natural replays over scumming.

---


## 8. QA checklist

- [ ] Autosave fires entering Tidal Caves
- [ ] Well manual save shows confirmation toast
- [ ] Game Over restores valid party HP
- [ ] Continue disabled after credits until New Game
- [ ] Flags restore correctly on load
