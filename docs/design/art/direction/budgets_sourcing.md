---
id: budgets-sourcing
type: reference
audience: [visual, builder]
phase: [1, 5]
status: active
authority: art
tokens_est: 481
summary: "Poly budgets & asset sourcing"
---
# Art Direction — Poly budgets & asset sourcing

**Hub:** [`ART_DIRECTION.md`](../ART_DIRECTION.md)

## 5. Poly budgets

| Asset | Tris (target) |
|-------|---------------|
| Urashima (hero) | 12k–18k |
| Party members | 10k–15k each |
| Standard enemy | 5k–10k |
| Boss | 25k–40k |
| Environment module | 500–3k |
| Handheld item / pickup | 200–1.2k |
| Equipped weapon | 800–2.5k |
| Key story prop (lacquer box) | 1k–3k |
| Hero set-piece (torii, gate) | 8k–20k |

---


## 6. Asset sourcing plan (automated)

**Priority:** AI-generated heroes + set-pieces; curated CC0 Japanese-environment packs for modular fill. **No commission or hand-paint ship path.**

| Need | Approach | License |
|------|----------|---------|
| Characters (Urashima, Yuzu, Roku, bosses) | **Meshy / Tripo / Rodin** + Mixamo rig | Service ToS + register |
| Japanese ruins / coastal kits | Curated packs (itch.io, Sketchfab CC0) + AI trim | CC0 / documented |
| Rocks, cliffs (shared) | Poly Haven + toon shader | CC0 |
| Zone textures | **ComfyUI** or **Material Maker** + `palette_remap.py` | Workflow output |
| UI frames / icons | **GameLab MCP** or ComfyUI UI workflow | Per tool ToS |
| Animations | Mixamo (humanoid rig) | Mixamo ToS |
| UI icons (fallback) | Procedural / GameLab ink-wash | CC0 / own |
| SFX | Freesound (filter CC0) + procedural | CC0 |
| Music | **ACE-Step 1.5** curated prompts | MIT (ACE-Step) |

**Deprecated for ship builds (M5):** Kenney Castle kit (European read), Quaternius as final character base, procedural primitive placeholders. Kenney Nature may remain only if art-reviewed — see `docs/design/art/LICENSES.md` §Kenney (dev greybox only).

**Rule:** Log every download in `docs/design/art/LICENSES.md` before import. **Run `bash tools/check_asset_compliance.sh` before commit.**

**Copyright policy:** Only ship-safe licenses (CC0, MIT, OFL, public domain, documented AI service ToS). **Banned:** all-rights-reserved, CC-BY-NC, CC-BY-SA, unknown sources. Full list: `docs/design/art/ASSET_COMPLIANCE.md`.

---
