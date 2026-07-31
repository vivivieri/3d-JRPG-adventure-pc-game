---
id: rejected-licenses
type: how-to
audience: [pm, builder]
status: active
authority: ops
tokens_est: 393
summary: "MCP — Setup & Cost — Rejected tools + licenses — Ship builds: disable/remove all Godot dev plugins before Steam export."
---
# MCP — Setup & Cost — Rejected tools + licenses

**Hub:** [`setup_and_cost.md`](../setup_and_cost.md)

## When to read

Use **MCP — Setup & Cost — Rejected tools + licenses** (roles: pm, builder) when executing this procedure Jump to a section below instead of reading end-to-end (2 sections).

## Jump to

- [Explicitly rejected (do not adopt)](#explicitly-rejected-do-not-adopt)
- [Licenses & cost](#licenses-cost)


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
