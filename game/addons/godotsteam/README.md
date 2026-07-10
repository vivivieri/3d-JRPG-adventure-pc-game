# GodotSteam

**Status:** Scaffold only — binaries not committed.

## Install

```bash
bash tools/install_godotsteam.sh
```

Download GodotSteam 4.x for Windows from [Codeberg releases](https://codeberg.org/godotsteam/godotsteam/releases) and copy GDExtension files into this folder.

## Runtime

`SteamManager` autoload (`res://scripts/core/steam_manager.gd`) unlocks achievements when story flags are set. It no-ops until the GodotSteam singleton is available.

See `steam/GODOTSTEAM_SETUP.md` for depot layout and achievement API names.
