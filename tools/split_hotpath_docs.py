#!/usr/bin/env python3
"""Split hot-path docs: ENVIRONMENT_KITS, ART_AUTOMATION_PIPELINE, ART_DIRECTION."""
from __future__ import annotations

import re
import subprocess
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


def by_num(sections: list[tuple[str, str]]) -> dict[str, str]:
    out: dict[str, str] = {}
    for heading, body in sections:
        match = re.match(r"##\s+(\d+)\b", heading)
        if match:
            out[match.group(1)] = body
        elif heading.startswith("## Related"):
            out["related"] = body
    return out


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not content.endswith("\n"):
        content += "\n"
    path.write_text(content, encoding="utf-8")
    print(f"write {path.relative_to(ROOT)} ({len(content)} bytes)")


def fm(
    stem: str,
    doc_type: str,
    audience: list[str],
    authority: str,
    tokens: int,
    phase: list[int] | None = None,
    summary: str | None = None,
) -> str:
    lines = [
        "---",
        f"id: {stem}",
        f"type: {doc_type}",
        f"audience: [{', '.join(audience)}]",
    ]
    if phase:
        lines.append(f"phase: [{', '.join(str(p) for p in phase)}]")
    lines += ["status: active", f"authority: {authority}", f"tokens_est: {tokens}"]
    if summary:
        safe = summary.replace("\n", " ").replace('"', "'").strip()
        lines.append(f'summary: "{safe}"')
    lines += ["---", ""]
    return "\n".join(lines)


def join_nums(nums: dict[str, str], keys: list[str]) -> str:
    return "\n".join(nums[k] for k in keys if k in nums).strip() + "\n"


def pack_table(subdir: str, rows: list[tuple[str, str]]) -> str:
    lines = ["| Pack | Topic |", "|------|-------|"]
    for name, label in rows:
        lines.append(f"| [`{name}`]({subdir}/{name}) | {label} |")
    lines.append("")
    return "\n".join(lines)


def load_source(rel: str) -> str:
    path = DOCS / rel
    text = path.read_text(encoding="utf-8")
    # Prefer full pre-hub blob from git if current file is already a thin hub
    if len(text) < 4000:
        try:
            blob = subprocess.check_output(
                ["git", "show", f"HEAD:docs/{rel}"],
                cwd=ROOT,
                text=True,
                stderr=subprocess.DEVNULL,
            )
            if len(blob) > len(text) * 1.5:
                return blob
        except subprocess.CalledProcessError as exc:
            print(f"WARN: git show HEAD:docs/{rel} failed: {exc}", file=sys.stderr)
    return text


def split_one(
    *,
    src_rel: str,
    pack_subdir: str,
    hub_title: str,
    hub_summary: str,
    audience: list[str],
    authority: str,
    doc_type: str,
    packs: list[tuple[str, list[str], str, list[int] | None]],
    phase: list[int] | None = None,
) -> None:
    src = DOCS / src_rel
    text = strip_fm(load_source(src_rel))
    preamble, sections = split_by_h2(text)
    nums = by_num(sections)
    pack_dir = src.parent / pack_subdir
    rows: list[tuple[str, str]] = []
    for name, keys, label, pphase in packs:
        body = join_nums(nums, keys)
        if not body.strip():
            print(f"WARN empty {name} keys={keys} available={sorted(nums)}")
            continue
        content = (
            fm(
                Path(name).stem.replace("_", "-"),
                doc_type,
                audience,
                authority,
                max(350, len(body) // 4),
                pphase or phase,
                summary=label,
            )
            + f"# {hub_title} — {label}\n\n**Hub:** [`{src.name}`](../{src.name})\n\n"
            + body
        )
        write(pack_dir / name, content)
        rows.append((name, label))
    hub = (
        fm(
            src.stem.lower().replace("_", "-"),
            doc_type,
            audience,
            authority,
            700,
            phase,
            summary=hub_summary,
        )
        + f"# {hub_title}\n\n**Hub** — load one pack for the zone/workflow you are on.\n\n"
        + pack_table(pack_subdir, rows)
        + preamble.strip()
        + "\n"
    )
    write(src, hub)


def main() -> int:
    split_one(
        src_rel="design/world/ENVIRONMENT_KITS.md",
        pack_subdir="env_kits",
        hub_title="Environment Kits",
        hub_summary="Per-zone lighting, kits, LOD — load only the active zone pack",
        audience=["builder", "builder_zone", "visual"],
        authority="world",
        doc_type="reference",
        phase=[1, 5],
        packs=[
            ("global_shared.md", ["1", "2"], "Global rules & shared kit", [1, 5]),
            ("beach_shore.md", ["3"], "Zone beach_shore", [1]),
            ("ruined_village.md", ["4"], "Zone ruined_village hub", [1]),
            ("tidal_caves.md", ["5"], "Zone tidal_caves", [1, 5]),
            ("dragon_palace.md", ["6", "7"], "Palace + endings", [5, 6]),
            ("lore_lod_production.md", ["8", "9", "10", "11"], "Lore, LOD, production, acceptance", [1, 5]),
        ],
    )
    split_one(
        src_rel="design/art/ART_AUTOMATION_PIPELINE.md",
        pack_subdir="automation",
        hub_title="Art Automation Pipeline",
        hub_summary="Tool tiers and workflows — load the asset class you are generating",
        audience=["visual", "builder"],
        authority="art",
        doc_type="how-to",
        phase=[5],
        packs=[
            ("tiers_requirements.md", ["1", "2"], "Tier matrix & MCP requirements", [1, 5]),
            ("zone_textures.md", ["3"], "Zone texture workflow", [1, 5]),
            ("ui_art.md", ["4"], "UI art (GameLab)", [5]),
            ("characters_props.md", ["5"], "3D character & prop workflow", [5]),
            ("palette_audio_gates.md", ["6", "7", "8"], "Palette remap, audio, M5 gates", [5]),
            ("pay_reject_related.md", ["9", "10", "related"], "Pay vs free, rejected tools, related", [5]),
        ],
    )
    split_one(
        src_rel="design/art/ART_DIRECTION.md",
        pack_subdir="direction",
        hub_title="Art Direction",
        hub_summary="Palette, silhouettes, style rules — load the section for your pass",
        audience=["visual", "builder"],
        authority="art",
        doc_type="reference",
        phase=[1, 5],
        packs=[
            ("palette.md", ["1"], "Color palette", [1, 5]),
            ("characters_env_ui.md", ["2", "3", "4"], "Silhouettes, environment, UI style", [1, 5]),
            ("budgets_sourcing.md", ["5", "6"], "Poly budgets & asset sourcing", [1, 5]),
            ("pipeline_mood_avoid.md", ["7", "8", "9"], "AI→Godot pipeline, mood, avoid list", [1, 5]),
            ("vertical_slice_gate.md", ["10"], "Vertical slice gate", [1]),
        ],
    )
    print("done")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
