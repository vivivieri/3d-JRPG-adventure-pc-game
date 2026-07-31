#!/usr/bin/env python3
"""Collapse arbitrary part_a/part_b pack halves into coherent named leaves.

Keeps meaningful topic splits; removes (A)/(B) maze hubs and hub-of-hub nesting
introduced by split_h3_halves in rounds 7–8.
"""
from __future__ import annotations

import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
sys.path.insert(0, str(ROOT / "tools"))
from enhance_docs_packs import fm, write  # noqa: E402


def strip_fm(text: str) -> str:
    if text.startswith("---"):
        end = text.find("\n---\n", 3)
        if end != -1:
            return text[end + 5 :]
    return text


def body_only(text: str) -> str:
    """Drop H1 + Hub pointer lines; keep section content."""
    text = strip_fm(text).strip() + "\n"
    lines = text.splitlines(keepends=True)
    out: list[str] = []
    skipping = True
    for i, line in enumerate(lines):
        if skipping:
            if line.startswith("# "):
                continue
            if line.startswith("**Hub:**") or line.startswith("**Hub**"):
                continue
            if line.strip() == "":
                continue
            # skip leftover hub pack tables if any leaked
            if line.startswith("| Pack |") or line.startswith("|------"):
                continue
            skipping = False
        out.append(line)
    return "".join(out).strip() + "\n"


def read_fm_meta(path: Path) -> dict[str, str]:
    text = path.read_text(encoding="utf-8")
    meta: dict[str, str] = {}
    if not text.startswith("---"):
        return meta
    end = text.find("\n---\n", 3)
    if end == -1:
        return meta
    for line in text[3:end].splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            meta[k.strip()] = v.strip()
    return meta


def parse_audience(raw: str) -> list[str]:
    raw = raw.strip()
    if raw.startswith("[") and raw.endswith("]"):
        inner = raw[1:-1].strip()
        if not inner:
            return []
        return [x.strip() for x in inner.split(",")]
    return [raw] if raw else []


def parse_phase(raw: str) -> list[int] | None:
    raw = raw.strip()
    if not raw.startswith("["):
        return None
    nums = re.findall(r"\d+", raw)
    return [int(n) for n in nums] if nums else None


def write_leaf(
    path: Path,
    *,
    title: str,
    body: str,
    parent_hub_rel: str,
    meta_src: Path,
    summary: str,
) -> None:
    meta = read_fm_meta(meta_src)
    audience = parse_audience(meta.get("audience", "[architect]"))
    authority = meta.get("authority", "ops").strip("\"'")
    doc_type = meta.get("type", "reference").strip()
    phase = parse_phase(meta.get("phase", ""))
    content = (
        fm(
            path.stem.lower().replace("_", "-"),
            doc_type,
            audience,
            authority,
            max(200, len(body) // 4 + 40),
            phase,
            summary=summary,
        )
        + f"# {title}\n\n"
        + f"**Hub:** [`{Path(parent_hub_rel).name}`]({parent_hub_rel})\n\n"
        + body
    )
    write(path, content)


def write_hub(
    path: Path,
    *,
    title: str,
    summary: str,
    packs: list[tuple[str, str]],
    parent_hub_rel: str | None,
    meta_src: Path,
    blurb: str = "",
) -> None:
    meta = read_fm_meta(meta_src)
    audience = parse_audience(meta.get("audience", "[architect]"))
    authority = meta.get("authority", "ops").strip("\"'")
    doc_type = meta.get("type", "reference").strip()
    phase = parse_phase(meta.get("phase", ""))
    rows = ["| Pack | Topic |", "|------|-------|"]
    for name, label in packs:
        rows.append(f"| [`{name}`]({name}) | {label} |")
    table = "\n".join(rows) + "\n"
    parent = ""
    if parent_hub_rel:
        parent = f"**Hub:** [`{Path(parent_hub_rel).name}`]({parent_hub_rel})\n\n"
    content = (
        fm(
            path.stem.lower().replace("_", "-"),
            doc_type,
            audience,
            authority,
            max(180, 120 + len(table) // 4),
            phase,
            summary=summary,
        )
        + f"# {title}\n\n"
        + "**Hub** — load only the pack for your current pass.\n\n"
        + table
        + parent
        + (blurb.strip() + "\n" if blurb.strip() else "")
    )
    write(path, content)


def rm_tree(path: Path) -> None:
    if path.is_dir():
        shutil.rmtree(path)
        print(f"rmdir {path.relative_to(ROOT)}")
    elif path.exists():
        path.unlink()
        print(f"rm {path.relative_to(ROOT)}")


def merge_ab_into_leaf(
    hub_rel: str,
    pack_dir_name: str,
    *,
    title: str,
    summary: str,
    parent_hub_rel: str,
) -> None:
    """Merge pack_dir/part_a.md + part_b.md into hub_rel as a leaf; delete pack_dir."""
    hub = DOCS / hub_rel
    pack_dir = hub.parent / pack_dir_name
    a = pack_dir / "part_a.md"
    b = pack_dir / "part_b.md"
    body = body_only(a.read_text(encoding="utf-8")) + "\n" + body_only(b.read_text(encoding="utf-8"))
    write_leaf(
        hub,
        title=title,
        body=body,
        parent_hub_rel=parent_hub_rel,
        meta_src=hub,
        summary=summary,
    )
    rm_tree(pack_dir)


def update_pack_catalog(remove: list[str], add: list[str]) -> None:
    index = DOCS / "INDEX.yaml"
    text = index.read_text(encoding="utf-8")
    m = re.search(r"(?ms)^(pack_catalog:\n)(.*?)(?=\n[a-z_]+:|\Z)", text)
    if not m:
        raise SystemExit("pack_catalog not found")
    lines = [ln for ln in m.group(2).rstrip("\n").splitlines()]
    remove_set = set(remove)
    kept = []
    existing = set()
    for ln in lines:
        mm = re.match(r"^\s*-\s+(docs/\S+)$", ln)
        if mm and mm.group(1) in remove_set:
            print(f"INDEX - {mm.group(1)}")
            continue
        kept.append(ln)
        if mm:
            existing.add(mm.group(1))
    for path in sorted(add):
        if path in existing:
            continue
        entry = f"  - {path}"
        inserted = False
        for i, ln in enumerate(kept):
            mm = re.match(r"^\s*-\s+(docs/\S+)$", ln)
            if mm and path < mm.group(1):
                kept.insert(i, entry)
                inserted = True
                break
        if not inserted:
            kept.append(entry)
        print(f"INDEX + {path}")
        existing.add(path)
    new_block = m.group(1) + "\n".join(kept) + "\n"
    index.write_text(text[: m.start()] + new_block + text[m.end() :], encoding="utf-8")


def main() -> int:
    removed: list[str] = []
    added: list[str] = []

    # --- Simple (A)/(B) → single leaf at the intermediate hub path ---
    simple = [
        (
            "design/art/visual_qa/judge/defense_layers.md",
            "layers",
            "Visual QA — Defense Layers",
            "Layers A–G defense stack",
            "../judge_layers.md",
        ),
        (
            "design/art/model_qa/polish/who_directs.md",
            "who",
            "Model QA — Who Directs Feel",
            "Direction authority + feel ownership",
            "../polish_direction.md",
        ),
        (
            "design/vision/narrative/emotional/project_rules.md",
            "rules",
            "Narrative — Project Emotional Rules",
            "JRPG emotional storytelling rules A–I",
            "../emotional_rules.md",
        ),
        (
            "ops/qa/testing/toolkit.md",
            "toolkit",
            "AI Testing — GDAI Toolkit",
            "GDAI MCP playtesting toolkit",
            "../AI_TESTING_SPEC.md",
        ),
        (
            "ops/qa/acceptance/gate_catalog.md",
            "catalog",
            "Acceptance — Gate Catalog",
            "Gate catalog summary",
            "../ACCEPTANCE_CRITERIA.md",
        ),
        (
            "ops/cheat-sheets/controls/gates_by_branch.md",
            "gates",
            "Controls — Gates by Branch",
            "Automated gates by branch",
            "../CONTROLS_CHEATSHEET.md",
        ),
        (
            "ops/agents/mcp/art_tools.md",
            "art",
            "MCP — Art Tools",
            "Art & design MCP/offline tools",
            "../MCP_STACK.md",
        ),
    ]
    for hub_rel, pack_dir, title, summary, parent in simple:
        for name in ("part_a.md", "part_b.md"):
            removed.append(f"docs/{Path(hub_rel).parent.as_posix()}/{pack_dir}/{name}")
        merge_ab_into_leaf(hub_rel, pack_dir, title=title, summary=summary, parent_hub_rel=parent)
        # hub path stays in catalog (already present); no add

    # --- Enemies: named field + bosses leaves (drop part_* and nested hub) ---
    enemies_hub = DOCS / "design/art/characters/enemies.md"
    field_body = body_only((DOCS / "design/art/characters/enemies/part_a.md").read_text(encoding="utf-8"))
    bosses_body = (
        body_only((DOCS / "design/art/characters/enemies/bosses/part_a.md").read_text(encoding="utf-8"))
        + "\n"
        + body_only((DOCS / "design/art/characters/enemies/bosses/part_b.md").read_text(encoding="utf-8"))
    )
    write_leaf(
        DOCS / "design/art/characters/enemies/field.md",
        title="Character Bible — Field Enemies",
        body=field_body,
        parent_hub_rel="../enemies.md",
        meta_src=enemies_hub,
        summary="Field enemy model briefs",
    )
    write_leaf(
        DOCS / "design/art/characters/enemies/bosses.md",
        title="Character Bible — Boss Enemies",
        body=bosses_body,
        parent_hub_rel="../enemies.md",
        meta_src=enemies_hub,
        summary="Shore Wraith, Palace Sentinel, Tide Keeper",
    )
    write_hub(
        enemies_hub,
        title="Character Bible — Enemies",
        summary="Enemy field + boss model briefs",
        packs=[
            ("enemies/field.md", "Field enemies"),
            ("enemies/bosses.md", "Boss enemies"),
        ],
        parent_hub_rel="../CHARACTER_BIBLE.md",
        meta_src=enemies_hub,
        blurb="Field trash → `field.md`; bosses → `bosses.md`.",
    )
    removed += [
        "docs/design/art/characters/enemies/part_a.md",
        "docs/design/art/characters/enemies/part_b.md",
        "docs/design/art/characters/enemies/bosses/part_a.md",
        "docs/design/art/characters/enemies/bosses/part_b.md",
    ]
    added += [
        "docs/design/art/characters/enemies/field.md",
        "docs/design/art/characters/enemies/bosses.md",
    ]
    rm_tree(DOCS / "design/art/characters/enemies/part_a.md")
    rm_tree(DOCS / "design/art/characters/enemies/part_b.md")
    rm_tree(DOCS / "design/art/characters/enemies/bosses")

    # --- Phase acceptance: hub → 4 named packs (drop part_a/part_b middle hubs) ---
    phase_hub = DOCS / "ops/workflow/ai_dev/phase_acceptance.md"
    # Rewrite leaf hub pointers from ../part_a.md → ../phase_acceptance.md
    for rel in (
        "ops/workflow/ai_dev/phases/early/phase_0_1.md",
        "ops/workflow/ai_dev/phases/early/phase_2_3.md",
        "ops/workflow/ai_dev/phases/late/phase_4_6.md",
        "ops/workflow/ai_dev/phases/late/phase_7_8.md",
    ):
        p = DOCS / rel
        t = p.read_text(encoding="utf-8")
        t = t.replace("](../part_a.md)", "](../../phase_acceptance.md)")
        t = t.replace("](../part_b.md)", "](../../phase_acceptance.md)")
        # Fix titles that say Phases 0–3 wrapper
        t = re.sub(
            r"(?m)^# AI Dev — Phases 0–3 — ",
            "# AI Dev — ",
            t,
        )
        t = re.sub(
            r"(?m)^# AI Dev — Phases 4–8 — ",
            "# AI Dev — ",
            t,
        )
        # Hub path depth: early/late are 2 levels under phases/; phase_acceptance is sibling of phases/
        # From phases/early/foo.md → ../../phase_acceptance.md is correct
        write(p, t)

    write_hub(
        phase_hub,
        title="AI Dev — Phase Acceptance",
        summary="Acceptance criteria by phase",
        packs=[
            ("phases/early/phase_0_1.md", "Phases 0–1"),
            ("phases/early/phase_2_3.md", "Phases 2–3"),
            ("phases/late/phase_4_6.md", "Phases 4–6"),
            ("phases/late/phase_7_8.md", "Phases 7–8"),
        ],
        parent_hub_rel="../AI_DEV_WORKFLOW.md",
        meta_src=phase_hub,
    )
    removed += [
        "docs/ops/workflow/ai_dev/phases/part_a.md",
        "docs/ops/workflow/ai_dev/phases/part_b.md",
    ]
    rm_tree(DOCS / "ops/workflow/ai_dev/phases/part_a.md")
    rm_tree(DOCS / "ops/workflow/ai_dev/phases/part_b.md")

    # --- CI what_runs: main + game_development named leaves ---
    what_runs = DOCS / "ops/ci-cd/ci/required_gates/what_runs.md"
    main_body = body_only((DOCS / "ops/ci-cd/ci/required_gates/runs/part_a.md").read_text(encoding="utf-8"))
    gd_body = (
        body_only((DOCS / "ops/ci-cd/ci/required_gates/runs/game_dev/gates_l0_l1.md").read_text(encoding="utf-8"))
        + "\n"
        + body_only((DOCS / "ops/ci-cd/ci/required_gates/runs/game_dev/gates_l2_plus.md").read_text(encoding="utf-8"))
    )
    write_leaf(
        DOCS / "ops/ci-cd/ci/required_gates/runs/main.md",
        title="CI — What Runs (`main`)",
        body=main_body,
        parent_hub_rel="../what_runs.md",
        meta_src=what_runs,
        summary="main branch docs CI gates",
    )
    write_leaf(
        DOCS / "ops/ci-cd/ci/required_gates/runs/game_development.md",
        title="CI — What Runs (`game/development`)",
        body=gd_body,
        parent_hub_rel="../what_runs.md",
        meta_src=what_runs,
        summary="game/development game-ci gates + Windows/CD",
    )
    write_hub(
        what_runs,
        title="CI — What Runs",
        summary="main vs game/development required gates",
        packs=[
            ("runs/main.md", "`main` docs CI"),
            ("runs/game_development.md", "`game/development` game CI"),
        ],
        parent_hub_rel="../required_gates.md",
        meta_src=what_runs,
    )
    removed += [
        "docs/ops/ci-cd/ci/required_gates/runs/part_a.md",
        "docs/ops/ci-cd/ci/required_gates/runs/part_b.md",
        "docs/ops/ci-cd/ci/required_gates/runs/game_dev/gates_l0_l1.md",
        "docs/ops/ci-cd/ci/required_gates/runs/game_dev/gates_l2_plus.md",
    ]
    added += [
        "docs/ops/ci-cd/ci/required_gates/runs/main.md",
        "docs/ops/ci-cd/ci/required_gates/runs/game_development.md",
    ]
    rm_tree(DOCS / "ops/ci-cd/ci/required_gates/runs/part_a.md")
    rm_tree(DOCS / "ops/ci-cd/ci/required_gates/runs/part_b.md")
    rm_tree(DOCS / "ops/ci-cd/ci/required_gates/runs/game_dev")

    # Also remove from catalog the simple part_* paths
    for hub_rel, pack_dir, *_ in simple:
        parent = Path(hub_rel).parent.as_posix()
        removed.append(f"docs/{parent}/{pack_dir}/part_a.md")
        removed.append(f"docs/{parent}/{pack_dir}/part_b.md")

    update_pack_catalog(sorted(set(removed)), added)

    # Sanity: no part_*.md left under docs (except archive)
    leftover = [
        str(p)
        for p in DOCS.rglob("part_*.md")
        if not str(p).startswith(str(DOCS / "archive"))
    ]
    if leftover:
        print("WARN leftover part_*:", leftover)
    else:
        print("OK — no active part_*.md left")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
