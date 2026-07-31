---
id: feel-survey-bugs
type: how-to
phase: [1, 6]
audience: [qa, flow]
status: active
authority: qa
tokens_est: 432
summary: "Feel checklist, survey, bugs"
---
# Playtest Script — Feel checklist, survey, bugs

**Hub:** [`PLAYTEST_SCRIPT.md`](../PLAYTEST_SCRIPT.md)

## 7b. Feel checklist (required — rate 1–5)

Per `docs/design/gameplay/GAME_FEEL.md`. Record per tester; average ≥3.5 required for ship.

| # | Question | 1 (bad) → 5 (great) |
|---|----------|---------------------|
| F1 | Movement feels responsive (no mushy input) | |
| F2 | Camera follows smoothly in field | |
| F3 | Combat hits feel readable (flash/SFX timing) | |
| F4 | Dialogue pacing comfortable (not too fast/slow) | |
| F5 | UI confirms/cancels feel snappy | |
| F6 | Hero silhouette readable at gameplay distance (field) | |
| F7 | Walk / combat animations feel natural (not robotic or floaty) | |
| F8 | Key story props read clearly (lacquer box, torii, boss telegraphs) | |

Per `docs/design/art/MODEL_QA.md` §9 — F6–F8 are the human arbiter for model polish direction when automated M1–M6 and visual jury pass but motion still feels wrong.

---


## 8. Post-play survey (5 questions)

1. Which ending did you choose and why? (free text)
2. Was combat difficulty appropriate? (1–5)
3. Did you understand the box's meaning before SC-16? (Y/N)
4. Any moment you felt stuck? (scene ID)
5. Would you play again for another ending? (Y/N)

---


## 9. Bug reporting

Use the full template and severity definitions in **`docs/ops/qa/QA_AND_BUG_PROCESS.md`** §2–§3.

Quick reference:

| Severity | Example |
|----------|---------|
| S0 Blocker | Cannot progress past puzzle |
| S1 Major | Crash, lost save |
| S2 Minor | UI overlap, typo |
| S3 Polish | Visual clip |
