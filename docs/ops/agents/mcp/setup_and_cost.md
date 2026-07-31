---
id: setup-and-cost
type: how-to
phase: [0, 1]
audience: [pm, builder]
status: active
authority: agents
tokens_est: 1074
summary: "disable/remove all Godot dev plugins before Steam export."
---
# MCP — Setup And Cost

**Hub:** [`MCP_STACK.md`](../MCP_STACK.md)

## Explicitly rejected (do not adopt)

| Tool | Reason |
|------|--------|
| **Summer Engine** | Replaces Godot 4.7 editor; invalidates GDAI stack |
| **Fennara (FAR)** | Fourth scene editor; overlaps GDAI/Godotiq/MCP Pro |
| **Ink narrative rewrite** | JSON spine already defined |
| **Kenney town kits** | European visual read; banned for player-facing builds |
| **Kenney knight / Castle kit** | Deprecated for ship (`ART_DIRECTION.md`) |
| **Notion MCP** | `docs/` + `game/data/` are authoritative — duplicate index adds OAuth friction, no ship value |

---

## Licenses & cost

| Tool | License | Cost | In git? |
|------|---------|------|---------|
| GDAI MCP | Commercial | ~$19 | ❌ gitignored |
| Godotiq Community | MIT (pip) | Free | ❌ addon gitignored |
| Godotiq Pro | Commercial | $19 one-time | Optional upgrade |
| Godot MCP Pro | Commercial | $15 one-time | ❌ gitignored |
| GameLab Studio | Commercial | Free tier + paid | API key in Secrets |
| Blender | OSS | Free | Offline |
| ACE-Step 1.5 | MIT | Free (local GPU) | `.cache/ace-step-1.5` gitignored |

**Ship builds:** disable/remove all Godot dev plugins before Steam export.

---

## User setup checklist (purchase & secrets)

Run: `bash tools/install_extended_toolchain.sh` then `bash tools/check_extended_toolchain.sh`

| Tool | You need to buy? | What you do |
|------|------------------|-------------|
| **GDAI MCP** | ✅ ~$19 one-time | Already installed — keep zip in cloud snapshot |
| **Godotiq** | ❌ Free (Pro $19 optional) | Already installed |
| **Godot MCP Pro** | ✅ $15 one-time | Already installed |
| **GameLab Studio** | Paid OK for quality; free tier for light UI | Sign up → API key → **Cursor Secrets: `GAMELAB_API_KEY`** → re-run install script |
| **ComfyUI / Material Maker** | ❌ Free | Local install; locked stylized workflows per `ART_AUTOMATION_PIPELINE.md` |
| **Meshy / Tripo / Rodin** | Paid OK for hero quality | Service ToS → register outputs in `LICENSES.md` |
| **Blender** | ❌ Free | Auto-installed in cloud via `install_extended_toolchain.sh` |
| **ACE-Step 1.5** | ❌ Free (local GPU) | `bash tools/install_ace_step.sh`; prompts in `game/data/audio/ace_step_prompts.json` |
| **ElevenLabs VO** | Paid API | `ELEVENLABS_API_KEY` in Cursor Secrets; `bash tools/generate_ai_vo.sh` |
| **generate_game_audio.py** | ❌ Free (repo tool) | Procedural fallback — auto on install |

**Cursor cloud dashboard:** Register P0 MCP servers from `.cursor/mcp.json`; add `gamelab-mcp` when `GAMELAB_API_KEY` is set. Restart agent after saving.

**Cannot be automated by agents:** GameLab API key (unless you add secret), ElevenLabs API key (unless you add secret), ACE-Step GPU generation (use prompt sheets + export), ComfyUI workflow runs (local GPU).

---

## Troubleshooting

| Issue | Fix |
|-------|-----|
| Any required MCP missing from catalog | Register in Cursor dashboard; restart agent |
| Too many MCP tools in Cursor | MCP Pro: use `--minimal` in mcp.json args |
| GDAI + MCP Pro both edit scene | **Rule:** GDAI builds; MCP Pro tests only |
| Godotiq bridge offline | Enable GodotIQ plugin; wait 5s |
| GameLab SSE fails | Check API key in Secrets; verify SSE URL |
| `node` not found | Install Node 18+ for Godot MCP Pro |

---

## Related

- `docs/ops/cheat-sheets/RR_CHEATSHEET.md` — printable one-page R&R summary
- `docs/design/art/ART_AUTOMATION_PIPELINE.md` — quality-first art/audio automation policy
- `docs/ops/qa/ACCEPTANCE_CRITERIA.md` — measurable QA gates (WARN/SKIP ≠ PASS)
- `docs/ops/qa/QA_REMEDIATION_LOOP.md` — FAIL iteration policy
- `docs/design/art/MODEL_QA.md` · `docs/design/art/VISUAL_QA.md` · `docs/design/audio/AUDIO_QA.md` · `docs/ops/qa/FLOW_QA.md`
- `game/data/qa/acceptance_criteria.json` — machine-readable thresholds
- `game/.godotiq.json` — Godotiq project conventions
- `game/addons/README.md` — addon policy
- `.cursor/mcp.json.example` — MCP config template
- `docs/ops/agents/PLUGIN_INSTALL_GUIDE.md` — install steps
- `docs/ops/agents/GDAI_CLOUD_SETUP.md` — cloud snapshot & GDAI bootstrap
