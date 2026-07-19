#!/usr/bin/env python3
"""Apply PCK encryption + ship secrets for export (docs/qa/SECURITY.md §9).

PCK encryption requires export templates compiled with SCRIPT_AES256_ENCRYPTION_KEY.
Official Godot 4.7 templates do not support encrypted PCK at runtime.
"""
from __future__ import annotations

import argparse
import json
import os
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HEX_KEY_RE = re.compile(r"^[0-9a-fA-F]{64}$")


def load_ship_security() -> dict:
    path = ROOT / "game/data/qa/ship_security.json"
    return json.loads(path.read_text(encoding="utf-8"))


def validate_hex_key(key: str, name: str) -> str:
    key = key.strip()
    if not HEX_KEY_RE.match(key):
        raise SystemExit(f"[FAIL] {name} must be 64 hex chars (256-bit AES)")
    return key.lower()


def enable_presets_encryption(presets_path: Path, include_filters: str) -> None:
    text = presets_path.read_text(encoding="utf-8")
    text = re.sub(r"^encrypt_pck=false", "encrypt_pck=true", text, flags=re.MULTILINE)
    text = re.sub(r"^encrypt_directory=false", "encrypt_directory=true", text, flags=re.MULTILINE)
    text = re.sub(
        r'^encryption_include_filters="[^"]*"',
        f'encryption_include_filters="{include_filters}"',
        text,
        flags=re.MULTILINE,
    )
    presets_path.write_text(text, encoding="utf-8")


def patch_custom_template_path(presets_path: Path, platform: str, template_path: str) -> None:
    lines = presets_path.read_text(encoding="utf-8").splitlines(keepends=True)
    out: list[str] = []
    active = False
    for line in lines:
        if line.startswith('platform="') and platform in line:
            active = True
        elif line.startswith("[preset.") and ".options]" in line and active:
            active = "options"
        elif line.startswith("[preset.") and active == "options":
            active = False
        if active == "options" and line.startswith("custom_template/release="):
            line = f'custom_template/release="{template_path}"\n'
            active = False
        out.append(line)
    presets_path.write_text("".join(out), encoding="utf-8")


def write_export_credentials(game_dir: Path, key: str, preset_count: int = 2) -> Path:
    cred_dir = game_dir / ".godot"
    cred_dir.mkdir(parents=True, exist_ok=True)
    cred_path = cred_dir / "export_credentials.cfg"
    lines = ["; Generated at export — never commit\n"]
    for idx in range(preset_count):
        lines.append(f"[preset.{idx}]\n\n")
        lines.append(f'pck_encryption_key="{key}"\n')
        lines.append(f'script_encryption_key="{key}"\n\n')
    cred_path.write_text("".join(lines), encoding="utf-8")
    return cred_path


def inject_save_pepper(project_path: Path, pepper: str) -> None:
    text = project_path.read_text(encoding="utf-8")
    setting = f'config/save_hmac_pepper="{pepper}"'
    if "config/save_hmac_pepper=" in text:
        text = re.sub(
            r'config/save_hmac_pepper="[^"]*"',
            setting,
            text,
            count=1,
        )
    elif "[application]" in text:
        text = text.replace(
            "[application]\n",
            f"[application]\n\n{setting}\n",
            1,
        )
    else:
        text = f"[application]\n\n{setting}\n\n" + text
    project_path.write_text(text, encoding="utf-8")


def cmd_apply(args: argparse.Namespace) -> int:
    cfg = load_ship_security()["player_build_protection"]
    game_dir = Path(args.game_dir)
    presets = game_dir / "export_presets.cfg"
    project = game_dir / "project.godot"

    if not presets.is_file():
        print(f"[FAIL] missing {presets}")
        return 1
    if not project.is_file():
        print(f"[FAIL] missing {project}")
        return 1

    enc_key = os.environ.get(cfg["pck_encryption"]["env_key"], "").strip()
    if enc_key:
        enc_key = validate_hex_key(enc_key, cfg["pck_encryption"]["env_key"])
    elif args.require:
        print(f"[FAIL] {cfg['pck_encryption']['env_key']} required for ship export (SHIP_RELEASE=1)")
        return 1
    else:
        print(f"[WARN] {cfg['pck_encryption']['env_key']} unset — PCK encryption skipped")
        return 0

    custom_linux = os.environ.get("GODOT_CUSTOM_TEMPLATE_LINUX", "").strip() or None
    custom_windows = os.environ.get("GODOT_CUSTOM_TEMPLATE_WINDOWS", "").strip() or None
    if not custom_linux and not custom_windows:
        msg = (
            "Custom export templates not configured "
            "(GODOT_CUSTOM_TEMPLATE_LINUX / GODOT_CUSTOM_TEMPLATE_WINDOWS). "
            "Build with tools/build_godot_export_templates_encrypted.sh first."
        )
        if args.require:
            print(f"[FAIL] {msg}")
            return 1
        print(f"[WARN] {msg}")
        return 0

    include = cfg["pck_encryption"].get("encryption_include_filters_default", "*")
    enable_presets_encryption(presets, include)
    if custom_linux:
        patch_custom_template_path(presets, "Linux", custom_linux)
    if custom_windows:
        patch_custom_template_path(presets, "Windows Desktop", custom_windows)
    write_export_credentials(game_dir, enc_key)
    print(f"[OK]   PCK encryption enabled on {presets.name}")

    save_key = os.environ.get(cfg["save_integrity"]["env_hmac_key"], "").strip()
    if save_key:
        save_key = validate_hex_key(save_key, cfg["save_integrity"]["env_hmac_key"])
        inject_save_pepper(project, save_key)
        print("[OK]   save_hmac_pepper injected into project.godot for export")
    elif args.require:
        print(f"[FAIL] {cfg['save_integrity']['env_hmac_key']} required for ship export")
        return 1
    else:
        print(f"[WARN] {cfg['save_integrity']['env_hmac_key']} unset — save pepper not injected")

    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Apply ship player-build protection at export")
    parser.add_argument("command", choices=["apply"])
    parser.add_argument("--game-dir", default=str(ROOT / "game"))
    parser.add_argument(
        "--require",
        action="store_true",
        help="Fail if encryption keys or custom templates are missing (SHIP_RELEASE=1)",
    )
    args = parser.parse_args()
    if args.command == "apply":
        return cmd_apply(args)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
