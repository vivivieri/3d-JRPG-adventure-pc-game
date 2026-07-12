# Tides of Urashima — Steam Store Page

Use this document when creating the Steamworks store listing. Localized sections match `game/locale/translations.csv` keys where noted.

---

## Game title

| Locale | Title |
|--------|-------|
| English | Tides of Urashima |
| Japanese | 浦島の潮 |
| Simplified Chinese | 浦岛潮汐 |

---

## Short description (≈300 chars)

**English:**  
A 2–3 hour stylized JRPG adapted from Urashima Tarō. Explore a ruined coastal village, descend through tidal caves, and confront the Dragon Palace Gate. Turn-based combat, three bittersweet endings, full English / Japanese / Chinese support.

**Japanese:**  
浦島太郎を題材にした約2〜3時間のスタイライズドJRPG。廃れた漁村を探索し、潮穴と竜宮の門を越えて対峙する。ターン制バトル、三つの結末、日本語・英語・中国語対応。

**简体中文:**  
改编自浦岛太郎的 2–3 小时风格化 JRPG。探索废弃渔村，穿越潮穴与龙宫之门。回合制战斗、三种结局，支持英/日/中文。

---

## About this game (long description)

**English:**

The sea returns what it claims.

**Tides of Urashima** is a short, atmospheric 3D JRPG for players who want emotional folklore — not a 40-hour grind. You play as Urashima, a fisherman who returns home to find centuries have passed in a single journey.

**Features:**
- **2–3 hour story** across three acts — village, tidal caves, Dragon Palace Gate
- **Turn-based combat** with speed initiative, boss phases, and party skills
- **Three endings** — Rewind, Anchor, or Drift — chosen during the final confrontation
- **Full localization** — English, Japanese, Simplified Chinese, Traditional Chinese (粵語 or 國語 VO)
- **Stylized coastal aesthetic** — muted ruins, bioluminescent caves, ethereal palace architecture

Walk the shore. Answer the tide.

**Japanese / 简体中文:** See `steam/STORE_PAGE_ja.md` and `steam/STORE_PAGE_zh.md` for full localized long descriptions.

---

## Tags (Steam)

Primary: `JRPG`, `Story Rich`, `Short`, `Atmospheric`, `Turn-Based Combat`

Secondary: `Singleplayer`, `3D`, `Emotional`, `Folklore`, `Indie`

---

## Price band

Suggested: **$4.99 – $7.99 USD** (short narrative game)

---

## Assets checklist

| Asset | Size | File |
|-------|------|------|
| Header capsule | 1232 × 706 | `steam/capsule_header.png` |
| Main capsule | 616 × 353 | `steam/capsule_main.png` |
| Small capsule | 231 × 87 | `steam/capsule_small.png` |
| Library hero | 3840 × 1240 | _TODO — wide key art_ |
| Screenshots | 1920 × 1080 min | `steam/screenshots/` (5 placeholders generated) |
| Trailer (EN) | 1920 × 1080 MP4 | `steam/trailer.mp4` (~68s — English on-screen text) |
| Trailer (JA) | 1920 × 1080 MP4 | `steam/trailer_ja.mp4` (~68s — Japanese on-screen text) |
| Trailer (ZH) | 1920 × 1080 MP4 | `steam/trailer_zh.mp4` (~68s — Chinese on-screen text) |
| Trailer BGM | OGG | `steam/trailer_bgm.ogg` (shared procedural score) |

---

## System requirements (Windows)

**Minimum:**
- OS: Windows 10 64-bit
- Processor: Dual-core 2.0 GHz
- Memory: 4 GB RAM
- Graphics: OpenGL 3.3 / Vulkan 1.0 compatible GPU
- Storage: 500 MB
- DirectX: Version 11

**Recommended:**
- OS: Windows 10/11 64-bit
- Memory: 8 GB RAM
- Graphics: Dedicated GPU with 2 GB VRAM

---

## Build & upload

```bash
./tools/export_windows.sh   # produces build/TidesOfUrashima.exe (~109 MB)
```

1. Open `game/project.godot` in Godot **4.7** stable (or use script above)
2. **Project → Export** → preset `Windows Desktop`
3. See `steam/GODOTSTEAM_SETUP.md` for depot layout + achievements

---

## GodotSteam note

GodotSteam plugin is **not yet integrated**. The export preset produces a standalone Windows build suitable for Steam upload once Steamworks app ID and depots are configured.
