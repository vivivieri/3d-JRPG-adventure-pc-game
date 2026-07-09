#!/usr/bin/env python3
"""Verify shipped art/audio assets match the documented license manifest.

Fails if unknown media files appear under game/assets/ or steam/ without a license entry.
All game art and audio must be original procedural (MIT), documented OFL fonts, or CC0 models.
"""
from __future__ import annotations

import json
import os
import sys

ROOT = os.path.join(os.path.dirname(__file__), "..")

# Extensions treated as licensable media.
MEDIA_EXT = {".png", ".ogg", ".wav", ".mp3", ".mp4", ".svg", ".ttf", ".otf", ".webp"}
MODEL_EXT = {".glb", ".obj", ".mtl", ".png"}

# Files allowed outside game/assets but in repo marketing folder.
STEAM_MEDIA = {
    "steam/capsule_main.png",
    "steam/capsule_header.png",
    "steam/capsule_small.png",
    "steam/trailer.mp4",
    "steam/screenshots/01_village.png",
    "steam/screenshots/02_caves.png",
    "steam/screenshots/03_combat.png",
    "steam/screenshots/04_palace.png",
    "steam/screenshots/05_endings.png",
    "steam/screenshots-capture/caves.png",
    "steam/screenshots-capture/caves_pool.png",
    "steam/screenshots-capture/caves_shrine.png",
    "steam/screenshots-capture/caves_water.png",
    "steam/screenshots-capture/beach.png",
    "steam/screenshots-capture/main_menu.png",
    "steam/screenshots-capture/palace.png",
    "steam/screenshots-capture/village.png",
    "steam/screenshots-capture/village_inspects.png",
}

# Basename allowlist under game/assets (procedural MIT or documented third-party).
ALLOWED = {
    # Audio — procedural MIT (tools/generate_game_audio.py)
    "game/assets/audio/bgm/menu.ogg": "MIT (repo, procedural)",
    "game/assets/audio/bgm/village.ogg": "MIT (repo, procedural)",
    "game/assets/audio/bgm/caves.ogg": "MIT (repo, procedural)",
    "game/assets/audio/bgm/palace.ogg": "MIT (repo, procedural)",
    "game/assets/audio/bgm/combat.ogg": "MIT (repo, procedural)",
    "game/assets/audio/bgm/boss.ogg": "MIT (repo, procedural)",
    "game/assets/audio/sfx/ui_confirm.ogg": "MIT (repo, procedural)",
    "game/assets/audio/sfx/ui_cancel.ogg": "MIT (repo, procedural)",
    "game/assets/audio/sfx/interact.ogg": "MIT (repo, procedural)",
    "game/assets/audio/sfx/heal.ogg": "MIT (repo, procedural)",
    "game/assets/audio/sfx/victory.ogg": "MIT (repo, procedural)",
    "game/assets/audio/sfx/defeat.ogg": "MIT (repo, procedural)",
    "game/assets/audio/sfx/hit.ogg": "MIT (repo, procedural)",
    "game/assets/audio/sfx/footstep.ogg": "MIT (repo, procedural)",
    "game/assets/audio/sfx/item.ogg": "MIT (repo, procedural)",
    "game/assets/audio/sfx/equip.ogg": "MIT (repo, procedural)",
    # Art — procedural MIT (tools/generate_game_art.py)
    "game/assets/textures/zones/village_ground.png": "MIT (repo, procedural)",
    "game/assets/textures/zones/village_wood.png": "MIT (repo, procedural)",
    "game/assets/textures/zones/cave_stone.png": "MIT (repo, procedural)",
    "game/assets/textures/zones/cave_algae.png": "MIT (repo, procedural)",
    "game/assets/textures/zones/palace_marble.png": "MIT (repo, procedural)",
    "game/assets/textures/zones/palace_gold.png": "MIT (repo, procedural)",
    "game/assets/ui/panel_dialogue.png": "MIT (repo, procedural)",
    "game/assets/ui/panel_menu.png": "MIT (repo, procedural)",
    "game/assets/ui/bar_bg.png": "MIT (repo, procedural)",
    "game/assets/ui/bar_hp_fill.png": "MIT (repo, procedural)",
    "game/assets/ui/bar_mp_fill.png": "MIT (repo, procedural)",
    "game/assets/ui/main_menu_bg.png": "MIT (repo, procedural)",
    "game/assets/ui/icon.png": "MIT (repo, procedural)",
    "game/assets/ui/icons/intent_attack.png": "MIT (repo, procedural)",
    "game/assets/ui/icons/intent_defend.png": "MIT (repo, procedural)",
    "game/assets/ui/icons/intent_magic.png": "MIT (repo, procedural)",
    "game/assets/ui/icons/intent_skull.png": "MIT (repo, procedural)",
    "game/assets/ui/portraits/urashima.png": "MIT (repo, procedural)",
    "game/assets/ui/portraits/yuzu.png": "MIT (repo, procedural)",
    "game/assets/ui/portraits/roku.png": "MIT (repo, procedural)",
    "game/assets/ui/portraits/shore_wraith.png": "MIT (repo, procedural)",
    "game/assets/ui/portraits/tide_keeper.png": "MIT (repo, procedural)",
    # Fonts — SIL OFL 1.1 (see game/assets/fonts/OFL.txt)
    "game/assets/fonts/NotoSans-Regular.ttf": "OFL 1.1",
    "game/assets/fonts/NotoSans-Bold.ttf": "OFL 1.1",
    "game/assets/fonts/NotoSansJP-Regular.otf": "OFL 1.1",
    "game/assets/fonts/NotoSansJP-Bold.otf": "OFL 1.1",
    "game/assets/fonts/NotoSansSC-Regular.otf": "OFL 1.1",
    "game/assets/fonts/NotoSansSC-Bold.otf": "OFL 1.1",
}

SKIP_NAMES = {
    "README.md",
    "ASSET_LICENSE.md",
    "OFL.txt",
    ".gitkeep",
    "LICENSE_KENNEY.txt",
    "LICENSE_POLYHAVEN.txt",
    "asset_manifest.json",
    "polyhaven_manifest.json",
    "model.path",
}


def load_model_manifest() -> set[str]:
    allowed: set[str] = set()
    for name in ("asset_manifest.json", "polyhaven_manifest.json"):
        manifest_path = os.path.join(ROOT, "game", "assets", "models", name)
        if not os.path.isfile(manifest_path):
            continue
        with open(manifest_path, encoding="utf-8") as f:
            data = json.load(f)
        for rel in data.get("files", []):
            allowed.add(f"game/assets/models/{rel}".replace("\\", "/"))
    return allowed


def iter_media(base: str, extensions: set[str]) -> list[str]:
    found: list[str] = []
    for dirpath, _, filenames in os.walk(base):
        for name in filenames:
            if name.endswith(".import") or name in SKIP_NAMES:
                continue
            ext = os.path.splitext(name)[1].lower()
            if ext in extensions:
                rel = os.path.relpath(os.path.join(dirpath, name), ROOT).replace("\\", "/")
                found.append(rel)
    return sorted(found)


def main() -> int:
    errors: list[str] = []
    model_allowed = load_model_manifest()
    checked = iter_media(os.path.join(ROOT, "game", "assets"), MEDIA_EXT)
    checked = [r for r in checked if not r.startswith("game/assets/models/")]
    models = iter_media(os.path.join(ROOT, "game", "assets", "models"), MODEL_EXT)

    for rel in checked:
        if rel not in ALLOWED:
            errors.append(f"Unlisted asset (add to docs/LICENSES.md or remove): {rel}")

    for rel in models:
        if rel not in model_allowed:
            errors.append(f"Unlisted 3D model (re-run install scripts): {rel}")

    for rel in STEAM_MEDIA:
        path = os.path.join(ROOT, rel)
        if not os.path.isfile(path):
            errors.append(f"Missing documented Steam media: {rel}")

    extra_steam = [
        r
        for r in iter_media(os.path.join(ROOT, "steam"), MEDIA_EXT)
        if r not in STEAM_MEDIA and not r.endswith(".md") and not r.endswith(".txt")
    ]
    for rel in extra_steam:
        errors.append(f"Unlisted Steam media: {rel}")

    if errors:
        print("ASSET LICENSE CHECK FAILED", file=sys.stderr)
        for e in errors:
            print(f"  - {e}", file=sys.stderr)
        return 1

    total = len(checked) + len(models)
    print(f"OK — {total} game assets ({len(models)} CC0 models) + {len(STEAM_MEDIA)} Steam files match manifest.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
