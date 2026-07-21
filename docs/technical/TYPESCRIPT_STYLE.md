# TypeScript / Node.js Style Guide — Tides of Urashima

**Version:** 1.0
**Scope:** `tools/godot-mcp-pro-server/` (Godot MCP Pro Node server) · future project-owned TS tooling
**Hub:** [`CODING_STANDARDS_HUB.md`](CODING_STANDARDS_HUB.md)
**Not shipped:** MCP server and `game/addons/godot_mcp/` are **dev-only** — stripped before Steam export.

---

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

Authority: [`PLUGIN_INSTALL_GUIDE.md`](../agents/PLUGIN_INSTALL_GUIDE.md) · [`MCP_STACK.md`](../agents/MCP_STACK.md).

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

**Project rule:** Always register **`--minimal`** in Cursor. Full mode duplicates GDAI scene-editing tools and violates R&R ([`MCP_STACK.md`](../agents/MCP_STACK.md)).

---

## 4. Naming conventions (Google TS + project)

| Kind | Convention | Example |
|------|------------|---------|
| Files | `kebab-case.ts` or `snake_case.ts` — **match vendor** | `index.ts`, `test-runner.ts` |
| Classes / interfaces | `PascalCase` | `TestScenarioRunner`, `McpToolDefinition` |
| Functions / variables | `camelCase` | `runScenario()`, `godotPort` |
| Constants | `UPPER_SNAKE` or `const` camelCase for config objects | `DEFAULT_PORT`, `maxRetries` |
| Private fields | `#field` (TS 3.8+) or `_leadingUnderscore` — match vendor | `_ws`, `#socket` |
| MCP tool names | `snake_case` per MCP convention | `run_test_scenario`, `assert_screen_text` |
| Env vars | `UPPER_SNAKE` | `GODOT_MCP_PORT`, `GODOT_MCP_PRO_MODE` |

---

## 5. TypeScript essentials (strict profile)

When editing vendor server sources, enable or preserve strict compiler options in `tsconfig.json`:

```json
{
  "compilerOptions": {
    "strict": true,
    "noImplicitAny": true,
    "strictNullChecks": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true
  }
}
```

### Types over `any`

```typescript
interface ScenarioResult {
  passed: boolean;
  gateId: string;
  message?: string;
}

async function runScenario(id: string): Promise<ScenarioResult> {
  ...
}
```

| Use | Avoid |
|-----|-------|
| `unknown` + narrow | `any` on public APIs |
| `interface` for tool payloads | Untyped JSON blobs |
| `readonly` for config | Mutable exported constants |
| `as const` for literal unions | Magic strings |

### Imports (Google TS style)

```typescript
// External → internal → relative
import { Server } from '@modelcontextprotocol/sdk/server/index.js';

import { loadProjectConfig } from './config.js';
import type { GodotBridge } from './godot-bridge.js';
```

- Prefer **`import type`** for type-only imports
- Use `.js` extension in import paths when `moduleResolution` is `Node16`/`NodeNext` (vendor default may vary)

---

## 6. MCP server patterns

### Tool handlers

- One function per MCP tool; schema in MCP tool descriptor
- Validate inputs at boundary; return structured errors to agent
- **Never** mutate `.tscn` in `--minimal` mode — testing/assertions only

```typescript
// Illustrative — actual names follow vendor package
server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const { name, arguments: args } = request.params;
  switch (name) {
    case 'run_test_scenario':
      return await handleRunTestScenario(args);
    default:
      throw new McpError(ErrorCode.MethodNotFound, `Unknown tool: ${name}`);
  }
});
```

### Error handling

| Layer | Pattern |
|-------|---------|
| Godot bridge down | Clear error: editor not running / port 6505 closed |
| Scenario timeout | Return FAIL with gate id — do not hang |
| Uncaught exception | Log to stderr; exit non-zero on boot failure only |

### Logging

- `console.error()` for operational errors (visible in Cursor MCP logs)
- Do not log secrets (`GAMELAB_API_KEY`, tokens)
- Structured prefix: `[godot-mcp-pro] …`

---

## 7. Project R&R (what agents may edit)

| Area | Agent may edit? | Notes |
|------|-----------------|-------|
| `tools/godot-mcp-pro-server/` TypeScript | **Rarely** — patch only with PM approval | Prefer vendor zip update |
| `game/addons/godot_mcp/` GDScript plugin | **No** — vendor | Enable in editor only |
| `.cursor/mcp.json.example` | Yes | Paths + `--minimal` |
| `tools/write_mcp_config.sh` | Yes | Path generation |
| `tools/install_godot_mcp_pro.sh` | Yes | Install automation |
| L4/L5 test scenarios | Yes — `game/data/qa/integration_scenarios.json` | Consumed by MCP Pro |

**Scene editing** remains **GDAI MCP** (`godot-mcp`) — never add scene-mutation tools to a project fork of MCP Pro.

---

## 8. ESLint / Prettier (when present in vendor package)

If `package.json` includes lint scripts, run before committing patches:

```bash
cd tools/godot-mcp-pro-server
npm run lint    # if defined
npm run build   # required — CI checks build/index.js
```

Align with [typescript-eslint recommended](https://typescript-eslint.io/rules/):

| Rule | Expectation |
|------|-------------|
| `@typescript-eslint/no-explicit-any` | warn/error on new code |
| `@typescript-eslint/consistent-type-imports` | `import type` |
| `no-unused-vars` | Clean build |
| `eqeqeq` | Use `===` |

If vendor ships no ESLint, rely on `strict` `tsc` and `npm run build` zero errors.

---

## 9. Security

| Rule | Detail |
|------|--------|
| No secrets in TS source | Env vars only |
| No arbitrary `eval` / `Function` on agent input | Injection risk |
| WebSocket to `127.0.0.1` only | Local Godot bridge |
| Ship build | `game/addons/godot_mcp/` disabled — `ship_security.json` |

---

## 10. Testing MCP Pro integration

```bash
bash tools/ensure_mcp_stack.sh
bash tools/check_mcp_ready.sh
# build/index.js must exist
test -f tools/godot-mcp-pro-server/build/index.js
```

L4/L5 scenarios: [`AI_TESTING_SPEC.md`](../qa/AI_TESTING_SPEC.md) · `bash tools/run_integration_tests.sh`

---

## 11. Anti-patterns

| Don't | Why |
|-------|-----|
| Register MCP Pro **without** `--minimal` in Cursor | Overlaps GDAI; R&R violation |
| Commit `node_modules/` or `build/` | Gitignored; snapshot installs |
| Fork server to add scene editors | Use GDAI MCP |
| `any` on tool argument types | Breaks agent contracts |
| Hardcode `/workspace` paths | Use env or `path.resolve` from config |
| Ship plugin in Steam build | `export_strip_dev_plugins` removes it |

---

## 12. PR checklist (TypeScript / MCP)

- [ ] Change is necessary — vendor update preferred over fork
- [ ] `npm run build` succeeds; `build/index.js` updated in dev env
- [ ] `bash tools/check_typescript_lint.sh` (`L1_typescript_lint`) when MCP Pro installed
- [ ] `--minimal` still default in `write_mcp_config.sh` / `.cursor/mcp.json.example`
- [ ] No new scene-editing MCP tools
- [ ] `bash tools/check_mcp_ready.sh` passes on `game/development`
- [ ] L4/L5 docs updated if scenario tools changed
- [ ] No secrets in diff

---

## 13. Quick reference links

- [TypeScript Handbook](https://www.typescriptlang.org/docs/handbook/intro.html)
- [Google TypeScript Style Guide](https://google.github.io/styleguide/tsguide.html)
- [Model Context Protocol](https://modelcontextprotocol.io/)
- Project: [`MCP_STACK.md`](../agents/MCP_STACK.md) · [`PLUGIN_INSTALL_GUIDE.md`](../agents/PLUGIN_INSTALL_GUIDE.md) · [`AI_TESTING_SPEC.md`](../qa/AI_TESTING_SPEC.md)
