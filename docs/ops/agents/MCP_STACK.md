---
id: mcp-stack
type: how-to
phase: [0, 1]
audience: [pm, builder]
status: active
authority: ops
tokens_est: 185
summary: "Full MCP toolchain — load R&R, conflict rules, or startup"
---
# MCP Stack

**Hub** — load only the pack for your current pass.

| Pack | Topic |
|------|-------|
| [`rr_map.md`](mcp_stack/rr_map.md) | Full R&R map |
| [`conflict_rules.md`](mcp_stack/conflict_rules.md) | Role split & conflict rules |
| [`session_startup.md`](mcp_stack/session_startup.md) | Session startup every run |
| [`packs_gates.md`](mcp_stack/packs_gates.md) | Existing packs + related gates |
**Version:** 2.0
**Applies to:** `main` rebuild workflow — **Godot 4.7 stable**

## Factory hooks (registry keywords)

- Tournament gate: `L2_candidate_select`

