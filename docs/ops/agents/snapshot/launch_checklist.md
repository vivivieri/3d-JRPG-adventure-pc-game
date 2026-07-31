---
id: launch-checklist
type: tutorial
phase: [0, 1]
audience: [pm, builder, architect]
status: active
authority: ops
tokens_est: 503
summary: "Launch checklist every session"
---
# Cloud Snapshot Launch — Launch checklist every session

**Hub:** [`CLOUD_SNAPSHOT_LAUNCH.md`](../CLOUD_SNAPSHOT_LAUNCH.md)

## 3. Launch checklist (every implementation session)

### Before starting the agent

- [ ] Open [Cloud Agents → Environments](https://cursor.com/dashboard/cloud-agents/environments/r/github.com/vivivieri/3d-jrpg-adventure-pc-game) (not a bare “new chat” on `main`)
- [ ] Branch = **`game/development`**
- [ ] Snapshot in dashboard matches `snapshot-20260714-8addf87a-f344-489f-bbe2-da0f57cb66d8` (or newer if rebuilt)
- [ ] **Cursor Secrets** set — see `docs/ops/agents/CURSOR_SECRETS_SETUP.md` (`GAMELAB_API_KEY`, `GH_TOKEN`, webhooks, etc.)
- [ ] **Dashboard → Integrations & MCP** — all four servers registered:

| Server | Transport | Notes |
|--------|-----------|-------|
| `godot-mcp` | stdio (`uv run …/gdai_mcp_server.py`) | Requires GDAI plugin in snapshot |
| `godotiq` | stdio (`uvx godotiq`) | |
| `godot-mcp-pro` | stdio (`node …/index.js --minimal`) | |
| `gamelab-mcp` | `mcp-remote` bridge | SSE-only server — see §5 |

### First commands in the agent (after boot)

```bash
bash tools/ensure_mcp_stack.sh
bash tools/check_mcp_ready.sh
bash tools/check_rr_compliance.sh
bash tools/check_extended_toolchain.sh
```

### Verify snapshot boot (agent or Setup Agent)

Ask the agent to run **cursor-cloud `environment-info`**, or check boot metadata with `bash tools/check_snapshot_boot.sh`:

| Check | Snapshot boot PASS | JIT boot FAIL |
|-------|-------------------|---------------|
| `build` | Has `buildId` / `snapshotId` | `null` |
| `godot4` in PATH | Yes | No |
| `game/addons/gdai-mcp-plugin-godot/` | Present | Missing |
| `curl -sf http://127.0.0.1:3571/tools` | JSON response | Connection refused |

If any FAIL → **STOP** scene work; fix launch path or rebuild snapshot (§4).

---
