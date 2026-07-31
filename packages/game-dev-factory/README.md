# game-dev-factory

Portable **PM + multi-agent development lifecycle** pack for similar game projects.

Authority: [`CONTROL_PLANE.md`](CONTROL_PLANE.md)

## Layout

| Path | Role |
|------|------|
| `CONTROL_PLANE.md` | Cut line — control plane vs game plugin |
| `python/factory_paths.py` | Path seam (`FACTORY_*` env) — sync with `tools/` |
| `python/factory_env.sh` | Bash path seam — sync with `tools/` |
| `templates/` | Empty JSON starters (`{{PROJECT}}` placeholders) |
| `schemas/` | Minimal shape notes for validators |
| `skills/` | Cursor agent skills (`SKILL.md`) |

## Skills

| Skill | When to load |
|-------|----------------|
| `skills/pm-session` | PM / Sprint Master session start |
| `skills/worker-session` | Architect/Builder/QA/Flow/Release/Visual session |
| `skills/factory-bootstrap` | First-time factory install in a new repo |

## Validate (this monorepo)

```bash
python3 tools/validate_game_dev_factory_pack.py
python3 tools/factory_paths.py
```

## Next layers (not MVP)

Watchdog Actions templates · pluggable Telegram · docs pack router submodule ·
alignment audit engine with domain plugins.
