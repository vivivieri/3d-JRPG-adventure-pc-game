#!/usr/bin/env bash
# Shared helpers for Linux/Windows Godot export scripts.
# Source from export_linux.sh / export_windows.sh — do not execute directly.
set -euo pipefail

export_godot_env() {
  local root="${1:?root required}"
  export PATH="${HOME}/.local/bin:${PATH}"
  export XDG_DATA_HOME="${root}/.cache/godot-data"
  export XDG_CONFIG_HOME="${root}/.cache/godot-config"
  export XDG_CACHE_HOME="${root}/.cache/godot-cache"
}

export_ensure_presets() {
  local game_dir="${1:?game dir}"
  local presets="${game_dir}/export_presets.cfg"
  if [[ -f "$presets" ]]; then
    return 0
  fi
  for src in \
    "${game_dir}/export_presets.cfg.example" \
    "tools/godot_templates/export_presets.cfg.example"; do
    if [[ -f "$src" ]]; then
      cp "$src" "$presets"
      echo "    Created export_presets.cfg from ${src}"
      return 0
    fi
  done
  echo "[FAIL] Missing export_presets.cfg — add tools/godot_templates/export_presets.cfg.example"
  return 1
}

export_strip_dev_plugins_begin() {
  local project="${1:?project.godot path}"
  local backup="${2:?backup path}"
  cp "$project" "$backup"
  python3 tools/godot_strip_dev_plugins.py strip "$project"
}

export_strip_dev_plugins_restore() {
  local project="${1:?}"
  local backup="${2:?}"
  if [[ -f "$backup" ]]; then
    mv -f "$backup" "$project"
  fi
}

# Backward-compatible aliases
export_strip_gdai_begin() { export_strip_dev_plugins_begin "$@"; }
export_strip_gdai_restore() { export_strip_dev_plugins_restore "$@"; }

export_ship_protection_begin() {
  local game_dir="${1:?game dir}"
  local project="${2:?project.godot}"
  local presets="${game_dir}/export_presets.cfg"
  local presets_bak="${3:?presets backup}"
  local require="${SHIP_RELEASE:-0}"

  if [[ -f "$presets" ]]; then
    cp "$presets" "$presets_bak"
  fi

  local args=(python3 tools/export_apply_pck_encryption.py apply --game-dir "$game_dir")
  if [[ "$require" == "1" ]]; then
    args+=(--require)
  fi
  "${args[@]}" || return 1
}

export_ship_protection_restore() {
  local game_dir="${1:?}"
  local presets_bak="${2:?}"
  local presets="${game_dir}/export_presets.cfg"
  if [[ -f "$presets_bak" ]]; then
    mv -f "$presets_bak" "$presets"
  fi
  rm -f "${game_dir}/.godot/export_credentials.cfg"
}

export_require_godot() {
  if ! command -v godot4 >/dev/null 2>&1; then
    echo "[FAIL] godot4 not in PATH. Run: bash tools/install_cloud_dev.sh (Linux) or tools/install_ci_deps_windows.sh (Windows)"
    return 1
  fi
}

export_pre_checks() {
  python3 tools/validate_story_data.py
  bash tools/check_asset_compliance.sh || {
    echo "[WARN] Asset compliance reported issues — review before Steam upload"
  }
  bash tools/check_ship_build_security.sh || {
    echo "[WARN] Ship security pre-check reported issues"
  }
}

is_windows_host() {
  case "$(uname -s 2>/dev/null || echo unknown)" in
    MINGW*|MSYS*|CYGWIN*|Windows*) return 0 ;;
  esac
  [[ "${OS:-}" == "Windows_NT" ]]
}
