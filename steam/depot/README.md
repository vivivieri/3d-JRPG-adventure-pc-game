# Steam depot build scripts (VDF templates)
#
# 1. Copy the example and replace placeholders (or let cd-steam.yml sed them from secrets):
#      cp steam/depot/app_build.vdf.example steam/depot/app_build.vdf
#      # @STEAM_APP_ID@  — Steamworks App ID
#      # @STEAM_DEPOT_ID@ — primary depot ID (Windows content by default)
#
# 2. Stage content (Linux + Windows):
#      bash tools/prepare_steam_depot.sh --platform all
#
# 3. Upload with steamcmd (or GitHub Actions `cd-steam.yml`):
#      steamcmd +login "$STEAM_USERNAME" "$STEAM_PASSWORD" \
#        +run_app_build "$(pwd)/steam/depot/app_build.vdf" \
#        +quit
#
# v1 ships **Linux + Windows** — see docs/qa/PLATFORM_SUPPORT.md
# See docs/ci-cd/CD.md and docs/ci-cd/STEAM_RELEASE_CHECKLIST.md §3.4
