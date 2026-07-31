---
id: part-b
type: reference
phase: [1, 6]
audience: [qa, builder]
status: active
authority: qa
tokens_est: 657
summary: "AI Testing — GDAI Toolkit (B)"
---
# AI Testing — GDAI Toolkit — AI Testing — GDAI Toolkit (B)

**Hub:** [`toolkit.md`](../toolkit.md)

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
