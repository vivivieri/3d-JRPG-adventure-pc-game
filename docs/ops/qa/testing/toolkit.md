---
id: toolkit
type: reference
phase: [1, 6]
audience: [qa, flow]
status: active
authority: qa
tokens_est: 1283
summary: "These techniques come from live-runtime MCP testing (recommended for JRPG UI-heavy flows). They extend L3–L5; they **do not** replace L0–L2 headless tests."
---
# GDAI MCP playtesting toolkit

**Hub:** [`AI_TESTING_SPEC.md`](../AI_TESTING_SPEC.md)

## 11. GDAI MCP playtesting toolkit (adopted)

These techniques come from live-runtime MCP testing (recommended for JRPG UI-heavy flows). They extend L3–L5; they **do not** replace L0–L2 headless tests.

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

### 11.3 Runtime GDScript injection (edge cases)

Use GDAI MCP to execute **short** runtime scripts for states hard to reach organically.

| Test ID | Inject example | Assert |
|---------|----------------|--------|
| `INJ-GAMEOVER-01` | Set party leader HP to 0 | Game over UI; reload works |
| `INJ-BOSS-01` | Set boss to phase 2 HP threshold | Phase banner + intent change |
| `INJ-FLAG-01` | `GameManager.set_flag("water_puzzle_solved")` | Gate opens without replaying puzzle |
| `INJ-ENDING-01` | Jump to SC-16 with Tide Keeper at low HP | Choice UI blocks attack input |

**Rules:**

- GodotPrompter writes inject snippets; GDAI MCP runs them in live session.
- Log inject script in test report.
- Prefer **unit tests** for pure math; use inject only for **UI / state integration**.

### 11.4 Example agent prompts (copy-paste)

**Combat UI smoke (Phase 4):**

```
Using GDAI MCP only: run the project, enter SC-05 tutorial combat.
Discover UI elements for the battle action menu.
Simulate ui_down twice and ui_accept to open Skills.
Capture a viewport screenshot and read the Output panel.
Report any overlapping UI text, errors, or soft-lock.
```

**Inventory equip (Phase 2+):**

```
Using GDAI MCP: from field, open the tab menu inventory.
Discover Equipment list Controls.
Navigate down 3 times, press ui_accept to equip the training sword.
Screenshot the stats panel and confirm ATK changed per items.json.
```

**Boss game-over edge case:**

```
Using GDAI MCP: start Shore Wraith encounter (SC-09).
Inject runtime GDScript to set Urashima HP to 1.
Take one enemy action that deals damage.
Verify game over screen appears and Continue returns to last save.
```

### 11.5 Division of labor (MCP stack)

| Concern | Tool |
|---------|------|
| Fire spell damage 25–30 vs fire-weak enemy | **L1 unit test** |
| Skills menu opens and lists skills | **GDAI** or **Godotiq** `godotiq_ui_map` |
| Why turn order stuck after enemy action | **Godotiq** `godotiq_trace_flow` |
| Automated scenario + on-screen text assert | **Godot MCP Pro** `run_test_scenario`, `assert_screen_text` |
| Full story three endings | **L5** headless + **Godot MCP Pro** input replay |
| Create/edit zone scene | **GDAI only** (`docs/ops/agents/MCP_STACK.md`) |
| JSON flag after quest stage | **L1 unit test** |

See `docs/ops/agents/MCP_STACK.md` for conflict rules and install.

---

