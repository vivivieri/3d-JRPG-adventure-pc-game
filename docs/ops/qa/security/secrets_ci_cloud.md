---
id: secrets-ci-cloud
type: reference
phase: [1, 6]
audience: [release, pm, architect]
status: active
authority: qa
tokens_est: 442
summary: "Secrets, CI gates, cloud factory"
---
# Security — Secrets, CI gates, cloud factory

**Hub:** [`SECURITY.md`](../SECURITY.md)

## 3. Secrets policy

| Rule | Detail |
|------|--------|
| **Storage** | Cursor Secrets + GitHub Actions Secrets only |
| **Never commit** | PATs, webhooks, API keys, Steam passwords, Telegram tokens |
| **Never in PRs** | Gate reports, screenshots, `artifacts/` committed to git |
| **Least privilege** | `GH_TOKEN` — issues/PRs/workflows scope; not admin unless `setup_github_project.sh` |
| **Rotate** | Webhook URLs and PATs on any leak suspicion |

**Scan:**

```bash
bash tools/check_no_secrets.sh           # L0_no_secrets
```

Patterns and allowlist: `game/data/qa/ship_security.json` → `secret_scan`.

---


## 4. CI gates

| Gate ID | Command | Branch |
|---------|---------|--------|
| `L0_no_secrets` | `bash tools/check_no_secrets.sh` | `main` + `game/development` |
| `L0_ship_build_security` | `bash tools/check_ship_build_security.sh` | `main` + `game/development` |
| `L0_player_build_protection` | `bash tools/check_player_build_protection.sh` | `main` + `game/development` |

Export smokes (`L2_linux_export_smoke`, `L2_windows_export_run`) re-run ship security after building binaries.

---


## 5. Cloud agent factory

| Risk | Mitigation |
|------|------------|
| Agent posts secret in issue/PR | Agent rules + `L0_no_secrets` |
| JIT VM without snapshot | No scene work; no perf sign-off (`PLATFORM_SUPPORT.md`) |
| Webhook abuse | Separate PM vs alert URLs; do not log full URLs |
| Commercial addons in repo | **Gitignored** — snapshot only; stripped before ship |

---
