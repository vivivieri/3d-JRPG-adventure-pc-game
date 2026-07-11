# MCP Stack — Full Toolchain (Godot 4.7)

**Version:** 2.0  
**Applies to:** `main` rebuild workflow — **Godot 4.7 stable**  
**Cross-refs:** `.cursorrules` §0–§1, `docs/GDAI_CLOUD_SETUP.md`, `docs/PLUGIN_INSTALL_GUIDE.md`, `docs/AI_DEV_WORKFLOW.md`, `docs/AI_TESTING_SPEC.md`, `docs/ART_DIRECTION.md`, `docs/ASSET_COMPLIANCE.md`

**All tools in this document are required.** Agents must not treat any layer as optional or “recommended only.” If a required tool is missing, **STOP and notify the user** — do not fall back to manual scene edits or undocumented web assets.

---

## Full R&R map

```
┌─────────────────────────────────────────────────────────────────┐
│  PLAN & CODE          GodotPrompter — GDScript, .gdshader, tests │
├─────────────────────────────────────────────────────────────────┤
│  DESIGN CONTEXT       Notion MCP — formulas, lore index, balance │
├─────────────────────────────────────────────────────────────────┤
│  ART GENERATE         GameLab MCP — textures, UI sheets, VFX     │
│  ART PIPELINE         Blender + AI Render (offline, human)       │
├─────────────────────────────────────────────────────────────────┤
│  BUILD                GDAI MCP (`godot-mcp`)                     │
├─────────────────────────────────────────────────────────────────┤
│  ANALYZE              Godotiq (`godotiq`)                        │
├─────────────────────────────────────────────────────────────────┤
│  TEST                 Godot MCP Pro (`godot-mcp-pro`, `--minimal`)│
├─────────────────────────────────────────────────────────────────┤
│  AUDIO PLACEHOLDER    tools/generate_game_audio.py              │
│  AUDIO PROTOTYPE      Suno / Udio (zone BGM until authored)      │
└─────────────────────────────────────────────────────────────────┘
```

| Layer | Tool | Cursor / access | Role |
|-------|------|-----------------|------|
| Plan & code | **GodotPrompter** | Cursor agent | GDScript, shaders, tests, architecture |
| Design context | **Notion MCP** | `notion` | Stat formulas, flag glossary, tone guides |
| Art generate | **GameLab Studio MCP** | `gamelab-mcp` (SSE) | Tileable textures, UI frames, sprite/VFX sheets |
| Art pipeline | **Blender + AI Render** | Offline — not MCP | Hand-painted albedo on low-poly hero meshes |
| Build | **GDAI MCP** | `godot-mcp` | Scenes, nodes, materials, lights, F5 playtest |
| Analyze | **Godotiq** | `godotiq` | Signals, debug console, `ui_map`, validation |
| Test | **Godot MCP Pro** | `godot-mcp-pro` | L4/L5 scenarios, asserts, input replay |
| Audio placeholder | `generate_game_audio.py` | Shell | Copyright-safe BGM/SFX until replaced |
| Audio prototype | **Suno / Udio** | Web (human export) | Zone BGM loops during iteration |

```
GodotPrompter (plan/code)
       │
       ├─► Notion MCP ────────► design context before data/combat edits
       ├─► GameLab MCP ───────► generate textures/UI → save to game/assets/
       ├─► Blender (offline) ─► hero GLB meshes → import → GDAI places
       ├─► GDAI MCP ──────────► create/edit scenes, F5 verify
       ├─► Godotiq ───────────► trace_flow, signal_map, debug console
       └─► Godot MCP Pro ─────► run_test_scenario, assert_screen_text
```

**Rule:** Each tool owns its layer. They **supplement** each other — none replaces GDAI for `.tscn` mutations, Godotiq for debug, or MCP Pro for L4/L5 tests.

---

## Role split & conflict rules

| Situation | Required tool |
|-----------|---------------|
| Create/edit `.tscn`, nodes, materials in editor | **GDAI MCP only** |
| Generate tileable zone texture | **GameLab MCP** → save file → **GDAI** assigns |
| Read stat formula before balancing skill | **Notion MCP** → edit `game/data/*.json` |
| Hero 3D model with painted albedo | **Blender offline** → GLB import → **GDAI** places |
| Combat signal hang — which signal failed? | **Godotiq** `godotiq_signal_map`, `godotiq_trace_flow` |
| Automated JRPG menu / combat test | **Godot MCP Pro** testing tools |
| Read Godot Output without copy-paste | **Godotiq** `godotiq_read_debug_console` |
| Screenshot game viewport | **GDAI**, **Godotiq**, or **MCP Pro**; save to `artifacts/screenshots/` |
| Zone BGM iteration | **Suno/Udio** export or `generate_game_audio.py` → **GDAI** wires in editor |
| Edit node tree / reparent | **GDAI only** |

**Never** use GameLab, Summer Engine, or Fennara for scene graph mutations when GDAI is available.

**Godot MCP Pro full mode (172 tools)** overlaps GDAI for scene editing. Always use **`--minimal`** (35 tools) in Cursor — testing + runtime + input focus only.

---

## Session startup (every agent run)

```bash
bash tools/ensure_mcp_stack.sh
bash tools/check_dev_environment.sh
```

### Block until all required checks pass

| Check | How |
|-------|-----|
| GDAI HTTP bridge | `curl -sf http://127.0.0.1:3571/tools` returns JSON |
| Godotiq WebSocket | Port `6007` listening; GodotIQ plugin enabled |
| MCP Pro server | `tools/godot-mcp-pro-server/build/index.js` exists; plugin enabled |
| Godot Editor | Running with `game/project.godot` open |
| Cursor MCP catalog | **All** of: `godot-mcp`, `godotiq`, `godot-mcp-pro`, `gamelab-mcp`, `notion` |
| Blender pipeline | Blender installed for hero 3D work (offline — verify with user if headless) |

If any MCP server is missing from Cursor → **STOP and notify the user**. See registration below.

---

## Install — Godot MCP plugins

**Step-by-step:** `docs/PLUGIN_INSTALL_GUIDE.md`, `docs/GDAI_CLOUD_SETUP.md`

### 1. GDAI MCP

```bash
bash tools/install_gdai_plugin.sh    # zip in game/addons/
```

Enable **GDAI MCP** plugin → panel → **Start**.

### 2. Godotiq

```bash
bash tools/install_godotiq.sh
```

Enable **GodotIQ** plugin. Pro license (optional upgrade): `GODOTIQ_LICENSE_KEY` in MCP env.

### 3. Godot MCP Pro

```bash
# Full package zip: game/addons/godot-mcp-pro*.zip
bash tools/install_godot_mcp_pro.sh
```

Requires **Node.js 18+**. Enable **Godot MCP Pro** plugin.

### 4. Bootstrap all Godot bridges

```bash
bash tools/ensure_mcp_stack.sh
```

Writes `.cursor/mcp.json` for installed Godot MCP servers, starts editor, checks HTTP/WebSocket bridges.

---

## Install — Cursor MCP servers

Register **every** server in Cursor (desktop Settings → Tools & MCP, or [cursor.com/agents](https://cursor.com/agents) cloud dashboard). Restart agent after save.

`tools/write_mcp_config.sh` generates Godot-related entries. Merge with GameLab and Notion manually (secrets in Cursor Secrets tab).

### Full `mcpServers` example

```json
{
  "mcpServers": {
    "godot-mcp": {
      "command": "uv",
      "args": ["run", "/workspace/game/addons/gdai-mcp-plugin-godot/gdai_mcp_server.py"]
    },
    "godotiq": {
      "command": "uvx",
      "args": ["godotiq"],
      "env": {
        "GODOTIQ_PROJECT_ROOT": "/workspace/game"
      }
    },
    "godot-mcp-pro": {
      "command": "node",
      "args": [
        "/workspace/tools/godot-mcp-pro-server/build/index.js",
        "--minimal"
      ],
      "env": {
        "GODOT_MCP_PORT": "6505"
      }
    },
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

**Notion MCP:** Enable via Cursor Integrations (Notion plugin). Used for design-context queries before editing `game/data/` or combat systems.

**GameLab API key:** Store in Cursor Secrets — not committed to git.

Template: `.cursor/mcp.json.example`

---

## Art & design tools (required)

### GameLab Studio MCP — textures & 2D art

**Role:** Tileable albedos, UI frames, sprite/VFX sheets.  
**Does NOT:** Edit `.tscn` — hand off to GDAI after export.

**Workflow:**

```
1. READ  docs/ART_DIRECTION.md palette for target zone
2. GameLab MCP — generate tileable wood/stone/ground albedo (muted coastal decay)
3. Save PNG → game/assets/textures/zones/<zone>/
4. python3 tools/register_asset.py + docs/LICENSES.md
5. GodotPrompter — tune toon shader if needed
6. GDAI MCP — assign materials in zone .tscn, F5 verify
7. bash tools/check_asset_compliance.sh
```

**Art constraints:** Muted palette (`#8B9DAF` fog, `#5C4A3A` wood, `#4AE8D8` biolume). Japanese coastal motifs — **not** bright Ghibli candy, not PBR realism, no European medieval reads.

Setup: [gamelabstudio.co](https://gamelabstudio.co/) API key → register `gamelab-mcp` SSE server.

### Notion MCP — design context & balancing

**Role:** Agent-readable index for stat formulas, skill curves, tone guides, lore tables.  
**Does NOT:** Replace `game/data/` JSON or `docs/` as source of truth.

**Workflow:**

1. Mirror key tables in Notion: combat formulas, item tiers, flag glossary, dialogue tone
2. Before editing `game/data/*.json` or combat GDScript → query Notion for design intent
3. Commit repo JSON changes; keep Notion synchronized

**Why not Ink (Inkle):** Story spine is JSON-driven (`scenes.json` → `dialogue/` → `flags.json`). Ink adds a second runtime with no v1 benefit. See `docs/NARRATIVE_WRITING_GUIDE.md`.

### Blender + AI Render — offline 3D hero pipeline

**Role:** Hand-painted albedo on low-poly Japanese coastal meshes.  
**Not MCP** — required human-in-the-loop before Godot import.

```
Blender mesh → AI Render / hand paint → GLB → game/assets/models/
  → toon_base.gdshader → GDAI MCP places in zone scene
```

**Use for:** Torii, lacquer box, palace trim, hero set-pieces (8k–20k tris per `ART_DIRECTION.md`).

### Shader policy

External cel-shading preset packs are **reference only** — GodotPrompter authors the project’s single `toon_base.gdshader` ramp family. No full PBR `StandardMaterial3D` in player-facing scenes.

### Suno / Udio — audio prototype

**Role:** Zone BGM loops during gameplay iteration.  
**Also required:** `python3 tools/generate_game_audio.py` for copyright-safe placeholders.

**Ship rule:** Replace all procedural and temp AI audio before release (`docs/AUDIO_PRODUCTION_GUIDE.md`). Log licenses in `docs/LICENSES.md`.

---

## Explicitly rejected (do not adopt)

| Tool | Reason |
|------|--------|
| **Summer Engine** | Replaces Godot 4.7 editor; invalidates GDAI stack |
| **Fennara (FAR)** | Fourth scene editor; overlaps GDAI/Godotiq/MCP Pro |
| **Ink narrative rewrite** | JSON spine already defined |
| **Kenney town kits** | European visual read; banned for player-facing builds |
| **Kenney knight / Castle kit** | Deprecated for ship (`ART_DIRECTION.md`) |

---

## Licenses & cost

| Tool | License | Cost | In git? |
|------|---------|------|---------|
| GDAI MCP | Commercial | ~$19 | ❌ gitignored |
| Godotiq Community | MIT (pip) | Free | ❌ addon gitignored |
| Godotiq Pro | Commercial | $19 one-time | Optional upgrade |
| Godot MCP Pro | Commercial | $15 one-time | ❌ gitignored |
| GameLab Studio | Commercial | Free tier + paid | API key in Secrets |
| Notion MCP | Notion ToS | Per workspace | N/A |
| Blender + AI Render | OSS / varies | Free–paid | Offline |
| Suno / Udio | Commercial | Budget tiers | Exported audio only |

**Ship builds:** disable/remove all Godot dev plugins before Steam export.

---

## Ports (defaults)

| Server | Port | Check |
|--------|------|-------|
| GDAI HTTP | 3571 | `curl -sf http://127.0.0.1:3571/tools` |
| Godotiq WebSocket | 6007 | GodotIQ plugin auto-connects |
| Godot MCP Pro | 6505 | Plugin panel in editor |

---

## Godot editor plugins (enable all)

| Plugin | MCP server |
|--------|------------|
| GDAI MCP | `godot-mcp` |
| GodotIQ | `godotiq` |
| Godot MCP Pro | `godot-mcp-pro` |

Start **GDAI MCP** panel → **Start** after editor opens.

---

## Testing workflow

See `docs/AI_TESTING_SPEC.md` §11.

| Layer | Tools |
|-------|-------|
| L0–L2 | Shell scripts (no MCP) |
| L3 | GDAI F5 + screenshot; Godotiq `godotiq_ui_map` for menus |
| L4 | Godot MCP Pro `run_test_scenario`; Godotiq `godotiq_verify_project_runs` |
| L5 | Godot MCP Pro input replay + `assert_screen_text`; Godotiq `godotiq_trace_flow` on failure |
| L6 | Human — **after** L5 |

### Example prompts

**Zone texture (GameLab → GDAI):**

```
Using gamelab-mcp: generate seamless tileable weathered wood albedo,
muted #5C4A3A, Japanese coastal decay, 1024×1024.
Save to game/assets/textures/zones/ruined_village/wood_planks.png.
Then using godot-mcp only: assign to pier meshes in ruined_village.tscn. F5 verify.
```

**Combat balance (Notion → code):**

```
Query Notion for current turn-order and damage formulas.
Update game/data/skills.json and CombatManager.gd to match.
Run bash tools/run_unit_tests.sh.
```

**Debug hung turn (Godotiq):**

```
Use godotiq_signal_map and godotiq_trace_flow on CombatManager.
Read debug console. GDAI only if a .tscn fix is needed.
```

**Automated combat menu (MCP Pro):**

```
Using godot-mcp-pro: run_test_scenario for SC-05 tutorial.
Assert battle menu text visible.
```

---

## Troubleshooting

| Issue | Fix |
|-------|-----|
| Any required MCP missing from catalog | Register in Cursor dashboard; restart agent |
| Too many MCP tools in Cursor | MCP Pro: use `--minimal` in mcp.json args |
| GDAI + MCP Pro both edit scene | **Rule:** GDAI builds; MCP Pro tests only |
| Godotiq bridge offline | Enable GodotIQ plugin; wait 5s |
| GameLab SSE fails | Check API key in Secrets; verify SSE URL |
| Notion queries fail | Re-authenticate Notion MCP in Cursor Integrations |
| `node` not found | Install Node 18+ for Godot MCP Pro |

---

## Related

- `game/.godotiq.json` — Godotiq project conventions
- `game/addons/README.md` — addon policy
- `.cursor/mcp.json.example` — MCP config template
- `docs/PLUGIN_INSTALL_GUIDE.md` — install steps
- `docs/GDAI_CLOUD_SETUP.md` — cloud snapshot & GDAI bootstrap
