---
id: standards-where
type: reference
phase: [1, 2, 3, 4, 5, 6]
audience: [architect, builder]
status: active
authority: engineering
tokens_est: 860
summary: "Vendor code: Godot MCP Pro server ships inside the purchased zip — treat as third-party. Prefer upstream updates over large forks; document any project patches"
---
# TypeScript Style — Standards, where TS lives, runtime

**Hub:** [`TYPESCRIPT_STYLE.md`](../TYPESCRIPT_STYLE.md)

## When to read

Use **TypeScript Style — Standards, where TS lives, runtime** (roles: architect, builder) when you need this reference during the current task Jump to a section below instead of reading end-to-end (4 sections).

## Jump to

- [1. Industry standards (authoritative externals)](#1-industry-standards-authoritative-externals)
- [2. Where TypeScript lives in this repo](#2-where-typescript-lives-in-this-repo)
- [3. Runtime & build](#3-runtime-build)
- [Mode flags (do not change without PM approval)](#mode-flags-do-not-change-without-pm-approval)


## 1. Industry standards (authoritative externals)

| Standard | Reference | What it governs |
|----------|-----------|-----------------|
| **TypeScript** | [TypeScript Handbook](https://www.typescriptlang.org/docs/handbook/intro.html) | Types, modules, strictness |
| **Style** | [Google TypeScript Style Guide](https://google.github.io/styleguide/tsguide.html) | Naming, imports, formatting |
| **Lint** | [typescript-eslint recommended](https://typescript-eslint.io/rules/) | CI-quality TS (when ESLint configured in package) |
| **Node.js** | [Node.js ES modules](https://nodejs.org/api/esm.html) | `import`/`export`, LTS 18+ |
| **MCP protocol** | [Model Context Protocol spec](https://modelcontextprotocol.io/) | Tool schemas, JSON-RPC transport |

**Vendor code:** Godot MCP Pro server ships inside the purchased zip — treat as **third-party**. Prefer upstream updates over large forks; document any project patches here.

---


## 2. Where TypeScript lives in this repo

| Path | Role | In git? |
|------|------|---------|
| `tools/godot-mcp-pro-server/` | MCP Pro Node server (`npm run build` → `build/index.js`) | **No** — gitignored; install via zip |
| `game/addons/godot_mcp/` | Godot editor plugin (GDScript + bridge) | **No** — gitignored |
| `.cursor/mcp.json.example` | Cursor MCP registration template | Yes |

Install:

```bash
bash tools/install_godot_mcp_pro.sh
# Success marker:
test -f tools/godot-mcp-pro-server/build/index.js && echo OK
```

Authority: [`PLUGIN_INSTALL_GUIDE.md`](../../../ops/agents/PLUGIN_INSTALL_GUIDE.md) · [`MCP_STACK.md`](../../../ops/agents/MCP_STACK.md).

---


## 3. Runtime & build

| Requirement | Value |
|-------------|-------|
| Node.js | **18+** (`node --version`) |
| Package manager | `npm` (vendor `package.json`) |
| Build output | `tools/godot-mcp-pro-server/build/index.js` |
| Cursor entry | `node …/build/index.js --minimal` |
| Godot bridge port | `6505` (`GODOT_MCP_PORT`) |

```bash
cd tools/godot-mcp-pro-server
npm install
npm run build
```

**Cursor MCP config** (from `tools/write_mcp_config.sh`):

```json
"godot-mcp-pro": {
  "command": "node",
  "args": [
    "/absolute/path/to/tools/godot-mcp-pro-server/build/index.js",
    "--minimal"
  ],
  "env": {
    "GODOT_MCP_PORT": "6505"
  }
}
```

### Mode flags (do not change without PM approval)

| Mode | Flag | Tools | Use |
|------|------|-------|-----|
| **Minimal** | `--minimal` | ~35 | **Cursor default** — L4/L5 tests only |
| Lite | `--lite` | ~84 | Tool-limit environments |
| Full | (none) | ~175 | Overlaps GDAI — **not** for Cursor agents |

**Project rule:** Always register **`--minimal`** in Cursor. Full mode duplicates GDAI scene-editing tools and violates R&R ([`MCP_STACK.md`](../../../ops/agents/MCP_STACK.md)).

---
