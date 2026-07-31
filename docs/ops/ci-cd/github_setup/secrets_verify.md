---
id: secrets-verify
type: tutorial
phase: [6, 8]
audience: [pm, release]
status: active
authority: ci-cd
tokens_est: 256
summary: "`GH_TOKEN` is for **setup script only** — do not confuse with Steam secrets."
---
# GitHub Setup — CD secrets + verify

**Hub:** [`GITHUB_SETUP.md`](../GITHUB_SETUP.md)

## When to read

Use **GitHub Setup — CD secrets + verify** (roles: pm, release) when learning/setup for the first time Jump to a section below instead of reading end-to-end (2 sections).

## Jump to

- [3. Secrets for CD (Phase 8 only)](#3-secrets-for-cd-phase-8-only)
- [4. Verify setup](#4-verify-setup)

## 3. Secrets for CD (Phase 8 only)

**Settings → Secrets and variables → Actions**

| Secret | When needed |
|--------|-------------|
| `STEAM_USERNAME` | Steam beta/prod CD |
| `STEAM_PASSWORD` | Steam beta/prod CD |
| `STEAM_APP_ID` | After Steamworks app created |
| `STEAM_DEPOT_ID` | After Windows depot created |

`GH_TOKEN` is for **setup script only** — do not confuse with Steam secrets.

---


## 4. Verify setup

```bash
gh label list --limit 30
gh api repos/$(gh repo view -q .nameWithOwner)/environments --jq '.environments[].name'
```

Open a test issue using template **Gate failure** — labels should apply.

---
