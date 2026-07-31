---
id: naming-strict-mcp
type: reference
phase: [1, 2, 3, 4, 5, 6]
audience: [architect, builder]
status: active
authority: engineering
tokens_est: 856
summary: "Naming, strict TS, MCP patterns"
---
# TypeScript Style — Naming, strict TS, MCP patterns

**Hub:** [`TYPESCRIPT_STYLE.md`](../TYPESCRIPT_STYLE.md)

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
