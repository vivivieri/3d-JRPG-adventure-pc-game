# Tides of Urashima — Character Bible

**Version:** 1.0 (Pre-build)  
**Visual target:** High-detail stylized Japanese — hand-painted albedo, readable silhouettes, no primitive placeholders in ship builds.  
**Cross-refs:** `docs/ART_DIRECTION.md`, `docs/STORYBOARD.md`, `docs/BOSS_DESIGNS.md`

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

- Joins party SC-10; **optional follower** in field from SC-12 (2m behind Urashima, no collision)
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
- SC-04–12: stays near shack unless story flag `roku_joins_party`
- Shop UI: same model in window silhouette or portrait only (performance)

### Combat read

Taunt = harpoon planted, roar anim; Shell Guard = crouch behind folded arms

---

## 5. Otohime (NPC — flashback only)

**ID:** `otohime`  
**Role:** Moral mirror; not playable  
**Appearances:** SC-11 (flashback), SC-17c (underwater glimpse)

### Design direction

- **Too perfect** — porcelain skin, no flaws, symmetrical
- **Ryūgū-jō court dress** — layered kimono, coral gold trim, long sleeves
- Face partially shadowed in flashback; never full idle in field
- **Uncanny**, not fanservice; stillness reads as wrong

### Silhouette

- Tall, elongated sleeves; hair ornament (kanzashi) like breaking wave
- No combat model required; cinematic bust + silhouette sufficient for v1

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

See `docs/BOSS_DESIGNS.md`. Colossal draped form; faces visible under cloth folds.

---

### Palace Sentinel (`palace_sentinel`) — MINIBOSS

| Field | Detail |
|-------|--------|
| Silhouette | Angular ryūgū armor; single horizontal eye slit |
| Tris | ~15k |
| Read | Lacquer plates, gold edging; no European plate mail |
| Palette | `#8B2A3A` lacquer, `#D4A55A` trim, `#1A1A2A` void gaps |

**Combat:** Shield block stance; spear thrust; weak to Spirit (Yuzu)

---

### Tide Keeper (`tide_keeper`) — FINAL BOSS

See `docs/BOSS_DESIGNS.md`. Humanoid tide; clock motifs in water cloak.

---

## 7. NPC / ambient (silhouettes only)

| ID | Usage | Model level |
|----|-------|-------------|
| `villager_spirit` | Rewind ending crowd | Low-poly silhouettes, 2 variants |
| `rebuilder` | Anchor ending shore | 3 figures with tools |
| `village_cat` | Hub ambient | Small organic mesh, not sphere |
| `village_dog` | Hub ambient | Small organic mesh, not sphere |

---

## 8. Master animation list

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
game/assets/models/enemies/salt_crab/salt_crab.glb
game/assets/ui/portraits/urashima.png
```

- Export GLB with embedded textures
- Scale: 1 Godot unit = 1 meter; Urashima height ≈ **1.7m**
- Register in manifest: `python3 tools/register_asset.py add --help`
- Log every external source in `docs/LICENSES.md` + `docs/ASSET_COMPLIANCE.md`

---

## 11. Production order

1. Urashima model + walk + idle (vertical slice gate)
2. Torii + shack set dressing with Urashima in SC-02
3. Salt Crab + combat portraits
4. Yuzu + Shore Wraith (Act II gate)
5. Roku + remaining enemies
6. Palace Sentinel + Tide Keeper + Otohime bust
7. Ending variants (crowd silhouettes, boat)
