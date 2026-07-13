# Generation Readiness — Human-Expectation Gaps for AI 3D Pipelines

**Version:** 1.0  
**Authority:** Extends (does not replace) `CHARACTER_BIBLE.md`, `ENVIRONMENT_KITS.md`, `ART_AUTOMATION_PIPELINE.md`, `GAME_FEEL.md`, and `game/data/models/qa_catalog.json`.  
**Audience:** GodotPrompter, GDAI MCP, offline mesh/texture generators (Meshy, ComfyUI, Material Maker), QA agents  
**Cross-refs:** `docs/ACCEPTANCE_CRITERIA.md`, `docs/MODEL_QA.md`, `docs/VISUAL_QA.md`, `docs/PLAYTEST_SCRIPT.md` §7b

---

## 1. What this document is for

Existing specs are **strong at blocking bad output** (wrong palette, greybox, rogue code, unlicensed assets, animation name drift). They are **weaker at prescribing generative recipes** that reliably produce assets humans enjoy **in motion and in space**.

This addendum lists, per **character** and **zone**, what is:

| Status | Meaning |
|--------|---------|
| **✅ Specified** | Agent can generate without guessing; enforced by doc or CI gate |
| **⚠️ Partial** | High-level direction exists; generation still needs designer judgment |
| **❌ Missing** | Must be authored before expecting human-grade output |

**Rule:** Do not mark M5 art **ship-ready** for a row until **Required before ship** items are ✅ or explicitly waived in a PR with human L6 evidence.

**Polish governance:** Structured iteration and direction authority — `docs/MODEL_QA.md` §8–§9 (who sets on-direction vs who arbitrates feel).

---

## 2. Cross-cutting gaps (all assets)

These apply to every character and zone. Fill once, reference everywhere.

| Gap ID | Topic | Current spec | Required before autonomous ship gen | Suggested gate |
|--------|-------|--------------|-------------------------------------|----------------|
| **X-01** | **Generation brief** | Bible rows describe *what*; not *how* to prompt Meshy/ComfyUI | One-page brief per hero/zone: positive prompt, negative prompt, 2–3 reference mood words, forbidden shapes | `docs/generation_briefs/<id>.md` in repo |
| **X-02** | **Camera-distance readability** | Jury checks silhouette at turntable | Golden screenshot at **gameplay FOV** (ruined_village cam, 8 m) with min face/boss read | `artifacts/screenshots/<zone>_gameplay.png` + `L2_visual_jury` |
| **X-03** | **Motion timing** | Animation *names* whitelisted; not frame counts or cycle length | Per clip: duration (s), loop yes/no, root motion yes/no in `qa_catalog.json` | Extend `check_animation_whitelist.py` |
| **X-04** | **Spatial composition** | Zone ASCII layouts in `ENVIRONMENT_KITS.md` | Min path width, max props per 10×10 m, vista anchor positions | Zone composition smoke (future `L2_zone_composition`) |
| **X-05** | **Feel in motion** | `GAME_FEEL.md` + `feel_thresholds.json` | Input latency, turn p95, camera spring — measured in-engine | `L2_feel_smoke` strict on game branch |
| **X-06** | **Human validation** | L6 playtest + feel checklist | ≥5 testers, feel avg ≥3.5 — cannot be automated away | `L6_human_playtest` |

---

## 3. Generation brief template (copy per asset)

Create `docs/generation_briefs/<asset_id>.md` when starting M5 work on that asset.

```markdown
# Generation brief — <asset_id>

## Intent (one sentence)
<!-- e.g. "Weathered fisherman, adult 1:5, lacquer box readable at 8m" -->

## Tool chain
<!-- Meshy → Blender decimate → Mixamo → GLB | ComfyUI tileable wood -->

## Positive prompt anchors
- Style: stylized Japanese coastal NPR, muted, not Ghibli bright
- Silhouette: <!-- from CHARACTER_BIBLE / ENVIRONMENT_KITS -->
- Palette: <!-- hex anchors from ART_DIRECTION -->

## Emotional intent (jury + human rubric)

| Field | Value |
|-------|-------|
| Primary mood | <!-- e.g. quiet guilt, dread, awe --> |
| Secondary mood | <!-- nuance — not comedy, not horror gore --> |
| Audience read | Men 20–30 — melancholy coastal; beauty with decay |
| Static read (turntable / screenshot) | <!-- what still image must communicate --> |
| Motion feel (human L6 only) | <!-- walk weight, telegraph timing — not automated --> |
| Must avoid | <!-- comedy cheer, horror gore, bright Ghibli, European medieval --> |
| Story anchor | <!-- SC-XX scene reference --> |

## Negative prompt (required)
- chibi, anime eyes, PBR glossy, European medieval, Kenney, low-poly blockout

## Hard metrics (from qa_catalog.json)
- Tris: <!-- min–max -->
- Textures: <!-- min count -->
- Rig: mixamo_humanoid (if character)
- Animations required: <!-- from required_animations -->

## Acceptance evidence
- [ ] Turntable 4-view PNG
- [ ] Gameplay-distance screenshot
- [ ] L2_model_jury PASS (heroes/bosses)
- [ ] L2_visual_jury PASS (in-zone placement)
```

---

## 4. Character rows (`qa_catalog.json`)

Legend: ✅ / ⚠️ / ❌ as above.

### Phase 1 — Vertical slice

| ID | ✅ Specified today | ⚠️ Partial | ❌ Missing (add before ship) | Phase |
|----|-------------------|------------|---------------------------|-------|
| **urashima** | Silhouette, layers, box states, tri budget, rig attachments, `required_animations` floor, **generation brief** | Coat wind bones, portrait match | Walk cycle **duration** validation in CI; gameplay-cam face read golden shot | 1 |
| **village_torii_damaged** | Set-piece role, zone palette, tri budget, **generation brief** | Splinter detail in-engine | Golden in-scene screenshot at torii interact | 1 |
| **village_well_stone** | Prop role, save marker linkage, **generation brief** | Weathering variation | Interact highlight golden shot | 1 |
| **village_shack_roku** | Set-piece ID, hub layout, **generation brief** | Interior clutter | SC-04 emerge F5 verify | 1 |

### Phase M5 — Party & enemies

| ID | ✅ Specified today | ⚠️ Partial | ❌ Missing (add before ship) | Phase |
|----|-------------------|------------|---------------------------|-------|
| **yuzu** | Spirit lower-body material rule, anim list, portrait framing, **generation brief** | Float walk polish | `materialize` duration in CI | M5 |
| **roku** | Harpoon strap, anim list, **generation brief** | Taunt/guard polish | Harpoon drawn mesh variant QA | M5 |
| **salt_crab** | Enemy anim contract, **generation brief** | Pier arena dressing | Tutorial intent UI timing verify | M5 |
| **tide_wraith** | Standard enemy kit, **generation brief** | Particle drip polish | Z-fight smoke in caves | M5 |
| **shore_wraith** | Boss anims, BOSS_DESIGNS kit, **generation brief** | Phase transition VFX | Boss arena golden shot | M5 |
| **palace_sentinel** | Stats/skills, **generation brief** | Full bible row depth | 12 m hall scale golden shot | M5 |
| **tide_keeper_p1** | Phase materials, anim list, **generation brief** | P2/P3 GLB ship | Numerals unreadable jury check | M5 |
| **palace_gate_main** | Set-piece in hero_jury, **generation brief** | Pearl socket tune | SC-12 vertigo golden shot | M5 |
| **lacquer_box** | Item guide, glow states, **generation brief** | Ground prop SC-01 | 3-state emission screenshot | M5 |

### Characters not yet in `qa_catalog.json`

| ID | Action |
|----|--------|
| `otohime` (bust) | Add catalog row + bible § when palace dialogue ships |
| `villager_spirit`, `rebuilder` | Silhouette-only — document as **low-poly crowd**, not hero jury scope |

---

## 5. Zone rows (`ENVIRONMENT_KITS.md`)

| Zone ID | ✅ Specified today | ⚠️ Partial | ❌ Missing (add before ship) | Build phase |
|---------|-------------------|------------|---------------------------|-------------|
| **beach_shore** (SC-01) | Mood, palette, kit table, spawn path, **generation brief** | Water foam polish | Golden screenshot capture | 2 |
| **ruined_village** (SC-02 hub) | Full kit + layout + lighting + **generation brief** | Pier submerge depth | Golden screenshot + `L2_visual_jury` PASS | **1** |
| **tidal_caves** (SC-06–10) | Biolume palette, modular kit, **generation brief** | Face decal polish | Puzzle state screenshots | 5 |
| **dragon_palace_gate** (SC-12+) | Palace void sky, gold trim, **generation brief** | Mirror chamber polish | SC-12 vertigo golden shot | 6 |

### Per-zone composition contract (to add to `ENVIRONMENT_KITS.md` or `game/data/qa/zone_composition.json`)

| Field | Example (`ruined_village`) | Why humans care |
|-------|---------------------------|-----------------|
| `min_path_width_m` | 2.0 | No stuck on geometry |
| `max_props_per_100m2` | 12 | Clutter vs clarity |
| `vista_anchor` | Torii at end of main path | Direction without UI compass |
| `gameplay_cam_height_m` | 1.6 | Validates door/well scale |
| `golden_screenshot` | `artifacts/screenshots/phase1_ruined_village_gameplay.png` | Visual regression |

---

## 6. Pipeline checklist (agent order)

For each new hero mesh or zone slice:

```
1. READ   CHARACTER_BIBLE / ENVIRONMENT_KITS row + ART_DIRECTION palette
2. WRITE  docs/generation_briefs/<id>.md (§3 template)
3. GEN    Meshy/ComfyUI/Material Maker per ART_AUTOMATION_PIPELINE.md
4. POST   palette_remap.py → register_asset.py
5. IMPORT bash tools/install_glb_import_pipeline.sh (characters/props)
6. MEASURE  python3 tools/check_model_technical.py --model <id>
7. MEASURE  python3 tools/check_animation_whitelist.py --phase m5 --strict
8. PLACE  GDAI MCP in zone — gameplay screenshot
9. JURY   L2_model_jury + L2_visual_jury (when keys exist)
10. HUMAN L6 feel checklist — only after L5 green
```

---

## 7. What “ready for generation” means per milestone

| Milestone | Characters | Zones | Human expectation |
|-----------|------------|-------|-------------------|
| **Phase 1 slice** | `urashima` + village set-pieces briefs | `ruined_village` brief | Golden shots pending capture |
| **Phase 4** | Party + salt crab briefs ✅ | `beach_shore` brief ✅ | Combat read at 6 m |
| **M5 ship** | All `m5` catalog rows have briefs ✅ | All player zones briefed ✅ | L2 juries + L6 feel ≥3.5 |
| **M6 Steam** | Portrait parity with field model | No greybox in any player scene | L6 ≥80% complete |

---

## 8. Recommended next docs/data (priority)

| Priority | Deliverable | Owner | Status |
|----------|-------------|-------|--------|
| P0 | All `qa_catalog.json` + player-zone briefs | Architect + Visual | ✅ Done (17 briefs) |
| P0 | Golden screenshot path enforced (`VISUAL_SMOKE_STRICT=1` on M5) | QA | Pending capture |
| P1 | `game/data/qa/zone_composition.json` — machine-readable §5 table | Architect | Pending |
| P1 | `animation_timing` block in `qa_catalog.json` (duration_ms, loop) | Architect | Pending |
| P2 | Expand `palace_sentinel` CHARACTER_BIBLE row to boss standard | PM + Visual | Pending |
| P2 | `L2_zone_composition` smoke script | QA | Pending |

---

## 9. Cross-refs

| Need | Doc |
|------|-----|
| What to build | `IMPLEMENTATION_PLAN.md` |
| How assets are generated | `ART_AUTOMATION_PIPELINE.md` |
| Character look | `CHARACTER_BIBLE.md` |
| Generation briefs | `generation_briefs/` |
| Zone modules | `ENVIRONMENT_KITS.md` |
| Measurable pass/fail | `ACCEPTANCE_CRITERIA.md` |
| Model polish cadence + direction authority | `MODEL_QA.md` §8–§9 |
| Feel targets | `GAME_FEEL.md`, `game/data/qa/feel_thresholds.json` |
| Human playtest | `PLAYTEST_SCRIPT.md` §7b |
