#!/usr/bin/env python3
"""Add zh-Hant locale strings to game/data JSON (from zh via OpenCC + overrides).

Usage:
  python3 tools/add_zh_hant_locale.py          # write files
  python3 tools/add_zh_hant_locale.py --check  # exit 1 if any zh without zh-Hant
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "game" / "data"

LOCALE_FILES = [
    DATA / "dialogue/chapter_01.json",
    DATA / "items/items.json",
    DATA / "lore/lore_entries.json",
    DATA / "quests/main_quests.json",
    DATA / "shop/roku_shop.json",
]

# Taiwan literary overrides after OpenCC (phrase-level, not just characters)
OVERRIDES: dict[str, str] = {
    "龙宫": "龍宮",
    "灵": "靈",
    "灵魂": "靈魂",
    "灵力": "靈力",
    "灵铃": "靈鈴",
    "灵刀": "靈刀",
    "灵之药": "靈之藥",
    "亡灵": "亡靈",
    "精灵": "精靈",
    "渔人": "漁人",
    "渔祭": "漁祭",
    "渔获": "漁獲",
    "废墟": "廢墟",
    "软件": "軟體",
    "回复": "恢復",
    "生命值": "生命值",
    "法力": "法力",
    "中毒": "中毒",
    "贝壳": "貝殼",
    "环贝": "環貝",
    "盐蚀": "鹽蝕",
    "龙宫禁赠之物，藏着被偷走的岁月。": "龍宮禁贈之物，藏著被偷走的歲月。",
    "你离开了。我们一直等着。": "你離開了。我們一直等著。",
    "三天。我三天就回来。": "三天。我三天就回來。",
}


def get_converter():
    try:
        from opencc import OpenCC  # type: ignore

        return OpenCC("s2twp")  # Simplified → Traditional (Taiwan, with phrases)
    except ImportError:
        return None


def to_zh_hant(zh: str, cc) -> str:
    out = cc.convert(zh) if cc else zh
    for src, dst in OVERRIDES.items():
        out = out.replace(src, dst)
    return out


def walk_locale_objects(obj, cc, missing: list[str], path: str = "") -> None:
    if isinstance(obj, dict):
        if "zh" in obj and isinstance(obj["zh"], str):
            if "zh-Hant" not in obj or not str(obj.get("zh-Hant", "")).strip():
                missing.append(path or "locale")
                if cc is not None:
                    obj["zh-Hant"] = to_zh_hant(obj["zh"], cc)
            elif cc is not None and not str(obj.get("zh-Hant", "")).strip():
                obj["zh-Hant"] = to_zh_hant(obj["zh"], cc)
        # Reorder keys: en, ja, zh, zh-Hant when all present
        if all(k in obj for k in ("en", "ja", "zh")) and "zh-Hant" in obj:
            ordered = {}
            for key in ("en", "ja", "zh", "zh-Hant"):
                if key in obj:
                    ordered[key] = obj[key]
            for key, val in obj.items():
                if key not in ordered:
                    ordered[key] = val
            obj.clear()
            obj.update(ordered)
        for k, v in obj.items():
            walk_locale_objects(v, cc, missing, f"{path}.{k}" if path else k)
    elif isinstance(obj, list):
        for i, item in enumerate(obj):
            walk_locale_objects(item, cc, missing, f"{path}[{i}]")


def process_file(path: Path, cc, check_only: bool) -> list[str]:
    missing: list[str] = []
    data = json.loads(path.read_text(encoding="utf-8"))
    walk_locale_objects(data, cc, missing)
    if check_only:
        return missing
    if cc is not None and missing:
        path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return missing


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true", help="Report missing zh-Hant only")
    args = ap.parse_args()

    cc = None if args.check else get_converter()
    if cc is None and not args.check:
        print("Install opencc-python-reimplemented: pip install opencc-python-reimplemented", file=sys.stderr)
        return 1

    err = 0
    for path in LOCALE_FILES:
        if not path.exists():
            print(f"Skip missing {path}", file=sys.stderr)
            continue
        missing = process_file(path, cc, args.check)
        if missing:
            if args.check:
                print(f"{path.relative_to(ROOT)}: {len(missing)} locale object(s) missing zh-Hant", file=sys.stderr)
                err = 1
            else:
                print(f"Updated {path.relative_to(ROOT)} (+{len(missing)} zh-Hant)")
        else:
            print(f"OK {path.relative_to(ROOT)}")

    return err


if __name__ == "__main__":
    sys.exit(main())
