# GodotSteam integration

Tides of Urashima ships with a `SteamManager` autoload that activates when the [GodotSteam](https://godotsteam.com/) GDExtension is present.

## Setup (one-time)

1. Download **GodotSteam 4.3** GDExtension for your editor OS from [GitHub releases](https://github.com/GodotSteam/GodotSteam/releases)
2. Extract into `game/addons/godotsteam/` so these exist:
   - `addons/godotsteam/godotsteam.gdextension`
   - platform libs under `addons/godotsteam/linux64/` (or win64 for Windows editor)
3. Enable the plugin: **Project → Project Settings → Plugins → GodotSteam**
4. Replace `game/steam_appid.txt` with your Steam App ID (use `480` for Spacewar testing)
5. Define matching achievement API names in Steamworks partner site (see `SteamManager.ACHIEVEMENTS`)

## Runtime behavior

| Environment | Behavior |
|-------------|----------|
| GodotSteam loaded + Steam running | Achievements unlock on story flags |
| No plugin / offline | Game runs normally; Steam calls are no-ops |

## Export notes

- Copy the **Windows** GodotSteam DLLs into the exported build folder alongside the `.exe`
- Ship `steam_api64.dll` from Steamworks SDK redist
- See `steam/GODOTSTEAM_SETUP.md` for depot upload checklist
