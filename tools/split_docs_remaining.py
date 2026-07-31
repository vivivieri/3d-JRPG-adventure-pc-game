#!/usr/bin/env python3
"""Split remaining fat hubs from the docs-pack remaining backlog."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"

# Reuse helpers from enhance_docs_packs
sys.path.insert(0, str(ROOT / "tools"))
from enhance_docs_packs import (  # type: ignore  # noqa: E402
    by_title,
    fm,
    pack_table,
    short_blurb,
    split_by_h2,
    split_by_title_keys,
    split_numbered,
    strip_fm,
    write,
)


def load_source(rel: str) -> str:
    path = DOCS / rel
    text = path.read_text(encoding="utf-8")
    if len(text) < 4500:
        try:
            blob = subprocess.check_output(
                ["git", "show", f"HEAD:docs/{rel}"],
                cwd=ROOT,
                text=True,
                stderr=subprocess.DEVNULL,
            )
            if len(blob) > len(text) * 1.2:
                return blob
        except subprocess.CalledProcessError as exc:
            print(f"WARN: git show HEAD:docs/{rel} failed: {exc}", file=sys.stderr)
    return text


def split_brief_ruined_village() -> None:
    """Thin generation brief — keep intent+metrics on hub, detail in packs."""
    rel = "briefs/ruined_village.md"
    src = DOCS / rel
    text = strip_fm(load_source(rel) if False else src.read_text(encoding="utf-8"))
    # briefs may lack frontmatter
    body = text
    preamble, sections = split_by_h2(body)
    titles = by_title(sections)
    pack_dir = src.parent / "ruined_village"
    packs = [
        (
            "prompts_toolchain.md",
            ["tool_chain", "positive_prompt_anchors", "negative_prompt_required"],
            "Toolchain + prompts",
        ),
        (
            "spatial_kit.md",
            ["spatial_composition_contract", "modular_kit_priorities_build_order"],
            "Spatial composition + kit build order",
        ),
        (
            "metrics_acceptance.md",
            [
                "hard_metrics",
                "camera_beats",
                "acceptance_evidence",
                "vertical_slice_minimum_ship_phase_1",
                "forbidden",
            ],
            "Metrics, camera, acceptance, forbidden",
        ),
    ]
    rows: list[tuple[str, str]] = []
    for name, keys, label in packs:
        parts = [titles[k] for k in keys if k in titles]
        # fuzzy: try substring match on keys
        if not parts:
            for k, v in titles.items():
                if any(key in k for key in keys):
                    parts.append(v)
        body_p = "\n".join(parts).strip() + "\n"
        if not body_p.strip():
            print(f"WARN brief pack empty {name} keys={keys} avail={sorted(titles)}")
            continue
        content = (
            fm(
                Path(name).stem.replace("_", "-"),
                "reference",
                ["visual", "builder"],
                "briefs",
                max(200, len(body_p) // 4),
                [1],
                label,
            )
            + f"# ruined_village brief — {label}\n\n**Hub:** [`ruined_village.md`](../ruined_village.md)\n\n"
            + body_p
        )
        write(pack_dir / name, content)
        rows.append((name, label))

    # Keep intent + emotional on hub
    keep_parts = []
    for k, v in titles.items():
        if "intent" in k or "emotional" in k:
            keep_parts.append(v)
    hub_body = "\n".join(keep_parts).strip()
    # preamble without duplicate H1
    intro = short_blurb(preamble, 500)
    hub = (
        fm(
            "ruined-village",
            "reference",
            ["visual", "builder"],
            "briefs",
            max(250, 200 + len(hub_body) // 4),
            [1],
            "Ruined village generation brief — load pack for prompts/kit/acceptance",
        )
        + "# Generation brief — `ruined_village`\n\n"
        + "**Hub** — load one pack for the generation step you are on.\n\n"
        + pack_table("ruined_village", rows)
        + intro
        + ("\n" + hub_body + "\n" if hub_body else "")
    )
    write(src, hub)


def main() -> int:
    split_by_title_keys(
        src_rel="design/vision/STORYBOARD.md",
        pack_subdir="storyboard",
        hub_title="Storyboard",
        hub_summary="Scene beats by act — load the act you are implementing",
        audience=["narrative", "builder", "flow"],
        authority="vision",
        doc_type="reference",
        phase=[1, 2, 3, 4, 5, 6],
        packs=[
            ("act_i.md", ["act_i_the_return"], "Act I — The Return"),
            ("act_ii.md", ["act_ii_the_depths"], "Act II — The Depths"),
            ("act_iii.md", ["act_iii_the_tide"], "Act III — The Tide"),
            ("flow_priority.md", ["scene_flow_diagram", "production_priority_pre_build_art_rebuild"], "Flow diagram + production priority"),
        ],
    )

    split_by_title_keys(
        src_rel="ops/workflow/MILESTONES.md",
        pack_subdir="milestones",
        hub_title="Milestones",
        hub_summary="M0–M6 checklist — load the active milestone pack",
        audience=["pm", "release", "architect"],
        authority="workflow",
        doc_type="reference",
        packs=[
            ("pre_build.md", ["m0_pre_production", "m0c_pre_build_design_art_rebuild_specs", "m0d_pre_build_game_design_gameplay_systems", "m0f_pre_build_design_narrative_polish", "m0g_pitch_illustrations", "m0e_story_data_layer_main_branch", "m0h_ai_dev_workflow_testing_main_baseline"], "M0 pre-build packs"),
            ("m1_m4_gameplay.md", ["m1_greybox_exploration", "m2_combat_vertical_slice", "m3_chapter_1", "m4_full_game"], "M1–M4 gameplay milestones"),
            ("m5_m6_ship.md", ["m5_art_rebuild_high_detail_japanese", "m6_steam_ship_prep"], "M5 art rebuild + M6 Steam"),
        ],
    )

    split_numbered(
        src_rel="design/gameplay/BOSS_DESIGNS.md",
        pack_subdir="bosses",
        hub_title="Boss Designs",
        hub_summary="Boss fights — load the encounter you are balancing",
        audience=["builder", "builder_combat", "qa"],
        authority="gameplay",
        doc_type="reference",
        phase=[2, 3, 5],
        packs=[
            ("global_rules.md", ["1"], "Global boss rules", [2]),
            ("shore_wraith.md", ["2"], "Shore Wraith", [2]),
            ("palace_sentinel.md", ["3"], "Palace Sentinel", [3, 5]),
            ("tide_keeper.md", ["4"], "Tide Keeper", [5]),
            ("enemies_timing_data.md", ["5", "6", "7", "8", "9"], "Tutorial/standard enemies, timing, data, playtest", [2, 5]),
        ],
    )

    split_numbered(
        src_rel="ops/agents/GDAI_CLOUD_SETUP.md",
        pack_subdir="gdai_setup",
        hub_title="GDAI Cloud Setup",
        hub_summary="GDAI MCP install — load desktop or cloud section",
        audience=["builder", "pm", "architect"],
        authority="ops",
        doc_type="how-to",
        packs=[
            ("architecture_prereqs.md", ["1"], "Prerequisites", None),
            # numbered sections after unnumbered - use title keys fallback
        ],
    )
    # GDAI has mixed heading styles — redo with titles
    split_by_title_keys(
        src_rel="ops/agents/GDAI_CLOUD_SETUP.md",
        pack_subdir="gdai_setup",
        hub_title="GDAI Cloud Setup",
        hub_summary="GDAI MCP install — load desktop or cloud section",
        audience=["builder", "pm", "architect"],
        authority="ops",
        doc_type="how-to",
        packs=[
            ("architecture_needs.md", ["architecture_two_layers_both_required", "what_you_need_3_pieces", "1_prerequisites"], "Architecture + needs + prereqs"),
            ("install_desktop.md", ["2_install_the_plugin_local_dev_only", "3_configure_cursor_desktop_local_ide"], "Install plugin + desktop Cursor"),
            ("cloud_steam_troubleshoot.md", ["4_configure_cursor_cloud_agents", "5_before_steam_release_export", "6_troubleshooting", "7_this_repos_shipped_addons"], "Cloud Agents, Steam, troubleshoot"),
        ],
    )

    split_numbered(
        src_rel="ops/qa/QA_AND_BUG_PROCESS.md",
        pack_subdir="bug_process",
        hub_title="QA and Bug Process",
        hub_summary="Triage, severity, verification — load the step you are on",
        audience=["qa", "pm", "builder"],
        authority="qa",
        doc_type="how-to",
        packs=[
            ("scope_severity.md", ["1", "2"], "QA scope + severity", None),
            ("report_triage.md", ["3", "4"], "Bug report template + triage", None),
            ("verify_regression.md", ["5", "6"], "Verification + regression suite", None),
            ("index_playtest_gates.md", ["7", "8", "9", "10", "11"], "System index, playtest loop, gates, won't-fix, RC checklist", None),
        ],
    )

    split_numbered(
        src_rel="design/vision/GDD.md",
        pack_subdir="gdd",
        hub_title="Game Design Document",
        hub_summary="GDD — load the section for your design question",
        audience=["narrative", "pm", "architect"],
        authority="vision",
        doc_type="explanation",
        packs=[
            ("pitch_scope.md", ["1", "2", "3", "4"], "Pitch, source, loop, scope", None),
            ("cast_world_combat.md", ["5", "6", "7", "8"], "Characters, world, combat, progression", None),
            ("narrative_endings.md", ["9", "10"], "Narrative structure + endings", None),
            ("controls_tech_ship.md", ["11", "12", "13", "14", "15", "16"], "Controls, tech, milestones, Steam, i18n, risks", None),
        ],
    )

    split_numbered(
        src_rel="ops/qa/FLOW_QA.md",
        pack_subdir="flow_qa",
        hub_title="Flow QA",
        hub_summary="Story soft-lock / quest / combat hang gates — load the layer you need",
        audience=["flow", "qa", "builder"],
        authority="qa",
        doc_type="how-to",
        packs=[
            ("standards_layers.md", ["1", "2"], "Industry standards + defense layers", None),
            ("scenarios_levers.md", ["3", "4"], "L4 scenarios + lever taxonomy", None),
            ("workflow_report.md", ["5", "6", "7", "8", "9"], "Agent workflow, iteration, smoke, report, tools", None),
        ],
    )

    split_brief_ruined_village()
    print("done")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
