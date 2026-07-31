---
id: rule-licenses
type: reference
phase: [1, 5]
audience: [visual, builder, release]
status: active
authority: art
tokens_est: 620
summary: "Golden rule, allowed, banned"
---
# Asset Compliance — Golden rule, allowed, banned

**Hub:** [`ASSET_COMPLIANCE.md`](../ASSET_COMPLIANCE.md)

## 1. Golden rule

> **Every file used in the shipped game must be copyright-safe for commercial PC release.**

That means you must have a **documented permissive license** or **documented AI service ToS** that allows commercial use and redistribution. Production is **fully automated** — no human artist commission path (`docs/design/art/ART_AUTOMATION_PIPELINE.md`).

**If you cannot prove the license, do not import the file.**

---


## 2. Allowed licenses (ship-safe)

| License | Commercial OK | Redistribution OK | Attribution | Notes |
|---------|---------------|-------------------|-------------|-------|
| **Public Domain** | ✓ | ✓ | No | Folklore, expired works |
| **CC0 1.0** | ✓ | ✓ | Appreciated | Poly Haven, Kenney |
| **MIT** | ✓ | ✓ | Yes | Godot, repo code, procedural tools |
| **Apache 2.0** | ✓ | ✓ | Yes | Some plugins |
| **BSD 2/3-Clause** | ✓ | ✓ | Yes | |
| **SIL OFL 1.1** | ✓ | ✓ | Yes | Noto fonts — no sold-by-itself |
| **CC-BY 4.0** | ✓ | ✓ | **Required** | Log author + credit screen |
| **AI-generated (documented ToS)** | ✓ | ✓ | Per service | Meshy, GameLab, ACE-Step, ElevenLabs — register in `LICENSES.md` |
| **Original / repo procedural** | ✓ | ✓ | Optional | `tools/generate_*` scripts |

---


## 3. Banned / not allowed without legal review

| Category | Examples | Why |
|----------|----------|-----|
| **All Rights Reserved** | Random Google images, Pinterest, ArtStation downloads | No redistribution right |
| **CC-BY-NC** | Many Freesound / OGA tracks | Non-commercial only |
| **CC-BY-NC-SA** | Sketchfab NC models | NC + SA |
| **CC-BY-SA** | Wikipedia SA photos | Share-alike infects project |
| **Editorial only** | Stock photo editorial licenses | Not for games |
| **Unity/Unreal Asset Store default** | Unless license explicitly allows standalone game | Usually restricted |
| **Anime / franchise IP** | Ghibli style traces, named characters | Trademark/copyright |
| **Mixamo** | ✓ Allowed with [Adobe terms](https://www.adobe.com/legal/terms.html) | Must comply with ToS; document in manifest |
| **AI-generated from copyrighted datasets** | Unclear training data | Avoid for ship without legal sign-off |

**When in doubt, reject the asset.**

---
