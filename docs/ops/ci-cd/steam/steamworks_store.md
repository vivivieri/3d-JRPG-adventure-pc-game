---
id: steamworks-store
type: how-to
phase: [6, 8]
audience: [release, pm]
status: active
authority: ci-cd
tokens_est: 651
summary: "Steam Release Checklist — Steamworks + store/marketing — covers 3. Steamworks — platform setup; 4. Store page & marketing"
---
# Steam Release Checklist — Steamworks + store/marketing

**Hub:** [`STEAM_RELEASE_CHECKLIST.md`](../STEAM_RELEASE_CHECKLIST.md)

## When to read

Use **Steam Release Checklist — Steamworks + store/marketing** (roles: release, pm) when executing this procedure Jump to a section below instead of reading end-to-end (2 sections).

## Jump to

- [3. Steamworks — platform setup](#3-steamworks-platform-setup)
- [4. Store page & marketing](#4-store-page-marketing)


## 3. Steamworks — platform setup

| # | Item | Status | Notes |
|---|------|--------|-------|
| 3.1 | Steamworks partner account | ❌ | $100 USD registration; tax/bank info |
| 3.2 | Steam App ID assigned | ❌ | `prepare_steam_depot.sh` uses test id **480** |
| 3.3 | Windows depot created | ❌ | Depot ID → GitHub Secret `STEAM_DEPOT_ID` |
| 3.4 | Depot VDF (`app_build_*.vdf`, `depot_build_*.vdf`) | ❌ | Not in repo — create in `steam/depot/` |
| 3.5 | `steamcmd` + build account | ❌ | For `cd-steam.yml` |
| 3.6 | GitHub Secrets (`STEAM_*`) | ❌ | See `docs/ops/ci-cd/CD.md` §5 |
| 3.7 | Achievements registered in Steamworks | ❌ | 13 APIs per `ACHIEVEMENTS.md` / `achievements.json` |
| 3.8 | Achievement icons (64×64) | ❌ | Upload per achievement in partner site |
| 3.9 | Beta branch + playtest keys | ❌ | Internal testers before prod |
| 3.10 | Steam DRM / depots config | ✅ | **Policy: none** — `ship_security.json` → `steam_drm`; achievements via Steam API |

---


## 4. Store page & marketing

| # | Item | Status | Notes |
|---|------|--------|-------|
| 4.1 | Store copy EN | ✅ | `steam/STORE_PAGE.md` |
| 4.2 | Store copy JA | ❌ | `STORE_PAGE_ja.md` referenced but **not created** |
| 4.3 | Store copy ZH (Simplified) | ❌ | `STORE_PAGE_zh.md` **not created** |
| 4.4 | Store copy zh-Hant | ✅ | `steam/STORE_PAGE_zh-Hant.md` |
| 4.5 | Trailer EN / JA / ZH / zh-Hant | ✅ | `steam/trailer*.mp4` (~75s each) |
| 4.6 | Trailer BGM | ✅ | `steam/trailer_bgm.ogg` |
| 4.7 | Header capsule 1232×706 | ❌ | `steam/capsule_header.png` missing |
| 4.8 | Main capsule 616×353 | ❌ | `steam/capsule_main.png` missing |
| 4.9 | Small capsule 231×87 | ❌ | `steam/capsule_small.png` missing |
| 4.10 | Library hero 3840×1240 | ❌ | TODO in STORE_PAGE |
| 4.11 | Screenshots 1920×1080 (5+) | ❌ | `steam/screenshots/` **empty** — need M5 3D captures |
| 4.12 | Tags & categories set | 🟡 | Listed in STORE_PAGE; not live on Steamworks |
| 4.13 | Pricing (USD + regions) | 🟡 | Suggested $4.99–$7.99; not configured |
| 4.14 | Release date / Coming Soon | ❌ | Business decision |
| 4.15 | Wishlist campaign / press kit | ❌ | Non-technical marketing |

---
