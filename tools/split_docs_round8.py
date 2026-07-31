#!/usr/bin/env python3
"""Docs pack round 8 — thin remaining leaves still ≥1.0k tokens."""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from enhance_docs_packs import (  # noqa: E402
    fm,
    pack_table,
    short_blurb,
    split_by_h2,
    split_by_title_keys,
    strip_fm,
    write,
)
from split_docs_round7 import (  # noqa: E402
    slug_heading,
    split_h3_halves,
    split_leaf_by_h3,
)

# NOTE: H4 sections are rewritten as ## in packs so markdown style (no H1→H4 jump) passes.


def split_by_h4(text: str) -> tuple[str, list[tuple[str, str]]]:
    lines = text.splitlines(keepends=True)
    preamble: list[str] = []
    sections: list[tuple[str, str]] = []
    current_heading = ""
    current_body: list[str] = []
    seen = False
    for line in lines:
        if line.startswith("#### "):
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


def split_leaf_by_h4(
    *,
    src_rel: str,
    pack_subdir: str,
    hub_title: str,
    hub_summary: str,
    audience: list[str],
    authority: str,
    doc_type: str,
    packs: list[tuple[str, list[str], str]],
    phase: list[int] | None = None,
) -> None:
    src = ROOT / "docs" / src_rel
    text = strip_fm(src.read_text(encoding="utf-8"))
    # Drop leading H1 / hub link into preamble; body may start with ### then ####
    preamble_h2, h2_sections = split_by_h2(text)
    if len(h2_sections) == 1:
        body = re.sub(r"^## .*\n", "", h2_sections[0][1], count=1)
        preamble = preamble_h2 + f"{h2_sections[0][0]}\n\n"
    else:
        body = text
        preamble = preamble_h2
    # Strip a single wrapping ### if present
    body2 = re.sub(r"^### .*\n+", "", body, count=1)
    intro, h4_sections = split_by_h4(body2)
    titles = {slug_heading(h): b for h, b in h4_sections}
    preamble = preamble + intro

    pack_dir = src.parent / pack_subdir
    rows: list[tuple[str, str]] = []
    for name, keys, label in packs:
        parts = [titles[k] for k in keys if k in titles]
        missing = [k for k in keys if k not in titles]
        if missing:
            print(f"WARN {src_rel} missing H4 {missing}; have={sorted(titles)}")
        # Promote #### → ## under pack H1 (avoid H1→H4 jump)
        body_out = "\n".join(parts).strip() + "\n"
        body_out = re.sub(r"(?m)^#### ", "## ", body_out)
        if not body_out.strip():
            continue
        content = (
            fm(
                Path(name).stem.replace("_", "-"),
                doc_type,
                audience,
                authority,
                max(200, len(body_out) // 4),
                phase,
                summary=label,
            )
            + f"# {hub_title} — {label}\n\n"
            + f"**Hub:** [`{src.name}`](../{src.name})\n\n"
            + body_out
        )
        write(pack_dir / name, content)
        rows.append((name, label))

    hub = (
        fm(
            src.stem.lower().replace("_", "-"),
            doc_type,
            audience,
            authority,
            max(220, 160 + len(pack_table(pack_subdir, rows)) // 4),
            phase,
            summary=hub_summary,
        )
        + f"# {hub_title}\n\n"
        + "**Hub** — load only the pack for your current pass.\n\n"
        + pack_table(pack_subdir, rows)
        + short_blurb(preamble)
        + "\n"
    )
    write(src, hub)


def split_table_rows_halves(
    *,
    src_rel: str,
    pack_subdir: str,
    hub_title: str,
    hub_summary: str,
    audience: list[str],
    authority: str,
    doc_type: str = "reference",
    phase: list[int] | None = None,
    split_after_gate_prefix: str | None = None,
) -> None:
    """Split a long markdown table leaf into two packs (row halves or by gate id)."""
    src = ROOT / "docs" / src_rel
    text = strip_fm(src.read_text(encoding="utf-8"))
    lines = text.splitlines(keepends=True)

    # Find first markdown table
    table_start = None
    for i, line in enumerate(lines):
        if line.startswith("|") and i + 1 < len(lines) and re.match(r"^\|[-: |]+\|\s*$", lines[i + 1]):
            table_start = i
            break
    if table_start is None:
        print(f"SKIP no table: {src_rel}")
        return

    header = lines[table_start]
    sep = lines[table_start + 1]
    rows: list[str] = []
    i = table_start + 2
    while i < len(lines) and lines[i].startswith("|"):
        rows.append(lines[i])
        i += 1
    after = "".join(lines[i:])
    before = "".join(lines[:table_start])
    # Drop prior H1 / Hub lines — packs get a fresh hub pointer
    before = re.sub(r"(?m)^# .+\n+", "", before)
    before = re.sub(r"(?m)^\*\*Hub:\*\*.+\n+", "", before)

    if split_after_gate_prefix:
        # Keep L0/L1 in pack A, rest in pack B based on first column gate id
        a_rows: list[str] = []
        b_rows: list[str] = []
        for row in rows:
            cells = [c.strip() for c in row.strip().strip("|").split("|")]
            gate = cells[0].strip("` ") if cells else ""
            if gate.startswith("L0_") or gate.startswith("L1_"):
                a_rows.append(row)
            else:
                b_rows.append(row)
    else:
        mid = max(1, len(rows) // 2)
        a_rows, b_rows = rows[:mid], rows[mid:]

    def pack_body(row_list: list[str], label: str) -> str:
        table = header + sep + "".join(row_list)
        return before + table + ("\n" if not after.startswith("\n") else "") + after

    packs = [
        ("gates_l0_l1.md", pack_body(a_rows, "L0/L1 gates"), "L0 + L1 gates"),
        ("gates_l2_plus.md", pack_body(b_rows, "L2+ gates"), "L2+ / Windows / CD"),
    ]
    pack_dir = src.parent / pack_subdir
    rows_meta: list[tuple[str, str]] = []
    for name, body, label in packs:
        content = (
            fm(
                Path(name).stem.replace("_", "-"),
                doc_type,
                audience,
                authority,
                max(200, len(body) // 4),
                phase,
                summary=label,
            )
            + f"# {hub_title} — {label}\n\n"
            + f"**Hub:** [`{src.name}`](../{src.name})\n\n"
            + body.strip()
            + "\n"
        )
        write(pack_dir / name, content)
        rows_meta.append((name, label))

    # Keep only hub pointer + short note (table lives in packs)
    blurb = short_blurb(before)
    hub = (
        fm(
            src.stem.lower().replace("_", "-"),
            doc_type,
            audience,
            authority,
            max(200, 140 + len(pack_table(pack_subdir, rows_meta)) // 4),
            phase,
            summary=hub_summary,
        )
        + f"# {hub_title}\n\n"
        + "**Hub** — load only the pack for your current pass.\n\n"
        + pack_table(pack_subdir, rows_meta)
        + blurb
        + "\n"
    )
    write(src, hub)


def update_pack_catalog(new_paths: list[str]) -> None:
    index = ROOT / "docs" / "INDEX.yaml"
    text = index.read_text(encoding="utf-8")
    m = re.search(r"(?ms)^(pack_catalog:\n)(.*?)(?=\n[a-z_]+:|\Z)", text)
    if not m:
        print("WARN: pack_catalog block not found")
        return
    existing = set(re.findall(r"^\s*-\s+(docs/\S+)$", m.group(2), flags=re.M))
    to_add = sorted(p for p in new_paths if p not in existing)
    if not to_add:
        print("pack_catalog: nothing new")
        return
    lines = m.group(2).rstrip("\n").splitlines()
    # Insert each path in sorted order among docs/ entries
    for path in to_add:
        entry = f"  - {path}"
        inserted = False
        for i, line in enumerate(lines):
            mm = re.match(r"^\s*-\s+(docs/\S+)$", line)
            if not mm:
                continue
            if path < mm.group(1):
                lines.insert(i, entry)
                inserted = True
                break
        if not inserted:
            lines.append(entry)
        print(f"INDEX + {path}")
    new_block = m.group(1) + "\n".join(lines) + "\n"
    text = text[: m.start()] + new_block + text[m.end() :]
    index.write_text(text, encoding="utf-8")


def collect_new_mds(before: set[str]) -> list[str]:
    after = {
        str(p.relative_to(ROOT)).replace("\\", "/")
        for p in (ROOT / "docs").rglob("*.md")
    }
    return sorted(p for p in after - before if p.startswith("docs/"))


def main() -> int:
    before = {
        str(p.relative_to(ROOT)).replace("\\", "/")
        for p in (ROOT / "docs").rglob("*.md")
    }

    # --- Design / world ---
    split_by_title_keys(
        src_rel="design/world/WORLD_MAP_AND_FLOW.md",
        pack_subdir="map_flow",
        hub_title="World Map & Flow",
        hub_summary="Zones, connections, layouts, save/nav, scene flow, QA",
        audience=["architect", "builder", "narrative"],
        authority="world",
        doc_type="reference",
        packs=[
            ("overview_zones.md", ["1_world_overview", "2_zone_reference", "3_connection_table"], "Overview + zones + connections"),
            (
                "layouts.md",
                [
                    "4_ruined_village_layout_hub",
                    "5_tidal_caves_layout_linear_with_branch",
                    "6_dragon_palace_gate_layout",
                ],
                "Zone layouts",
            ),
            (
                "nav_flow_qa.md",
                ["7_save_points", "8_player_navigation_aids", "9_scene_flow_canonical", "10_qa_checklist"],
                "Save, nav, scene flow, QA",
            ),
        ],
    )
    split_by_title_keys(
        src_rel="design/world/quests/main_quests_detail.md",
        pack_subdir="detail",
        hub_title="Main Quests — Detail",
        hub_summary="Five main quests overview + per-quest detail",
        audience=["narrative", "builder"],
        authority="world",
        doc_type="reference",
        packs=[
            ("overview.md", ["1_main_quests_5"], "Main quests overview"),
            ("quest_detail.md", ["2_quest_detail"], "Per-quest detail"),
        ],
    )

    # --- Art / items / rendering / characters ---
    split_by_title_keys(
        src_rel="design/art/items/global_sheets_rig.md",
        pack_subdir="global",
        hub_title="Items — Global Sheets & Rig",
        hub_summary="Global rules, sheet template, rig attachment",
        audience=["visual", "builder"],
        authority="art",
        doc_type="reference",
        packs=[
            ("rules_sheets.md", ["1_global_item_prop_rules", "2_model_sheet_template"], "Rules + sheet template"),
            ("rig_parenting.md", ["3_rig_attachment_parenting"], "Rig attachment & parenting"),
        ],
    )
    split_by_title_keys(
        src_rel="design/art/items/weapons_armor_charms.md",
        pack_subdir="equipment",
        hub_title="Items — Weapons / Armor / Charms",
        hub_summary="Equipment model briefs",
        audience=["visual", "builder"],
        authority="art",
        doc_type="reference",
        packs=[
            ("weapons.md", ["4_equipment_weapons"], "Weapons"),
            ("armor_charms.md", ["5_equipment_armor", "6_equipment_charms"], "Armor + charms"),
        ],
    )
    split_by_title_keys(
        src_rel="design/art/items/consumables_key_currency.md",
        pack_subdir="consumables",
        hub_title="Items — Consumables / Key / Currency",
        hub_summary="Consumables, key items, materials & currency",
        audience=["visual", "builder"],
        authority="art",
        doc_type="reference",
        packs=[
            ("consumables.md", ["7_consumables"], "Consumables"),
            ("key_items.md", ["8_key_items"], "Key items"),
            ("materials_currency.md", ["9_materials_currency"], "Materials & currency"),
        ],
    )
    split_by_title_keys(
        src_rel="design/art/rendering/defaults_environment.md",
        pack_subdir="defaults",
        hub_title="Rendering — Defaults & Environment",
        hub_summary="Checklist, renderer defaults, WorldEnvironment, sky",
        audience=["visual", "builder"],
        authority="art",
        doc_type="reference",
        packs=[
            ("checklist_renderer.md", ["1_summary_checklist", "2_renderer_project_defaults"], "Checklist + renderer"),
            ("world_sky.md", ["3_worldenvironment_per_zone", "4_sky"], "WorldEnvironment + sky"),
        ],
    )
    split_by_title_keys(
        src_rel="design/art/generation_readiness/characters_zones.md",
        pack_subdir="rows",
        hub_title="Generation Readiness — Characters & Zones",
        hub_summary="qa_catalog character rows + zone composition rows",
        audience=["visual", "qa"],
        authority="art",
        doc_type="reference",
        packs=[
            ("characters.md", ["4_character_rows_qa_catalog_json"], "Character rows"),
            ("zones.md", ["5_zone_rows_environment_kits_md"], "Zone rows"),
        ],
    )
    split_h3_halves(
        "design/art/characters/enemies/part_b.md",
        "bosses",
        "Character Bible — Enemy Bosses",
        "Shore Wraith / Sentinel / Tide Keeper",
        ["visual", "builder"],
        "art",
    )
    split_leaf_by_h3(
        src_rel="design/art/model_qa/layers/defense_layers.md",
        pack_subdir="m_layers",
        hub_title="Model QA — Defense Layers",
        hub_summary="M1–M3b model QA defense layers",
        audience=["visual", "qa"],
        authority="art",
        doc_type="how-to",
        packs=[
            (
                "m1_m2.md",
                [
                    "m1_catalog",
                    "m2_technical_glb_lint",
                    "m2b_glb_import_sanitizer_editorscenepostimport",
                    "m2c_animation_whitelist",
                ],
                "M1–M2c",
            ),
            (
                "m3_jury.md",
                ["m3_turntable_render_blender", "m3b_multi_llm_vision_jury_hero_set_pieces", "why_turntable_in_game_screenshot"],
                "M3 turntable + jury",
            ),
        ],
    )

    # --- Audio / vision / UI ---
    split_by_title_keys(
        src_rel="design/audio/audio_qa/automate_layers.md",
        pack_subdir="layers",
        hub_title="Audio QA — Automate Layers",
        hub_summary="Automate vs human + A1–L6 defense layers",
        audience=["audio", "qa"],
        authority="audio",
        doc_type="how-to",
        packs=[
            ("automate_vs_human.md", ["1_what_to_automate_vs_human"], "Automate vs human"),
            ("defense_layers.md", ["2_defense_layers"], "Defense layers A1–L6"),
        ],
    )
    split_leaf_by_h4(
        src_rel="design/audio/production/bgm_map/sheets/per_track_specs.md",
        pack_subdir="tracks",
        hub_title="BGM — Per-track Specs",
        hub_summary="Per-track production specs",
        audience=["audio", "builder"],
        authority="audio",
        doc_type="reference",
        packs=[
            (
                "menu_zones.md",
                ["bgm_menu", "bgm_prologue", "bgm_village", "bgm_caves", "bgm_palace"],
                "Menu + zone BGM",
            ),
            (
                "combat_endings.md",
                [
                    "bgm_combat",
                    "bgm_boss",
                    "bgm_boss_tide_keeper_p2",
                    "bgm_boss_tide_keeper_p3",
                    "bgm_ending_rewind_bgm_ending_anchor_bgm_ending_drift",
                ],
                "Combat + boss + endings",
            ),
        ],
    )
    split_by_title_keys(
        src_rel="design/vision/illustrations/shots_briefs.md",
        pack_subdir="shots",
        hub_title="Illustrations — Shots & Briefs",
        hub_summary="Priority shot list + per-scene briefs",
        audience=["visual", "narrative"],
        authority="vision",
        doc_type="reference",
        packs=[
            ("priority_shots.md", ["4_priority_shot_list_generate_in_this_order"], "Priority shot list"),
            ("scene_briefs.md", ["5_per_scene_illustration_briefs"], "Per-scene briefs"),
        ],
    )
    split_h3_halves(
        "design/vision/narrative/emotional/project_rules.md",
        "rules",
        "Narrative — Project Emotional Rules",
        "JRPG emotional storytelling rules A–I",
        ["narrative"],
        "vision",
    )
    split_by_title_keys(
        src_rel="design/ui/cinematics/storyboard_endings.md",
        pack_subdir="cine",
        hub_title="Cinematics — Storyboard & Endings",
        hub_summary="Storyboard scene specs + ending cinematics",
        audience=["narrative", "visual", "builder"],
        authority="ui",
        doc_type="reference",
        packs=[
            ("storyboard.md", ["7_storyboard_scene_specs"], "Storyboard scene specs"),
            ("endings.md", ["8_ending_cinematics"], "Ending cinematics"),
        ],
    )

    # --- Engineering ---
    split_by_title_keys(
        src_rel="engineering/technical/python/standards_pep8.md",
        pack_subdir="pep8",
        hub_title="Python — PEP 8 Standards",
        hub_summary="External standards + project PEP 8 profile",
        audience=["architect", "builder"],
        authority="engineering",
        doc_type="reference",
        packs=[
            ("externals.md", ["1_industry_standards_authoritative_externals"], "Authoritative externals"),
            ("project_profile.md", ["2_pep_8_essentials_project_profile"], "Project PEP 8 profile"),
        ],
    )
    split_by_title_keys(
        src_rel="engineering/technical/data/story_spine.md",
        pack_subdir="spine",
        hub_title="Data — Story Spine",
        hub_summary="scenes/flags/quests/dialogue JSON shapes",
        audience=["architect", "narrative", "builder"],
        authority="engineering",
        doc_type="reference",
        packs=[
            ("scenes_flags.md", ["3_story_spine_story_scenes_json", "4_flag_registry_story_flags_json"], "Scenes + flags"),
            ("quests_dialogue.md", ["5_quest_data_model_5_quests_3_acts", "7_dialogue_structure"], "Quests + dialogue"),
        ],
    )
    split_by_title_keys(
        src_rel="engineering/technical/data/i18n_validation.md",
        pack_subdir="i18n",
        hub_title="Data — i18n & Validation",
        hub_summary="Localization split, validators, migration, schemas",
        audience=["architect", "builder"],
        authority="engineering",
        doc_type="reference",
        packs=[
            (
                "locale_tools.md",
                ["12_localization_split", "13_validation_tools_implemented", "14_migration_from_old_3_quest_data"],
                "Locale + tools + migration",
            ),
            (
                "maintenance_schemas.md",
                ["15_file_maintenance_order_all_files_already_exist", "16_scene_index_vs_storyboard_count", "17_json_schema_versions"],
                "Maintenance + schemas",
            ),
        ],
    )

    # --- Ops / QA / workflow / agents ---
    split_by_title_keys(
        src_rel="ops/qa/alignment/visuals_history_integration.md",
        pack_subdir="visuals",
        hub_title="Alignment — Visuals / History / Integration",
        hub_summary="Stakeholder visuals, history, PM integration, workflow, catalog",
        audience=["pm", "qa"],
        authority="qa",
        doc_type="how-to",
        packs=[
            ("stakeholder_visuals.md", ["7_stakeholder_visuals"], "Stakeholder visuals"),
            ("history.md", ["8_history_committed_on_github"], "Committed history"),
            (
                "integration_workflow.md",
                [
                    "9_integration_with_pm_stakeholder_reporting",
                    "10_agent_workflow_mandatory_after_alignment_work",
                    "11_catalog_validation",
                ],
                "PM integration + workflow + catalog",
            ),
        ],
    )
    # Keep radar keyword discoverable on the hub for humans (packs hold full tables)
    vis_hub = ROOT / "docs/ops/qa/alignment/visuals_history_integration.md"
    vis_text = vis_hub.read_text(encoding="utf-8")
    if "audit_radar_spec.png" not in vis_text:
        vis_text = vis_text.rstrip() + (
            "\n\n## Factory hooks\n\n"
            "- Management visuals: `audit_radar_spec.png` + `audit_radar_build.png` "
            "(see [`visuals/stakeholder_visuals.md`](visuals/stakeholder_visuals.md)).\n"
            "- After alignment work: `bash tools/run_alignment_audit.sh`.\n"
        )
        write(vis_hub, vis_text)

    split_table_rows_halves(
        src_rel="ops/ci-cd/ci/required_gates/runs/part_b.md",
        pack_subdir="game_dev",
        hub_title="CI — game/development Gates",
        hub_summary="game-ci.yml gate table (L0–L4 + Windows/CD)",
        audience=["release", "qa", "pm"],
        authority="ci-cd",
        phase=[6, 8],
        split_after_gate_prefix="L0_L1",
    )

    split_by_title_keys(
        src_rel="ops/workflow/agile/cadence/duration.md",
        pack_subdir="duration",
        hub_title="Agile — Sprint Duration",
        hub_summary="Calendar ceilings + AI-native cadence",
        audience=["pm"],
        authority="workflow",
        doc_type="how-to",
        packs=[
            ("recommendations.md", ["12_sprint_duration_recommendations"], "Duration recommendations"),
            ("ai_native.md", ["12_1_ai_native_cadence_pure_agent_implementation"], "AI-native cadence"),
        ],
    )
    split_leaf_by_h3(
        src_rel="ops/workflow/ai_dev/build_policy.md",
        pack_subdir="policy",
        hub_title="AI Dev — Build Policy",
        hub_summary="Toolchain, base classes, session startup, build loop, forbids",
        audience=["pm", "architect", "builder"],
        authority="workflow",
        doc_type="how-to",
        packs=[
            (
                "toolchain_base.md",
                ["1_1_mandatory_toolchain", "1_1b_code_base_classes_extend_only"],
                "Toolchain + base classes",
            ),
            (
                "session_loop.md",
                ["1_2_session_startup_every_agent_run", "1_3_build_loop_per_task", "1_4_what_ai_agents_must_not_do"],
                "Session startup + loop + forbids",
            ),
        ],
    )
    split_leaf_by_h3(
        src_rel="ops/workflow/ai_dev/phases/part_a.md",
        pack_subdir="early",
        hub_title="AI Dev — Phases 0–3",
        hub_summary="Phase acceptance 0–3",
        audience=["pm", "qa", "architect"],
        authority="workflow",
        doc_type="reference",
        packs=[
            ("phase_0_1.md", ["phase_0_dev_environment_baseline", "phase_1_environment_foundation"], "Phases 0–1"),
            ("phase_2_3.md", ["phase_2_core_systems_shell", "phase_3_narrative_exploration"], "Phases 2–3"),
        ],
    )
    split_leaf_by_h3(
        src_rel="ops/workflow/ai_dev/phases/part_b.md",
        pack_subdir="late",
        hub_title="AI Dev — Phases 4–8",
        hub_summary="Phase acceptance 4–8",
        audience=["pm", "qa", "architect"],
        authority="workflow",
        doc_type="reference",
        packs=[
            (
                "phase_4_6.md",
                ["phase_4_combat_vertical_slice", "phase_5_chapter_1_dungeons", "phase_6_full_story_endings"],
                "Phases 4–6",
            ),
            ("phase_7_8.md", ["phase_7_m5_art_rebuild", "phase_8_ship_prep"], "Phases 7–8"),
        ],
    )
    split_by_title_keys(
        src_rel="ops/workflow/milestones/m5_m6_ship.md",
        pack_subdir="ship",
        hub_title="Milestones — M5 / M6 Ship",
        hub_summary="M5 art rebuild + M6 Steam ship prep",
        audience=["pm", "release", "visual"],
        authority="workflow",
        doc_type="reference",
        packs=[
            ("m5.md", ["m5_art_rebuild_high_detail_japanese"], "M5 art rebuild"),
            ("m6.md", ["m6_steam_ship_prep"], "M6 Steam & ship"),
        ],
    )

    split_leaf_by_h3(
        src_rel="ops/agents/gdai_setup/cloud_steam/cloud_agents.md",
        pack_subdir="steps",
        hub_title="GDAI — Configure Cloud Agents",
        hub_summary="Bootstrap, plugin, MCP register, verify, workflow",
        audience=["pm", "builder"],
        authority="ops",
        doc_type="how-to",
        packs=[
            (
                "bootstrap_plugin.md",
                ["4_1_environment_bootstrap_vm", "4_2_gdai_plugin_in_cloud_required_not_in_git"],
                "Bootstrap + GDAI plugin",
            ),
            (
                "mcp_verify_workflow.md",
                [
                    "4_3_register_mcp_in_cursor_dashboard_required_for_agent_tools",
                    "4_4_verify_cloud",
                    "4_5_workflow_mandatory_no_manual_fallback",
                ],
                "MCP register + verify + workflow",
            ),
        ],
    )
    split_leaf_by_h3(
        src_rel="ops/agents/cloud_setup/automations/cursor_automations.md",
        pack_subdir="automations",
        hub_title="Cloud Setup — Cursor Automations",
        hub_summary="Automations A–D (event-driven)",
        audience=["pm", "architect"],
        authority="ops",
        doc_type="tutorial",
        packs=[
            ("automation_a_pm.md", ["automation_a_pm_sprint_master_primary"], "Automation A — PM"),
            (
                "automation_bcd.md",
                [
                    "automation_b_ci_failure_triage_required",
                    "automation_c_human_uat_notify_end_of_pipeline",
                    "automation_d_factory_watchdog_human_alert_exception_only",
                ],
                "Automations B–D",
            ),
        ],
    )
    split_by_title_keys(
        src_rel="ops/agents/factory_setup/automations_github_bootstrap.md",
        pack_subdir="bootstrap",
        hub_title="Factory Setup — Automations & Bootstrap",
        hub_summary="Phase 4–6 automations, labels, bootstrap, steady-state",
        audience=["pm"],
        authority="ops",
        doc_type="how-to",
        packs=[
            ("phase4_automations.md", ["6_phase_4_cursor_automations_dashboard"], "Phase 4 Cursor Automations"),
            (
                "labels_bootstrap_steady.md",
                ["7_phase_5_github_labels_issues", "8_phase_6_bootstrap_factory_loop", "9_steady_state_loop_no_human"],
                "Labels + bootstrap + steady-state",
            ),
        ],
    )
    split_by_title_keys(
        src_rel="ops/agents/mcp/setup_and_cost.md",
        pack_subdir="setup",
        hub_title="MCP — Setup & Cost",
        hub_summary="Rejected tools, licenses, setup checklist, troubleshoot",
        audience=["pm", "builder"],
        authority="ops",
        doc_type="how-to",
        packs=[
            (
                "rejected_licenses.md",
                ["explicitly_rejected_do_not_adopt", "licenses_cost"],
                "Rejected tools + licenses",
            ),
            (
                "checklist_troubleshoot.md",
                ["user_setup_checklist_purchase_secrets", "troubleshooting", "related"],
                "Checklist + troubleshoot + related",
            ),
        ],
    )
    split_by_title_keys(
        src_rel="ops/agents/secrets/webhooks.md",
        pack_subdir="hooks",
        hub_title="Secrets — Webhooks",
        hub_summary="PM cycle, factory alert, worker webhook URLs",
        audience=["pm", "builder"],
        authority="ops",
        doc_type="how-to",
        packs=[
            ("pm_cycle.md", ["2_cursor_pm_cycle_webhook_url"], "PM cycle webhook"),
            (
                "alert_worker.md",
                ["3_cursor_factory_alert_webhook_url", "3b_cursor_worker_webhook_url_cursor_worker_webhook_auth"],
                "Alert + worker webhooks",
            ),
        ],
    )
    split_by_title_keys(
        src_rel="ops/agents/pm_runbook/planning_watchdog.md",
        pack_subdir="ops",
        hub_title="PM Runbook — Planning & Watchdog",
        hub_summary="Sprint planning, close, watchdog, quick ref",
        audience=["pm"],
        authority="ops",
        doc_type="how-to",
        packs=[
            (
                "planning_close.md",
                ["5_sprint_planning_create_sync_issues", "6_sprint_close_checklist"],
                "Planning + close",
            ),
            (
                "watchdog_refs.md",
                ["7_watchdog_recovery_when_factory_stalls", "8_quick_reference", "9_cross_refs"],
                "Watchdog + quick ref",
            ),
        ],
    )

    new_paths = collect_new_mds(before)
    update_pack_catalog(new_paths)
    print(f"round8 done — {len(new_paths)} new md files")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
