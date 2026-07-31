---
id: npc-ambient
type: reference
audience: [visual, builder]
phase: [5]
status: active
authority: art
tokens_est: 926
summary: "Scope: Low-poly crowd and ambient life — excluded from `hero_jury` and `L2_model_jury`. Zone composition counts apply (`zone_composition.json` max props). See."
---
# Characters — NPC / ambient

**Hub:** [`CHARACTER_BIBLE.md`](../CHARACTER_BIBLE.md)

## When to read

Use **Characters — NPC / ambient** (roles: visual, builder) when you need this reference during the current task Jump to a section below instead of reading end-to-end (4 sections).

## Jump to

- [7. NPC / ambient (silhouettes & crowd)](#7-npc-ambient-silhouettes-crowd)
- [Villager spirit (`villager_spirit`) — ending crowd](#villager-spirit-villager_spirit-ending-crowd)
- [Rebuilder (`rebuilder`) — ending shore](#rebuilder-rebuilder-ending-shore)
- [Village cat / dog (`village_cat`, `village_dog`)](#village-cat-dog-village_cat-village_dog)


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

