---
id: local-secrets
type: how-to
phase: [6, 8]
audience: [release, pm]
status: active
authority: ci-cd
tokens_est: 305
summary: "Continuous Delivery — Local CD + Steam secrets — git checkout game/development"
---
# Continuous Delivery — Local CD + Steam secrets

**Hub:** [`CD.md`](../CD.md)

## When to read

Use **Continuous Delivery — Local CD + Steam secrets** (roles: release, pm) when executing this procedure Jump to a section below instead of reading end-to-end (2 sections).

## Jump to

- [4. Local CD (same gates as CI runner)](#4-local-cd-same-gates-as-ci-runner)
- [5. GitHub Secrets (Steam — Phase 8)](#5-github-secrets-steam-phase-8)


## 4. Local CD (same gates as CI runner)

```bash
git checkout game/development
git tag v0.1.0-rc1
git push origin v0.1.0-rc1          # triggers cd-artifact.yml

# Or locally without pushing:
bash tools/run_cd_gates.sh --channel rc
bash tools/install_godotsteam.sh
bash tools/export_linux.sh
bash tools/export_windows.sh
bash tools/prepare_steam_depot.sh --platform all
```

---


## 5. GitHub Secrets (Steam — Phase 8)

| Secret | Purpose |
|--------|---------|
| `STEAM_USERNAME` | Steamworks build account |
| `STEAM_PASSWORD` | Account password (or use Steam Guard token flow) |
| `STEAM_APP_ID` | Your game's App ID (not 480) |
| `STEAM_DEPOT_ID` | Windows depot ID from Steamworks |

Optional: store `steam/depot/*.vdf` in repo (without secrets) once App ID is assigned.

---
