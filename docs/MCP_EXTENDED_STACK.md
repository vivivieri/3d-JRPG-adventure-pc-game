# MCP Extended Stack — Art, Design Context & Offline Pipelines

**Version:** 1.0  
**Applies to:** `main` rebuild — **Godot 4.7 stable**  
**Cross-refs:** `docs/MCP_STACK.md` (core build/analyze/test), `.cursorrules` §0–§1, `docs/ART_DIRECTION.md`, `docs/ASSET_COMPLIANCE.md`

This document extends the **mandatory** MCP stack (GDAI + Godotiq + Godot MCP Pro) with **optional** tools for asset generation, design context, and offline art pipelines. It codifies adoption decisions after external tooling review (2026-07).

**Rule:** Extended tools **supplement** the core stack. They do **not** replace GDAI for scene edits, Godotiq for debug, or Godot MCP Pro for L4/L5 tests.

---

## Full R&R map

```
┌─────────────────────────────────────────────────────────────────┐
│  PLAN & CODE          GodotPrompter — GDScript, .gdshader, tests │
├─────────────────────────────────────────────────────────────────┤
│  DESIGN CONTEXT       Notion MCP (optional) — formulas, lore index│
├─────────────────────────────────────────────────────────────────┤
│  ART GENERATE         GameLab MCP (optional) — textures, UI sheets │
│  ART PIPELINE         Blender + AI Render (offline, human)        │
├─────────────────────────────────────────────────────────────────┤
│  BUILD                GDAI MCP (`godot-mcp`) — REQUIRED           │
├─────────────────────────────────────────────────────────────────┤
│  ANALYZE              Godotiq (`godotiq`) — recommended           │
├─────────────────────────────────────────────────────────────────┤
│  TEST                 Godot MCP Pro (`godot-mcp-pro`) — L4/L5     │
├─────────────────────────────────────────────────────────────────┤
│  AUDIO PLACEHOLDER    generate_game_audio.py (ship-safe default)  │
│  AUDIO PROTOTYPE      Suno / Udio (optional temp BGM)             │
└─────────────────────────────────────────────────────────────────┘
```

| Layer | Tool | Cursor / access | Required? |
|-------|------|-----------------|-----------|
| Plan & code | **GodotPrompter** | Cursor agent | ✅ Yes |
| Design context | **Notion MCP** | Cursor Integrations | Optional (Phase 2+) |
| Art generate | **GameLab Studio MCP** | `gamelab-mcp` (SSE) | Optional (Phase 1+) |
| Art pipeline | **Blender + AI Render** | Offline — not MCP | Optional (hero assets) |
| Build | **GDAI MCP** | `godot-mcp` | ✅ Yes |
| Analyze | **Godotiq** | `godotiq` | Recommended |
| Test | **Godot MCP Pro** | `godot-mcp-pro` (`--minimal`) | Recommended |
| Audio placeholder | `tools/generate_game_audio.py` | Shell | Default until authored |
| Audio prototype | Suno / Udio | Web (human export) | Optional temp |

Core stack details: `docs/MCP_STACK.md`.

---

## Adopted tools

### 1. GameLab Studio MCP — textures & 2D art

**Role:** Generate tileable albedos, UI frames, sprite sheets, VFX sheets.  
**Does NOT:** Place nodes or edit `.tscn` — hand off to **GDAI MCP** after export.

**When:** Phase 1 environment vertical slice (`ruined_village`, beach, caves).

**Setup (desktop or cloud dashboard):**

1. Create API key at [gamelabstudio.co](https://gamelabstudio.co/)
2. Register in **Cursor Settings → Tools & MCP** (or cloud Integrations):

```json
{
  "mcpServers": {
    "gamelab-mcp": {
      "type": "sse",
      "url": "http://api.gamelabstudio.co:8765/sse",
      "headers": {
        "X-API-Key": "YOUR_GAMELAB_API_KEY"
      }
    }
  }
}
```

3. Merge with existing `godot-mcp`, `godotiq`, `godot-mcp-pro` entries — do not remove core servers.

**Workflow:**

```
1. READ  docs/ART_DIRECTION.md palette for target zone
2. GameLab MCP — generate tileable wood/stone/ground albedo (muted coastal decay)
3. Save PNG → game/assets/textures/zones/<zone>/
4. python3 tools/register_asset.py … + docs/LICENSES.md
5. GodotPrompter — tune toon shader if needed
6. GDAI MCP — assign materials in zone .tscn, F5 verify
7. bash tools/check_asset_compliance.sh
```

**Art constraints (mandatory):**

- Muted palette — fog `#8B9DAF`, weathered wood `#5C4A3A`, biolume `#4AE8D8`
- **Not** bright Ghibli fantasy, not photoreal PBR
- Japanese coastal / ryūgū motifs — no European medieval reads
- Reject outputs that look like generic anime candy colors

---

### 2. Notion MCP — design context & balancing

**Role:** Agent-readable index for stat formulas, skill curves, tone guides, and lore tables.  
**Does NOT:** Replace `game/data/` JSON or `docs/` as source of truth.

**When:** Phase 2 (combat shell) and Phase 3 (narrative).

**Workflow:**

1. Mirror or link key tables in Notion: combat formulas, item tiers, flag glossary, dialogue tone
2. Before editing `game/data/*.json` or combat GDScript, agent queries Notion for current design intent
3. Commit changes to repo JSON; Notion stays synchronized manually or via export

**Why not Ink (Inkle):** Story spine is JSON-driven (`scenes.json` → `dialogue/` → `flags.json`). Ink would add a second narrative runtime with no v1 benefit. See `docs/NARRATIVE_WRITING_GUIDE.md`.

---

### 3. Blender + AI Render — offline 3D hero pipeline

**Role:** Hand-painted albedo on low-poly modular kits and hero props.  
**Not MCP** — human-in-the-loop before Godot import.

**Pipeline:**

```
Blender mesh (low-poly, Japanese coastal silhouette)
  → AI Render / hand paint stylized albedo
  → Export GLB → game/assets/models/
  → Godot import → toon_base.gdshader family
  → GDAI MCP places in zone scene
```

**Use for:** Torii, lacquer box, palace trim, hero set-pieces (8k–20k tris per `ART_DIRECTION.md`).

---

### 4. Suno / Udio — audio prototype (optional)

**Role:** Temporary zone BGM loops while iterating gameplay.  
**Default:** `python3 tools/generate_game_audio.py` (ORIGINAL, ship-safe placeholder).

**Ship rule:** Replace all procedural and temp AI audio before release (`docs/AUDIO_PRODUCTION_GUIDE.md`). Log commercial/temp licenses in `docs/LICENSES.md`.

---

## Shader policy — adapt ideas, do not import PBR presets

External “cel-shading preset” packs (Asset Library plugins, `StandardMaterial3D` templates) are **reference only**.

| Allowed | Forbidden in player-facing scenes |
|---------|-----------------------------------|
| Custom `toon_base.gdshader` ramp family | Full PBR / glossy `StandardMaterial3D` realism |
| GodotPrompter-authored `.gdshader` | Copy-paste preset without palette review |
| Stepped diffuse, optional subtle outlines | ORM packs, HDR skin, candy anime defaults |

Reference libraries (study only): [godot4-cel-shader](https://github.com/eldskald/godot4-cel-shader), community comic/toon shaders. GodotPrompter adapts patterns into the project’s single ramp family.

---

## Explicitly rejected (v1)

| Tool | Reason |
|------|--------|
| **Summer Engine** | Replaces Godot 4.7 editor; invalidates GDAI + Godotiq + MCP Pro investment |
| **Fennara (FAR)** | Fourth scene editor; overlaps GDAI (build), Godotiq (debug), MCP Pro (screenshots/tests) |
| **Ink rewrite** | JSON narrative spine already defined; major architecture change |
| **Kenney town kits** | European visual read; banned for player-facing builds (`ART_DIRECTION.md`) |
| **Kenney knight / Castle kit** | Deprecated for ship; wrong silhouette for Japanese coastal JRPG |

Kenney CC0 may exist in repo history for greybox only — **never** in SC-02 vertical slice or ship builds.

---

## Conflict rules (extended stack)

| Situation | Use |
|-----------|-----|
| Create/edit `.tscn`, nodes, materials in editor | **GDAI MCP only** |
| Generate tileable zone texture | **GameLab MCP** → save file → **GDAI** assigns |
| Debug combat signal hang | **Godotiq** |
| Automated battle menu test | **Godot MCP Pro** |
| Read stat formula before balancing skill | **Notion MCP** → edit `game/data/skills.json` |
| Hero 3D model with painted albedo | **Blender offline** → import → **GDAI** places |
| Temp zone BGM | `generate_game_audio.py` or Suno/Udio export → **GDAI** wires in editor |

**Never** use GameLab, Fennara, or Summer for scene graph mutations when GDAI is available.

---

## Phased adoption

| Phase | Add | Keep |
|-------|-----|------|
| **Phase 1** (environment) | GameLab MCP for zone textures | GDAI + Godotiq + MCP Pro |
| **Phase 2** (systems) | Notion MCP for combat/item design context | JSON data architecture |
| **Phase 3** (narrative) | Notion for tone/flag glossary | `DialogueRunner` + JSON dialogue |
| **Ongoing** | Blender pipeline for hero 3D | Custom toon shaders via GodotPrompter |
| **Pre-ship** | Replace Suno/Udio / procedural audio | `AUDIO_PRODUCTION_GUIDE.md` |

---

## Example prompts

**Zone texture (GameLab → GDAI):**

```
Using gamelab-mcp: generate a seamless tileable weathered wood albedo,
muted #5C4A3A, Japanese coastal decay, 1024×1024.
Save to game/assets/textures/zones/ruined_village/wood_planks.png.
Then using godot-mcp only: assign to pier meshes in ruined_village.tscn
with toon_base material. F5 verify.
```

**Combat balance (Notion → code):**

```
Query Notion for current turn-order and damage formulas.
Update game/data/skills.json and CombatManager.gd to match.
Run bash tools/run_unit_tests.sh.
```

**Debug hung turn (Godotiq — no extended tools):**

```
Use godotiq_signal_map on CombatManager. Read debug console.
Do not edit scenes — GDAI only if a .tscn fix is needed.
```

---

## Related

- `docs/MCP_STACK.md` — core GDAI + Godotiq + MCP Pro
- `docs/GDAI_CLOUD_SETUP.md` — GDAI install & cloud snapshot
- `docs/PLUGIN_INSTALL_GUIDE.md` — Godotiq & MCP Pro install
- `docs/AI_DEV_WORKFLOW.md` — build & test acceptance criteria
- `.cursor/mcp.json.example` — MCP config template
