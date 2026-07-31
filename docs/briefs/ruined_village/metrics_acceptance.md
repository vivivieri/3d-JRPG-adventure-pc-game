---
id: metrics-acceptance
type: reference
audience: [visual, builder]
phase: [1]
status: active
authority: briefs
tokens_est: 581
summary: "Metrics, camera, acceptance, forbidden"
---
# ruined_village brief — Metrics, camera, acceptance, forbidden

**Hub:** [`ruined_village.md`](../ruined_village.md)

## Hard metrics

| Constraint | Value |
|------------|-------|
| Materials visible at gameplay cam | ≤ **8** (`RENDERING_GUIDE.md` §11) |
| FPS target | 60 @ 1080p GTX 1060 |
| Toon shader family | Single ramp — no stray PBR glossy |
| Primitive placeholders | **Forbidden** in player-facing view |
| BGM | `bgm_village` |

---


## Camera beats

| Moment | Spec |
|--------|------|
| First enter (SC-02) | 4 s pan to torii silhouette (`CINEMATICS.md`) |
| Gameplay follow | Third-person; path readable; well in peripheral sightline from spawn approach |
| Establishing shot | Wide overcast — pier + submerged roofs in background fog |

---


## Acceptance evidence

- [ ] `WorldEnvironment` — Filmic/ACES tonemap, fog on, procedural overcast sky
- [ ] Directional `#B8C8D8` + warm fill at lantern/shack
- [ ] Main path ≥2 m wide; torii visible as vista from well–shack approach
- [ ] Well save interactable from path without compass
- [ ] Urashima walk cycle through hub — coat hem acceptable clip
- [ ] `artifacts/screenshots/phase1_ruined_village_gameplay.png` captured
- [ ] `artifacts/screenshots/phase1_ruined_village_establishing.png` captured (SC-02 pan)
- [ ] `python3 tools/check_screenshot_palette.py --zone ruined_village --screenshot ...` — PASS
- [ ] `L2_visual_jury` — PASS (2-of-3 when keys set)
- [ ] `L2_visual_palette` — PASS
- [ ] Golden master committed: `artifacts/golden/ruined_village_gameplay.png`
- [ ] No `BoxMesh` / greybox in player camera frustum
- [ ] GDAI `.gdai_built` marker with `verified_f5=true`

---


## Vertical slice minimum (ship Phase 1)

Build **in this order** (per `CHARACTER_BIBLE.md` §11 + `ENVIRONMENT_KITS.md` §4):

1. Ground + main path + fog/sky/lighting preset
2. `village_well_stone` + `VillageWell` marker
3. `village_torii_damaged` + `village_shrine_pad` + `ToriiShrine`
4. `village_shack_roku` + `RokuShack`
5. Urashima placed — walk cycle + interact at well
6. Gameplay + establishing screenshots → visual jury

Defer to M5: full modular kit scatter, banner/sandal inspect props, pier combat arena polish, cave entrance cliff dressing.

---


## Forbidden

- Kenney / European medieval kits
- Sunny gold sky or PhysicalSky HDRI
- Pure white point lights
- Hand-edited `.tscn` without GDAI MCP (R&R policy)
- Ship without golden screenshot when `VISUAL_SMOKE_STRICT=1`
