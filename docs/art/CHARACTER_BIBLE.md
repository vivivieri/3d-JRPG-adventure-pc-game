# Tides of Urashima — Character Bible

**Version:** 1.2 (Pre-build)  
**Visual target:** High-detail stylized Japanese — automated stylized albedo, readable silhouettes, no primitive placeholders in ship builds.  
**Cross-refs:** `docs/art/ART_DIRECTION.md`, `docs/vision/STORYBOARD.md`, `docs/gameplay/BOSS_DESIGNS.md`, `docs/art/ITEMS_3D_MODEL_GUIDE.md`

---

## 1. Global character rules

| Rule | Detail |
|------|--------|
| Proportions | Head-to-body **1:5** (adult, not chibi) |
| Poly budget (field) | Hero 12k–18k tris; party 10k–15k; standard enemy 5k–10k; boss 25k–40k |
| Materials | One toon ramp shader family; spirits use additive/alpha on lower body |
| Rig | Humanoid (Mixamo-compatible); 1 skin per character |
| Animations | See §8 master list; no T-pose in shipped scenes |
| Portraits | Painted bust 512×512 min; match field model face/hair |
| Naming | File prefix = character id (`urashima`, `yuzu`, `roku`, etc.) |

**Ship rule:** No `CapsuleMesh`, `BoxMesh`, or Kenney knight placeholders in player-facing builds.

### Model sheet template

Every character and boss requires an orthographic model sheet before modeling. Full template and required fields: `docs/art/ITEMS_3D_MODEL_GUIDE.md` §2. Store sheets in `docs/model_sheets/<character_id>.png` (design-time only).

### Rig attachment points

| Empty name | Parent bone | Used by |
|------------|-------------|---------|
| `attach_weapon_r` | `RightHand` | Urashima weapons; Yuzu spirit knife |
| `attach_back_prop` | `Spine2` | Roku harpoon (stowed) |
| `attach_box_hip_l` | `Hips` | Urashima lacquer box |
| `attach_charm_head` | `Head` | Yuzu fox bell (part of hair mesh v1) |

Weapon parenting, combat offsets, and per-item mesh paths: `docs/art/ITEMS_3D_MODEL_GUIDE.md` §3–4.

### Character LOD (field only)

Combat uses full-detail mesh. Field exploration may swap LODs for performance.

| LOD | Tris (hero) | Tris (party) | Tris (enemy) | When |
|-----|-------------|--------------|--------------|------|
| LOD0 | 12k–18k | 10k–15k | 5k–10k | Player within 15 m |
| LOD1 | 6k–9k | 5k–8k | 3k–5k | 15–30 m |
| LOD2 | 2k–4k | 2k–3k | 1k–2k | 30 m+ or off-screen |

- **Bosses:** LOD0 only in boss arenas (no swap during fight).
- **Followers:** Yuzu/Roku use LOD1 beyond 10 m from camera.
- **Blend:** 0.2 s cross-fade; no pop on swap.
- **Portraits / combat:** Always LOD0 source mesh.

---

## 2. Urashima Tarō (protagonist)

**ID:** `urashima`  
**Role:** Balanced fighter / party leader  
**Element:** Water  
**Arc:** Escapist → accountable (posture straightens across acts)

### Silhouette

- Long **dark indigo coat** (`#2A3A4A`) over cream fisherman tunic
- **Straw sandals**, rolled trousers, rope belt
- **Lacquer box** on left hip — always visible; glow state varies by zone
- Slightly hunched in Act I → upright by SC-15

### Costume layers (model order)

1. Body + face (weathered, late 20s read)
2. Tunic + trousers (cream `#D8C8A8`, salt stains)
3. Coat (open front, wind-reactive hem — 2 bone chains max)
4. Obi + rope belt
5. Sandals
6. Lacquer box (separate mesh for glow swap)

### Lacquer box states

| State | When | VFX |
|-------|------|-----|
| Dormant | Hub, caves | Faint red seam glow `#8B2A3A` at 15% |
| Awakened | Palace zones | Pulse 40–60%, particle motes |
| Choice | SC-16 | Full bloom, UI sync, screen rim light |

### Colors

| Part | Hex |
|------|-----|
| Coat | `#2A3A4A` |
| Tunic | `#D8C8A8` |
| Skin | `#C8A888` |
| Hair | `#1A1A1A` (tied back) |
| Box lacquer | `#6B1A1A` + gold clasp `#C8A040` |

### Field vs combat

- **Field:** Third-person follow; coat hem clips minimally
- **Combat:** Static battle pose + attack anim; box visible on hip in UI portrait

### Key scenes

| Scene | Presentation |
|-------|----------------|
| SC-01 | Clutching box, exhausted walk |
| SC-13 | Mirror shows young + old Urashima |
| SC-16 | Close-up; box glow; choice UI |
| SC-17a/b/c | Ending-specific pose (dissolve / stand / row) |

### Voice tone (writing ref)

Quiet guilt; short sentences in Act I; firm declarations in Act III.

---

## 3. Yuzu (shrine maiden spirit)

**ID:** `yuzu`  
**Role:** Healer / buffer  
**Element:** Spirit  
**Unlock:** SC-10 (after Shore Wraith)

### Silhouette

- **Miko hakama** — white haori, red hakama (`#8B2A3A`)
- **Twin braids** with **fox bell** (`kitsune-suzu`) on left braid
- **Semi-transparent** legs/feet — spirit tether to ground
- Torn hem on hakama (right side)

### Spirit treatment

- Lower body alpha 40–55% with soft noise scroll
- Foot contact: faint cyan `#4AE8D8` ripple decal, no footprints
- Materialize VFX (SC-10): torii shard particles → fade in over 2s

### Colors

| Part | Hex |
|------|-----|
| Haori | `#F0ECE4` (aged) |
| Hakama | `#8B2A3A` |
| Hair | `#1A1410` |
| Bell | `#D4A55A` |
| Spirit glow | `#6EC8C0` |

### Field presence

- Joins party SC-10 (`yuzu_joined`); field follower from SC-10 onward (2m behind Urashima, no collision)
- Idle: hands clasped; occasional bell chime SFX

### Combat read

Small, upright; heal cast = hands raised, light pillar; purify = bell shake + wave

---

## 4. Roku (old diver)

**ID:** `roku`  
**Role:** Tank / debuffer  
**Element:** Physical  
**Unlock:** SC-04 (shack); confirms party SC-12 if missed

### Silhouette

- **Bulky patched dive suit** — canvas `#5C5A48`, rubber seals `#2A2A2A`
- **Harpoon** strapped across back (hero prop mesh)
- **Wide stance**, slightly bowed legs
- Weathered face, white stubble, missing left glove finger

### Colors

| Part | Hex |
|------|-----|
| Suit | `#5C5A48` |
| Patches | `#7A6A52` |
| Harpoon wood | `#4A3A2A` |
| Harpoon metal | `#6A6A6A` |

### Field presence

- SC-04: emerges from shack interior trigger
- SC-04–12: stays near shack; becomes field follower when `roku_combat_active` is set (SC-12)
- Shop UI: same model in window silhouette or portrait only (performance)

### Combat read

Taunt = harpoon planted, roar anim; Shell Guard = crouch behind folded arms

---

## 5. Otohime (NPC — flashback / glimpse)

**ID:** `otohime`  
**Role:** Moral mirror; not playable  
**Appearances:** SC-11 (flashback), SC-17c (underwater glimpse — no dialogue)

**Cross-refs:** `docs/vision/NARRATIVE_WRITING_GUIDE.md` §Otohime, `docs/ui/CINEMATICS.md` SC-11, `docs/generation_briefs/otohime.md`

### Design direction

- **Too perfect** — porcelain skin, no flaws, symmetrical; uncanny stillness (not fanservice)
- **Ryūgū-jō court dress** — layered kimono, coral gold trim, elongated sleeves
- Face **partially shadowed** in flashback; never full idle in field
- SC-17c: submerged silhouette only — palace tempts again; no VO

### Silhouette

- Tall, elongated sleeves; **kanzashi** ornament reads as breaking wave
- Ship mesh: **bust only** (chest-up) — sufficient for mirror chamber + flashback letterbox

| Spec | Detail |
|------|--------|
| **Height (bust)** | ~0.65 m mesh (implies ~1.75 m full figure scale) |
| **Silhouette** | Symmetrical collar; sleeves frame face; half-face in shadow |
| **Tris** | ~3k–6k (bust); no locomotion rig |
| **Mesh breakdown** | (1) Face + hair + kanzashi 1.5k; (2) Kimono collar + sleeve sculpt 1.5k–3k — folds baked, no cloth sim |
| **Palette** | Skin porcelain `#F0E8E0`; kimono coral `#C87068`; gold trim `#D4A55A`; shadow `#1A1A2A` on obscured half |
| **Materials** | Skin slightly glossy (unsettling); kimono matte NPR toon — **not** bright Ghibli |
| **VFX** | SC-11: restrained trim bloom; SC-17c: underwater caustic pass, desaturated |
| **Animations** | None required v1; optional `idle_still` 4s loop (hands folded) for flashback hold |
| **GLB** | `game/assets/models/npcs/otohime/otohime_bust.glb` |
| **Portrait** | `portraits/otohime.png` — 512×512 shadowed half-face (`portraits/otohime_ethereal` variant for SC-11 UI) |

### Voice tone (writing ref)

Seductive stillness; short lines; no villain monologue. See `VO_HIT_LIST.md` `sc11_otohime_01`.

---

## 6. Enemies (field + combat models)

### Salt Crab (`salt_crab`)

| Field | Detail |
|-------|--------|
| Silhouette | Low, wide; one oversized claw |
| Tris | ~6k |
| Read | Barnacles on shell; wet sheen |
| Palette | `#4A5A52` shell, `#8B3A2A` rust spots |

**Combat:** Sideways scuttle idle; claw snap attack

---

### Tide Wraith (`tide_wraith`)

| Field | Detail |
|-------|--------|
| Silhouette | Tall, dripping, **no legs** — taper to mist |
| Tris | ~8k |
| Read | Featureless smooth "face"; water drip particles |
| Palette | `#3A5A6A` body, `#4AE8D8` drip highlights |

**Combat:** Float idle; lunge with arm extension

---

### Shore Wraith (`shore_wraith`) — BOSS

**Combat design:** `docs/gameplay/BOSS_DESIGNS.md` §2.

| Spec | Detail |
|------|--------|
| **Height** | ~4.0 m (colossal; camera looks up in arena) |
| **Silhouette** | Draped monolith; no legs; cloth pools at base |
| **Tris** | ~32k (LOD0); LOD1 ~15k for intro cinematic wide shot |
| **Mesh breakdown** | (1) Outer drape 18k — sculpted folds, no cloth sim; (2) Inner face cluster 6k — 5–7 embedded villager faces; (3) Arm tendrils 4k; (4) Base mist cards 4k |
| **Palette** | Drape `#2A3A4A`; wet highlights `#4AE8D8`; faces `#C8A888` desaturated |
| **Materials** | Matte cloth toon; faces slightly glossy (unsettling); additive drip particles |
| **VFX** | Water drip particles from hem; phase 2 whisper overlay on faces |
| **Animations** | `idle_float`, `drowned_grasp`, `regret_aura`, `heavy_slam`, `phase_transition`, `summon_wraith`, `death_collapse` |
| **Intro** | Emerges from pool — 5s; mesh rises from water plane with alpha fade on lower drape |
| **GLB** | `game/assets/models/enemies/shore_wraith/shore_wraith.glb` |
| **Portrait** | 512×512 — draped form + single visible face |

---

### Palace Sentinel (`palace_sentinel`) — MINIBOSS

**Combat design:** `docs/gameplay/BOSS_DESIGNS.md` §3.

| Spec | Detail |
|------|--------|
| **Height** | ~2.5 m (tall guard; spear+shield read at **12 m** down `palace_sentinel_hall`) |
| **Silhouette** | Angular ryūgū lacquer plates; **tower shield + spear**; single horizontal gold eye slit (only face read) |
| **Tris** | ~22k LOD0; LOD1 ~11k for intro wide shot |
| **Mesh breakdown** | (1) Torso + leg armor 10k — lacquer plates, void gaps between segments; (2) Tower shield 5k — flat profile, gold rim; (3) Spear 2k; (4) Helmet 3k — horizontal slit, emissive eye; (5) Pauldrons/greaves 2k |
| **Palette** | Lacquer `#8B2A3A`; gold trim `#D4A55A`; void gaps `#1A1A2A`; eye slit emissive `#FFD890` at ~35% intensity |
| **Materials** | Matte lacquer toon ramp; gold trim stepped highlight; **no** European plate mail, no gloss PBR chrome |
| **Weakness** | Spirit ×1.5 (`spirit_weakness` in data) — Yuzu `purify` VFX must contrast lacquer red |
| **VFX** | Eye slit pulse on `shell_harden`; single-frame spear glint on thrust — no heavy particles |
| **Animations** | `idle`, `spear_thrust`, `shell_harden`, `hit`, `death` |
| **Intro** | 3s march from hall depth (`BOSS_DESIGNS.md` §7) |
| **Arena** | `palace_sentinel_hall` — SC-14; save shrine exterior marker `palace_sentinel_hall` |
| **GLB** | `game/assets/models/enemies/palace_sentinel/palace_sentinel.glb` |
| **Portrait** | 512×512 — helmet + slit eye; shield rim visible |

**Combat:** Shield block stance; spear thrust telegraph ≥0.3 s; weak to Spirit (Yuzu)

---

### Tide Keeper (`tide_keeper`) — FINAL BOSS

**Combat design:** `docs/gameplay/BOSS_DESIGNS.md` §4.

| Spec | Detail |
|------|--------|
| **Height** | Phase 1–2: ~3.2 m; Phase 3: ~1.8 m (shrinks to human scale) |
| **Silhouette** | Humanoid water form; blurred clock numerals in cloak volume |
| **Tris** | ~38k LOD0 (phase 1 body); phase 2 cloak swap +8k; phase 3 mesh swap 18k |
| **Mesh breakdown** | (1) Core body 12k — translucent water shell; (2) Cloak volume 20k — sculpted wave + embedded numeral cards (blurred, not readable); (3) Crown/head 6k |
| **Palette** | Body `#1A4A5A` → `#4AE8D8` edge; cloak `#1A1A3A`; numerals `#D4A55A` at 30% opacity |
| **Phase materials** | P1: calm ripple scroll; P2: faster flow + higher emissive; P3: muted, more opaque, tragic stillness |
| **VFX** | Flowing UV scroll on body; Maelstrom phase = cloak mesh scale pulse |
| **Animations** | `idle_drift`, `tidal_fingers`, `borrowed_moment`, `gentle_pull`, `maelstrom`, `ebb_remembrance`, `phase_transition` ×2, `last_mercy`, `death_dissolve` |
| **Choice gate** | At 10% HP combat pauses; mesh holds idle_drift; UI overlay only |
| **GLB** | `game/assets/models/enemies/tide_keeper/tide_keeper_p1.glb`, `tide_keeper_p2.glb`, `tide_keeper_p3.glb` |
| **Portrait** | 768×768 — phase 1 hero; UI may swap to p3 for choice moment |

---

## 7. NPC / ambient (silhouettes & crowd)

**Scope:** Low-poly crowd and ambient life — **excluded** from `hero_jury` and `L2_model_jury`. Zone composition counts apply (`zone_composition.json` max props). See `game/data/models/qa_catalog.json` `category: crowd`.

| ID | Usage | Model level |
|----|-------|-------------|
| `villager_spirit` | SC-17a Rewind festival crowd | 2 silhouette variants, instanced 8–12× |
| `rebuilder` | SC-17b Anchor shore rebuild | 3 tool poses, placed once each |
| `village_cat` | Hub ambient | Small organic mesh, not sphere |
| `village_dog` | Hub ambient | Small organic mesh, not sphere |

### Villager spirit (`villager_spirit`) — ending crowd

**Usage:** SC-17a (`ending_rewind`) — restored village festival; crane-up crowd shot.  
**Kit hook:** `village_crowd_silhouettes` in `ENVIRONMENT_KITS.md` §7.

| Spec | Detail |
|------|--------|
| **Variants** | 2 sub-meshes in one GLB: `lantern_bearer` (chochin prop), `festival_goer` (hands clasped, head bowed) |
| **Instances** | 8–12 placed in scene; no faces — hood/shadow read only |
| **Tris** | 400–800 **per instance** |
| **Silhouette** | Edo coastal festival dress; post-and-beam silhouette; **no** European peasant dress |
| **Palette** | Lantern warm `#D4A880`; clothing `#5C4A3A`; nobori accent `#8B2A3A` / white |
| **Materials** | Flat toon ramp; lower detail than hero NPCs — readable in warm sunset crowd |
| **Animations** | Optional `idle_sway` 3s loop; no root motion |
| **GLB** | `game/assets/models/npcs/crowd/villager_spirit.glb` |
| **LOD** | Single LOD; cull beyond 40 m in ending cinematic |

**Ship rule:** Instances are **silhouettes** — no individual facial geometry or hero jury.

---

### Rebuilder (`rebuilder`) — ending shore

**Usage:** SC-17b (`ending_anchor`) — dawn shore; three figures rebuild with Roku sapling beat.  
**Kit hook:** `rebuilder_figures` in `ENVIRONMENT_KITS.md` §7.

| Spec | Detail |
|------|--------|
| **Variants** | 3 sub-meshes in one GLB: `hoe` (working soil), `rope_pull` (hauling timber), `timber_carry` (shoulder beam) |
| **Instances** | Exactly **3** placed figures + Roku sapling prop separate |
| **Tris** | 600–1,000 per figure |
| **Silhouette** | Coastal laborer — wide stance, tool readable at 15 m |
| **Palette** | Work clothes `#5C5A48`; wood `#4A3A2A`; dawn rim `#E8C8A0` |
| **Materials** | Matte NPR; tools slightly higher roughness than cloth |
| **Animations** | Optional slow `work_loop` 4s per variant; static pose acceptable for cinematic |
| **GLB** | `game/assets/models/npcs/crowd/rebuilder.glb` |
| **Placement** | Near `prop_sapling_new`; Urashima on driftwood mid-ground |

**Ship rule:** Three distinct tool reads at gameplay camera — not interchangeable capsules.

---

### Village cat / dog (`village_cat`, `village_dog`)

| Field | Detail |
|-------|--------|
| Tris | 300–600 each |
| Usage | Ruined village hub ambient; optional idle anim |
| GLB | `game/assets/models/npcs/ambient/village_cat.glb`, `village_dog.glb` |
| Jury | Excluded from hero jury — ambient only |

---

## 8. Master animation list

**CI whitelist:** Rigged GLB clips must satisfy `required_animations` ⊆ found ⊆ `allowed_animations` in `game/data/models/qa_catalog.json`. Enforced by `L2_animation_whitelist` (`check_animation_whitelist.py --phase m5 --strict`). Update the catalog when adding Mixamo clips.

### Urashima

| Anim | Loop | Priority |
|------|------|----------|
| `idle` | Yes | P0 |
| `walk` | Yes | P0 |
| `run` | Yes | P1 |
| `interact` | No | P0 |
| `attack_light` | No | P0 |
| `attack_heavy` | No | P0 |
| `skill_cast` | No | P0 |
| `hit` | No | P0 |
| `defeat` | No | P1 |
| `ending_dissolve` | No | P1 |
| `ending_stand` | Yes | P1 |
| `ending_row` | Yes | P1 |

### Yuzu

`idle`, `walk` (float), `heal_cast`, `purify_cast`, `hit`, `materialize` (SC-10)

### Roku

`idle`, `walk`, `taunt`, `guard`, `harpoon_strike`, `hit`

### Enemies

Per `game/data/enemies/enemies.json` attack skills — minimum: `idle`, `attack`, `hit`, `death`; bosses add `phase_transition`, `special`

---

## 9. Portrait spec (UI)

| Character | File | Framing |
|-----------|------|---------|
| Urashima | `portraits/urashima.png` | Chest up; box edge visible |
| Yuzu | `portraits/yuzu.png` | Chest up; bell visible |
| Roku | `portraits/roku.png` | Chest up; harpoon strap |
| Otohime | `portraits/otohime.png` | Shadowed half-face |
| Enemies | `portraits/<enemy_id>.png` | Silhouette or bust per boss importance |

Resolution: **512×512** (enemies), **768×768** (party). Ink-wash border per `ART_DIRECTION.md` §4.

---

## 10. File naming & export

```
game/assets/models/characters/urashima/urashima.glb
game/assets/models/characters/yuzu/yuzu.glb
game/assets/models/characters/roku/roku.glb
game/assets/models/enemies/palace_sentinel/palace_sentinel.glb
game/assets/models/npcs/otohime/otohime_bust.glb
game/assets/models/npcs/crowd/villager_spirit.glb
game/assets/models/npcs/crowd/rebuilder.glb
game/assets/ui/portraits/urashima.png
```

- Export GLB with embedded textures
- Scale: 1 Godot unit = 1 meter; Urashima height ≈ **1.7m**
- Register in manifest: `python3 tools/register_asset.py add --help`
- Log every external source in `docs/art/LICENSES.md` + `docs/art/ASSET_COMPLIANCE.md`

---

## 11. Production order

1. Urashima model + walk + idle (vertical slice gate)
2. Lacquer box + `fisher_katana` (`docs/art/ITEMS_3D_MODEL_GUIDE.md` §4, §8)
3. Torii + shack set dressing with Urashima in SC-02
4. Salt Crab + combat portraits
5. Yuzu + Shore Wraith (Act II gate)
6. Roku + remaining enemies
7. Palace Sentinel + Tide Keeper + Otohime bust
8. Ending crowd (`villager_spirit`, `rebuilder`) + ending variants (boat, restored village kit)
9. Remaining item pickups and weapon tiers
