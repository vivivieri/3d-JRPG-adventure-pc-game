#!/usr/bin/env python3
"""Docs pack round 5 — remaining fat must_read + optional hubs."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from enhance_docs_packs import (  # noqa: E402
    rethin_existing_hub,
    split_by_title_keys,
    split_numbered,
)


def main() -> int:
    # --- Must-read fat hubs ---
    split_numbered(
        src_rel="engineering/technical/CODE_STYLE.md",
        pack_subdir="code_style",
        hub_title="Code Style",
        hub_summary="Project code style — load layout, GDScript, or checklist",
        audience=["builder", "architect"],
        authority="engineering",
        doc_type="reference",
        packs=[
            ("layout_naming.md", ["1", "2"], "Folder layout + naming", None),
            ("gdscript_autoload_signals.md", ["3", "4", "5"], "GDScript, autoload, signals", None),
            ("data_scene_shader.md", ["6", "7", "8"], "Data access, scenes, shaders", None),
            ("errors_tests_checklist.md", ["9", "10", "11", "12", "13"], "Errors, comments, tests, assets, PR checklist", None),
        ],
    )

    split_numbered(
        src_rel="ops/agents/CLOUD_SNAPSHOT_LAUNCH.md",
        pack_subdir="snapshot",
        hub_title="Cloud Snapshot Launch",
        hub_summary="Snapshot launch — load dashboard branch, checklist, or rebuild",
        audience=["pm", "builder", "architect"],
        authority="ops",
        doc_type="tutorial",
        packs=[
            ("dashboard_branch.md", ["0", "1", "2"], "Dashboard branch + active snapshot + skip reasons", None),
            ("launch_checklist.md", ["3"], "Launch checklist every session", None),
            ("rebuild_gamelab_troubleshoot.md", ["4", "5", "6"], "Rebuild, GameLab transport, troubleshooting", None),
        ],
    )

    split_numbered(
        src_rel="design/gameplay/PROGRESSION_TUNING.md",
        pack_subdir="progression",
        hub_title="Progression & Tuning",
        hub_summary="XP/stats tuning — load curve, party, or difficulty",
        audience=["builder", "builder_combat", "qa"],
        authority="gameplay",
        doc_type="reference",
        phase=[2, 3],
        packs=[
            ("targets_xp.md", ["1", "2"], "Design targets + XP curve", [2, 3]),
            ("party_equipment_boss.md", ["3", "4", "5"], "Party stats, equipment, bosses", [2, 3]),
            ("difficulty_mp_qa.md", ["6", "7", "8", "9", "10"], "Difficulty, MP, milestones, workflow, QA", [2, 3]),
        ],
    )

    split_numbered(
        src_rel="ops/agents/SPRINT_ORCHESTRATION.md",
        pack_subdir="sprint_orch",
        hub_title="Sprint Orchestration",
        hub_summary="Enforced multi-agent workflow — load roles, flow, or escalation",
        audience=["pm"],
        authority="ops",
        doc_type="how-to",
        packs=[
            ("problem_sources_roles.md", ["1", "2", "3"], "Problem, sources of truth, roles", None),
            ("session_flow_carry.md", ["4", "5"], "Session flow + carry-over", None),
            ("escalation_ci_forbidden.md", ["6", "7", "8", "9"], "Escalation, CI, forbidden, cross-refs", None),
        ],
    )

    split_by_title_keys(
        src_rel="ops/agents/MCP_STACK.md",
        pack_subdir="mcp_stack",
        hub_title="MCP Stack",
        hub_summary="Full MCP toolchain — load R&R map, conflict rules, or startup",
        audience=["pm", "builder"],
        authority="ops",
        doc_type="how-to",
        packs=[
            ("rr_map.md", ["full_r_r_map"], "Full R&R map"),
            ("conflict_rules.md", ["role_split_conflict_rules"], "Role split & conflict rules"),
            ("session_startup.md", ["session_startup_every_agent_run"], "Session startup every run"),
            ("packs_gates.md", ["packs_progressive_disclosure", "related_gates"], "Existing packs + related gates"),
        ],
    )

    split_numbered(
        src_rel="ops/workflow/BRANCHING.md",
        pack_subdir="branching",
        hub_title="Branching Policy",
        hub_summary="main vs game/development — load roles, rules, or CI",
        audience=["pm", "architect", "builder", "release"],
        authority="workflow",
        doc_type="reference",
        packs=[
            ("roles_rules.md", ["1", "2"], "Branch roles + rules", None),
            ("workflow_ci.md", ["3", "4"], "Developer workflow + CI per branch", None),
            ("create_branch_refs.md", ["5", "6"], "Creating game branch + cross-refs", None),
        ],
    )

    split_by_title_keys(
        src_rel="design/vision/VO_HIT_LIST.md",
        pack_subdir="vo_hit",
        hub_title="Selective VO Hit List",
        hub_summary="12 emotional VO clips — load rules, hit list, or ElevenLabs setup",
        audience=["audio", "narrative"],
        authority="vision",
        doc_type="reference",
        packs=[
            ("rules_list.md", ["design_rules", "hit_list_12_clips"], "Design rules + 12-clip list"),
            ("layout_elevenlabs.md", ["file_layout", "ai_vo_setup_elevenlabs"], "File layout + ElevenLabs setup"),
            ("playback_ship.md", ["godot_playback_phase_2", "ship_checklist"], "Godot playback + ship checklist"),
        ],
    )

    split_numbered(
        src_rel="design/audio/AUDIO_DIRECTION.md",
        pack_subdir="direction",
        hub_title="Audio Direction",
        hub_summary="Audio direction — load music map, SFX, or mix",
        audience=["audio", "builder"],
        authority="audio",
        doc_type="reference",
        packs=[
            ("goals_music.md", ["1", "2"], "Design goals + music map", None),
            ("sfx_cues_mix.md", ["3", "4", "5"], "SFX taxonomy, scene cues, mix levels", None),
            ("sourcing_impl.md", ["6", "7", "8"], "Sourcing, implementation, production order", None),
        ],
    )

    # --- Engineering optionals ---
    split_numbered(
        src_rel="engineering/technical/ERROR_HANDLING.md",
        pack_subdir="errors",
        hub_title="Error Handling",
        hub_summary="Error handling — load principles, language patterns, or CI",
        audience=["architect", "builder"],
        authority="engineering",
        doc_type="reference",
        packs=[
            ("principles_format.md", ["1", "2"], "Principles + message format", None),
            ("language_exit.md", ["3", "4"], "Language patterns + exit codes", None),
            ("telemetry_ci_checklist.md", ["5", "6", "7", "8", "9"], "Logging, anti-patterns, CI, PR, links", None),
        ],
    )

    split_by_title_keys(
        src_rel="engineering/technical/LOCALIZATION.md",
        pack_subdir="i18n",
        hub_title="Localization",
        hub_summary="i18n — load architecture, translations, or fonts",
        audience=["architect", "narrative", "builder"],
        authority="engineering",
        doc_type="how-to",
        packs=[
            ("architecture_dialect.md", ["architecture", "traditional_chinese_dialect_vo"], "Architecture + ZH dialect VO"),
            ("translations_fonts.md", ["adding_translations", "fonts_cjk"], "Adding translations + CJK fonts"),
            ("steam_workflow_checklist.md", ["steam_store", "translator_workflow", "checklist_for_new_content"], "Steam, translator workflow, checklist"),
        ],
    )

    split_numbered(
        src_rel="engineering/technical/JSON_DATA_STYLE.md",
        pack_subdir="json_style",
        hub_title="JSON Data Style",
        hub_summary="JSON conventions — load schema shapes or integrity rules",
        audience=["architect", "builder"],
        authority="engineering",
        doc_type="reference",
        packs=[
            ("standards_format_naming.md", ["1", "2", "3", "4"], "Standards, format, naming, schema metadata", None),
            ("i18n_story_registry.md", ["5", "6", "7"], "i18n objects, story spine, registries", None),
            ("integrity_extend_pr.md", ["8", "9", "10", "11", "12"], "Integrity, extend, maintenance, anti-patterns, PR", None),
        ],
    )

    split_numbered(
        src_rel="engineering/technical/SAVE_AND_FAIL_STATES.md",
        pack_subdir="save",
        hub_title="Save & Fail States",
        hub_summary="Save system — load schema, persist rules, or fail states",
        audience=["architect", "builder", "qa"],
        authority="engineering",
        doc_type="reference",
        packs=[
            ("system_schema.md", ["1", "2", "3"], "Save system, schema, what persists", None),
            ("continue_fail.md", ["4", "5", "6"], "Continue, fail states, death vs story", None),
            ("scum_qa.md", ["7", "8"], "Save scumming + QA", None),
        ],
    )

    split_numbered(
        src_rel="engineering/technical/CODE_BASE_CLASS_RULES.md",
        pack_subdir="base_classes",
        hub_title="Code Base Class Rules",
        hub_summary="Extend-only base classes — load rules, components, or verification",
        audience=["architect", "builder"],
        authority="engineering",
        doc_type="reference",
        packs=[
            ("meaning_rules.md", ["1", "2"], "What inherit means + hard R&R", None),
            ("assets_components.md", ["3", "4"], "3D asset sources + component scenes", None),
            ("verify_refs.md", ["5", "6"], "Verification + cross-refs", None),
        ],
    )

    split_numbered(
        src_rel="engineering/technical/BASH_STYLE.md",
        pack_subdir="bash",
        hub_title="Bash Style",
        hub_summary="Shell script style — load template, CI gates, or checklist",
        audience=["architect", "builder"],
        authority="engineering",
        doc_type="reference",
        packs=[
            ("standards_template_naming.md", ["1", "2", "3", "4"], "Standards, template, naming, quoting", None),
            ("ci_logging.md", ["5", "6", "7"], "CI gate pattern, logging, Python invoke", None),
            ("antipatterns_pr.md", ["8", "9"], "Anti-patterns + PR checklist", None),
        ],
    )

    split_by_title_keys(
        src_rel="engineering/technical/PLUGIN_COMPATIBILITY.md",
        pack_subdir="plugin_compat",
        hub_title="Plugin Compatibility",
        hub_summary="Godot 4.7 plugin matrix — load engine, GDAI, or ship plugins",
        audience=["architect", "builder", "pm"],
        authority="engineering",
        doc_type="reference",
        packs=[
            ("summary_engine_gdai.md", ["summary", "godot_engine_4_7_stable", "gdai_mcp_build_primary"], "Summary, engine, GDAI"),
            ("godotiq_mcp_pro.md", ["godotiq_analyze_debug", "godot_mcp_pro_test_l4_l5"], "Godotiq + MCP Pro"),
            ("steam_enable_check.md", ["godotsteam_ship_phase_8_only", "editor_plugin_enablement", "automated_check", "if_a_plugin_fails_on_4_7", "related"], "Steam, enablement, check, fail, related"),
        ],
    )

    # --- Ops optionals ---
    split_by_title_keys(
        src_rel="ops/qa/PLAYTEST_TELEMETRY.md",
        pack_subdir="playtest_tel",
        hub_title="Playtest Telemetry",
        hub_summary="Human playtest JSONL — load schema, metrics, or privacy",
        audience=["qa", "flow"],
        authority="qa",
        doc_type="reference",
        packs=[
            ("purpose_pipeline_schema.md", ["purpose", "pipeline", "event_schema_jsonl"], "Purpose, pipeline, schema"),
            ("metrics_usage_logger.md", ["metrics_thresholds", "usage", "in_game_logger_implement_on_game_development_via_gdai"], "Metrics, usage, in-game logger"),
            ("privacy.md", ["privacy"], "Privacy"),
        ],
    )

    split_numbered(
        src_rel="ops/agents/PROJECT_MANAGEMENT.md",
        pack_subdir="pm_github",
        hub_title="Project Management",
        hub_summary="GitHub Issues PM — load labels, templates, or sprint checklist",
        audience=["pm"],
        authority="ops",
        doc_type="how-to",
        packs=[
            ("tools_labels.md", ["1", "2"], "Tool choice + label taxonomy", None),
            ("templates_trace_logs.md", ["3", "4", "5"], "Templates, traceability, log sources", None),
            ("mcp_board_checklist.md", ["6", "7", "8", "9"], "Optional MCP, board, PM checklist, refs", None),
        ],
    )

    split_numbered(
        src_rel="ops/qa/WORKFLOW_INTEGRATION.md",
        pack_subdir="workflow_int",
        hub_title="Workflow Integration",
        hub_summary="Register factory features before merge — load checklist or registry",
        audience=["pm", "architect"],
        authority="qa",
        doc_type="how-to",
        packs=[
            ("problem_register.md", ["1", "2"], "Problem + register-before-merge", None),
            ("checklist_features.md", ["3", "4"], "Add-feature checklist + registered features", None),
            ("alignment_gates.md", ["5", "6"], "Alignment coop + related gates", None),
        ],
    )

    split_numbered(
        src_rel="ops/agents/FACTORY_WATCHDOG.md",
        pack_subdir="watchdog",
        hub_title="Factory Watchdog",
        hub_summary="Stall recovery — load layers, commands, or playbook",
        audience=["pm"],
        authority="ops",
        doc_type="how-to",
        packs=[
            ("layers_monitor.md", ["1", "2"], "Two layers + what is monitored", None),
            ("commands_recovery.md", ["3", "4"], "Commands + recovery behavior", None),
            ("automations_playbook.md", ["5", "6", "7", "8"], "Automations, events, playbook, refs", None),
        ],
    )

    split_numbered(
        src_rel="ops/agents/PM_STAKEHOLDER_REPORTING.md",
        pack_subdir="stakeholder",
        hub_title="PM Stakeholder Reporting",
        hub_summary="Telegram/HTML stakeholder digests — load setup or report contents",
        audience=["pm"],
        authority="ops",
        doc_type="how-to",
        packs=[
            ("what_telegram.md", ["1", "2"], "What you get + Telegram setup", None),
            ("when_commands_contents.md", ["3", "4", "5"], "When reports fire, commands, contents", None),
            ("dashboard_duty_troubleshoot.md", ["6", "7", "8", "9", "10"], "Dashboard, duty, troubleshoot, alignment, refs", None),
        ],
    )

    split_numbered(
        src_rel="ops/qa/AGENT_JURY.md",
        pack_subdir="jury",
        hub_title="Agent Jury",
        hub_summary="Vision/audio jury protocol — load limitation or checklist",
        audience=["qa", "visual", "audio"],
        authority="qa",
        doc_type="how-to",
        packs=[
            ("why_limit.md", ["1", "2"], "Why + hard limitation", None),
            ("protocol_fields.md", ["3", "4", "5"], "Protocol, checklist fields, external API jury", None),
        ],
    )

    split_numbered(
        src_rel="ops/qa/CANDIDATE_TOURNAMENT.md",
        pack_subdir="tournament",
        hub_title="Candidate Tournament",
        hub_summary="L2.5 champion/challenger — load workflow or promotion rules",
        audience=["pm", "visual", "builder"],
        authority="qa",
        doc_type="how-to",
        packs=[
            ("what_stack_data.md", ["1", "2", "3"], "What it is, stack position, data files", None),
            ("workflow_promotion.md", ["4", "5", "6"], "Workflow, promotion, PM involvement", None),
            ("when_ci_forbidden.md", ["7", "8", "9", "10"], "When required, CI, forbidden, related", None),
        ],
    )

    split_numbered(
        src_rel="ops/ci-cd/ENVIRONMENTS.md",
        pack_subdir="environments",
        hub_title="Environments",
        hub_summary="dev→qa→uat→prod — load map, requirements, or promotion",
        audience=["pm", "release"],
        authority="ci-cd",
        doc_type="reference",
        packs=[
            ("map_preprod.md", ["1", "2"], "Environment map + preprod necessity", None),
            ("requirements_github.md", ["3", "4"], "Per-env requirements + GitHub Environments", None),
            ("promotion_logs.md", ["5", "6", "7"], "Promotion, log correlation, refs", None),
        ],
    )

    split_numbered(
        src_rel="ops/qa/PLATFORM_SUPPORT.md",
        pack_subdir="platform",
        hub_title="Platform Support",
        hub_summary="Linux+Windows v1 — load policy, platforms, or M6 matrix",
        audience=["release", "qa", "pm"],
        authority="qa",
        doc_type="reference",
        packs=[
            ("policy_platforms.md", ["1", "2", "3"], "Policy, platforms, dev env map", None),
            ("m6_perf_faq.md", ["4", "5", "6", "7"], "M6 deliverables, perf matrix, FAQ, related", None),
        ],
    )

    split_numbered(
        src_rel="design/art/ASSET_COMPLIANCE.md",
        pack_subdir="compliance",
        hub_title="Asset Compliance",
        hub_summary="License-safe assets — load allowed licenses or import workflow",
        audience=["visual", "builder", "release"],
        authority="art",
        doc_type="reference",
        packs=[
            ("rule_licenses.md", ["1", "2", "3"], "Golden rule, allowed, banned", None),
            ("workflow_proof.md", ["4", "5", "6"], "Import workflow, proof tools, documentation", None),
            ("credits_violations.md", ["7", "8", "9"], "Credits, cross-refs, violations", None),
        ],
    )

    split_numbered(
        src_rel="ops/ci-cd/GITHUB_SETUP.md",
        pack_subdir="github_setup",
        hub_title="GitHub Setup",
        hub_summary="Repo/Actions setup — load quick script or manual UI",
        audience=["pm", "release"],
        authority="ci-cd",
        doc_type="tutorial",
        packs=[
            ("quick_manual.md", ["1", "2"], "Quick setup + manual UI", None),
            ("secrets_verify.md", ["3", "4"], "CD secrets + verify", None),
            ("mcp_troubleshoot.md", ["5", "6"], "Optional MCP + troubleshooting", None),
        ],
    )

    split_numbered(
        src_rel="ops/qa/PLAYTEST_SCRIPT.md",
        pack_subdir="playtest_script",
        hub_title="Playtest Script",
        hub_summary="Human L6 playtest — load act scripts or survey",
        audience=["qa", "flow"],
        authority="qa",
        doc_type="how-to",
        packs=[
            ("goals_setup_act1.md", ["1", "2", "3"], "Goals, setup, Act I", None),
            ("act2_act3_regression.md", ["4", "5", "6"], "Act II, Act III, regression", None),
            ("feel_survey_bugs.md", ["7b", "8", "9"], "Feel checklist, survey, bugs", None),
        ],
    )

    split_numbered(
        src_rel="ops/ci-cd/CD.md",
        pack_subdir="cd",
        hub_title="Continuous Delivery",
        hub_summary="CD workflows — load purpose, Steam secrets, or remediation",
        audience=["release", "pm"],
        authority="ci-cd",
        doc_type="how-to",
        packs=[
            ("purpose_prereqs_workflows.md", ["1", "2", "3"], "Purpose, prerequisites, workflows", None),
            ("local_secrets.md", ["4", "5"], "Local CD + Steam secrets", None),
            ("vs_ci_remediation.md", ["6", "7", "8"], "CD vs CI, remediation, refs", None),
        ],
    )

    split_by_title_keys(
        src_rel="ops/qa/ESCALATION_POLICY.md",
        pack_subdir="escalation",
        hub_title="Escalation Policy",
        hub_summary="Bounded escalation ladder — load problem, ladder, or usage",
        audience=["pm", "qa"],
        authority="qa",
        doc_type="reference",
        packs=[
            ("problem_ladder.md", ["the_problem", "the_ladder_bounded_always_converges"], "Problem + ladder"),
            ("usage_bounds.md", ["using_it_tools_pm_escalate_py", "why_it_can_t_loop_forever"], "Usage + anti-loop"),
        ],
    )

    split_by_title_keys(
        src_rel="ops/workflow/BRANCHING_DECISION_RECORD.md",
        pack_subdir="branching_adr",
        hub_title="Branching Decision Record",
        hub_summary="Why main + game/development — load decision or rejected alternatives",
        audience=["pm", "architect"],
        authority="workflow",
        doc_type="explanation",
        packs=[
            ("context_decision.md", ["context", "decision", "comparison_with_common_strategies"], "Context, decision, comparison"),
            ("rejected_alternatives.md", ["why_environment_branches_were_rejected", "why_per_agent_forks_were_rejected", "why_trunk_based_was_not_rejected"], "Rejected alternatives"),
            ("consequences_compliance.md", ["consequences", "mapping_external_advice_this_project", "compliance", "references"], "Consequences, mapping, compliance, refs"),
        ],
    )

    # AI_DEV — move remaining fat §1 into pack, keep existing ai_dev packs via rethin after split
    split_numbered(
        src_rel="ops/workflow/AI_DEV_WORKFLOW.md",
        pack_subdir="ai_dev",
        hub_title="AI Dev Workflow",
        hub_summary="Build/test/acceptance policy — load build policy or existing packs",
        audience=["pm", "architect", "builder"],
        authority="workflow",
        doc_type="how-to",
        packs=[
            ("build_policy.md", ["1"], "AI build policy", None),
            ("packs_gates.md", ["related"], "Related gates (packs TOC lived here)", None),
        ],
    )
    # Note: existing ai_dev/*.md (commands, testing_policy, phase_acceptance) preserved;
    # hub rewrite only lists new packs — patch hub table after to include siblings.
    _patch_ai_dev_hub()

    # --- Design optionals ---
    split_numbered(
        src_rel="design/world/QUEST_AND_FLAGS.md",
        pack_subdir="quests",
        hub_title="Quests & Flags",
        hub_summary="Main quests + story flags — load quest list or flag master",
        audience=["narrative", "builder", "flow"],
        authority="world",
        doc_type="reference",
        packs=[
            ("main_quests_detail.md", ["1", "2"], "Main quests + detail", None),
            ("flags_blockers_party.md", ["3", "4", "5"], "Flag list, zone blockers, party join", None),
            ("ui_json_qa.md", ["6", "7", "8"], "Quest UI, JSON, QA", None),
        ],
    )

    split_numbered(
        src_rel="design/audio/AUDIO_QA.md",
        pack_subdir="audio_qa",
        hub_title="Audio QA",
        hub_summary="BGM/VO QA gates — load layers, smoke, or tools",
        audience=["audio", "qa"],
        authority="audio",
        doc_type="how-to",
        packs=[
            ("automate_layers.md", ["1", "2"], "Automate vs human + defense layers", None),
            ("smoke_workflow.md", ["3", "4", "5"], "L2 smoke, agent workflow, report template", None),
            ("tools_vs_visual.md", ["6", "7"], "Tools + vs Visual QA", None),
        ],
    )

    split_numbered(
        src_rel="design/gameplay/ITEMS_AND_ECONOMY.md",
        pack_subdir="economy",
        hub_title="Items & Economy",
        hub_summary="Items/shop/economy — load currency, equipment, or pacing",
        audience=["builder", "builder_combat", "qa"],
        authority="gameplay",
        doc_type="reference",
        packs=[
            ("currency_consumables_equip.md", ["1", "2", "3"], "Currency, consumables, equipment", None),
            ("key_materials_start_shop.md", ["4", "5", "6", "7"], "Key items, materials, start inv, shop", None),
            ("pacing_drops_qa.md", ["8", "9", "10", "11"], "Pacing, drops, JSON, QA", None),
        ],
    )

    split_numbered(
        src_rel="design/gameplay/TUTORIAL_DESIGN.md",
        pack_subdir="tutorial",
        hub_title="Tutorial Design",
        hub_summary="Teaching flow — load philosophy, matrix, or scene scripts",
        audience=["narrative", "builder", "flow"],
        authority="gameplay",
        doc_type="reference",
        packs=[
            ("philosophy_prologue_matrix.md", ["1", "2", "3"], "Philosophy, prologue, matrix", None),
            ("scenes_ui.md", ["4", "5"], "Scene scripts + prompt UI", None),
            ("not_taught_replay_qa.md", ["6", "7", "8"], "Not taught, replay, QA", None),
        ],
    )

    split_numbered(
        src_rel="design/gameplay/GAME_FEEL.md",
        pack_subdir="feel",
        hub_title="Game Feel",
        hub_summary="Juice & feedback — load combat, field, or UI feel",
        audience=["builder", "visual", "qa"],
        authority="gameplay",
        doc_type="reference",
        packs=[
            ("principles_combat.md", ["1", "2"], "Principles + combat feedback", None),
            ("field_puzzle_ui.md", ["3", "4", "5"], "Field, puzzle, UI feedback", None),
            ("story_shake_reward_qa.md", ["6", "7", "8", "9"], "Story, shake, rewards, QA", None),
        ],
    )

    split_numbered(
        src_rel="design/gameplay/ENCOUNTER_TABLE.md",
        pack_subdir="encounters",
        hub_title="Encounter Table",
        hub_summary="Encounters by act — load Act I–III or economy pacing",
        audience=["builder", "builder_combat", "qa"],
        authority="gameplay",
        doc_type="reference",
        packs=[
            ("goals_xp_act1.md", ["1", "2", "3"], "Goals, XP curve, Act I", None),
            ("act2_act3_summary.md", ["4", "5", "6"], "Act II, Act III, summary", None),
            ("economy_equip_policy_qa.md", ["7", "8", "9", "10", "11", "12"], "Economy, equipment, limit, hard, random, QA", None),
        ],
    )

    split_numbered(
        src_rel="design/ui/UI_UX_FLOW.md",
        pack_subdir="ui_flow",
        hub_title="UI/UX Flow",
        hub_summary="Screen map & flows — load HUD, combat UI, or input",
        audience=["builder", "visual"],
        authority="ui",
        doc_type="reference",
        packs=[
            ("screens_menu_hud.md", ["1", "2", "3", "4"], "Screen map, main menu, HUD, field menu", None),
            ("dialogue_combat_rewards.md", ["5", "6", "7", "8", "9"], "Dialogue, combat, rewards, choice, game over", None),
            ("input_qa.md", ["10", "11", "12"], "Keyboard/mouse, controller, QA", None),
        ],
    )

    split_numbered(
        src_rel="design/vision/LORE_AND_ENVIRONMENTAL_STORY.md",
        pack_subdir="lore",
        hub_title="Lore & Environmental Story",
        hub_summary="Discoverable lore — load catalog, placements, or zone storytelling",
        audience=["narrative", "builder", "visual"],
        authority="vision",
        doc_type="reference",
        packs=[
            ("intent_channels_catalog.md", ["1", "2", "3"], "Intent, channels, lore catalog", None),
            ("placement_inspect_hub.md", ["4", "5", "6"], "Placement map, inspect vs lore, hub emptiness", None),
            ("zones_box_checklists.md", ["7", "8", "9", "10"], "Per-zone story, box ladder, writer/QA checklists", None),
        ],
    )

    split_numbered(
        src_rel="design/vision/ENDING_DESIGN.md",
        pack_subdir="endings",
        hub_title="Ending Design",
        hub_summary="Three endings — load choice gate, outcomes, or credits",
        audience=["narrative", "flow"],
        authority="vision",
        doc_type="reference",
        packs=[
            ("intent_choice_outcomes.md", ["1", "2", "3"], "Intent, choice gate, outcomes", None),
            ("mirror_boss_credits.md", ["4", "5", "6"], "Mirror choice, boss resolution, credits", None),
            ("replay_achievements_qa.md", ["7", "8", "9", "10"], "Replay, achievements, voice notes, QA", None),
        ],
    )

    split_numbered(
        src_rel="design/gameplay/SKILLS_BIBLE.md",
        pack_subdir="skills",
        hub_title="Skills Bible",
        hub_summary="Party/enemy skills — load character kits or MP economy",
        audience=["builder", "builder_combat"],
        authority="gameplay",
        doc_type="reference",
        packs=[
            ("party_kits.md", ["1", "2", "3"], "Urashima, Yuzu, Roku skills", None),
            ("enemy_mp_scrolls.md", ["4", "5", "6"], "Enemy skills, MP, scrolls", None),
            ("hooks_qa.md", ["7", "8"], "Animation/SFX hooks + QA", None),
        ],
    )

    split_numbered(
        src_rel="design/vision/REPLAY_DESIGN.md",
        pack_subdir="replay",
        hub_title="Replay Design",
        hub_summary="New Game / gallery — load first-run vs replay or incentives",
        audience=["narrative", "flow"],
        authority="vision",
        doc_type="reference",
        packs=[
            ("intent_first_newgame.md", ["1", "2", "3"], "Intent, first vs replay, New Game", None),
            ("gallery_incentives_hard.md", ["4", "5", "6"], "Gallery, incentives, hard mode", None),
            ("mirror_economy_credits_qa.md", ["7", "8", "9", "10", "11"], "Mirror, economy, credits, backlog, QA", None),
        ],
    )

    split_numbered(
        src_rel="design/vision/NARRATIVE_DENSITY.md",
        pack_subdir="density",
        hub_title="Narrative Density",
        hub_summary="Line budget discipline — load decision tree or ship budgets",
        audience=["narrative"],
        authority="vision",
        doc_type="reference",
        packs=[
            ("problem_tree.md", ["1", "2"], "Problem + decision tree", None),
            ("budgets_pass.md", ["3", "4"], "Ship budgets + optimized pass", None),
            ("workflow_raise_anti.md", ["5", "6", "7"], "Workflow, raise budget, anti-patterns", None),
        ],
    )

    split_by_title_keys(
        src_rel="design/art/LICENSES.md",
        pack_subdir="licenses",
        hub_title="Licenses",
        hub_summary="Third-party license log — load fonts, audio, or 3D models",
        audience=["visual", "release", "audio"],
        authority="art",
        doc_type="reference",
        packs=[
            ("story_engine_fonts.md", ["story_source", "engine_plugins", "fonts_bundled"], "Story, engine, fonts"),
            ("audio_models.md", ["audio", "3d_models_cc0_kenney_dev_greybox_only", "3d_models_cc0_poly_haven_high_poly"], "Audio + 3D models"),
            ("art_code_ship.md", ["art_original_no_third_party_images", "3d_models_ship_status", "code", "checklist_before_steam_ship_m6"], "Art, ship status, code, M6 checklist"),
        ],
    )

    # Rethin any hubs that still carry leftover body after prior packs
    for rel, sub, title, summary in [
        ("ops/agents/MCP_STACK.md", "mcp_stack", "MCP Stack", "Full MCP toolchain — load R&R, conflict rules, or startup"),
        ("ops/workflow/AI_DEV_WORKFLOW.md", "ai_dev", "AI Dev Workflow", "Build/test/acceptance — load build policy or testing pack"),
    ]:
        rethin_existing_hub(rel, sub, title, summary)

    print("round5 splits done")
    return 0


def _patch_ai_dev_hub() -> None:
    """Ensure AI_DEV hub lists both new and pre-existing ai_dev packs."""
    hub = ROOT / "docs/ops/workflow/AI_DEV_WORKFLOW.md"
    pack_dir = ROOT / "docs/ops/workflow/ai_dev"
    if not hub.is_file() or not pack_dir.is_dir():
        return
    rows: list[tuple[str, str]] = []
    labels = {
        "build_policy.md": "AI build policy",
        "packs_gates.md": "Related gates",
        "commands.md": "Commands quick ref",
        "testing_policy.md": "AI testing policy",
        "phase_acceptance.md": "Phase acceptance",
        "README.md": "Pack index",
    }
    for path in sorted(pack_dir.glob("*.md")):
        if path.name == "README.md":
            continue
        rows.append((path.name, labels.get(path.name, path.stem.replace("_", " "))))
    table = "| Pack | Topic |\n|------|-------|\n"
    for name, label in rows:
        table += f"| [`{name}`](ai_dev/{name}) | {label} |\n"
    text = hub.read_text(encoding="utf-8")
    # Replace pack table region
    import re

    text2 = re.sub(
        r"\| Pack \| Topic \|.*?(\n\*\*|\n[A-Z]|\n$)",
        table + r"\1",
        text,
        count=1,
        flags=re.S,
    )
    if text2 == text:
        # append table after Hub line
        text2 = text.replace(
            "**Hub** — load only the pack for your current pass.\n\n",
            "**Hub** — load only the pack for your current pass.\n\n" + table + "\n",
            1,
        )
    hub.write_text(text2, encoding="utf-8")
    print("patched AI_DEV hub pack table")


if __name__ == "__main__":
    raise SystemExit(main())
