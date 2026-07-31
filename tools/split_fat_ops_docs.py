#!/usr/bin/env python3
"""Split remaining large ops/design/engineering guides into hubs + packs."""
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
        match = re.match(r"##\s+(\d+(?:\.\d+)?[a-z]?)\b", heading)
        if match:
            out[match.group(1)] = body
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
        # keep one line
        safe = summary.replace("\n", " ").strip()
        lines.append(f"summary: \"{safe}\"")
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


def split_generic(
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
    text = strip_fm(src.read_text(encoding="utf-8"))
    preamble, sections = split_by_h2(text)
    nums = by_num(sections)
    pack_dir = src.parent / pack_subdir
    rows: list[tuple[str, str]] = []
    for name, keys, label, pphase in packs:
        body = join_nums(nums, keys)
        if not body.strip():
            print(f"WARN skip empty pack {name} keys={keys}")
            continue
        content = (
            fm(
                Path(name).stem.replace("_", "-"),
                doc_type,
                audience,
                authority,
                max(400, len(body) // 4),
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
            900,
            phase,
            summary=hub_summary,
        )
        + f"# {hub_title}\n\n**Hub** — load one pack below.\n\n"
        + pack_table(pack_subdir, rows)
        + preamble.strip()
        + "\n"
    )
    write(src, hub)


def main() -> int:
    split_generic(
        src_rel="ops/workflow/AGILE_WITHIN_PHASES.md",
        pack_subdir="agile",
        hub_title="Agile Within Phases",
        hub_summary="Phase-gated Agile process for the AI factory",
        audience=["pm", "architect"],
        authority="workflow",
        doc_type="how-to",
        packs=[
            ("summary_why.md", ["1", "2"], "Summary & why hybrid", None),
            ("linear_sprints.md", ["3", "4", "5", "6"], "Linear setup & sprint flow", None),
            ("waterfall_mcp_metrics.md", ["7", "8", "9", "10"], "Waterfall bounds, MCP, metrics", None),
            ("sprint_master_cadence.md", ["11", "12", "12.1"], "Sprint Master & AI cadence", None),
        ],
    )
    split_generic(
        src_rel="ops/agents/CURSOR_SECRETS_SETUP.md",
        pack_subdir="secrets",
        hub_title="Cursor Secrets Setup",
        hub_summary="Day-one Cursor / GitHub secrets for the factory",
        audience=["pm", "builder", "release"],
        authority="agents",
        doc_type="how-to",
        phase=[0, 1],
        packs=[
            ("day_one_checklist.md", ["1"], "Day-one checklist", [0, 1]),
            ("webhooks.md", ["2", "3"], "PM / alert / worker webhooks", [0, 1]),
            ("api_keys.md", ["4", "5", "6", "7", "8"], "API keys (GameLab, GH, Telegram, VO, Cursor)", [0, 1]),
            ("scope_troubleshoot.md", ["9", "10", "11", "12"], "Scope, later phases, troubleshooting", [0, 1]),
        ],
    )

    # LEVEL_DESIGN by zone
    split_generic(
        src_rel="design/world/LEVEL_DESIGN.md",
        pack_subdir="levels",
        hub_title="Level Design",
        hub_summary="Zone layouts, interactables, encounter index",
        audience=["builder", "builder_zone", "architect"],
        authority="world",
        doc_type="reference",
        phase=[1, 3, 5],
        packs=[
            ("global_rules.md", ["1"], "Global level rules", [1]),
            ("beach_shore.md", ["2"], "Zone beach_shore", [1]),
            ("ruined_village.md", ["3"], "Zone ruined_village", [1]),
            ("tidal_caves.md", ["4"], "Zone tidal_caves", [1, 5]),
            ("dragon_palace.md", ["5", "6"], "Palace + endings", [5, 6]),
            ("encounters_flags_qa.md", ["7", "8", "9", "10"], "Encounters, flags, QA", [1, 5]),
        ],
    )

    split_generic(
        src_rel="ops/ci-cd/CI.md",
        pack_subdir="ci",
        hub_title="Continuous Integration",
        hub_summary="Required CI gates, local reproduction, remediation",
        audience=["release", "qa", "pm"],
        authority="ci-cd",
        doc_type="reference",
        packs=[
            ("branch_purpose.md", ["0", "1"], "Branch split & purpose", None),
            ("required_gates.md", ["2", "3"], "What CI runs / does not run", None),
            ("local_rr_remediation.md", ["4", "5", "6"], "Local repro, R&R, remediation", None),
            ("branch_protection_refs.md", ["7", "8"], "Branch protection & cross-refs", None),
        ],
    )

    split_generic(
        src_rel="ops/workflow/DEVELOPMENT_LIFECYCLE.md",
        pack_subdir="lifecycle",
        hub_title="Development Lifecycle",
        hub_summary="Macro lifecycle, branching, gates, promotion",
        audience=["pm", "architect", "release"],
        authority="workflow",
        doc_type="explanation",
        packs=[
            ("overview_time.md", ["1", "2", "3"], "Doc map, overview, time model", None),
            ("branching_agents.md", ["4", "5", "6"], "Branching, agent envs, issue lifecycle", None),
            ("gates_trackers.md", ["7", "8", "9"], "Quality ladder, trackers, promotion", None),
            ("enhancements_commands.md", ["10", "11", "12"], "Enhancements, commands, cross-refs", None),
        ],
    )

    split_generic(
        src_rel="engineering/technical/GDSCRIPT_REGENERATION.md",
        pack_subdir="gdscript_regen",
        hub_title="GDScript Regeneration",
        hub_summary="Helper regeneration order and EventBus wiring",
        audience=["architect", "builder"],
        authority="engineering",
        doc_type="how-to",
        phase=[1, 2],
        packs=[
            ("principle_rr.md", ["1", "2", "3"], "Principle, R&R, prerequisites", [1, 2]),
            ("order_helpers.md", ["4", "5"], "Regen order & per-helper steps", [1, 2]),
            ("checklist_recover.md", ["6", "7", "8", "9", "10"], "Checklist, recover, new helpers, Phase 1 visuals", [1, 2]),
        ],
    )

    # Fix CURSOR_SECRETS 3b: re-parse from packs is incomplete. Pull 3b from git show if needed.
    import subprocess

    raw = subprocess.check_output(
        ["git", "show", "HEAD:docs/ops/agents/CURSOR_SECRETS_SETUP.md"],
        cwd=ROOT,
        text=True,
    )
    # If already hub on HEAD, use working tree backup — we overwrote. Use sections from first split
    # by reading webhook pack and appending 3b from subprocess of original blob.
    # On this branch HEAD still has full file until we commit — good.
    raw_body = strip_fm(raw)
    _, secs = split_by_h2(raw_body)
    extra = ""
    for heading, body in secs:
        if heading.startswith("## 3b") or "WORKER_WEBHOOK" in heading:
            extra += body
    if extra:
        wh = DOCS / "ops/agents/secrets/webhooks.md"
        if wh.is_file():
            text = wh.read_text(encoding="utf-8")
            if "WORKER_WEBHOOK" not in text:
                wh.write_text(text.rstrip() + "\n\n" + extra, encoding="utf-8")
                print("patched secrets/webhooks.md with §3b")

    # Also fix api_keys — section 3 was incorrectly duplicated in webhooks keys list.
    # day_one is fine. Re-split secrets more carefully from raw if packs look thin.
    nums = by_num(secs)
    # Rebuild api_keys and webhooks cleanly from original
    if nums:
        packs_fix = [
            (
                "webhooks.md",
                ["2", "3"],
                "PM / alert webhooks",
                DOCS / "ops/agents/secrets/webhooks.md",
            ),
            (
                "api_keys.md",
                ["4", "5", "6", "7", "8"],
                "API keys",
                DOCS / "ops/agents/secrets/api_keys.md",
            ),
        ]
        for name, keys, label, path in packs_fix:
            body = join_nums(nums, keys)
            if name == "webhooks.md" and extra:
                body = body.rstrip() + "\n\n" + extra
            content = (
                fm(
                    Path(name).stem.replace("_", "-"),
                    "how-to",
                    ["pm", "builder", "release"],
                    "agents",
                    max(400, len(body) // 4),
                    [0, 1],
                    summary=label,
                )
                + f"# Cursor Secrets Setup — {label}\n\n"
                + "**Hub:** [`CURSOR_SECRETS_SETUP.md`](../CURSOR_SECRETS_SETUP.md)\n\n"
                + body
            )
            write(path, content)

    print("done")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
