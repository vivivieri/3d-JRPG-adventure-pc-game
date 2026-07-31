---
id: rr-security-pr
type: reference
phase: [1, 2, 3, 4, 5, 6]
audience: [architect, builder]
status: active
authority: engineering
tokens_est: 1065
summary: "Scene editing remains GDAI MCP (`godot-mcp`) — never add scene-mutation tools to a project fork of MCP Pro."
---
# TypeScript Style — R&R, lint, security, testing, PR

**Hub:** [`TYPESCRIPT_STYLE.md`](../TYPESCRIPT_STYLE.md)

## When to read

Use **TypeScript Style — R&R, lint, security, testing, PR** (roles: architect, builder) when you need this reference during the current task Jump to a section below instead of reading end-to-end (7 sections).

## Jump to

- [7. Project R&R (what agents may edit)](#7-project-rr-what-agents-may-edit)
- [8. ESLint / Prettier (when present in vendor package)](#8-eslint-prettier-when-present-in-vendor-package)
- [9. Security](#9-security)
- [10. Testing MCP Pro integration](#10-testing-mcp-pro-integration)
- [11. Anti-patterns](#11-anti-patterns)
- [12. PR checklist (TypeScript / MCP)](#12-pr-checklist-typescript-mcp)
- [13. Quick reference links](#13-quick-reference-links)


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

L4/L5 scenarios: [`AI_TESTING_SPEC.md`](../../../ops/qa/AI_TESTING_SPEC.md) · `bash tools/run_integration_tests.sh`

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
- Project: [`MCP_STACK.md`](../../../ops/agents/MCP_STACK.md) · [`PLUGIN_INSTALL_GUIDE.md`](../../../ops/agents/PLUGIN_INSTALL_GUIDE.md) · [`AI_TESTING_SPEC.md`](../../../ops/qa/AI_TESTING_SPEC.md)
