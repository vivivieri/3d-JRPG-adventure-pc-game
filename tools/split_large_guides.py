#!/usr/bin/env python3
"""Split remaining large guides into hubs + packs (token progressive disclosure)."""
from __future__ import annotations

import re
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
        match = re.match(r"##\s+(\d+)", heading)
        if match:
            out[match.group(1)] = body
        else:
            # unnumbered H2 (IMPLEMENTATION_PLAN phase titles use "## Phase N")
            out[heading] = body
    return out


def by_phase_heading(sections: list[tuple[str, str]]) -> dict[str, str]:
    """Map Phase N / named H2 → body for IMPLEMENTATION_PLAN."""
    out: dict[str, str] = {}
    for heading, body in sections:
        match = re.match(r"##\s+Phase\s+(\d+)", heading, flags=re.I)
        if match:
            out[match.group(1)] = body
        else:
            key = re.sub(r"^##\s+", "", heading).strip().lower()
            key = re.sub(r"[^a-z0-9]+", "_", key).strip("_")
            out[key] = body
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
) -> str:
    aud = ", ".join(audience)
    lines = [
        "---",
        f"id: {stem}",
        f"type: {doc_type}",
        f"audience: [{aud}]",
    ]
    if phase:
        lines.append(f"phase: [{', '.join(str(p) for p in phase)}]")
    lines += [
        "status: active",
        f"authority: {authority}",
        f"tokens_est: {tokens}",
        "---",
        "",
    ]
    return "\n".join(lines)


def join_nums(nums: dict[str, str], keys: list[str]) -> str:
    return "\n".join(nums[k] for k in keys if k in nums).strip() + "\n"


def pack_link_table(subdir: str, rows: list[tuple[str, str]]) -> str:
    lines = ["| Pack | Topic |", "|------|-------|"]
    for rel, label in rows:
        name = Path(rel).name
        lines.append(f"| [`{name}`]({subdir}/{name}) | {label} |")
    lines.append("")
    return "\n".join(lines)


def split_narrative() -> None:
    src = DOCS / "design/vision/NARRATIVE_WRITING_GUIDE.md"
    text = strip_fm(src.read_text(encoding="utf-8"))
    preamble, sections = split_by_h2(text)
    nums = {k: v for k, v in by_num(sections).items() if k.isdigit()}
    pack = DOCS / "design/vision/narrative"
    packs = [
        ("audio_themes.md", "1-2", ["1", "2"], "Audio & themes"),
        ("character_voice.md", "3", ["3"], "Character voice"),
        ("scene_dialogue.md", "4-5", ["4", "5"], "Scene dialogue"),
        ("localization_emotion.md", "6-7", ["6", "7"], "Localization & emotion tags"),
        ("checklist_production.md", "8-10", ["8", "9", "10"], "Checklist & production"),
        ("emotional_rules.md", "11-12", ["11", "12"], "Emotional storytelling rules"),
    ]
    rows: list[tuple[str, str]] = []
    for name, _rng, keys, label in packs:
        body = join_nums(nums, keys)
        content = (
            fm(Path(name).stem.replace("_", "-"), "reference", ["narrative"], "narrative", max(400, len(body) // 4), [3, 6])
            + f"# Narrative — {label}\n\n**Hub:** [`NARRATIVE_WRITING_GUIDE.md`](../NARRATIVE_WRITING_GUIDE.md)\n\n"
            + body
        )
        write(pack / name, content)
        rows.append((name, label))
    hub = (
        fm("narrative-writing-guide", "reference", ["narrative"], "narrative", 900, [3, 6])
        + "# Tides of Urashima — Narrative Writing Guide\n\n"
        + "**Hub** — load one pack below, not the old monolith.\n\n"
        + pack_link_table("narrative", rows)
        + preamble.strip()
        + "\n"
    )
    write(src, hub)


def split_implementation_plan() -> None:
    src = DOCS / "ops/workflow/IMPLEMENTATION_PLAN.md"
    text = strip_fm(src.read_text(encoding="utf-8"))
    preamble, sections = split_by_h2(text)
    keyed = by_phase_heading(sections)
    pack = DOCS / "ops/workflow/implementation"
    phase_rows: list[tuple[str, str]] = []
    for n in range(0, 9):
        body = keyed.get(str(n))
        if not body:
            continue
        name = f"phase_{n}.md"
        content = (
            fm(f"implementation-phase-{n}", "how-to", ["pm", "architect", "builder"], "workflow", max(400, len(body) // 4), [n])
            + f"# Implementation Plan — Phase {n}\n\n**Hub:** [`IMPLEMENTATION_PLAN.md`](../IMPLEMENTATION_PLAN.md)\n\n"
            + body
        )
        write(pack / name, content)
        phase_rows.append((name, f"Phase {n}"))
    extras = [
        ("zone_build_order.md", "zone_build_order", "Zone build order"),
        ("validation_commands.md", "validation_commands", "Validation commands"),
        ("coverage_review.md", "coverage_review_gaps_closed_in_v1_2", "Coverage review"),
    ]
    for name, key, label in extras:
        body = keyed.get(key)
        if not body:
            # fuzzy: try partial
            body = next((v for k, v in keyed.items() if key.split("_")[0] in k), None)
        if not body:
            continue
        content = (
            fm(Path(name).stem.replace("_", "-"), "how-to", ["pm", "architect"], "workflow", max(400, len(body) // 4))
            + f"# Implementation Plan — {label}\n\n**Hub:** [`IMPLEMENTATION_PLAN.md`](../IMPLEMENTATION_PLAN.md)\n\n"
            + body
        )
        write(pack / name, content)
        phase_rows.append((name, label))
    hub = (
        fm("implementation-plan", "how-to", ["pm", "architect"], "workflow", 900)
        + "# Tides of Urashima — Implementation Plan\n\n"
        + "**Hub** — open the phase pack for the active sprint; do not preload all phases.\n\n"
        + pack_link_table("implementation", phase_rows)
        + preamble.strip()
        + "\n"
    )
    write(src, hub)


def split_cloud_runbook() -> None:
    src = DOCS / "ops/agents/CLOUD_AGENT_SETUP_RUNBOOK.md"
    text = strip_fm(src.read_text(encoding="utf-8"))
    preamble, sections = split_by_h2(text)
    nums = {k: v for k, v in by_num(sections).items() if k.isdigit()}
    pack = DOCS / "ops/agents/cloud_setup"
    packs = [
        ("goal_architecture.md", ["1", "2"], "Goal & architecture", [0, 1]),
        ("setup_automations.md", ["3", "4"], "One-time setup & automations", [0, 1]),
        ("cycle_events.md", ["5", "6"], "End-of-cycle & events", [0, 1]),
        ("github_timeline.md", ["7", "8"], "GitHub path & timeline", [0, 1]),
        ("antipatterns_troubleshoot.md", ["9", "10", "11", "12"], "Anti-patterns & troubleshooting", [0, 1]),
    ]
    rows: list[tuple[str, str]] = []
    for name, keys, label, phase in packs:
        body = join_nums(nums, keys)
        content = (
            fm(Path(name).stem.replace("_", "-"), "how-to", ["pm", "builder"], "agents", max(400, len(body) // 4), phase)
            + f"# Cloud Agent Setup — {label}\n\n**Hub:** [`CLOUD_AGENT_SETUP_RUNBOOK.md`](../CLOUD_AGENT_SETUP_RUNBOOK.md)\n\n"
            + body
        )
        write(pack / name, content)
        rows.append((name, label))
    hub = (
        fm("cloud-agent-setup-runbook", "how-to", ["pm", "builder"], "agents", 900, [0, 1])
        + "# Cloud Agent Setup Runbook\n\n"
        + "**Hub** — load the pack for your setup step.\n\n"
        + pack_link_table("cloud_setup", rows)
        + preamble.strip()
        + "\n"
    )
    write(src, hub)


def split_items_guide() -> None:
    src = DOCS / "design/art/ITEMS_3D_MODEL_GUIDE.md"
    text = strip_fm(src.read_text(encoding="utf-8"))
    preamble, sections = split_by_h2(text)
    nums = {k: v for k, v in by_num(sections).items() if k.isdigit()}
    pack = DOCS / "design/art/items"
    packs = [
        ("global_sheets_rig.md", ["1", "2", "3"], "Global rules, sheets, rig", [2, 5]),
        ("weapons_armor_charms.md", ["4", "5", "6"], "Weapons, armor, charms", [2, 5]),
        ("consumables_key_currency.md", ["7", "8", "9"], "Consumables, key items, currency", [2, 5]),
        ("export_qa.md", ["10", "11", "12"], "Export & QA", [5]),
    ]
    rows: list[tuple[str, str]] = []
    for name, keys, label, phase in packs:
        body = join_nums(nums, keys)
        content = (
            fm(Path(name).stem.replace("_", "-"), "reference", ["visual", "builder"], "art", max(400, len(body) // 4), phase)
            + f"# Items 3D — {label}\n\n**Hub:** [`ITEMS_3D_MODEL_GUIDE.md`](../ITEMS_3D_MODEL_GUIDE.md)\n\n"
            + body
        )
        write(pack / name, content)
        rows.append((name, label))
    hub = (
        fm("items-3d-model-guide", "reference", ["visual", "builder"], "art", 900, [2, 5])
        + "# Items & Props — 3D Model Guide\n\n"
        + "**Hub** — load one pack for the asset class you are building.\n\n"
        + pack_link_table("items", rows)
        + preamble.strip()
        + "\n"
    )
    write(src, hub)


def split_rendering() -> None:
    src = DOCS / "design/art/RENDERING_GUIDE.md"
    text = strip_fm(src.read_text(encoding="utf-8"))
    preamble, sections = split_by_h2(text)
    nums = {k: v for k, v in by_num(sections).items() if k.isdigit()}
    pack = DOCS / "design/art/rendering"
    packs = [
        ("defaults_environment.md", ["1", "2", "3", "4"], "Defaults, WorldEnvironment, sky", [1, 5]),
        ("lighting_fog.md", ["5", "6"], "Lighting & fog", [1, 5]),
        ("materials_gi_glow.md", ["7", "8", "9"], "Materials, GI, glow", [1, 5]),
        ("quality_zones.md", ["10", "11", "12"], "Quality presets & zone map", [1, 5]),
        ("zone_visuals_contract.md", ["13", "14", "15"], "zone_visuals contract & refs", [1, 5]),
    ]
    rows: list[tuple[str, str]] = []
    for name, keys, label, phase in packs:
        body = join_nums(nums, keys)
        content = (
            fm(Path(name).stem.replace("_", "-"), "reference", ["visual", "builder"], "art", max(400, len(body) // 4), phase)
            + f"# Rendering — {label}\n\n**Hub:** [`RENDERING_GUIDE.md`](../RENDERING_GUIDE.md)\n\n"
            + body
        )
        write(pack / name, content)
        rows.append((name, label))
    hub = (
        fm("rendering-guide", "reference", ["visual", "builder"], "art", 900, [1, 5])
        + "# Tides of Urashima — Rendering Guide\n\n"
        + "**Hub** — load the pack for the lighting/material pass you are doing.\n\n"
        + pack_link_table("rendering", rows)
        + preamble.strip()
        + "\n"
    )
    write(src, hub)


def split_model_qa() -> None:
    src = DOCS / "design/art/MODEL_QA.md"
    text = strip_fm(src.read_text(encoding="utf-8"))
    preamble, sections = split_by_h2(text)
    nums = {k: v for k, v in by_num(sections).items() if k.isdigit()}
    pack = DOCS / "design/art/model_qa"
    packs = [
        ("layers_workflow.md", ["1", "2", "3"], "Defense layers & agent workflow", [5]),
        ("smoke_report_tools.md", ["4", "5", "6", "7"], "L2 smoke, report, tools", [5]),
        ("polish_direction.md", ["8", "9"], "Polish cadence & direction", [5]),
    ]
    rows: list[tuple[str, str]] = []
    for name, keys, label, phase in packs:
        body = join_nums(nums, keys)
        content = (
            fm(Path(name).stem.replace("_", "-"), "how-to", ["visual", "builder"], "art", max(400, len(body) // 4), phase)
            + f"# Model QA — {label}\n\n**Hub:** [`MODEL_QA.md`](../MODEL_QA.md)\n\n"
            + body
        )
        write(pack / name, content)
        rows.append((name, label))
    hub = (
        fm("model-qa", "how-to", ["visual", "builder"], "art", 900, [5])
        + "# 3D Model QA — Technical Gates + Turntable Vision Jury\n\n"
        + "**Hub** — load the pack for the QA step you are running.\n\n"
        + pack_link_table("model_qa", rows)
        + preamble.strip()
        + "\n"
    )
    write(src, hub)


def main() -> int:
    split_narrative()
    split_implementation_plan()
    split_cloud_runbook()
    split_items_guide()
    split_rendering()
    split_model_qa()
    print("done")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
