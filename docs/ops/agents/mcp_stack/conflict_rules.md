---
id: conflict-rules
type: how-to
phase: [0, 1]
audience: [pm, builder]
status: active
authority: ops
tokens_est: 436
summary: "Role split & conflict rules"
---
# MCP Stack — Role split & conflict rules

**Hub:** [`MCP_STACK.md`](../MCP_STACK.md)

## Role split & conflict rules

| Situation | Required tool |
|-----------|---------------|
| Create/edit `.tscn`, nodes, materials in editor | **GDAI MCP only** |
| Generate tileable zone albedo | **ComfyUI** or **Material Maker** → `palette_remap.py` → **GDAI** assigns |
| Generate UI frame / ink border | **GameLab MCP** → `palette_remap.py` → **GDAI** UI scenes |
| Read stat formula before balancing skill | **`docs/` + `game/data/`** → edit JSON |
| Hero 3D model + stylized albedo | **Meshy/Tripo/Rodin** → Blender → GLB → **GDAI** places |
| Combat signal hang — which signal failed? | **Godotiq** `godotiq_signal_map`, `godotiq_trace_flow` |
| Automated JRPG menu / combat test | **Godot MCP Pro** testing tools |
| Read Godot Output without copy-paste | **Godotiq** `godotiq_read_debug_console` |
| Screenshot game viewport | **GDAI**, **Godotiq**, or **MCP Pro**; save to `artifacts/screenshots/` |
| Zone BGM iteration | **ACE-Step** via `bash tools/generate_ai_bgm.sh` or `generate_game_audio.py` fallback → **GDAI** wires in editor |
| Selective story VO | **ElevenLabs** via `bash tools/generate_ai_vo.sh` — **only** lines with `voice_id` in `chapter_01.json`; never full script |
| Edit node tree / reparent | **GDAI only** |

**Never** use GameLab, Summer Engine, or Fennara for scene graph mutations when GDAI is available.

**Godot MCP Pro full mode (172 tools)** overlaps GDAI for scene editing. Always use **`--minimal`** (35 tools) in Cursor — testing + runtime + input focus only.

---
