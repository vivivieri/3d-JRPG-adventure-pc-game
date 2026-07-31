---
id: purpose-gaps-brief
type: reference
audience: [visual, builder]
phase: [1, 5]
status: active
authority: art
tokens_est: 946
summary: "Purpose, cross-cutting gaps, brief template"
---
# Generation Readiness — Purpose, cross-cutting gaps, brief template

**Hub:** [`GENERATION_READINESS.md`](../GENERATION_READINESS.md)

## When to read

Use **Generation Readiness — Purpose, cross-cutting gaps, brief template** (roles: visual, builder) when you need this reference during the current task Jump to a section below instead of reading end-to-end (3 sections).

## Jump to

- [1. What this document is for](#1-what-this-document-is-for)
- [2. Cross-cutting gaps (all assets)](#2-cross-cutting-gaps-all-assets)
- [3. Generation brief template (copy per asset)](#3-generation-brief-template-copy-per-asset)


## 1. What this document is for

Existing specs are **strong at blocking bad output** (wrong palette, greybox, rogue code, unlicensed assets, animation name drift). They are **weaker at prescribing generative recipes** that reliably produce assets humans enjoy **in motion and in space**.

This addendum lists, per **character** and **zone**, what is:

| Status | Meaning |
|--------|---------|
| **✅ Specified** | Agent can generate without guessing; enforced by doc or CI gate |
| **⚠️ Partial** | High-level direction exists; generation still needs designer judgment |
| **❌ Missing** | Must be authored before expecting human-grade output |

**Rule:** Do not mark M5 art **ship-ready** for a row until **Required before ship** items are ✅ or explicitly waived in a PR with human L6 evidence.

**Polish governance:** Structured iteration and direction authority — `docs/design/art/MODEL_QA.md` §8–§9 (who sets on-direction vs who arbitrates feel).

---


## 2. Cross-cutting gaps (all assets)

These apply to every character and zone. Fill once, reference everywhere.

| Gap ID | Topic | Current spec | Required before autonomous ship gen | Suggested gate |
|--------|-------|--------------|-------------------------------------|----------------|
| **X-01** | **Generation brief** | Bible rows describe *what*; not *how* to prompt Meshy/ComfyUI | One-page brief per hero/zone: positive prompt, negative prompt, 2–3 reference mood words, forbidden shapes | `docs/briefs/<id>.md` in repo |
| **X-02** | **Camera-distance readability** | Jury checks silhouette at turntable | Golden screenshot at **gameplay FOV** (ruined_village cam, 8 m) with min face/boss read | `artifacts/screenshots/<zone>_gameplay.png` + `L2_visual_jury` |
| **X-03** | **Motion timing** | Animation *names* whitelisted; duration/loop/root motion in `qa_catalog.json` | Per clip: `animation_timing` validated L0; GLB duration when `--check-timing` | `validate_qa_catalog.py` + `check_animation_whitelist.py --check-timing` |
| **X-04** | **Spatial composition** | Zone ASCII layouts in `ENVIRONMENT_KITS.md` | `zone_composition.json` — min path width, vista anchor, golden paths | `validate_zone_composition.py` (L0); in-scene `run_zone_composition_checks.sh` (P2) |
| **X-05** | **Feel in motion** | `GAME_FEEL.md` + `feel_thresholds.json` | Input latency, turn p95, camera spring — measured in-engine | `L2_feel_smoke` strict on game branch |
| **X-06** | **Human validation** | L6 playtest + feel checklist | ≥5 testers, feel avg ≥3.5 — cannot be automated away | `L6_human_playtest` |
| **X-07** | **Audio generation brief** | ACE-Step prompts in `ace_step_prompts.json` | Per hero track + P0 VO: emotional intent, loudness/loop in `audio_qa_catalog.json` | `validate_audio_qa_catalog.py` + BGM A6/A7 + VO V6/V7 jury |
| **X-08** | **Scene audio map** | Prose in `AUDIO_PRODUCTION_GUIDE.md` §4 | Zone/scene → BGM, amb, sting, duck rules machine-readable | `scene_audio_map.json` + `validate_scene_audio_map.py` |

---


## 3. Generation brief template (copy per asset)

Create `docs/briefs/<asset_id>.md` when starting M5 work on that asset.

```markdown
# Generation brief — <asset_id>
