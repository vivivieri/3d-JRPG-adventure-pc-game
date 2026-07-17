# Tides of Urashima — Project Journey & Scope Record

**Version:** 1.0  
**Purpose:** Single reference for how the game was conceived, scoped, and documented — including **consideration points** for extending story, lore, and world background.  
**Audience:** Writers, designers, agents, and stakeholders adding content post–M0.

**Canonical detail lives in linked docs** — this file is the narrative of *why* those docs exist and *what to check* before changing them.

---

## 1. Elevator pitch (locked)

> *Urashima Tarō returns from the Dragon Palace to find his village erased by time. A short, melancholy JRPG about consequence, memory, and the price of paradise.*

| Field | Decision |
|-------|----------|
| **Title** | Tides of Urashima |
| **Source** | Public-domain *Urashima Tarō* (no licensing fee) |
| **Genre** | 3D adventure JRPG, turn-based combat |
| **Engine** | Godot 4.7 (Forward+) |
| **Platform** | PC (Steam) — Linux + Windows v1 |
| **Audience** | Men 20–30 |
| **Playtime** | 2–3 hours (main story) |
| **Price band** | $4.99–$9.99 (short narrative game) |
| **USP** | "A 2–3 hour emotional folktale — Dark Urashima Tarō" |

**Player fantasy:** *"I can fix what I broke — but should I?"*

---

## 2. Idea origin — from folktale to dark adaptation

### 2.1 Original tale (baseline)

A fisherman saves a turtle, visits the Dragon Palace, spends days with Princess Otohime, returns with a forbidden box. Centuries have passed; opening the box ages him instantly.

### 2.2 Why this story

| Consideration | Decision |
|---------------|----------|
| **Licensing** | Folktale is public domain — safe for indie Steam ship |
| **Emotional core** | Regret, time, consequence — fits short runtime |
| **JRPG structure** | Hub → dungeons → boss → choice maps cleanly to 3 acts |
| **Audience tone** | Muted coastal decay, not bright Ghibli whimsy |
| **Differentiation** | Dark retelling + three equally valid endings |

### 2.3 Adaptation choices (locked)

| Folktale element | Our version | Rationale |
|------------------|-------------|-----------|
| Turtle rescue | Wounded **spirit-turtle** of the coast | Sacred, not cartoon |
| Dragon Palace | Beautiful, sterile — no children, no seasons | Unease under paradise |
| Return home | Village is **ruin overtaken by sea** | Visual guilt before palace beauty |
| Survivors | Spirits bound to objects; one living elder (Roku) | Emptiness is deliberate |
| The box | Holds **the village's stolen years**, not personal age alone | Stakes are communal |
| Antagonist | **Tide Keeper** — time personified, not evil princess | Otohime is mirror, not villain |
| Endings | Rewind / Anchor / Drift — no "true" ending | Three philosophies, not morality score |

**Themes (non-negotiable):**

- Consequence over nostalgia  
- Masculine duty vs. escape  
- Bittersweet endings over power fantasy  

---

## 3. Scope journey — what we locked and what we cut

### 3.1 v1 shippable scope (frozen)

| Content | Count | Notes |
|---------|-------|-------|
| Hub areas | 1 | Ruined Fishing Village |
| Dungeons | 2 | Tidal Caves, Dragon Palace Gate |
| Bosses | 3 | Shore Wraith, Palace Sentinel, Tide Keeper |
| Party | 3 | Urashima, Yuzu, Roku |
| Main quests | 5 | See `docs/world/QUEST_AND_FLAGS.md` |
| Lore collectibles | 8 | Optional; achievement for all 8 |
| Skills | 14 player + 6 enemy | `docs/gameplay/SKILLS_BIBLE.md` |
| Endings | 3 | Rewind, Anchor, Drift |
| Languages | 4 written + dialect VO | en, ja, zh, zh-Hant |

### 3.2 Explicit cuts (do not re-add without scope review)

| Cut | Reason |
|-----|--------|
| Reverse-gravity palace rooms | Complexity vs. 2–3 h runtime |
| World map screen | Single continuous coastal walk |
| Fast travel | Hub backtracking is intentional |
| Living village NPCs | Breaks Act I dread |
| Full voice acting | Hurts pacing; 12 selective VO clips only |
| Fourth / "true" ending | Three endings are equally valid |
| NG+ stat carry | Replay = endings + Hard mode, not power creep |
| Chapter select v1 | New Game only |
| Chatty town NPCs | Wind + rot are the "NPCs" in Act I |
| GodotPrompter on GDAI-regen branch | Tooling comparison experiment only |

### 3.3 Scope creep mitigations (risk register)

From `docs/vision/GDD.md` §16:

- Lock **3 locations** until post-launch  
- Single style bible + vertical slice gate before art production  
- Combat vertical slice before content production  
- Asset compliance checks before ship  

---

## 4. Story journey — scene spine and acts

### 4.1 Narrative structure

**20 storyboard headings** (`SC-00` prologue + `SC-01`–`SC-16` + three `SC-17` variants). One playthrough experiences **18** scenes.

```
Act I — The Return (~30 min)
  SC-00 Prologue → SC-01 Shore → SC-02 Empty Village → SC-03 Torii (Yuzu)
  → SC-04 Roku → SC-05 Tutorial combat

Act II — The Depths (~60 min)
  SC-06 Cave entrance → SC-07 Water puzzle (SILENT) → SC-08 Drowned echoes
  → SC-09 Shore Wraith boss → SC-10 Yuzu joins → SC-11 Otohime flashback
  → SC-12 Palace gate

Act III — The Tide (~30–45 min)
  SC-13 Box truth → SC-14 Palace Sentinel → SC-15 Tide Keeper
  → SC-16 Choice → SC-17a/b/c Ending
```

**Canonical scene bible:** `docs/vision/STORYBOARD.md`  
**Dialogue data:** `game/data/dialogue/chapter_01.json`  
**Flags / quests:** `docs/world/QUEST_AND_FLAGS.md`, `game/data/story/`

### 4.2 Five main quests (story backbone)

| # | Quest | Completes when |
|---|-------|----------------|
| 1 | The Return | `met_roku` |
| 2 | Echoes at the Torii | `shore_wraith_defeated` |
| 3 | Depths of Guilt | `gate_reached` |
| 4 | The Palace Gate | `sentinel_defeated` |
| 5 | The Tide's Answer | `game_completed` |

### 4.3 Three endings (choice philosophy)

**Player question at SC-16:** *Who pays for stolen time — the past, the land, or yourself?*

| Ending | Action | Tone | Theme |
|--------|--------|------|-------|
| **Rewind** | Open box — village restored | Bittersweet | Nostalgia has a price |
| **Anchor** | Break box — spirits bind to shore | Hopeful | Accountability over escape |
| **Drift** | Walk into tide — refuse bargain | Tragic | Cycle continues |

**Rules:** No morality labels. No "best" ending badge. SC-13 mirror choice (`open` / `break` / `unknown`) only warms SC-16 subtext — does not lock endings.

Full spec: `docs/vision/ENDING_DESIGN.md`

---

## 5. Story consideration points — checklist for suggested additions

Use this section when proposing **new dialogue, lore, characters, zones, or backstory**.

### 5.1 Core story constraints

| # | Consideration | Pass? |
|---|---------------|-------|
| 1 | Does it serve **consequence over nostalgia**? | |
| 2 | Does it respect **2–3 hour** runtime (density over padding)? | |
| 3 | Does it avoid making Otohime a **cartoon villain**? | |
| 4 | Does it preserve **village emptiness** in Act I (no living crowds)? | |
| 5 | Does it reinforce the **box mystery ladder** (clues before SC-13)? | |
| 6 | Does it support **≥70% box comprehension** before SC-16? | |
| 7 | Are all three endings still **equally valid**? | |
| 8 | Does it match **men 20–30** tone (no chibi, no Ghibli banter)? | |

### 5.2 Character voice constraints

| Character | Must | Must not |
|-----------|------|----------|
| **Urashima** | Act I fragments → Act III declarations; short clauses when guilty | Jokes, boasting, anime victory lines |
| **Yuzu** | Accusatory → resolve; poetic but clear | Cute slang, flirting, chibi asides |
| **Roku** | Gravelly elder; concrete warnings | Comic relief, lecturing exposition dumps |
| **Otohime** | Seductive stillness; too perfect | Fanservice, villain monologues |
| **Tide Keeper** | Sea/time metaphors; shorter barks in phase 3 | Modern tech refs, essay-length speeches |

Full voice guide: `docs/vision/NARRATIVE_WRITING_GUIDE.md` §3

### 5.3 Scene-type limits

| Scene type | Max lines | Max chars/line (EN) |
|------------|-----------|---------------------|
| Field greeting | 4 | 90 |
| Inspect / lore | 2 | 100 |
| Boss intro | 3 | 80 |
| Revelation (SC-13) | 8 | 100 |
| Ending cinematic | 6 | 120 |

**SC-07 is silent by design** — do not add Urashima muttering or Roku radio bark before hint timer.

### 5.4 Environmental storytelling rules

| Channel | Use for | Data |
|---------|---------|------|
| **Scene inspect** (E on story object) | Immediate emotional beat | `chapter_01.json` (`SC-02-*`) |
| **Lore pickup** (journal Tab) | Archival detail, 2–4 sentences | `lore_entries.json` |

**8 lore entries** — optional depth, not required for endings. Do not duplicate inspect text verbatim in lore.

**Box clue ladder** (order matters):

1. SC-00 / SC-04 — box from palace; don't open  
2. `fishing_ledger` — village waited  
3. `cave_inscription` — years stolen  
4. SC-11 — paradise bargain  
5. SC-13 — box holds **their** years  
6. SC-16 — player chooses price  

Full spec: `docs/vision/LORE_AND_ENVIRONMENTAL_STORY.md`

### 5.5 Narrative density gate (before adding any line)

```
New line proposed
    → Does environment/camera already carry the emotion? YES → skip
    → Which pattern? (boss bark / inspect / quiet beat / callback)
    → Run: python3 tools/validate_narrative_density.py
```

**Budgets:** `game/data/narrative/narrative_density.json`  
**Guide:** `docs/vision/NARRATIVE_DENSITY.md`

| Pattern | Budget |
|---------|--------|
| Quiet beats | ≤6 total; Act II caves allow up to 4 |
| Flag callbacks | ≤2 lines/scene; ≤3 uses/flag |
| Hub inspect (village) | ≤4 scenes; narrator before PC speaks |
| Field battle_start barks | Allowlist: `tide_wraith` only |

### 5.6 JRPG reference steals (what to borrow vs. reject)

**Borrow (emotion + structure, not runtime):**

| Reference | Steal |
|-----------|-------|
| Ni no Kuni | Grief externalized; healing = carrying loss |
| Trails | Hub inspectables earn the ending |
| FFX | Outsider pilgrimage; intimate scale |
| Persona 5 | Fight harm people feel, not abstract evil |
| 13 Sentinels (lite) | One mid-game reframe (SC-11) |
| Metaphor | Companions as philosophies; three worldviews |

**Reject:**

- Dozens-of-hours slow burn only  
- Bright whimsy / chibi comedy  
- Shock twists without foreshadowing  
- "True ending" or morality score  
- Full multi-POV mystery  

Full table: `docs/vision/NARRATIVE_WRITING_GUIDE.md` §12

### 5.7 Localization parity

Any new line needs **en / ja / zh / zh-Hant** together. JA/ZH may use +1 line vs EN. Choice subtext max 2 lines wrap. Names fixed: Urashima, Yuzu, Roku, Otohime.

### 5.8 Writer smoke test (per scene)

1. What does the player **feel** without reading dialogue?  
2. Does this scene **change** a flag, relationship, or world read?  
3. Could this be **30% shorter** and hit harder?  
4. Does music/SFX carry emotion when text is removed?

If (1) fails → add environment or camera, **not more lines**.

---

## 6. World & visual journey

### 6.1 Zone graph (no world map)

```
beach_shore ←→ ruined_village → tidal_caves → dragon_palace_gate → endings
```

| Zone | Act | Mood | Palette role |
|------|-----|------|--------------|
| Beach / Village | I | Dread, emptiness | Fog grey, weathered wood, rust |
| Tidal Caves | II | Wonder + wrongness | Deep teal, biolume cyan |
| Palace Gate | III | Awe, sterile gold | Coral gold, void blue |
| Endings | — | Triptych tones | Festival / dawn / open sea |

### 6.2 Art direction pivot (M0c)

**Target:** High-detail stylized Japanese 3D — *Ni no Kuni* richness + *Eastward* clarity. Muted palette, emotional weight. **No primitive placeholders** in ship builds.

**Motifs:** Japanese coastal / ryūgū only — no European castle props.

Full bible: `docs/art/ART_DIRECTION.md` v1.1

### 6.3 Emotional pacing rules

1. **No combat** before SC-05 (~22 min)  
2. **SC-07 puzzle breather** before horror (SC-08) and boss (SC-09)  
3. **Yuzu join** heals tone after wraith catharsis  
4. **Choice** immediately after Tide Keeper peak — no extra grind  

Chart: `docs/vision/PACING_CHART.md`

---

## 7. Production & development journey

### 7.1 Milestone timeline

| Stage | Status | Deliverable |
|-------|--------|-------------|
| **M0** | ✅ Done | GDD, storyboard, repo |
| **M0b** | ✅ Data written | i18n in `game/data/` + `translations.csv` |
| **M0c–M0h** | ✅ Done | Art, gameplay, narrative, QA specs |
| **M0e** | ✅ Done | Story JSON spine + validators |
| **Phase 0** | ✅ Done | Dev environment, docs CI, alignment audit |
| **Phases 1–6** | 🔲 Pending | Implementation on `game/development` |
| **M5 / Phase 7** | 🔲 Pending | Art rebuild (NPR zones, hero meshes) |
| **M6 / Phase 8** | 🔲 Pending | Steam export, compliance, Windows playtest |

**Build order authority:** `docs/workflow/IMPLEMENTATION_PLAN.md`  
**Checklist:** `docs/workflow/MILESTONES.md`

### 7.2 Spec-first architecture (ADR)

| Branch | Contents |
|--------|----------|
| **`main`** | Design docs + `game/data/` JSON only — no `project.godot`, no ship code |
| **`game/development`** | Godot implementation trunk until M6 ship |

**Rejected:** Long-lived `qa`/`uat`/`prod` branches, per-agent forks, GitFlow.  
**Adopted:** Dual trunk + short `cursor/*` feature branches + tag-based release promotion.

ADR: `docs/workflow/BRANCHING_DECISION_RECORD.md`

### 7.3 Implementation experiments (feature branches)

Parallel prototype branches explored different build approaches:

| Branch | Approach | Notes |
|--------|----------|-------|
| `cursor/japanese-environment-dc91` | Procedural `zone_visuals.gd` code pass | Village → cave → beach → palace polish |
| `cursor/gdai-regen-dc91` | GDAI MCP scene-authored rebuild | No GodotPrompter; no `ZoneVisuals` |
| `cursor/urashima-jrpg-scaffold-dc91` | Initial greybox scaffold | Movement, dialogue, combat stubs |
| Others | Narrative, audio, palace endings, assets | Isolated feature work |

**Comparison intent:** Code-driven environment vs. editor-driven GDAI regen — for GDAI evaluation, not merge to `main` until ship gate.

### 7.4 Tooling stack

| Tool | Role |
|------|------|
| GodotPrompter | Plan + write `.gd`, shaders, tests |
| GDAI MCP | Build scenes in editor (commercial plugin — dev only) |
| Godotiq | Debug signals, Output panel |
| ComfyUI / Material Maker | Zone NPR albedos (offline) |
| GameLab MCP | UI art frames, icon sheets |

GDAI setup: `docs/agents/GDAI_CLOUD_SETUP.md` (plugin gitignored; not in Steam builds)

### 7.5 Alignment audit (2026-07-17)

Pre-build docs scored **ALIGNED** on `main` — narrative, data, gameplay specs at 10/10; runtime proof pending implementation.

Report: `docs/compliance/alignment_audit_reports/20260717T102357Z_committed_history/report.md`

---

## 8. Combat & systems journey (story-relevant)

Combat is **punctuation**, not filler between movies.

| Fight | Story function |
|-------|----------------|
| SC-05 Salt Crab | Agency after dread |
| SC-08 Tide Wraiths | Guilt made physical |
| SC-09 Shore Wraith | Solo catharsis; Yuzu unlocks after |
| SC-14 Palace Sentinel | Yuzu Spirit weakness tutorial |
| SC-15 Tide Keeper | Phases map to ebb → surge → stillness; choice at 10% HP |

**Design:** Turn-based, speed-initiative, JSON-driven. No grind required on Normal. Boss intent UI telegraphs patterns.

Specs: `docs/gameplay/COMBAT_SYSTEMS.md`, `docs/gameplay/BOSS_DESIGNS.md`

---

## 9. Audio & presentation journey

| Layer | v1 decision |
|-------|-------------|
| Dialogue | Written text + portraits (4 locales) |
| VO | 12 selective emotional clips — not full script |
| Music | Zone BGM + boss themes + ending stings |
| SC-08 crowd | Whisper SFX bed — not 20 voice actors |
| SC-16 choice | Near-silence; `sting_choice_silence` |
| SC-17 Drift | Final seconds: surf only, no BGM |

Specs: `docs/audio/AUDIO_DIRECTION.md`, `docs/vision/VO_HIT_LIST.md`

---

## 10. Replay & meta journey

| Feature | Decision |
|---------|----------|
| Second run time | 1.5–2 h (prologue skip, knowledge) |
| Ending gallery | Unlocks after first completion; no spoilers before unlock |
| Hard mode | Mechanical mastery only — not secret fourth ending |
| Lore achievement | Optional `ACH_LORE_COMPLETE` — 8/8 entries |

Spec: `docs/vision/REPLAY_DESIGN.md`

---

## 11. How to add more background information — workflow

### 11.1 Before writing

1. Read this doc §5 consideration checklist  
2. Check scene exists or propose new scene ID in `STORYBOARD.md`  
3. Confirm fit within scope cuts (§3.2)  
4. Trace flag impact in `QUEST_AND_FLAGS.md`

### 11.2 Where to put content

| Content type | Location |
|--------------|----------|
| Main story dialogue | `game/data/dialogue/chapter_01.json` |
| Optional journal lore | `game/data/lore/lore_entries.json` + `lore_placements.json` |
| Scene metadata / flags | `game/data/story/scenes.json` |
| Quest objectives | `game/data/quests/main_quests.json` |
| Combat barks | `game/data/enemies/*.json` |
| Design rationale (prose) | `docs/vision/` — update relevant guide, not orphan notes |

### 11.3 After writing

```bash
python3 tools/validate_story_data.py
python3 tools/validate_narrative_density.py
bash tools/run_docs_ci_checks.sh
```

### 11.4 Red flags — escalate to scope review

- New named character with dialogue  
- New zone or dungeon  
- New ending or "true" route  
- Living villagers in hub  
- Full VO for a scene  
- Lore that contradicts box truth ladder  
- Morality scoring or ending recommendations in UI  

---

## 12. Document map (quick reference)

| Question | Read |
|----------|------|
| What is the game? | `docs/vision/GDD.md` |
| What happens scene by scene? | `docs/vision/STORYBOARD.md` |
| How should we write? | `docs/vision/NARRATIVE_WRITING_GUIDE.md` |
| How much text per scene? | `docs/vision/NARRATIVE_DENSITY.md` |
| What lore exists? | `docs/vision/LORE_AND_ENVIRONMENTAL_STORY.md` |
| How do endings work? | `docs/vision/ENDING_DESIGN.md` |
| What quests / flags? | `docs/world/QUEST_AND_FLAGS.md` |
| Zone layout? | `docs/world/WORLD_MAP_AND_FLOW.md`, `LEVEL_DESIGN.md` |
| What to build next? | `docs/workflow/IMPLEMENTATION_PLAN.md` |
| Branch / ship policy? | `docs/workflow/BRANCHING.md` |
| JSON data shapes? | `docs/technical/DATA_ARCHITECTURE.md` |

---

## 13. Changelog

| Date | Change |
|------|--------|
| 2026-07-17 | v1.0 — Initial project journey record compiled from M0 docs, ADR, alignment audit, and prototype branch history |
