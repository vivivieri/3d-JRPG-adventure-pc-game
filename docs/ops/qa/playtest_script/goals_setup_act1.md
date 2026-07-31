---
id: goals-setup-act1
type: how-to
phase: [1, 6]
audience: [qa, flow]
status: active
authority: qa
tokens_est: 427
summary: "- [ ] `bash tools/run_playtest_smoke.sh` → PASS"
---
# Playtest Script — Goals, setup, Act I

**Hub:** [`PLAYTEST_SCRIPT.md`](../PLAYTEST_SCRIPT.md)

## 1. Playtest goals

| Goal | Metric |
|------|--------|
| Complete without guide | ≥80% testers |
| Understand 3 endings | Post-survey |
| Combat too easy/hard | Boss attempts ≤3 Normal |
| Movement / camera feel | Feel checklist §7b (1–5 scale) |
| Soft-lock | Zero |
| Localization | No missing keys en/ja/zh/zh-Hant |

---


## 2. Session setup

**Before starting — verify AI suite (or ask agent for report):**

- [ ] `bash tools/run_playtest_smoke.sh` → PASS
- [ ] `bash tools/run_integration_tests.sh` → PASS
- [ ] `REQUIRE_L5=1 bash tools/run_e2e_playthrough.sh` → PASS
- [ ] Record commit SHA: `git rev-parse HEAD`

**Human session:**

- [ ] Fresh `user://` delete
- [ ] Record playtime, deaths, ending chosen
- [ ] Note build commit + branch
- [ ] Language rotation across testers: en / ja / zh / zh-Hant (incl. one zh-Hant + Cantonese VO session)

---


## 3. Act I script (~30 min)

| Step | Action | Verify |
|------|--------|--------|
| 1 | New Game | SC-00 prologue plays |
| 2 | Skip / watch prologue | SC-01 spawn |
| 3 | WASD to village | Movement tutorial |
| 4 | Inspect banner, sandal, well | Q1 stage 1 |
| 5 | Save at well | Autosave + manual |
| 6 | Torii scene SC-03 | `met_yuzu_spirit` |
| 7 | Roku shack SC-04 | Shop opens; cave unlocked |
| 8 | Buy 1 salve | Economy works |
| 9 | SC-05 crab fight | Tutorial 3 turns |
| 10 | Enter caves SC-06 | Zone transition |

**Pass:** Reach caves in ≤35 min without stuck.

---
