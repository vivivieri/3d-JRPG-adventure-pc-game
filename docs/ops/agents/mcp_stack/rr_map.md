---
id: rr-map
type: how-to
phase: [0, 1]
audience: [pm, builder]
status: active
authority: ops
tokens_est: 615
summary: "GodotPrompter (plan/code)"
---
# MCP Stack — Full R&R map

**Hub:** [`MCP_STACK.md`](../MCP_STACK.md)

## Full R&R map

| Layer | Tool | Cursor / access | Role |
|-------|------|-----------------|------|
| Plan & code | **GodotPrompter** | Cursor agent | GDScript, shaders, tests, architecture |
| Design context | **`docs/` + `game/data/`** | Repo | Stat formulas, flags, dialogue — authoritative |
| Zone NPR albedos | **ComfyUI** or **Material Maker** | Offline — not MCP | Stylized tileables; `tools/palette_remap.py` post-step |
| UI art generate | **GameLab Studio MCP** | `gamelab-mcp` (SSE) | UI frames, ink borders, icon/VFX sheets **(required)** |
| 3D heroes / props | **Meshy / Tripo / Rodin** + **Blender** (required) | Offline — not MCP | AI 3D → GLB; Mixamo rig; M5 turntable QA |
| Build | **GDAI MCP** | `godot-mcp` | Scenes, nodes, materials, lights, F5 playtest |
| Analyze | **Godotiq** | `godotiq` | Signals, debug console, `ui_map`, validation |
| Test | **Godot MCP Pro** | `godot-mcp-pro` (`--minimal`) | L4/L5 scenarios, asserts, input replay |
| Audio placeholder | `generate_game_audio.py` | Shell | Copyright-safe BGM/SFX until replaced |
| Audio prototype | **ACE-Step 1.5** | Local (`bash tools/install_ace_step.sh`) | Zone + opening/boss/ending hero BGM |
| VO selective | **ElevenLabs** | `ELEVENLABS_API_KEY` + `generate_ai_vo.py` | 12 emotional hit clips — `docs/design/vision/VO_HIT_LIST.md` |
| Marketing trailer | `generate_marketing_trailer.py` | Shell (`ffmpeg`, `numpy`) | Ken Burns pitch PNGs → `steam/trailer*.mp4` |
| Video AI (optional) | Runway / Kling / similar | Offline — not MCP | Marketing trailer b-roll only — never in-game |

```
GodotPrompter (plan/code)
       │
       ├─► ComfyUI / Material Maker ─► zone albedos → palette_remap.py → game/assets/
       ├─► GameLab MCP ─────────────► UI sheets / frames → palette_remap.py → game/assets/
       ├─► AI 3D + Blender (offline) ► hero GLB → import → GDAI places
       ├─► GDAI MCP ────────────────► create/edit scenes, F5 verify
       ├─► Godotiq ─────────────────► trace_flow, signal_map, debug console
       └─► Godot MCP Pro ───────────► run_test_scenario, assert_screen_text
```

**Rule:** Each tool owns its layer. They **supplement** each other — none replaces GDAI for `.tscn` mutations, Godotiq for debug, or MCP Pro for L4/L5 tests.

---
