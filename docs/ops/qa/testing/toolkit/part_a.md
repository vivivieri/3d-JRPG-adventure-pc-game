---
id: part-a
type: reference
phase: [1, 6]
audience: [qa, builder]
status: active
authority: qa
tokens_est: 608
summary: "AI Testing — GDAI Toolkit (A)"
---
# AI Testing — GDAI Toolkit — AI Testing — GDAI Toolkit (A)

**Hub:** [`toolkit.md`](../toolkit.md)

### 11.1 Adoption matrix (external advice → this project)

| Technique | Adopt? | Layer | Notes |
|-----------|--------|-------|-------|
| **UI tree discovery** (live `Control` scan) | ✅ Yes | L3, L4 | Required for Equipment / Skills / Items / Save menus |
| **Runtime action sequences** (keypress + wait batches) | ✅ Yes | L3, L4, L5 | `ui_down`, `ui_accept`, `interact`, movement keys |
| **Viewport screenshots + visual review** | ✅ Yes | L3, L4 | Agent analyzes overlap, clipping, missing fonts |
| **Runtime GDScript injection** | ✅ Yes | L4, L5 | Edge cases: HP=1, boss phase, grant item, set flag |
| **GodotPrompter for test code** | ✅ Yes | L1, L4 | Already policy — Godot 4 APIs only, no Unity-style tests |
| **GUT (Godot Unit Test)** | ⚠️ Optional | L1 | Keep lightweight `test_runner.gd`; GUT optional Phase 4+ |
| **Godot MCP Pro** | ✅ Yes | L4, L5 | `run_test_scenario`, `assert_screen_text`, `compare_screenshots` — **test role only** (`--minimal`) |
| **Godotiq** | ✅ Yes | L3–L5 | `godotiq_signal_map`, `godotiq_trace_flow`, `godotiq_ui_map`, `godotiq_read_debug_console`, `godotiq_verify_project_runs` |
| **LimboAI / Beehave** | ❌ No (v1) | — | Turn-based enemy AI is **data-driven** (`enemies.json`) |


### 11.2 UI discovery + action sequences

**When:** Any JRPG menu, combat action select, shop, tab inventory, ending choice UI.

**Procedure:**

1. GDAI MCP: run game to target state (F5 or run scene).
2. **Discover UI elements** — walk live scene tree; collect `Control` text, name, position, `visible`, focus.
3. Plan key sequence from discovered nodes (do not hard-code stale node paths from `.tscn` files).
4. Execute batched input, e.g.:

```
Open inventory → wait 0.5s → ui_down × 3 → ui_accept → verify Equipment label updated
```

5. Screenshot immediately after; agent checks layout + Output panel.

**JRPG menus to cover (Phase 2–4):**

| Menu | Min action sequence |
|------|---------------------|
| Main menu | New Game → zone load |
| Field HUD | Open quest tracker; close |
| Dialogue | Advance to end; no soft-lock |
| Combat | Attack → Skill → Item → Defend paths |
| Shop (Roku) | Buy + sell one item |
| Save / load | Well save → menu continue |
