# Cursor Cloud environment config

| Branch | File | Purpose |
|--------|------|---------|
| **`main`** | `.cursor/environment.json` | `bootstrap_cloud_environment.sh` → auto-checkout `game/development` |
| **`game/development`** | `.cursor/environment.json` | Godot + MCP dev stack (snapshot + `install_cloud_dev.sh`) |

**Dev environment / Setup Agent:** Dashboard has **no branch picker**. `main`'s `.cursor/environment.json` uses `bootstrap_cloud_environment.sh` to auto-checkout `game/development` before install. `game/development` keeps snapshot + `install_cloud_dev.sh`.

Template for manual copy: `.cursor/environment.game-development.json.example`

Authority: `docs/agents/CLOUD_SNAPSHOT_LAUNCH.md` §0 · `AGENTS.md` (Setup Agent section)
