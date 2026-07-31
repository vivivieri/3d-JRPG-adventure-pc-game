---
id: map-preprod
type: reference
phase: [6, 8]
audience: [pm, release]
status: active
authority: ci-cd
tokens_est: 568
summary: "Environments — Environment map + preprod necessity — game/development ──CI──► QA (automated)"
---
# Environments — Environment map + preprod necessity

**Hub:** [`ENVIRONMENTS.md`](../ENVIRONMENTS.md)

## When to read

Use **Environments — Environment map + preprod necessity** (roles: pm, release) when you need this reference during the current task Jump to a section below instead of reading end-to-end (2 sections).

## Jump to

- [1. Environment map](#1-environment-map)
- [2. Is preproduction necessary?](#2-is-preproduction-necessary)


## 1. Environment map

| Environment | Purpose | Git ref | CD / artifact | Human gate | Agent owner |
|-------------|---------|---------|---------------|------------|-------------|
| **Design** | Docs + story JSON only | `main` | — | — | PM + Architect |
| **Development** | Daily implementation | `game/development` | — | — | Builder + Architect |
| **QA** | Automated test gates | `game/development` @ CI green | — | — | QA Agent |
| **UAT** | Stakeholder / playtest builds | Tag `v*-rc*` or `v*-uat*` | `cd-artifact.yml` → GitHub Release (draft) | L6 playtest script | QA Lead + Human |
| **Preproduction** | Steam beta / near-final | Tag `v*-beta*` | `cd-steam.yml` → Steam **beta** depot | Beta testers | Release Agent |
| **Production** | Steam public | Tag `v*.*.*` | `cd-steam.yml` → Steam **default** depot | CI gates only | Release + PM |

```
main (design)
  │
game/development ──CI──► QA (automated)
  │
  ├── tag v0.8.0-uat1 ──CD artifact──► UAT (humans)
  │
  ├── tag v0.9.0-beta1 ──CD steam──► Preprod (Steam beta)
  │
  └── tag v1.0.0 ──CD steam (CI gates)──► Production
```

---


## 2. Is preproduction necessary?

**For this project (2–3 h indie, small AI team):**

| Approach | When to use |
|----------|-------------|
| **Skip separate preprod early** | Phases 1–6: UAT RC zips from `cd-artifact.yml` are enough for internal + friend playtest |
| **Add preprod at M6** | When Steamworks beta branch exists and you need real depot keys, achievements, and store-linked builds |

**Recommendation:** Treat **UAT** = internal RC artifacts; **Preproduction** = Steam beta channel only. Do not build separate infra until Phase 8 — one beta tag (`v*-beta*`) is sufficient.

Preprod is **not** a duplicate of QA. QA is automated gates on every push; preprod is a **near-ship binary** on Steam's beta branch.

---
