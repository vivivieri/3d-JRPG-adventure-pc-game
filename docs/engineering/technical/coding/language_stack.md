---
id: language-stack
type: reference
phase: [1, 2, 3, 4, 5, 6]
audience: [architect, builder]
status: active
authority: engineering
tokens_est: 653
summary: "Coding Standards Hub — Language stack + branch policy — Not shipped in the game: Godot MCP Pro server + addon, GDAI/Godotiq plugins, GitHub Actions YAML."
---
# Coding Standards Hub — Language stack + branch policy

**Hub:** [`CODING_STANDARDS_HUB.md`](../CODING_STANDARDS_HUB.md)

## When to read

Use **Coding Standards Hub — Language stack + branch policy** (roles: architect, builder) when you need this reference during the current task Jump to a section below instead of reading end-to-end (2 sections).

## Jump to

- [1. Language stack](#1-language-stack)
- [Branch policy](#branch-policy)


## 1. Language stack

| Language | Role | Location | Authority |
|----------|------|----------|-----------|
| **GDScript 2.0** | Game runtime — combat, narrative, UI, world | `game/scripts/` (`game/development`) | [**GDSCRIPT_STYLE.md**](../GDSCRIPT_STYLE.md) · [`CODE_STYLE.md`](../CODE_STYLE.md) |
| **Godot Shader** (`.gdshader`) | NPR toon, water, emissive VFX | `game/shaders/` | [**SHADER_STYLE.md**](../SHADER_STYLE.md) · [`RENDERING_GUIDE.md`](../../../design/art/RENDERING_GUIDE.md) |
| **Godot Scene** (`.tscn`) | Zones, UI, components — **GDAI built** | `game/scenes/` | [**SCENE_STYLE.md**](../SCENE_STYLE.md) · [`MCP_STACK.md`](../../../ops/agents/MCP_STACK.md) |
| **Markdown** | Design docs, runbooks, QA policy | `docs/` | [**MARKDOWN_STYLE.md**](../MARKDOWN_STYLE.md) |
| **JSON** | Story, combat, registries, QA catalogs | `game/data/` | [**JSON_DATA_STYLE.md**](../JSON_DATA_STYLE.md) · [`DATA_ARCHITECTURE.md`](../DATA_ARCHITECTURE.md) |
| **Python 3** | Validators, CI, procedural generators, reference libs | `tools/*.py` | [**PYTHON_STYLE.md**](../PYTHON_STYLE.md) · [PEP 8](https://peps.python.org/pep-0008/) |
| **Bash** | CI runners, bootstrap, QA orchestration | `tools/*.sh` | [**BASH_STYLE.md**](../BASH_STYLE.md) · [`CI.md`](../../../ops/ci-cd/CI.md) |
| **HTML** | Generated stakeholder dashboards | `docs/archive/compliance/` | [`ALIGNMENT_AUDIT.md`](../../../ops/qa/ALIGNMENT_AUDIT.md) |
| **TypeScript** | Godot MCP Pro server (dev tooling — **not shipped**) | `tools/godot-mcp-pro-server/` | [**TYPESCRIPT_STYLE.md**](../TYPESCRIPT_STYLE.md) |

**Not shipped in the game:** Godot MCP Pro server + addon, GDAI/Godotiq plugins, GitHub Actions YAML.

**Engine:** Godot **4.7** Forward+ · scene tree + autoload singletons — **not** ECS.

### Branch policy

| Branch | Code you write | CI |
|--------|----------------|-----|
| **`main`** | JSON data, Python validators, docs | `bash tools/run_docs_ci_checks.sh` |
| **`game/development`** | GDScript, shaders, scenes (via GDAI MCP) | `bash tools/run_ci_checks.sh` |

See [`BRANCHING.md`](../../../ops/workflow/BRANCHING.md) · [`SPEC_FIRST_DEVELOPMENT.md`](../SPEC_FIRST_DEVELOPMENT.md).

---
