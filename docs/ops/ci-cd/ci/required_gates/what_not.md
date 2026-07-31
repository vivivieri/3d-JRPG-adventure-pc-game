---
id: what-not
type: reference
audience: [release, qa, pm]
phase: [6, 8]
status: active
authority: ci-cd
tokens_est: 345
summary: "What CI does not run"
---
# CI Required Gates — What CI does not run

**Hub:** [`required_gates.md`](../required_gates.md)

## 3. What CI does **not** run

These are **agent-local or ship-only** — intentionally excluded from GitHub Actions:

| Check | Why excluded | Where it runs |
|-------|--------------|---------------|
| `check_mcp_ready.sh` | Commercial GDAI plugin + live editor | `install_cloud_dev.sh`, Cursor cloud agents |
| L3_gdai_f5 (full viewport) | Requires Godot editor + GDAI MCP F5 | Per-scene agent tasks |
| `L2_windows_export_run` | Requires Windows host | `game-ci.yml` **windows-latest** job (not ubuntu `run_ci_checks.sh`) |
| L2 visual/audio/model jury | Needs screenshots + LLM API keys | `run_playtest_smoke.sh` when assets exist |
| L5 E2E three endings | Needs Godot MCP Pro + playable build | Phase 6 gate, release candidates |
| L6 human playtest | Human-only — **required ship gate** | `docs/ops/qa/PLAYTEST_SCRIPT.md` after L0–L5 (Phase 8 prod CD) |

**Rule:** Exit **2** = SKIP. On `main`, SKIP is allowed for game-only gates. On `game/development`, `tools/gate_lib.sh` treats SKIP as **FAIL** for required gates (`global_rules.skip_is_not_pass`). Ship/M5 still requires real PASS with evidence — not SKIP.

---
