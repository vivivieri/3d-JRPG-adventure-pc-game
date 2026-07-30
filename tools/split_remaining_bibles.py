#!/usr/bin/env python3
"""Split remaining fat design/engineering bibles into hubs + packs."""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"


def strip_fm(text: str) -> str:
    if text.startswith("---\n"):
        return re.sub(r"^---\n.*?\n---\n", "", text, count=1, flags=re.S)
    return text


def split_by_h2(text: str) -> tuple[str, list[tuple[str, str]]]:
    lines = text.splitlines(keepends=True)
    preamble: list[str] = []
    sections: list[tuple[str, str]] = []
    current_heading = ""
    current_body: list[str] = []
    seen = False
    for line in lines:
        if line.startswith("## "):
            if seen:
                sections.append((current_heading, "".join(current_body)))
            else:
                while preamble and preamble[-1].strip() == "":
                    preamble.pop()
                preamble.append("\n")
            seen = True
            current_heading = line.strip()
            current_body = [line]
        elif not seen:
            preamble.append(line)
        else:
            current_body.append(line)
    if seen:
        sections.append((current_heading, "".join(current_body)))
    return "".join(preamble), sections


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not content.endswith("\n"):
        content += "\n"
    path.write_text(content, encoding="utf-8")
    print(f"write {path.relative_to(ROOT)} ({len(content)} bytes)")


def fm(rel: str, doc_type: str, audience: list[str], authority: str) -> str:
    path = DOCS / rel
    tokens = max(400, path.stat().st_size // 4) if path.is_file() else 800
    aud = ", ".join(audience)
    return (
        "---\n"
        f"id: {Path(rel).stem.lower().replace('_', '-')}\n"
        f"type: {doc_type}\n"
        f"audience: [{aud}]\n"
        f"status: active\n"
        f"authority: {authority}\n"
        f"tokens_est: {tokens}\n"
        "---\n\n"
    )


def by_num(sections: list[tuple[str, str]]) -> dict[str, tuple[str, str]]:
    out: dict[str, tuple[str, str]] = {}
    for heading, body in sections:
        match = re.match(r"##\s+(\d+)", heading)
        if match:
            out[match.group(1)] = (heading, body)
    return out


def split_character_bible() -> None:
    src = DOCS / "design/art/CHARACTER_BIBLE.md"
    text = strip_fm(src.read_text(encoding="utf-8"))
    preamble, sections = split_by_h2(text)
    nums = by_num(sections)
    pack_dir = DOCS / "design/art/characters"
    # Packs written below (sections 2–11; animation merges 8+9, export merges 10+11).
    write(
        pack_dir / "urashima.md",
        "# Character — Urashima\n\n**Hub:** [`CHARACTER_BIBLE.md`](../CHARACTER_BIBLE.md)\n\n"
        + nums["2"][1],
    )
    write(
        pack_dir / "yuzu.md",
        "# Character — Yuzu\n\n**Hub:** [`CHARACTER_BIBLE.md`](../CHARACTER_BIBLE.md)\n\n"
        + nums["3"][1],
    )
    write(
        pack_dir / "roku.md",
        "# Character — Roku\n\n**Hub:** [`CHARACTER_BIBLE.md`](../CHARACTER_BIBLE.md)\n\n"
        + nums["4"][1],
    )
    write(
        pack_dir / "otohime.md",
        "# Character — Otohime\n\n**Hub:** [`CHARACTER_BIBLE.md`](../CHARACTER_BIBLE.md)\n\n"
        + nums["5"][1],
    )
    write(
        pack_dir / "enemies.md",
        "# Characters — Enemies\n\n**Hub:** [`CHARACTER_BIBLE.md`](../CHARACTER_BIBLE.md)\n\n"
        + nums["6"][1],
    )
    write(
        pack_dir / "npc_ambient.md",
        "# Characters — NPC / ambient\n\n**Hub:** [`CHARACTER_BIBLE.md`](../CHARACTER_BIBLE.md)\n\n"
        + nums["7"][1],
    )
    write(
        pack_dir / "animation_portraits.md",
        "# Characters — Animation & portraits\n\n**Hub:** [`CHARACTER_BIBLE.md`](../CHARACTER_BIBLE.md)\n\n"
        + nums["8"][1]
        + nums["9"][1],
    )
    write(
        pack_dir / "export_order.md",
        "# Characters — Export & production order\n\n**Hub:** [`CHARACTER_BIBLE.md`](../CHARACTER_BIBLE.md)\n\n"
        + nums["10"][1]
        + nums["11"][1],
    )
    hub = [preamble.rstrip() + "\n", nums["1"][1]]
    hub.append(
        "## Character packs (progressive disclosure)\n\n"
        "Load the hub + one character/pack — not the whole bible.\n\n"
        "| Pack | Path |\n"
        "|------|------|\n"
        "| Urashima | [characters/urashima.md](characters/urashima.md) |\n"
        "| Yuzu | [characters/yuzu.md](characters/yuzu.md) |\n"
        "| Roku | [characters/roku.md](characters/roku.md) |\n"
        "| Otohime | [characters/otohime.md](characters/otohime.md) |\n"
        "| Enemies | [characters/enemies.md](characters/enemies.md) |\n"
        "| NPC / ambient | [characters/npc_ambient.md](characters/npc_ambient.md) |\n"
        "| Animation & portraits | [characters/animation_portraits.md](characters/animation_portraits.md) |\n"
        "| Export & order | [characters/export_order.md](characters/export_order.md) |\n\n"
    )
    write(src, "".join(hub))


def split_audio_production() -> None:
    src = DOCS / "design/audio/AUDIO_PRODUCTION_GUIDE.md"
    text = strip_fm(src.read_text(encoding="utf-8"))
    preamble, sections = split_by_h2(text)
    nums = by_num(sections)
    pack_dir = DOCS / "design/audio/production"
    write(
        pack_dir / "bgm_and_scene_map.md",
        "# Audio production — BGM & scene map\n\n"
        "**Hub:** [`AUDIO_PRODUCTION_GUIDE.md`](../AUDIO_PRODUCTION_GUIDE.md)\n\n"
        + nums["3"][1]
        + nums["4"][1],
    )
    write(
        pack_dir / "combat_sfx.md",
        "# Audio production — Combat & SFX\n\n"
        "**Hub:** [`AUDIO_PRODUCTION_GUIDE.md`](../AUDIO_PRODUCTION_GUIDE.md)\n\n"
        + nums["5"][1]
        + nums["6"][1]
        + nums["7"][1],
    )
    write(
        pack_dir / "mix_impl_qa.md",
        "# Audio production — Mix, implementation, QA\n\n"
        "**Hub:** [`AUDIO_PRODUCTION_GUIDE.md`](../AUDIO_PRODUCTION_GUIDE.md)\n\n"
        + nums["8"][1]
        + nums["9"][1]
        + nums["10"][1]
        + nums["11"][1],
    )
    hub = [preamble.rstrip() + "\n", nums["1"][1], nums["2"][1]]
    hub.append(
        "## Production packs (progressive disclosure)\n\n"
        "| Pack | Path |\n"
        "|------|------|\n"
        "| BGM + scene map | [production/bgm_and_scene_map.md](production/bgm_and_scene_map.md) |\n"
        "| Combat + SFX | [production/combat_sfx.md](production/combat_sfx.md) |\n"
        "| Mix / impl / QA | [production/mix_impl_qa.md](production/mix_impl_qa.md) |\n\n"
    )
    write(src, "".join(hub))


def split_data_architecture() -> None:
    src = DOCS / "engineering/technical/DATA_ARCHITECTURE.md"
    text = strip_fm(src.read_text(encoding="utf-8"))
    preamble, sections = split_by_h2(text)
    nums = by_num(sections)
    pack_dir = DOCS / "engineering/technical/data"
    write(
        pack_dir / "story_spine.md",
        "# Data architecture — Story spine\n\n"
        "**Hub:** [`DATA_ARCHITECTURE.md`](../DATA_ARCHITECTURE.md)\n\n"
        + nums["3"][1]
        + nums["4"][1]
        + nums["5"][1]
        + nums["7"][1],
    )
    write(
        pack_dir / "combat_economy.md",
        "# Data architecture — Combat & economy\n\n"
        "**Hub:** [`DATA_ARCHITECTURE.md`](../DATA_ARCHITECTURE.md)\n\n"
        + nums["6"][1]
        + nums["8"][1]
        + nums["9"][1]
        + nums["10"][1]
        + nums["11"][1]
        + nums["18"][1],
    )
    write(
        pack_dir / "i18n_validation.md",
        "# Data architecture — i18n, validation, schema\n\n"
        "**Hub:** [`DATA_ARCHITECTURE.md`](../DATA_ARCHITECTURE.md)\n\n"
        + nums["12"][1]
        + nums["13"][1]
        + nums["14"][1]
        + nums["15"][1]
        + nums["16"][1]
        + nums["17"][1],
    )
    hub = [preamble.rstrip() + "\n", nums["1"][1], nums["2"][1]]
    hub.append(
        "## Data packs (progressive disclosure)\n\n"
        "| Pack | Path |\n"
        "|------|------|\n"
        "| Story spine / flags / dialogue | [data/story_spine.md](data/story_spine.md) |\n"
        "| Combat & economy | [data/combat_economy.md](data/combat_economy.md) |\n"
        "| i18n / validation / schema | [data/i18n_validation.md](data/i18n_validation.md) |\n\n"
    )
    write(src, "".join(hub))


def stamp_new_packs() -> None:
    sys.path.insert(0, str(ROOT / "tools"))
    from apply_docs_packs_frontmatter import format_frontmatter, infer_frontmatter

    for path in DOCS.rglob("*.md"):
        rel = path.relative_to(DOCS).as_posix()
        if not any(
            rel.startswith(p)
            for p in (
                "design/art/characters/",
                "design/audio/production/",
                "engineering/technical/data/",
            )
        ):
            # also re-stamp hubs we rewrote
            if path.name not in {
                "CHARACTER_BIBLE.md",
                "AUDIO_PRODUCTION_GUIDE.md",
                "DATA_ARCHITECTURE.md",
            }:
                continue
        text = path.read_text(encoding="utf-8")
        if text.startswith("---\n"):
            text = strip_fm(text)
        meta = infer_frontmatter(rel)
        path.write_text(format_frontmatter(meta) + text, encoding="utf-8")
        print(f"stamp {rel}")


def main() -> int:
    split_character_bible()
    split_audio_production()
    split_data_architecture()
    stamp_new_packs()
    for rel in (
        "design/art/CHARACTER_BIBLE.md",
        "design/audio/AUDIO_PRODUCTION_GUIDE.md",
        "engineering/technical/DATA_ARCHITECTURE.md",
    ):
        print(f"size {rel}: {(DOCS / rel).stat().st_size}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
