#!/usr/bin/env python3
"""Docs pack round 4 — release/language/factory/narrative splits."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from enhance_docs_packs import split_by_title_keys, split_numbered  # noqa: E402


def main() -> int:
    split_numbered(
        src_rel="ops/qa/SECURITY.md",
        pack_subdir="security",
        hub_title="Security",
        hub_summary="Ship security — load threat model, secrets, or M6 checklist",
        audience=["release", "pm", "architect"],
        authority="qa",
        doc_type="reference",
        packs=[
            ("threat_ship.md", ["1", "2"], "Threat model + ship build rule", None),
            ("secrets_ci_cloud.md", ["3", "4", "5"], "Secrets, CI gates, cloud factory", None),
            ("steam_supply.md", ["6", "7"], "Steam/CD + supply chain", None),
            ("m6_player_protect.md", ["8", "9", "11"], "M6 checklist, anti-tamper, related", None),
        ],
    )

    split_numbered(
        src_rel="ops/ci-cd/STEAM_RELEASE_CHECKLIST.md",
        pack_subdir="steam",
        hub_title="Steam Release Checklist",
        hub_summary="Steam ship checklist — load the phase you are on",
        audience=["release", "pm"],
        authority="ci-cd",
        doc_type="how-to",
        packs=[
            ("complete_tech.md", ["1", "2"], "Game complete + build/engine", None),
            ("steamworks_store.md", ["3", "4"], "Steamworks + store/marketing", None),
            ("legal_qa_release.md", ["5", "6", "7", "8", "9"], "Legal, QA, release sequence, commands, refs", None),
        ],
    )

    split_numbered(
        src_rel="engineering/technical/GDSCRIPT_STYLE.md",
        pack_subdir="gdscript",
        hub_title="GDScript Style",
        hub_summary="GDScript conventions — load naming, typing, or signals section",
        audience=["builder", "architect"],
        authority="engineering",
        doc_type="reference",
        packs=[
            ("standards_layout.md", ["1", "2", "3", "4"], "Standards, layout, naming, structure", None),
            ("typing_syntax_base.md", ["5", "6", "7", "8"], "Typing, Godot 4 syntax, base classes, autoload", None),
            ("data_signals_shaders.md", ["9", "10", "11"], "Data access, signals, shaders", None),
            ("errors_lint.md", ["12", "13", "14"], "Errors, comments, lint/tests", None),
        ],
    )

    split_numbered(
        src_rel="engineering/technical/PYTHON_STYLE.md",
        pack_subdir="python",
        hub_title="Python Style",
        hub_summary="Python tooling style — load PEP profile or project patterns",
        audience=["architect", "builder"],
        authority="engineering",
        doc_type="reference",
        packs=[
            ("standards_pep8.md", ["1", "2"], "Industry standards + PEP 8 profile", None),
            ("docs_types_patterns.md", ["3", "4", "5"], "Docstrings, types, project patterns", None),
            ("deps_test_pr.md", ["6", "7", "8", "9", "10"], "Deps, testing, anti-patterns, PR, links", None),
        ],
    )

    split_numbered(
        src_rel="engineering/technical/TYPESCRIPT_STYLE.md",
        pack_subdir="typescript",
        hub_title="TypeScript Style",
        hub_summary="MCP Pro TypeScript — load runtime or MCP patterns",
        audience=["architect", "builder"],
        authority="engineering",
        doc_type="reference",
        packs=[
            ("standards_where.md", ["1", "2", "3"], "Standards, where TS lives, runtime", None),
            ("naming_strict_mcp.md", ["4", "5", "6"], "Naming, strict TS, MCP patterns", None),
            ("rr_security_pr.md", ["7", "8", "9", "10", "11", "12", "13"], "R&R, lint, security, testing, PR", None),
        ],
    )

    split_numbered(
        src_rel="ops/agents/FACTORY_SETUP_GUIDE.md",
        pack_subdir="factory_setup",
        hub_title="Factory Setup Guide",
        hub_summary="Multi-agent factory setup — load the phase you are configuring",
        audience=["pm", "architect"],
        authority="ops",
        doc_type="tutorial",
        packs=[
            ("what_boundaries.md", ["1", "2"], "What you build + control boundaries", None),
            ("phases_snapshot_secrets_mcp.md", ["3", "4", "5"], "Snapshot, secrets, MCP", None),
            ("automations_github_bootstrap.md", ["6", "7", "8", "9"], "Automations, labels, bootstrap, steady-state", None),
            ("audit_antipatterns.md", ["10", "11", "12"], "Audit, anti-patterns, cross-refs", None),
        ],
    )

    split_numbered(
        src_rel="ops/qa/ALIGNMENT_AUDIT.md",
        pack_subdir="alignment",
        hub_title="Alignment Audit",
        hub_summary="Spec↔build alignment — load run rules or radar visuals",
        audience=["pm", "qa"],
        authority="qa",
        doc_type="how-to",
        packs=[
            ("purpose_when_run.md", ["1", "2", "3"], "Purpose, when, how to run", None),
            ("verdict_scores.md", ["4", "5", "6"], "Verdict rules, radar axes, checklist", None),
            ("visuals_history_integration.md", ["7", "8", "9", "10", "11"], "Visuals, history, stakeholder, workflow, catalog", None),
        ],
    )

    split_numbered(
        src_rel="ops/agents/PM_AGENT_RUNBOOK.md",
        pack_subdir="pm_runbook",
        hub_title="PM Agent Runbook",
        hub_summary="Sprint Master runbook — load dispatch, close-loop, or watchdog",
        audience=["pm"],
        authority="ops",
        doc_type="how-to",
        packs=[
            ("orchestrator_dispatch.md", ["0", "1", "2"], "Sprint Master, orchestrator, dispatch", None),
            ("close_loop_features.md", ["3", "3b", "4"], "Close loop, factory features, stale agents", None),
            ("planning_watchdog.md", ["5", "6", "7", "8", "9"], "Planning, close, watchdog, never-do, refs", None),
        ],
    )

    split_numbered(
        src_rel="design/ui/CINEMATICS.md",
        pack_subdir="cinematics",
        hub_title="Cinematics",
        hub_summary="Cameras & cinematics — load exploration, combat, or ending pack",
        audience=["builder", "visual", "narrative"],
        authority="ui",
        doc_type="reference",
        phase=[1, 5],
        packs=[
            ("global_field_dialogue.md", ["1", "2", "3"], "Global, field, dialogue cameras", [1, 5]),
            ("combat_boss.md", ["4", "5", "6"], "Combat transitions + boss cameras", [2, 5]),
            ("storyboard_endings.md", ["7", "8"], "Storyboard specs + endings", [5, 6]),
            ("vfx_impl_checklist.md", ["9", "10", "11", "12", "13"], "VFX, Godot hooks, skip, M5 priority, checklist", [5]),
        ],
    )

    split_numbered(
        src_rel="design/vision/STORYBOARD_ILLUSTRATIONS.md",
        pack_subdir="illustrations",
        hub_title="Storyboard Illustrations",
        hub_summary="Pitch illustration briefs — load style, shot list, or prompts",
        audience=["visual", "narrative", "pm"],
        authority="vision",
        doc_type="how-to",
        packs=[
            ("why_style_layout.md", ["1", "2", "3"], "Why, visual style, file layout", None),
            ("shots_briefs.md", ["4", "5"], "Priority shot list + per-scene briefs", None),
            ("prompts_pitch_qa.md", ["6", "7", "8", "9", "10"], "Prompts, regen, pitch deck, 3D relationship, QA", None),
        ],
    )

    split_numbered(
        src_rel="ops/qa/PERFORMANCE_BASELINE.md",
        pack_subdir="perf",
        hub_title="Performance Baseline",
        hub_summary="Perf profiles — load reference PC or Steam minimum",
        audience=["qa", "builder", "release"],
        authority="qa",
        doc_type="reference",
        packs=[
            ("why_profiles.md", ["1", "2"], "Why + profile summary", None),
            ("reference_machines.md", ["3", "4", "5", "6"], "Cloud/PC/Steam/invalid envs", None),
            ("procedure_evidence.md", ["7", "8", "9", "10", "11", "12"], "Procedure, evidence, gates, plan, commands", None),
        ],
    )

    split_numbered(
        src_rel="ops/qa/AGENT_SESSION_TELEMETRY.md",
        pack_subdir="telemetry",
        hub_title="Agent Session Telemetry",
        hub_summary="Session telemetry — load storage, tokens, or analysis",
        audience=["pm", "qa"],
        authority="qa",
        doc_type="reference",
        packs=[
            ("what_storage_hooks.md", ["1", "2", "3"], "What logs, storage, hooks", None),
            ("tokens_analysis.md", ["4", "5", "6"], "Token reporting, analysis, categories", None),
            ("privacy_refs.md", ["7", "8", "9"], "Privacy, cross-refs, workflow coop", None),
        ],
    )

    split_by_title_keys(
        src_rel="ops/agents/PLUGIN_INSTALL_GUIDE.md",
        pack_subdir="plugins",
        hub_title="Plugin Install Guide",
        hub_summary="Godotiq / MCP Pro install — load the plugin you need",
        audience=["builder", "pm"],
        authority="ops",
        doc_type="how-to",
        packs=[
            ("godotiq.md", ["godotiq"], "Godotiq install"),
            ("mcp_pro.md", ["godot_mcp_pro"], "Godot MCP Pro install"),
            ("stack_troubleshoot.md", ["install_everything_full_mcp_stack", "troubleshooting", "ship_builds", "related"], "Full stack, troubleshoot, ship"),
        ],
    )

    split_numbered(
        src_rel="ops/agents/MULTI_AGENT_TEAM.md",
        pack_subdir="multi_agent",
        hub_title="Multi-Agent Team",
        hub_summary="Team roster & handoffs — load lifecycle or parallel patterns",
        audience=["pm", "builder", "qa"],
        authority="ops",
        doc_type="explanation",
        packs=[
            ("why_roster_lifecycle.md", ["1", "2", "3"], "Why, roster, session lifecycle", None),
            ("handoffs_parallel.md", ["4", "5", "6"], "Handoffs, parallel patterns, env matrix", None),
            ("startup_done.md", ["7", "8", "9", "10"], "Cloud startup, subagents, DoD, refs", None),
        ],
    )

    split_numbered(
        src_rel="engineering/technical/SPEC_FIRST_DEVELOPMENT.md",
        pack_subdir="spec_first",
        hub_title="Spec-First Development",
        hub_summary="Spec-before-code gate — load rule, registries, or refinement mode",
        audience=["architect", "pm"],
        authority="engineering",
        doc_type="how-to",
        packs=[
            ("rule_registries_gate.md", ["1", "2", "3", "4"], "Core rule, what is spec, registries, start gate", None),
            ("build_coverage.md", ["5", "6", "7", "8"], "Build workflow, not on main, coverage, anti-patterns", None),
            ("refinement_refs.md", ["10", "11"], "Spec refinement mode + cross-refs", None),
        ],
    )

    split_numbered(
        src_rel="design/gameplay/COMBAT_SYSTEMS.md",
        pack_subdir="combat",
        hub_title="Combat Systems",
        hub_summary="Combat rules — load turns, elements, or UI states",
        audience=["builder", "builder_combat", "qa"],
        authority="gameplay",
        doc_type="reference",
        phase=[2, 3],
        packs=[
            ("turns_elements_stats.md", ["1", "2", "3"], "Turn structure, elements, stats", [2]),
            ("status_limit_intent.md", ["4", "5", "6"], "Status, limit gauge, enemy intent", [2, 3]),
            ("party_xp_ui_qa.md", ["7", "8", "9", "10", "11"], "Party, XP, UI, hard mode, QA", [2, 3]),
        ],
    )

    print("done")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
