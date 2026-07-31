#!/usr/bin/env python3
"""Split remaining fat hubs for docs-pack enhance batch + re-thin leftover hub bodies."""
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
        match = re.match(r"##\s+(\d+[A-Za-z]?)\b", heading)
        if match:
            out[match.group(1)] = body
            out[match.group(1).upper()] = body
            out[match.group(1).lower()] = body
        elif heading.startswith("## Related"):
            out["related"] = body
    return out


def by_title(sections: list[tuple[str, str]]) -> dict[str, str]:
    out: dict[str, str] = {}
    for heading, body in sections:
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
        safe = summary.replace("\n", " ").replace('"', "'").strip()[:160]
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


def short_blurb(preamble: str, max_chars: int = 420) -> str:
    text = strip_fm(preamble).strip()
    # Drop duplicate H1 after hub title
    lines = []
    for line in text.splitlines():
        if line.startswith("# "):
            continue
        lines.append(line)
    text = "\n".join(lines).strip()
    if len(text) <= max_chars:
        return text + ("\n" if text else "")
    cut = text[:max_chars]
    if "\n" in cut:
        cut = cut.rsplit("\n", 1)[0]
    return cut.rstrip() + "\n"


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


def split_numbered(
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
    keep_blurb: bool = True,
) -> None:
    src = DOCS / src_rel
    text = strip_fm(load_source(src_rel))
    preamble, sections = split_by_h2(text)
    nums = by_num(sections)
    if not nums:
        # fall back to title keys for non-numbered hubs
        titles = by_title(sections)
        print(f"INFO {src_rel}: using title keys {list(titles)[:8]}")
        # remap numeric keys from packs? handled by titled split callers
        nums = titles
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
                max(200, len(body) // 4),
                pphase or phase,
                summary=label,
            )
            + f"# {hub_title} — {label}\n\n**Hub:** [`{src.name}`](../{src.name})\n\n"
            + body
        )
        write(pack_dir / name, content)
        rows.append((name, label))
    blurb = short_blurb(preamble) if keep_blurb else ""
    hub = (
        fm(
            src.stem.lower().replace("_", "-"),
            doc_type,
            audience,
            authority,
            max(250, 180 + len(pack_table(pack_subdir, rows)) // 4),
            phase,
            summary=hub_summary,
        )
        + f"# {hub_title}\n\n**Hub** — load only the pack for your current pass.\n\n"
        + pack_table(pack_subdir, rows)
        + (blurb + "\n" if blurb else "")
    )
    write(src, hub)


def rethin_existing_hub(rel: str, pack_subdir: str, hub_title: str, hub_summary: str) -> None:
    """Strip leftover full-body after pack TOC on already-split hubs."""
    src = DOCS / rel
    text = src.read_text(encoding="utf-8")
    if "Pack | Topic" not in text and "| Pack |" not in text:
        print(f"skip rethin (no pack table): {rel}")
        return
    # Keep frontmatter + content until end of pack table
    fm_match = re.match(r"^---\n.*?\n---\n", text, flags=re.S)
    fm_block = fm_match.group(0) if fm_match else ""
    body = text[len(fm_block) :]
    lines = body.splitlines(keepends=True)
    out: list[str] = []
    in_table = False
    for i, line in enumerate(lines):
        out.append(line)
        if "| Pack |" in line or line.strip().startswith("| Pack"):
            in_table = True
        if in_table and line.strip() == "":
            # end of table + blank — keep one short blurb paragraph if next isn't another H1 dump
            # peek remaining for a short blurb (stop at duplicate H1)
            rest = "".join(lines[i + 1 :])
            blurb_lines: list[str] = []
            for rl in rest.splitlines():
                if rl.startswith("# "):
                    break
                if rl.startswith("## "):
                    break
                blurb_lines.append(rl)
                if sum(len(x) for x in blurb_lines) > 420:
                    break
            blurb = "\n".join(blurb_lines).strip()
            if blurb:
                out.append(blurb + "\n")
            break
    # rewrite tokens_est + summary in fm
    tokens = max(250, len("".join(out)) // 4)
    if fm_block:
        fm_block = re.sub(r"(?m)^tokens_est:\s*\d+", f"tokens_est: {tokens}", fm_block)
        if "summary:" in fm_block:
            fm_block = re.sub(
                r'(?m)^summary:\s*".*"',
                f'summary: "{hub_summary}"',
                fm_block,
            )
        else:
            fm_block = fm_block.replace(
                "---\n\n",
                f'summary: "{hub_summary}"\n---\n\n',
            ) if fm_block.endswith("---\n") else fm_block
    write(src, fm_block + "".join(out))


def split_by_title_keys(
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
    src = DOCS / src_rel
    text = strip_fm(load_source(src_rel))
    preamble, sections = split_by_h2(text)
    titles = by_title(sections)
    pack_dir = src.parent / pack_subdir
    rows: list[tuple[str, str]] = []
    for name, keys, label in packs:
        parts = [titles[k] for k in keys if k in titles]
        body = "\n".join(parts).strip() + "\n"
        if not body.strip():
            print(f"WARN empty titled {name} keys={keys} available={sorted(titles)}")
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
            max(250, 180 + len(pack_table(pack_subdir, rows)) // 4),
            phase,
            summary=hub_summary,
        )
        + f"# {hub_title}\n\n**Hub** — load only the pack for your current pass.\n\n"
        + pack_table(pack_subdir, rows)
        + short_blurb(preamble)
        + "\n"
    )
    write(src, hub)


def main() -> int:
    # Re-thin prior hot-path hubs (leftover full body after TOC)
    rethin_existing_hub(
        "design/art/ART_DIRECTION.md",
        "direction",
        "Art Direction",
        "Palette, silhouettes, style rules — load the section for your pass",
    )
    rethin_existing_hub(
        "design/art/ART_AUTOMATION_PIPELINE.md",
        "automation",
        "Art Automation Pipeline",
        "Tool tiers and workflows — load the asset class you are generating",
    )
    rethin_existing_hub(
        "design/world/ENVIRONMENT_KITS.md",
        "env_kits",
        "Environment Kits",
        "Per-zone lighting, kits, LOD — load only the active zone pack",
    )
    rethin_existing_hub(
        "design/art/RENDERING_GUIDE.md",
        "rendering",
        "Rendering Guide",
        "Tonemap, fog, glow, shadows — load the section for your pass",
    )

    split_numbered(
        src_rel="design/art/VISUAL_QA.md",
        pack_subdir="visual_qa",
        hub_title="Visual QA",
        hub_summary="Screenshot + vision gates — load the layer for your pass",
        audience=["visual", "builder", "qa"],
        authority="art",
        doc_type="how-to",
        phase=[1, 5],
        packs=[
            ("judge_layers.md", ["1", "2"], "What AI can judge + defense layers", [1, 5]),
            ("tools_antipattern.md", ["2H", "3"], "Tools + black-box anti-pattern", [1, 5]),
            ("report_phase_tools.md", ["4", "5", "6"], "Report template, phase gates, tools", [1, 5]),
        ],
    )
    # VISUAL_QA has ## 2H — by_num only catches digits; fix 2H via title split merge
    # Re-run with title keys for 2H if empty
    vqa_tools = DOCS / "design/art/visual_qa/tools_antipattern.md"
    if not vqa_tools.is_file() or vqa_tools.stat().st_size < 200:
        text = strip_fm(load_source("design/art/VISUAL_QA.md"))
        _, sections = split_by_h2(text)
        titles = by_title(sections)
        body = "\n".join(
            titles[k]
            for k in titles
            if k.startswith("2h") or k.startswith("3_") or k == "3_the_black_box_scenario_explicit_anti_pattern"
        )
        # more robust: grab by heading prefix
        parts = []
        for heading, body_s in sections:
            h = heading.lower()
            if "2h." in h or h.startswith("## 3."):
                parts.append(body_s)
        body = "\n".join(parts).strip() + "\n"
        write(
            vqa_tools,
            fm("tools-antipattern", "how-to", ["visual", "builder", "qa"], "art", max(200, len(body) // 4), [1, 5], "Tools + black-box anti-pattern")
            + "# Visual QA — Tools + black-box anti-pattern\n\n**Hub:** [`VISUAL_QA.md`](../VISUAL_QA.md)\n\n"
            + body,
        )

    split_numbered(
        src_rel="design/art/GENERATION_READINESS.md",
        pack_subdir="generation_readiness",
        hub_title="Generation Readiness",
        hub_summary="Human-expectation gaps for AI 3D — load character or zone rows",
        audience=["visual", "builder"],
        authority="art",
        doc_type="reference",
        phase=[5],
        packs=[
            ("purpose_gaps_brief.md", ["1", "2", "3"], "Purpose, cross-cutting gaps, brief template", [1, 5]),
            ("characters_zones.md", ["4", "5"], "Character + zone readiness rows", [5]),
            ("pipeline_milestones.md", ["6", "7", "8", "9"], "Pipeline checklist, milestones, next docs", [5]),
        ],
    )

    split_numbered(
        src_rel="engineering/technical/TECHNICAL_DESIGN.md",
        pack_subdir="tdd",
        hub_title="Technical Design",
        hub_summary="Runtime architecture — load the stack for your feature",
        audience=["architect", "builder"],
        authority="engineering",
        doc_type="reference",
        phase=[1, 2, 3, 4, 5, 6],
        packs=[
            ("principles_runtime.md", ["1", "2"], "Design principles + runtime architecture", [1]),
            ("scene_data_save.md", ["3", "4", "5"], "Scene flow, data loading, save/load", [1, 2]),
            ("narrative_combat.md", ["6", "7"], "Narrative + combat stacks", [2, 3]),
            ("exploration_audio_ui.md", ["8", "9", "10"], "Exploration, audio, UI", [1, 4]),
            ("testing_phases.md", ["11", "12", "13"], "Testing hooks, phase map, related", [1, 6]),
        ],
    )

    split_numbered(
        src_rel="engineering/technical/CODING_STANDARDS_HUB.md",
        pack_subdir="coding",
        hub_title="Coding Standards Hub",
        hub_summary="Languages, naming, CI — load the section for your change type",
        audience=["architect", "builder"],
        authority="engineering",
        doc_type="reference",
        packs=[
            ("language_stack.md", ["1"], "Language stack + branch policy", None),
            ("naming.md", ["2"], "Naming conventions", None),
            ("ci_pr_commands.md", ["9", "10", "11", "12"], "CI matrix, PR checklist, related, commands", None),
        ],
    )

    split_numbered(
        src_rel="ops/qa/QA_REMEDIATION_LOOP.md",
        pack_subdir="remediation",
        hub_title="QA Remediation Loop",
        hub_summary="FAIL → one lever → re-measure — load the section for your domain",
        audience=["qa", "builder", "visual"],
        authority="qa",
        doc_type="how-to",
        packs=[
            ("standards_loop.md", ["1", "2"], "Industry standards + remediation loop", None),
            ("levers_commands.md", ["3", "4"], "Lever taxonomy + commands", None),
            ("report_stop_maps.md", ["5", "6", "7"], "Report template, stop rules, medium maps", None),
            ("tools_related.md", ["8", "9", "10"], "Tools, related docs, unified improvement", None),
        ],
    )

    split_numbered(
        src_rel="ops/qa/ACCEPTANCE_CRITERIA.md",
        pack_subdir="acceptance",
        hub_title="Acceptance Criteria",
        hub_summary="Measurable pass/fail gates — load catalog or jury section",
        audience=["qa", "pm", "builder"],
        authority="qa",
        doc_type="reference",
        packs=[
            ("why_rules.md", ["1", "2"], "Why QA fails without this + global pass rules", None),
            ("gate_catalog.md", ["3"], "Gate catalog summary", None),
            ("jury_report.md", ["4", "5"], "Jury enforcement + agent report template", None),
            ("phase_tools.md", ["6", "7", "8"], "Phase gates, tools, remediation relationship", None),
        ],
    )

    split_by_title_keys(
        src_rel="ops/cheat-sheets/RR_CHEATSHEET.md",
        pack_subdir="rr",
        hub_title="R&R Cheat Sheet",
        hub_summary="Roles & responsibilities — load the pack for your session step",
        audience=["pm", "builder", "qa"],
        authority="ops",
        doc_type="reference",
        packs=[
            ("golden_rules.md", ["golden_rules"], "Golden rules"),
            ("tools_roster.md", ["controls_at_a_glance", "tool_r_r_what_owns_what", "agent_roster"], "Controls, tools, agent roster"),
            ("workflow_handoff.md", ["default_workflow_one_feature", "situation_tool_conflict_resolver", "handoff_minimums"], "Workflow, situation→tool, handoffs"),
            ("escalation_branch.md", ["escalation_ladder_no_infinite_dev_qa_loops", "branch_environment", "sprint_batches_ai_native", "forbidden_without_user_override"], "Escalation, branch, sprint, forbidden"),
            ("commands_hooks.md", ["quick_commands", "factory_hooks_names_for_l0_workflow_integration", "related_docs_full_detail"], "Commands, factory hooks, related"),
        ],
    )
    # Preserve existing specialized packs already linked from stubs
    for keep in ("session.md", "pick_work.md", "performance_review.md", "qa_gates.md"):
        p = DOCS / "ops/cheat-sheets/rr" / keep
        if p.is_file():
            print(f"keep existing {p.relative_to(ROOT)}")

    split_by_title_keys(
        src_rel="ops/cheat-sheets/CONTROLS_CHEATSHEET.md",
        pack_subdir="controls",
        hub_title="Controls Cheat Sheet",
        hub_summary="How roles are enforced — load gates or PR controls for your branch",
        audience=["pm", "builder", "qa", "release"],
        authority="ops",
        doc_type="reference",
        packs=[
            ("golden_stack.md", ["golden_rules", "control_stack_strong_weak"], "Golden rules + control stack"),
            ("gates_by_branch.md", ["automated_gates_by_branch"], "Automated gates by branch"),
            ("roles_l3.md", ["per_role_controls", "l3_split_important"], "Per-role controls + L3 split"),
            ("pr_session_ship.md", ["pr_github_controls", "session_startup_before_scene_work", "ship_cd_controls"], "PR, session, ship/CD"),
            ("remediation_done.md", ["remediation_qa_fail_loop", "definition_of_done_merge", "quick_verify_commands", "related_docs"], "Remediation, DoD, verify, related"),
        ],
    )

    print("done")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
