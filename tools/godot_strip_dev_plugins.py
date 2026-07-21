#!/usr/bin/env python3
"""Strip or verify removal of dev-only MCP/GDAI plugins from project.godot for ship export."""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = ROOT / "game/data/qa/ship_security.json"

DEFAULT_AUTOLOADS = {
    "GDAIMCPRuntime",
    "GodotIQRuntime",
    "MCPScreenshot",
    "MCPInputService",
    "MCPGameInspector",
}
DEFAULT_PLUGIN_SUBSTRINGS = (
    "gdai-mcp-plugin-godot",
    "godot_mcp",
    "godotiq",
)


def load_config() -> dict:
    if CONFIG_PATH.is_file():
        return json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
    return {
        "forbidden_autoloads": sorted(DEFAULT_AUTOLOADS),
        "forbidden_editor_plugin_substrings": list(DEFAULT_PLUGIN_SUBSTRINGS),
    }


def strip_text(text: str, cfg: dict) -> str:
    autoload_keys = set(cfg.get("forbidden_autoloads") or DEFAULT_AUTOLOADS)
    plugin_substrings = tuple(cfg.get("forbidden_editor_plugin_substrings") or DEFAULT_PLUGIN_SUBSTRINGS)
    lines = text.splitlines(keepends=True)
    out: list[str] = []
    section = ""
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("[") and stripped.endswith("]"):
            section = stripped[1:-1]
            out.append(line)
            continue
        if section == "autoload":
            key = stripped.split("=", 1)[0].strip() if "=" in stripped else ""
            if key in autoload_keys:
                continue
        if section == "editor_plugins" and stripped.startswith("enabled="):
            m = re.search(r"PackedStringArray\((.*)\)", stripped)
            if m:
                parts = [p.strip().strip('"') for p in m.group(1).split(",") if p.strip()]
                kept = [p for p in parts if not any(s in p for s in plugin_substrings)]
                quoted = ", ".join(f'"{p}"' for p in kept)
                out.append(f"enabled=PackedStringArray({quoted})\n")
                continue
        out.append(line)
    return "".join(out)


def find_violations(text: str, cfg: dict) -> list[str]:
    errors: list[str] = []
    autoload_keys = set(cfg.get("forbidden_autoloads") or DEFAULT_AUTOLOADS)
    plugin_substrings = tuple(cfg.get("forbidden_editor_plugin_substrings") or DEFAULT_PLUGIN_SUBSTRINGS)
    section = ""
    for i, line in enumerate(text.splitlines(), start=1):
        stripped = line.strip()
        if stripped.startswith("[") and stripped.endswith("]"):
            section = stripped[1:-1]
            continue
        if section == "autoload" and "=" in stripped:
            key = stripped.split("=", 1)[0].strip()
            if key in autoload_keys:
                errors.append(f"line {i}: forbidden autoload {key}")
        if section == "editor_plugins" and "res://" in stripped:
            for sub in plugin_substrings:
                if sub in stripped:
                    errors.append(f"line {i}: forbidden editor plugin reference ({sub})")
    return errors


def scan_binary_forbidden(path: Path, cfg: dict | None = None) -> list[str]:
    cfg = cfg or load_config()
    forbidden = cfg.get("forbidden_ship_path_substrings") or []
    if not forbidden or not path.is_file():
        return []
    try:
        data = path.read_bytes()
    except OSError as exc:
        return [f"cannot read {path}: {exc}"]
    chunk = data[:32_000_000]
    hits = [sub for sub in forbidden if sub.encode() in chunk]
    if hits:
        return [f"{path.name} contains forbidden dev strings: {', '.join(hits)}"]
    return []


def cmd_strip(path: Path) -> int:
    cfg = load_config()
    text = path.read_text(encoding="utf-8")
    cleaned = strip_text(text, cfg)
    if cleaned != text:
        path.write_text(cleaned, encoding="utf-8")
        print(f"[OK]   stripped dev plugins from {path}")
    else:
        print(f"[OK]   no dev plugin entries in {path}")
    return 0


def cmd_check(path: Path) -> int:
    cfg = load_config()
    errors = find_violations(path.read_text(encoding="utf-8"), cfg)
    if errors:
        for err in errors:
            print(f"[FAIL] {err}", file=sys.stderr)
        return 1
    print(f"[OK]   {path} has no forbidden dev autoloads/plugins")
    return 0


def cmd_check_after_strip(path: Path) -> int:
    cfg = load_config()
    text = path.read_text(encoding="utf-8")
    cleaned = strip_text(text, cfg)
    errors = find_violations(cleaned, cfg)
    if errors:
        for err in errors:
            print(f"[FAIL] strip incomplete: {err}", file=sys.stderr)
        return 1
    print("[OK]   strip logic removes all forbidden dev entries")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)

    for name in ("strip", "check", "check-after-strip"):
        p = sub.add_parser(name)
        p.add_argument("project_godot", type=Path)

    args = parser.parse_args()
    path = args.project_godot
    if not path.is_file():
        print(f"[FAIL] missing {path}", file=sys.stderr)
        return 1

    if args.command == "strip":
        return cmd_strip(path)
    if args.command == "check":
        return cmd_check(path)
    if args.command == "check-after-strip":
        return cmd_check_after_strip(path)
    return 2


if __name__ == "__main__":
    sys.exit(main())
