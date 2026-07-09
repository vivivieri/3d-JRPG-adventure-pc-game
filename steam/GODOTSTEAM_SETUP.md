# GodotSteam + Steamworks deployment

## Achievements (map in Steamworks → `SteamManager.gd`)

| API name | Trigger flag |
|----------|----------------|
| `ACH_MET_ROKU` | `met_roku` |
| `ACH_SHORE_WRAITH` | `shore_wraith_defeated` |
| `ACH_SENTINEL` | `sentinel_defeated` |
| `ACH_TIDE_KEEPER` | `tide_keeper_defeated` |
| `ACH_ENDING_REWIND` | `ending_rewind` |
| `ACH_ENDING_ANCHOR` | `ending_anchor` |
| `ACH_ENDING_DRIFT` | `ending_drift` |

## Build pipeline

```bash
# From repo root — installs Godot 4.3 + templates if missing, exports Windows build
./tools/export_windows.sh
```

Output: `build/TidesOfUrashima.exe` (embedded PCK)

## Steam depot layout

```
TidesOfUrashima/
  TidesOfUrashima.exe
  steam_api64.dll          # from Steamworks SDK
  godotsteam.windows.dll   # from GodotSteam win64 release
  steam_appid.txt          # optional for dev; remove for production depot
```

## Cloud saves (future)

`SaveSystem.SAVE_PATH` is `user://save_slot_0.json` — wire to `Steam.fileWrite` when cloud is enabled.
