---
id: architecture-prereqs
type: how-to
phase: [0, 1]
audience: [builder, pm, architect]
status: active
authority: ops
tokens_est: 184
summary: "curl -LsSf https://astral.sh/uv/install.sh | sh"
---
# GDAI Cloud Setup — Prerequisites

**Hub:** [`GDAI_CLOUD_SETUP.md`](../GDAI_CLOUD_SETUP.md)

## 1. Prerequisites

### `uv` (required by GDAI)

**macOS / Linux:**

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
uv --version
```

**Windows (PowerShell):**

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.sh | iex"
```

### Godot 4.7 stable

Open `game/project.godot` in Godot **4.7** (Forward+). Cloud: `bash tools/install_cloud_dev.sh`. See `docs/engineering/technical/TECH_STACK.md`.

---
