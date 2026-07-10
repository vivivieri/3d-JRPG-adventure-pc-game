# Tides of Urashima — Narrative & Writing Guide

**Version:** 1.0 (Pre-build)  
**Story reference:** `docs/STORYBOARD.md` (canonical scene bible), `game/data/dialogue/chapter_01.json`, `docs/GDD.md` §2  
**Cross-refs:** `docs/ENDING_DESIGN.md`, `docs/LOCALIZATION.md`, `docs/PACING_CHART.md`, `docs/CHARACTER_BIBLE.md`

**Canonical rule:** All story beats trace to `STORYBOARD.md`. Dialogue data lives in `game/data/dialogue/chapter_01.json`. This doc defines **how** we write — voice, limits, silence, and localization.

---

## 1. Audio & presentation model

| Layer | v1 ship |
|-------|---------|
| **Dialogue** | Written text only — dialogue box + portraits |
| **Voice acting** | **None** — no recorded VO lines |
| **Music** | BGM per zone / boss (`docs/AUDIO_PRODUCTION_GUIDE.md`) |
| **Sound** | SFX + ambient beds only |

### What “narrator” means

`speaker: "narrator"` in dialogue JSON is **on-screen text**, not voice-over. Do not write as if a voice actor will read it aloud.

| Term in old notes | Correct v1 term |
|-------------------|-----------------|
| Voice-over | Narrator line (text) |
| Spirit voice | Yuzu dialogue line (text) + optional reverb SFX |
| Drowned whispers (SC-08) | Layered **text** lines + whisper SFX bed — not VO |

**Mix implication:** No voice bus. Dialogue readability = font size + contrast only (`docs/SETTINGS_ACCESSIBILITY.md`).

---

## 2. Themes & adaptation spine

From `GDD.md` §2 and `STORYBOARD.md`:

| Theme | How it shows in prose |
|-------|----------------------|
| Consequence over nostalgia | Village ruin before palace beauty |
| Masculine duty vs. escape | Urashima's short sentences → declarations |
| Stolen time | Box, mirror, Tide Keeper dialogue |
| No villain princess | Otohime seductive, not cruel |
| Bittersweet endings | No ending labeled “good” or “bad” |

**Folklore anchor:** Public-domain *Urashima Tarō* — kappa-turtle rescue, Dragon Palace, forbidden box, centuries passed. We darken: spirits bound to objects, box holds **village years**, not personal age alone.

---

## 3. Character voice

### Urashima (`urashima`)

| Act | Voice | Example |
|-----|-------|---------|
| I | Quiet guilt; fragments | *"Three days... it was only three days..."* |
| II | Defensive → listening | *"The tide carved this place."* |
| III | Firm accountability | *"Mercy that drowns the world isn't mercy."* |

**Rules:** Short clauses in Act I. Avoid jokes. Never boast. Posture in stage direction = hunched → upright (`CHARACTER_BIBLE.md`).

### Yuzu (`yuzu`)

| Trait | Rule |
|-------|------|
| Tone | Accusatory → resolve; never cute |
| Structure | Complete sentences; poetic but clear |
| Avoid | Modern slang, flirting, chibi asides |

**Example:** *"You left. We waited."* / *"The tide took our years. You took our tomorrow."*

### Roku (`roku`)

| Trait | Rule |
|-------|------|
| Tone | Gravelly, blunt, protective |
| Register | Elder fisherman — "boy", concrete warnings |
| Role | Exposition carrier without lecturing |

**Example:** *"That box isn't a gift. Don't open it."*

### Otohime (`otohime`)

| Trait | Rule |
|-------|------|
| Appearances | SC-11 flashback, SC-17c glimpse only |
| Tone | Too perfect; seductive stillness |
| Avoid | Fanservice, villain monologuing |

**Example:** *"Stay, and the world will not touch you."*

### Tide Keeper (`tide_keeper`)

| Trait | Rule |
|-------|------|
| Tone | Calm mercy → exhausted tide |
| Metaphor | Sea, time, borrowed moments — not modern tech |
| Phase 3 | Shorter barks; more pauses |

### Narrator (`narrator`)

| Use | When |
|-----|------|
| Environmental | Scene-setting, horror beats |
| Not for | Character opinions disguised as omniscient |

**Style:** Present tense or literary past. One image per line max. Salt, tide, rot, bells.

### Enemies (combat barks)

| Enemy | Voice |
|-------|-------|
| Salt Crab | One line pre-fight (`SC-05`); no mid-combat chatter v1 |
| Shore Wraith | Accusatory collective: *"You chose her over us."* |
| Palace Sentinel | Formal guardian: duty, stolen time |
| Tide Keeper | See above |

---

## 4. Scene dialogue rules

### Line count limits

| Scene type | Max lines | Max chars/line (EN) |
|------------|-----------|---------------------|
| Field greeting | 4 | 90 |
| Inspect / lore | 2 | 100 |
| Boss intro | 3 | 80 |
| Boss mid-fight | 1 per phase | 60 |
| Revelation (SC-13) | 8 | 100 |
| Choice (SC-16) | UI copy only — see `ENDING_DESIGN.md` |
| Ending cinematic | 6 | 120 |

**Combat:** Minimize dialogue during fights except phase banners and SC-15 choice gate.

### Intentional silence — SC-07

**SC-07 has no dialogue block in `chapter_01.json` — by design.**

| Field | Detail |
|-------|--------|
| **Purpose** | Pacing breather after SC-06; quiet problem-solving before SC-08 horror |
| **Mood** | *Quiet problem-solving* (`STORYBOARD.md`, `PACING_CHART.md`) |
| **Story** | Water raises/lowers; player learns tide logic without words |
| **Feedback** | Switch SFX, water animation, quest log hint after 3 min (`PUZZLE_DESIGN.md`) |
| **Do not add** | Urashima muttering, Roku radio bark before hint timer |

Other silent beats:

| Scene | Silence type |
|-------|--------------|
| SC-02 explore | Minimal lines at entry; inspectables carry weight |
| SC-16 choice | Urashima **silent** — player projects (`ENDING_DESIGN.md`) |
| SC-17 endings | 1–2 lines max before credits |

---

## 5. Scene writing reference (from storyboard)

| Scene | Dialogue focus | Data ID |
|-------|----------------|---------|
| SC-00 | Mythic setup; box origin | `SC-00` |
| SC-01 | Disorientation; "three days" | `SC-01` |
| SC-02 | Emptiness; 3 inspect sub-scenes | `SC-02`, `SC-02-BANNER`, etc. |
| SC-03 | Yuzu accusation | `SC-03` |
| SC-04 | Roku warning + map | `SC-04` |
| SC-05 | Crab prelude | `SC-05` |
| SC-06 | Cave wonder | `SC-06` |
| SC-07 | **No dialogue** | — |
| SC-08 | Drowned voices (text) | `SC-08` |
| SC-09 | Shore Wraith | `SC-09` |
| SC-10 | Yuzu join | `SC-10` |
| SC-11 | Otohime flashback | `SC-11` |
| SC-12 | Palace gate | `SC-12` |
| SC-13 | Box truth + mirror flavor choice | `SC-13` |
| SC-14 | Sentinel | `SC-14` |
| SC-15 | Tide Keeper | `SC-15` |
| SC-16 | Choice UI only | `SC-16` |
| SC-17a/b/c | Ending lines | `SC-17a`, etc. |

**Inspect vs lore:** Village inspect scenes (`SC-02-*`) deliver immediate dialogue. Separate lore pickups (`game/data/lore/`) deliver journal entries — see `LORE_AND_ENVIRONMENTAL_STORY.md`.

---

## 6. Localization writing (en / ja / zh)

| Rule | Detail |
|------|--------|
| **Parity** | Same meaning and emotional beat across all three |
| **Line count** | JA/ZH may use 1–2 lines where EN uses 1; max +1 line vs EN |
| **Choice subtext** | Max 2 lines wrap (`ENDING_DESIGN.md`) |
| **Names** | Urashima, Yuzu, Roku, Otohime — consistent transliteration in CSV |
| **Folklore terms** | 龍宮 / 漆箱 / 環貝 — use established terms in JA; gloss in ZH if needed |

### JA notes

- Roku → 六さん in dialogue (respectful distance)
- Spirit speech: slightly archaic but readable (avoid heavy classical grammar)

### ZH notes

- Simplified characters throughout
- 浦岛, 柚, 六, 乙姬 — fixed cast table in `LOCALIZATION.md`

### QA

- No raw `UI_*` keys in ship build
- Playtest 1/3 per language (`PLAYTEST_SCRIPT.md`)

---

## 7. Emotion tags (`emotion` field)

Use in `chapter_01.json` for portrait selection:

| Tag | Portrait lean |
|-----|---------------|
| `neutral` | Default / narrator |
| `uneasy` | Urashima wary |
| `confused` | Urashima lost |
| `guilty` | Urashima shame |
| `weary` | Urashima exhausted |
| `accusatory` | Yuzu SC-03 |
| `sorrow` | Yuzu melancholy |
| `grim` | Roku |
| `urgent` | Roku warning |
| `wonder` | Narrator awe |
| `dread` | Horror beats |

---

## 8. Box comprehension target

**Playtest question:** *Did you understand the box before SC-16?*

Design target: **≥70% yes** without external guide.

| Beat | What player should learn |
|------|--------------------------|
| SC-00 / SC-04 | Box is forbidden; from palace |
| SC-02 lore + inspect | Village lost time |
| SC-11 | Paradise bargain |
| SC-13 | Box holds **their** years; opening costs Urashima |
| SC-16 | Three prices — no wrong answer |

If playtest fails, add lore or one Roku line — **not** SC-07 dialogue (preserve silence).

---

## 9. Writer checklist (per new line)

- [ ] Matches character voice §3
- [ ] Within line count §4
- [ ] en / ja / zh drafted together
- [ ] No VO assumptions
- [ ] Scene ID exists in `STORYBOARD.md`
- [ ] No morality label on endings
- [ ] Registered in `chapter_01.json` if shippable

---

## 10. Production order

1. Lock SC-00–SC-06 dialogue (Act I)
2. Confirm SC-07 remains silent
3. Act II horror + boss (SC-08–SC-11)
4. Act III revelation + choice copy (SC-13–SC-16)
5. Three ending scripts (SC-17a/b/c)
6. Localization pass en → ja → zh
