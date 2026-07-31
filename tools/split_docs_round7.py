#!/usr/bin/env python3
"""Docs pack round 7 — thin remaining fat pack siblings (>1.2k)."""
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


def split_by_h3(text: str) -> tuple[str, list[tuple[str, str]]]:
    lines = text.splitlines(keepends=True)
    preamble: list[str] = []
    sections: list[tuple[str, str]] = []
    current_heading = ""
    current_body: list[str] = []
    seen = False
    for line in lines:
        if line.startswith("### "):
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


def slug_heading(heading: str) -> str:
    key = re.sub(r"^#{2,3}\s+", "", heading).strip().lower()
    return re.sub(r"[^a-z0-9]+", "_", key).strip("_")


def split_leaf_by_h2(
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
    split_by_title_keys(
        src_rel=src_rel,
        pack_subdir=pack_subdir,
        hub_title=hub_title,
        hub_summary=hub_summary,
        audience=audience,
        authority=authority,
        doc_type=doc_type,
        packs=packs,
        phase=phase,
    )


def split_leaf_by_h3(
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
    preamble_h2, h2_sections = split_by_h2(text)
    if len(h2_sections) == 1:
        h2_heading, h2_body = h2_sections[0]
        body_wo_h2 = re.sub(r"^## .*\n", "", h2_body, count=1)
        intro, h3_sections = split_by_h3(body_wo_h2)
        titles = {slug_heading(h): b for h, b in h3_sections}
        preamble = preamble_h2 + f"{h2_heading}\n\n" + intro
    else:
        preamble, h3_sections = split_by_h3(text)
        titles = {slug_heading(h): b for h, b in h3_sections}

    pack_dir = src.parent / pack_subdir
    rows: list[tuple[str, str]] = []
    for name, keys, label in packs:
        parts = [titles[k] for k in keys if k in titles]
        missing = [k for k in keys if k not in titles]
        if missing:
            print(f"WARN {src_rel} missing H3 {missing}; have={sorted(titles)}")
        body = "\n".join(parts).strip() + "\n"
        if not body.strip():
            continue
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
            + body
        )
        write(pack_dir / name, content)
        rows.append((name, label))

    if not rows:
        print(f"SKIP empty packs: {src_rel}")
        return

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


def discover_h3_keys(src_rel: str) -> list[str]:
    text = strip_fm((ROOT / "docs" / src_rel).read_text(encoding="utf-8"))
    _, h2 = split_by_h2(text)
    body = text
    if len(h2) == 1:
        body = re.sub(r"^## .*\n", "", h2[0][1], count=1)
    _, h3 = split_by_h3(body)
    return [slug_heading(h) for h, _ in h3]


def split_h3_halves(
    src_rel: str,
    pack_subdir: str,
    hub_title: str,
    hub_summary: str,
    audience: list[str],
    authority: str,
    doc_type: str = "reference",
    phase: list[int] | None = None,
) -> None:
    keys = discover_h3_keys(src_rel)
    print(f"{src_rel} h3_count={len(keys)}")
    if len(keys) >= 2:
        mid = max(1, len(keys) // 2)
        split_leaf_by_h3(
            src_rel=src_rel,
            pack_subdir=pack_subdir,
            hub_title=hub_title,
            hub_summary=hub_summary,
            audience=audience,
            authority=authority,
            doc_type=doc_type,
            phase=phase,
            packs=[
                ("part_a.md", keys[:mid], f"{hub_title} (A)"),
                ("part_b.md", keys[mid:], f"{hub_title} (B)"),
            ],
        )
    elif len(keys) == 1:
        split_leaf_by_h3(
            src_rel=src_rel,
            pack_subdir=pack_subdir,
            hub_title=hub_title,
            hub_summary=hub_summary,
            audience=audience,
            authority=authority,
            doc_type=doc_type,
            phase=phase,
            packs=[("detail.md", keys, hub_summary)],
        )
    else:
        print(f"SKIP no H3: {src_rel}")


def main() -> int:
    split_leaf_by_h2(
        src_rel="engineering/technical/coding/ci_pr_commands.md",
        pack_subdir="ci_pr",
        hub_title="Coding — CI & PR",
        hub_summary="CI matrix, PR checklist, commands",
        audience=["architect", "builder"],
        authority="engineering",
        doc_type="reference",
        packs=[
            ("ci_matrix.md", ["9_ci_enforcement_matrix"], "CI enforcement matrix"),
            ("pr_checklist.md", ["10_pr_checklist_by_change_type"], "PR checklist by change type"),
            ("refs_commands.md", ["11_related_authority_docs", "12_quick_commands"], "Related docs + quick commands"),
        ],
    )
    split_leaf_by_h2(
        src_rel="engineering/technical/data/combat_economy.md",
        pack_subdir="combat_economy",
        hub_title="Data — Combat & Economy",
        hub_summary="Encounter/items/shop/achievements JSON shapes",
        audience=["architect", "builder"],
        authority="engineering",
        doc_type="reference",
        packs=[
            (
                "encounters_items.md",
                [
                    "6_encounter_data_encounters_story_encounters_json",
                    "8_items_tied_to_story_beats",
                ],
                "Encounters + story items",
            ),
            (
                "shop_achievements_newgame.md",
                [
                    "9_shop_as_data_shop_roku_shop_json",
                    "10_achievements_achievements_achievements_json",
                    "11_new_game_defaults_starting_new_game_json",
                ],
                "Shop, achievements, new game",
            ),
            ("combat_barks.md", ["18_combat_barks_on_enemy_entries"], "Enemy combat_barks"),
        ],
    )
    split_leaf_by_h3(
        src_rel="engineering/technical/gdscript_regen/checklist/phase1_visuals.md",
        pack_subdir="phase1",
        hub_title="Phase 1 Visuals Regen",
        hub_summary="ZoneVisuals + toon_base regen steps",
        audience=["architect", "builder"],
        authority="engineering",
        doc_type="how-to",
        phase=[1],
        packs=[
            ("prereqs_order.md", ["10_1_prerequisites", "10_2_regeneration_order_mandatory"], "Prereqs + order"),
            ("artifact_steps.md", ["10_3_per_artifact_steps"], "Per-artifact steps"),
            (
                "verify_handoff.md",
                [
                    "10_4_verify",
                    "10_5_builder_handoff_p1_02",
                    "10_6_recovering_prior_ports_diff_hints",
                    "10_7_one_command_checklist",
                ],
                "Verify, handoff, recover, checklist",
            ),
        ],
    )

    split_h3_halves(
        "design/art/characters/enemies.md",
        "enemies",
        "Character Bible — Enemies",
        "Enemy field/combat model briefs",
        ["visual", "builder"],
        "art",
    )
    split_leaf_by_h2(
        src_rel="design/art/visual_qa/judge_layers.md",
        pack_subdir="judge",
        hub_title="Visual QA — Judge Layers",
        hub_summary="What AI can judge + defense layers",
        audience=["visual", "qa"],
        authority="art",
        doc_type="how-to",
        packs=[
            ("what_ai_judges.md", ["1_what_ai_can_and_cannot_judge"], "What AI can/cannot judge"),
            ("defense_layers.md", ["2_defense_layers_use_all_not_pick_one"], "Defense layers"),
        ],
    )
    split_leaf_by_h2(
        src_rel="design/art/model_qa/layers_workflow.md",
        pack_subdir="layers",
        hub_title="Model QA — Layers & Workflow",
        hub_summary="Automate vs human, layers, agent workflow",
        audience=["visual", "qa"],
        authority="art",
        doc_type="how-to",
        packs=[
            ("automate_vs_human.md", ["1_what_to_automate_vs_human"], "Automate vs human"),
            ("defense_layers.md", ["2_defense_layers"], "Defense layers"),
            ("agent_workflow.md", ["3_agent_workflow_3d_model_task"], "Agent workflow"),
        ],
    )
    split_leaf_by_h2(
        src_rel="design/art/model_qa/polish_direction.md",
        pack_subdir="polish",
        hub_title="Model QA — Polish Direction",
        hub_summary="Polish cadence + who directs feel",
        audience=["visual", "qa"],
        authority="art",
        doc_type="how-to",
        packs=[
            ("cadence.md", ["8_model_polish_cadence_structured_iteration"], "Polish cadence"),
            ("who_directs.md", ["9_who_gives_direction_vs_who_knows_feels_right"], "Who directs feel"),
        ],
    )
    split_leaf_by_h2(
        src_rel="design/vision/narrative/emotional_rules.md",
        pack_subdir="emotional",
        hub_title="Narrative — Emotional Rules",
        hub_summary="JRPG emotional rules + external steals",
        audience=["narrative"],
        authority="vision",
        doc_type="reference",
        packs=[
            ("project_rules.md", ["11_jrpg_emotional_storytelling_project_rules"], "Project emotional rules"),
            ("external_steals.md", ["12_narrative_reference_steals_external_jrpgs"], "External JRPG steals"),
        ],
    )
    split_leaf_by_h2(
        src_rel="design/audio/production/bgm_and_scene_map.md",
        pack_subdir="bgm_map",
        hub_title="Audio Production — BGM & Scene Map",
        hub_summary="BGM track sheets + scene→audio map",
        audience=["audio", "builder"],
        authority="audio",
        doc_type="reference",
        packs=[
            ("bgm_sheets.md", ["3_bgm_track_sheets"], "BGM track sheets"),
            ("scene_map.md", ["4_scene_audio_map"], "Scene → audio map"),
        ],
    )
    split_leaf_by_h2(
        src_rel="design/audio/production/combat_sfx.md",
        pack_subdir="combat_sfx",
        hub_title="Audio Production — Combat SFX",
        hub_summary="Boss hooks, SFX manifest, loop template",
        audience=["audio", "builder"],
        authority="audio",
        doc_type="reference",
        packs=[
            ("boss_hooks.md", ["5_combat_boss_audio_hooks"], "Combat & boss hooks"),
            ("sfx_manifest.md", ["6_sfx_manifest"], "SFX manifest"),
            ("loop_template.md", ["7_loop_sheet_template"], "Loop sheet template"),
        ],
    )

    split_h3_halves(
        "ops/qa/testing/toolkit.md",
        "toolkit",
        "AI Testing — GDAI Toolkit",
        "GDAI MCP playtesting toolkit",
        ["qa", "builder"],
        "qa",
    )
    split_h3_halves(
        "ops/qa/acceptance/gate_catalog.md",
        "catalog",
        "Acceptance — Gate Catalog",
        "Gate catalog summary",
        ["qa", "pm"],
        "qa",
    )
    split_h3_halves(
        "ops/cheat-sheets/controls/gates_by_branch.md",
        "gates",
        "Controls — Gates by Branch",
        "Automated gates by branch",
        ["pm", "qa", "release"],
        "ops",
    )
    split_h3_halves(
        "ops/workflow/ai_dev/phase_acceptance.md",
        "phases",
        "AI Dev — Phase Acceptance",
        "Acceptance criteria by phase",
        ["pm", "qa", "architect"],
        "workflow",
    )
    split_h3_halves(
        "ops/ci-cd/ci/required_gates/what_runs.md",
        "runs",
        "CI — What Runs",
        "main vs game/development required gates",
        ["release", "qa", "pm"],
        "ci-cd",
    )
    split_h3_halves(
        "ops/agents/mcp/art_tools.md",
        "art",
        "MCP — Art Tools",
        "Art & design MCP/offline tools",
        ["visual", "builder", "pm"],
        "ops",
    )

    split_leaf_by_h2(
        src_rel="ops/qa/remediation/standards_loop.md",
        pack_subdir="loop",
        hub_title="Remediation — Standards & Loop",
        hub_summary="Industry map + FAIL remediation loop",
        audience=["qa", "pm"],
        authority="qa",
        doc_type="how-to",
        packs=[
            ("industry_map.md", ["1_industry_standards_we_map_to"], "Industry standards map"),
            ("remediation_loop.md", ["2_the_remediation_loop_required_on_every_fail"], "Remediation loop"),
        ],
    )
    split_leaf_by_h2(
        src_rel="ops/qa/perf/procedure_evidence.md",
        pack_subdir="procedure",
        hub_title="Perf — Procedure & Evidence",
        hub_summary="L3 perf procedure, evidence, plan, commands",
        audience=["qa", "release", "builder"],
        authority="qa",
        doc_type="how-to",
        packs=[
            ("procedure_evidence.md", ["7_test_procedure_l3_perf_review", "8_evidence_schema"], "Procedure + evidence schema"),
            ("gates_plan.md", ["9_relationship_to_gates", "10_implementation_plan"], "Gates relationship + plan"),
            ("commands_refs.md", ["11_commands", "12_related_docs"], "Commands + related"),
        ],
    )
    split_leaf_by_h2(
        src_rel="ops/qa/security/m6_player_protect.md",
        pack_subdir="m6",
        hub_title="Security — M6 Player Protect",
        hub_summary="M6 checklist + anti-tamper",
        audience=["release", "pm"],
        authority="qa",
        doc_type="how-to",
        packs=[
            ("ship_checklist.md", ["8_m6_ship_security_checklist"], "M6 ship security checklist"),
            ("anti_tamper.md", ["9_player_build_protection_anti_rip_anti_tamper"], "Player build protection"),
            ("related.md", ["11_related_docs"], "Related docs"),
        ],
    )
    split_leaf_by_h2(
        src_rel="ops/workflow/milestones/pre_build.md",
        pack_subdir="pre_build",
        hub_title="Milestones — Pre-build",
        hub_summary="M0 / M0c–M0h pre-build milestone packs",
        audience=["pm", "architect"],
        authority="workflow",
        doc_type="reference",
        packs=[
            (
                "m0_core.md",
                [
                    "m0_pre_production",
                    "m0c_pre_build_design_art_rebuild_specs",
                    "m0d_pre_build_game_design_gameplay_systems",
                ],
                "M0 / M0c / M0d",
            ),
            (
                "m0_narrative_pitch.md",
                ["m0f_pre_build_design_narrative_polish", "m0g_pitch_illustrations"],
                "M0f / M0g",
            ),
            (
                "m0_data_ai.md",
                ["m0e_story_data_layer_main_branch", "m0h_ai_dev_workflow_testing_main_baseline"],
                "M0e / M0h",
            ),
        ],
    )
    split_leaf_by_h2(
        src_rel="ops/workflow/ai_dev/testing_policy.md",
        pack_subdir="testing",
        hub_title="AI Dev — Testing Policy",
        hub_summary="AI testing policy + unit tests",
        audience=["pm", "qa", "architect", "builder"],
        authority="workflow",
        doc_type="how-to",
        packs=[
            ("ai_testing.md", ["2_ai_testing_policy"], "AI testing policy"),
            ("unit_tests.md", ["3_unit_tests"], "Unit tests"),
        ],
    )
    split_leaf_by_h2(
        src_rel="ops/workflow/agile/sprint_master_cadence.md",
        pack_subdir="cadence",
        hub_title="Agile — Sprint Master Cadence",
        hub_summary="Sprint Master role + duration recommendations",
        audience=["pm"],
        authority="workflow",
        doc_type="how-to",
        packs=[
            ("sprint_master.md", ["11_sprint_master_facilitator_role"], "Sprint Master role"),
            (
                "duration.md",
                [
                    "12_sprint_duration_recommendations",
                    "12_1_ai_native_cadence_pure_agent_implementation",
                ],
                "Duration + AI-native cadence",
            ),
        ],
    )
    split_leaf_by_h2(
        src_rel="ops/workflow/agile/linear_sprints.md",
        pack_subdir="linear",
        hub_title="Agile — Linear Sprints",
        hub_summary="Linear setup, ceremony, issue flow, Phase 1 example",
        audience=["pm"],
        authority="workflow",
        doc_type="how-to",
        packs=[
            (
                "setup_ceremony.md",
                [
                    "3_linear_setup_when_mcp_authenticated",
                    "4_sprint_ceremony_lightweight_ai_team",
                ],
                "Setup + ceremony",
            ),
            (
                "flow_example.md",
                ["5_issue_flow_github_linear", "6_example_phase_1_sprint_breakdown"],
                "Issue flow + Phase 1 example",
            ),
        ],
    )
    split_leaf_by_h2(
        src_rel="ops/agents/secrets/api_keys.md",
        pack_subdir="keys",
        hub_title="Secrets — API Keys",
        hub_summary="GameLab, GH, Telegram, ElevenLabs, Cursor API keys",
        audience=["pm", "builder"],
        authority="ops",
        doc_type="how-to",
        packs=[
            ("gamelab_gh.md", ["4_gamelab_api_key", "5_gh_token"], "GAMELAB + GH_TOKEN"),
            (
                "telegram_vo.md",
                ["6_telegram_bot_token_telegram_chat_id", "7_elevenlabs_api_key"],
                "Telegram + ElevenLabs",
            ),
            ("cursor_api.md", ["8_cursor_api_key"], "CURSOR_API_KEY"),
        ],
    )
    split_leaf_by_h2(
        src_rel="ops/agents/cloud_setup/setup_automations.md",
        pack_subdir="automations",
        hub_title="Cloud Setup — Automations",
        hub_summary="One-time setup + Cursor Automations",
        audience=["pm", "architect"],
        authority="ops",
        doc_type="tutorial",
        packs=[
            ("one_time.md", ["3_one_time_setup"], "One-time setup"),
            (
                "cursor_automations.md",
                ["4_cursor_automations_event_driven_not_cron"],
                "Cursor Automations",
            ),
        ],
    )
    split_leaf_by_h2(
        src_rel="ops/agents/gdai_setup/cloud_steam_troubleshoot.md",
        pack_subdir="cloud_steam",
        hub_title="GDAI Setup — Cloud / Steam / Troubleshoot",
        hub_summary="Cloud Agents config, Steam export, troubleshooting",
        audience=["pm", "builder", "release"],
        authority="ops",
        doc_type="how-to",
        packs=[
            ("cloud_agents.md", ["4_configure_cursor_cloud_agents"], "Configure Cloud Agents"),
            ("steam_export.md", ["5_before_steam_release_export"], "Before Steam export"),
            ("troubleshoot.md", ["6_troubleshooting"], "Troubleshooting"),
        ],
    )

    print("round7 done")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
