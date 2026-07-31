#!/usr/bin/env python3
"""Docs pack round 6 — leftover sprint dump, FRONTMATTER, fat pack siblings, urashima brief."""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from enhance_docs_packs import (  # noqa: E402
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


def split_sprint_issues() -> None:
    src_rel = "ops/sprints/Phase1-Sprint1-issues.md"
    src = ROOT / "docs" / src_rel
    text = strip_fm(src.read_text(encoding="utf-8"))
    preamble, sections = split_by_h2(text)
    titles = by_title(sections)

    packs: list[tuple[str, list[str], str]] = [
        ("labels.md", ["labels_apply_to_every_issue"], "Shared labels"),
        ("p1_00_bootstrap.md", ["p1_00_bootstrap_game_development_prerequisite"], "P1-00 bootstrap"),
        (
            "p1_01_architect_toon.md",
            ["p1_01_architect_toon_shader_zone_visuals", "handoff_to_builder_p1_02"],
            "P1-01 architect toon + Builder handoff",
        ),
        (
            "p1_02_builder_village.md",
            ["p1_02_builder_gdai_ruined_village_greybox_vertical_slice", "handoff_to_qa"],
            "P1-02 Builder greybox + QA handoff",
        ),
        ("p1_03_architect_water.md", ["p1_03_architect_water_stylized_shader_parallel"], "P1-03 water shader"),
        (
            "p1_04_qa_ci.md",
            ["p1_04_qa_ci_green_phase_1_gate_report", "gate_report_phase1_sprint1"],
            "P1-04 QA CI + gate report",
        ),
        (
            "p1_05_golden_screenshot.md",
            ["p1_05_qa_builder_golden_screenshot_zone_composition_gr_001_gr_003"],
            "P1-05 golden screenshot",
        ),
        (
            "p1_06_review_preview.md",
            [
                "p1_06_pm_phase_1_sprint_review_carry_over",
                "phase1_sprint2_preview_file_issues_next_cycle",
                "quick_copy_github_issue_titles_only",
            ],
            "P1-06 review + Sprint2 preview",
        ),
    ]

    pack_dir = src.parent / "phase1_sprint1"
    rows: list[tuple[str, str]] = []
    for name, keys, label in packs:
        parts = [titles[k] for k in keys if k in titles]
        missing = [k for k in keys if k not in titles]
        if missing:
            print(f"WARN sprint missing keys {missing}; available={sorted(titles)[:20]}…")
        body = "\n".join(parts).strip() + "\n"
        if not body.strip():
            continue
        content = (
            fm(
                Path(name).stem.replace("_", "-"),
                "how-to",
                ["pm", "architect", "builder", "qa"],
                "ops",
                max(200, len(body) // 4),
                [1],
                summary=label,
            )
            + f"# Phase1-Sprint1 — {label}\n\n"
            + f"**Hub:** [`{src.name}`](../{src.name})\n\n"
            + body
        )
        write(pack_dir / name, content)
        rows.append((name, label))

    hub = (
        fm(
            "phase1-sprint1-issues",
            "how-to",
            ["pm", "architect", "builder", "qa"],
            "ops",
            max(250, 180 + len(pack_table("phase1_sprint1", rows)) // 4),
            [1],
            summary="Phase1-Sprint1 GitHub issue pack — load one issue at a time",
        )
        + "# Phase1-Sprint1 — GitHub Issue Pack\n\n"
        + "**Hub** — never auto-loaded; open one issue pack per dispatch.\n\n"
        + pack_table("phase1_sprint1", rows)
        + short_blurb(preamble)
        + "\n"
    )
    write(src, hub)


def fix_frontmatter_schema() -> None:
    """Correct false tokens_est (example YAML was scanned as 3500)."""
    path = ROOT / "docs/_meta/FRONTMATTER.md"
    text = path.read_text(encoding="utf-8")
    # Shrink example budget so scanners don't treat schema as a 3.5k doc
    text = text.replace("tokens_est: 3500         # optional soft budget", "tokens_est: 450          # optional soft budget")
    if not text.startswith("---\n"):
        fm_block = (
            "---\n"
            "id: frontmatter-schema\n"
            "type: reference\n"
            "audience: [pm, architect, builder, qa]\n"
            "phase: [0]\n"
            "status: active\n"
            "authority: meta\n"
            "tokens_est: 320\n"
            'summary: "YAML frontmatter schema for docs/**/*.md"\n'
            "---\n"
        )
        text = fm_block + text
    else:
        text = re.sub(r"(?m)^tokens_est:\s*\d+", "tokens_est: 320", text, count=1)
    path.write_text(text if text.endswith("\n") else text + "\n", encoding="utf-8")
    print("fixed docs/_meta/FRONTMATTER.md")


def patch_hub_table(hub_rel: str, pack_subdir: str, extra_rows: list[tuple[str, str]]) -> None:
    hub = ROOT / "docs" / hub_rel
    if not hub.is_file():
        return
    text = hub.read_text(encoding="utf-8")
    for name, label in extra_rows:
        needle = f"[`{name}`]({pack_subdir}/{name})"
        if needle in text:
            continue
        # Insert before end of pack table (blank line after table)
        row = f"| [`{name}`]({pack_subdir}/{name}) | {label} |\n"
        if "| Pack | Topic |" in text:
            # append after last table row that references pack_subdir
            lines = text.splitlines(keepends=True)
            out: list[str] = []
            last_pack_row = -1
            for i, line in enumerate(lines):
                out.append(line)
                if f"]({pack_subdir}/" in line:
                    last_pack_row = len(out) - 1
            if last_pack_row >= 0:
                out.insert(last_pack_row + 1, row)
                text = "".join(out)
            else:
                text = text.replace(
                    "| Pack | Topic |\n|------|-------|\n",
                    "| Pack | Topic |\n|------|-------|\n" + row,
                    1,
                )
    # Refresh tokens_est roughly
    tokens = max(250, len(text) // 4)
    text = re.sub(r"(?m)^tokens_est:\s*\d+", f"tokens_est: {min(tokens, 600)}", text, count=1)
    hub.write_text(text if text.endswith("\n") else text + "\n", encoding="utf-8")
    print(f"patched hub table {hub_rel}")


def main() -> int:
    split_sprint_issues()
    fix_frontmatter_schema()

    # Split fat CI pack sibling further
    # required_gates only has ## 2 and ## 3 — use title keys after renumbering via title split
    split_by_title_keys(
        src_rel="ops/ci-cd/ci/required_gates.md",
        pack_subdir="required_gates",
        hub_title="CI Required Gates",
        hub_summary="What CI runs / does not run — load main gates or exclusions",
        audience=["release", "qa", "pm"],
        authority="ci-cd",
        doc_type="reference",
        packs=[
            ("what_runs.md", ["2_what_ci_runs_required_blocks_merge"], "What CI runs (required)"),
            ("what_not.md", ["3_what_ci_does_not_run"], "What CI does not run"),
        ],
        phase=[6, 8],
    )
    # required_gates.md was itself a pack under CI.md — now it's a sub-hub.
    # Point CI.md at the thin required_gates hub (already linked) — OK.
    # Also add deep packs to CI hub for discoverability.
    patch_hub_table(
        "ops/ci-cd/CI.md",
        "ci",
        [
            ("required_gates/what_runs.md", "CI what-runs detail"),
            ("required_gates/what_not.md", "CI exclusions detail"),
        ],
    )

    # Split fat gdscript_regen checklist pack
    split_numbered(
        src_rel="engineering/technical/gdscript_regen/checklist_recover.md",
        pack_subdir="checklist",
        hub_title="GDScript Regen — Checklist & Phase 1",
        hub_summary="Checklist/recover helpers or Phase 1 visuals",
        audience=["architect", "builder"],
        authority="engineering",
        doc_type="how-to",
        phase=[1, 2],
        packs=[
            ("checklist_helpers.md", ["6", "7", "8", "9"], "Checklist, recover, new helpers, ref map", [1, 2]),
            ("phase1_visuals.md", ["10"], "Phase 1 ZoneVisuals + toon_base", [1]),
        ],
    )
    patch_hub_table(
        "engineering/technical/GDSCRIPT_REGENERATION.md",
        "gdscript_regen",
        [
            ("checklist/checklist_helpers.md", "Checklist + recover helpers"),
            ("checklist/phase1_visuals.md", "Phase 1 visuals (P1-01)"),
        ],
    )

    # Fat urashima generation brief (never_autoload but still progressive)
    split_by_title_keys(
        src_rel="briefs/urashima.md",
        pack_subdir="urashima",
        hub_title="Urashima Generation Brief",
        hub_summary="Hero gen brief — load prompts, metrics, or acceptance",
        audience=["visual", "builder"],
        authority="briefs",
        doc_type="how-to",
        packs=[
            (
                "intent_prompts.md",
                [
                    "intent_one_sentence",
                    "emotional_intent_jury_human_rubric",
                    "tool_chain",
                    "positive_prompt_anchors",
                    "negative_prompt_required",
                ],
                "Intent + prompts",
            ),
            (
                "metrics_props.md",
                [
                    "hard_metrics_qa_catalog_json",
                    "lacquer_box_attached_prop",
                    "camera_distance_readability_x_02",
                    "costume_layers_model_order",
                ],
                "Hard metrics + props",
            ),
            (
                "acceptance_forbidden.md",
                ["acceptance_evidence", "forbidden"],
                "Acceptance + forbidden",
            ),
        ],
        phase=[1, 5],
    )

    print("round6 done")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
