# Tides of Urashima — Narrative & Writing Guide

**Version:** 1.0 (Pre-build)  
**Story reference:** `docs/STORYBOARD.md` (canonical scene bible), `game/data/dialogue/chapter_01.json`, `docs/GDD.md` §2  
**Cross-refs:** `docs/ENDING_DESIGN.md`, `docs/LOCALIZATION.md`, `docs/PACING_CHART.md`, `docs/CHARACTER_BIBLE.md`

**Canonical rule:** All story beats trace to `STORYBOARD.md`. Dialogue data lives in `game/data/dialogue/chapter_01.json`. This doc defines **how** we write — voice, limits, silence, and localization.

---

## 1. Audio & presentation model

| Layer | v1 ship |
|-------|---------|
| **Dialogue** | Written text — dialogue box + portraits (canonical en / ja / zh / zh-Hant) |
| **Voice acting** | **Selective short VO** — 12 emotional hit clips only (`docs/VO_HIT_LIST.md`) |
| **VO engine** | ElevenLabs AI (`tools/generate_ai_vo.py`) — not full script |
| **Music** | BGM per zone / boss (`docs/AUDIO_PRODUCTION_GUIDE.md`) |
| **Sound** | SFX + ambient beds; SC-08 crowd = whisper bed, not voiced |

Lines with `voice_id` in `chapter_01.json` play one short clip; **all other lines stay text-only**.

### What “narrator” means

`speaker: "narrator"` is **on-screen text** by default. Only `sc14_narrator_01` has optional VO (P2 tier).

| Term in old notes | Correct v1 term |
|-------------------|-----------------|
| Spirit voice | Yuzu dialogue (text) + optional `sc03_yuzu_01` VO + reverb SFX |
| Drowned whispers (SC-08) | Layered **text** + whisper SFX bed — not 20 voice actors |
| Full voice acting | **Rejected** — hurts pacing in 2–3 h game |

**Mix implication:** Voice bus for `voice_id` clips only; duck music −6 dB (SC-16: −18 dB). Subtitles always on.

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

## 6. Localization writing (en / ja / zh / zh-Hant)

| Rule | Detail |
|------|--------|
| **Parity** | Same meaning and emotional beat across all four written locales |
| **Line count** | JA/ZH/zh-Hant may use 1–2 lines where EN uses 1; max +1 line vs EN |
| **Choice subtext** | Max 2 lines wrap (`ENDING_DESIGN.md`) |
| **Names** | Urashima, Yuzu, Roku, Otohime — consistent transliteration in CSV |
| **Folklore terms** | 龍宮 / 漆箱 / 環貝 — use established terms in JA; gloss in ZH if needed |

### JA notes

- Roku → 六さん in dialogue (respectful distance)
- Spirit speech: slightly archaic but readable (avoid heavy classical grammar)

### ZH notes (Simplified — `zh`)

- Simplified characters throughout
- 浦岛, 柚, 六, 乙姬 — fixed cast table in `LOCALIZATION.md`

### zh-Hant notes (Traditional)

- Traditional characters throughout — **not** auto-converted from `zh`
- 浦島, 柚, 六, 乙姬 — Taiwan/HK standard forms
- VO dialect (Cantonese / Mandarin) is separate from written text; subtitles always `zh-Hant`
- Cantonese VO may use spoken particles in TTS direction notes only — subtitles stay literary Traditional

### QA

- No raw `UI_*` keys in ship build
- Playtest 1/4 per written language + both zh-Hant dialects (`PLAYTEST_SCRIPT.md`)

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
- [ ] en / ja / zh / zh-Hant drafted together
- [ ] No full-VO assumptions — only lines with `voice_id` get audio
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
6. Localization pass en → ja → zh → zh-Hant (VO: cant + cmn)

---

## 11. JRPG emotional storytelling — project rules

Tides of Urashima is a **2–3 hour** game. Depth comes from **restraint**, callbacks, and systems that echo theme — not from cutscene count or word count.

### A. Show before tell

| Technique | Where | Example |
|-----------|-------|---------|
| Inspectables before dialogue | SC-02 | Child's sandal, rotting banner — Urashima says *"Anyone...?"* after player sees emptiness |
| Zone contrast | Beach → village → caves → palace | Grey decay → biolume wonder → sterile gold void |
| Box glow states | All acts | Dim (guilt) → pulse (palace) → blinding (SC-16) — no UI tutorial needed |
| Enemy as metaphor | Combat | Salt Crab / Wraith lines reference abandonment, not random taunts |

**Rule:** If a line explains what the camera already showed, cut the line.

### B. Silence is a beat

| Scene | Silence use |
|-------|-------------|
| SC-07 | Puzzle — **no dialogue** by design |
| SC-08 | Whisper SFX bed under layered text; gaps between lines |
| SC-16 | Near-silence before choice; `sting_choice_silence` |
| SC-17 Drift | Final seconds: surf only, no BGM |

Do not fill quiet moments with narrator exposition.

### C. Callbacks (cheap, high impact)

Wire these in dialogue / barks when flags are set:

| Earlier beat | Later callback |
|--------------|----------------|
| SC-02 sandal inspect | SC-08 drowned faces — optional Urashima line |
| SC-04 Roku warning | SC-13 mirror — Roku doesn't repeat; trusts player |
| SC-11 Otohime offer | SC-16 choice subtext echoes *"stay"* without naming her |
| `mirror_choice` (SC-13) | Ending flavor line variant — not a branch |

One callback per act is enough. Avoid winking at the player.

### D. Party as emotional mirror

| Character | Story function | Writing note |
|-----------|----------------|--------------|
| Yuzu | Accusation → alliance | Fewer words over time; more weight per line |
| Roku | Grounding elder | Gravelly wisdom; never comic relief |
| Urashima | Player avatar | Act I fragments → Act III declarations (`§3`) |

**Field barks:** After `met_yuzu_spirit`, `wraith_defeated`, `knows_box_truth` — swap idle barks so the world feels changed without new cutscenes.

### E. Combat as punctuation

Combat is not filler between movies. Each fight should **change the emotional temperature**:

- SC-05 tutorial: agency after dread  
- SC-08 wraiths: guilt made physical — before SC-09 catharsis  
- SC-14 sentinel: discipline / Yuzu shines — before final act  
- SC-15 Tide Keeper: phases map to ebb → surge → stillness (choice gate)

Boss defeat lines: tragic, not triumphant. No *"You win!"* anime cadence.

### F. Endings earn their length

Endings are the **only** place to spend 60–120s of non-interactive time (`CINEMATICS.md` §8). Each must **look and sound different**:

| Ending | Visual thesis | Audio |
|--------|---------------|-------|
| Rewind | Crowd + dissolve | Bittersweet festival |
| Anchor | Dawn + sapling | Restrained hope |
| Drift | Open sea + palace below | Sparse tragedy |

No morality labels in UI copy (`ENDING_DESIGN.md`).

### G. Replay without bloat

Second run value (`REPLAY_DESIGN.md`):

- Skip SC-00 / SC-11 / SC-12 after 3s — respect player time  
- Gallery unlocks ending stills — emotional recap, not lore wiki  
- Hard mode: mechanical mastery, **not** secret fourth ending v1  

### H. What to avoid (audience 20–30)

- Bright Ghibli banter or chibi reactions  
- Long villain monologues — Tide Keeper speaks in tides, not essays  
- Moral scoring (*"Anchor ending 78% good"*)  
- VO assumptions — prose must read on screen (`§1`)  
- Extra mid-game movies beyond SC-12 — dilutes pacing (`PACING_CHART.md`)

### I. Writer smoke test

Before shipping a scene, ask:

1. What does the player **feel** without reading dialogue?  
2. Does this scene **change** a flag, relationship, or world read?  
3. Could this be 30% shorter and hit harder?  
4. Does music/SFX carry emotion when text is removed?

If (1) fails, add environment or camera — not more lines.
