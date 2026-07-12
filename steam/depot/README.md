# Steam depot build scripts (VDF templates)
#
# Replace placeholders before first upload:
#   @STEAM_APP_ID@  — your Steamworks App ID
#   @STEAM_DEPOT_ID@ — Windows depot ID
#
# Usage with steamcmd:
#   steamcmd +login "$STEAM_USERNAME" "$STEAM_PASSWORD" \
#     +run_app_build "$(pwd)/steam/depot/app_build.vdf" \
#     +quit
#
# See docs/CD.md and docs/STEAM_RELEASE_CHECKLIST.md §3.4
