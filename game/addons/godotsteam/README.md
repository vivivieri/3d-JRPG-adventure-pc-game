# GodotSteam integration

Tides of Urashima ships with a `SteamManager` autoload that activates when the [GodotSteam](https://godotsteam.com/) GDExtension is present.

## Setup

Binaries are installed in this repo. To reinstall from scratch:

```bash
./tools/install_godotsteam.sh
```

1. `godotsteam.gdextension` + platform libs live under `addons/godotsteam/`
2. No plugin toggle required — restart the Godot editor after install
3. Replace `game/steam_appid.txt` with your Steam App ID (default `480` = Spacewar test app)
4. Define matching achievement API names in Steamworks partner site (see `SteamManager.ACHIEVEMENTS`)

## Runtime behavior

| Environment | Behavior |
|-------------|----------|
| GodotSteam loaded + Steam running | Achievements unlock on story flags |
| No plugin / offline | Game runs normally; Steam calls are no-ops |

## Export notes

- Copy the **Windows** GodotSteam DLLs into the exported build folder alongside the `.exe`
- Ship `steam_api64.dll` from Steamworks SDK redist
- See `steam/GODOTSTEAM_SETUP.md` for depot upload checklist
