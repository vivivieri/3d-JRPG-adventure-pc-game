#!/usr/bin/env python3
"""Split oversized docs into hubs+packs and stamp YAML frontmatter on active docs."""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"

SKIP_FRONTMATTER_NAMES = {
    "README.md",
    "BOOT.md",
    "llms.txt",
    "INDEX.yaml",
}
SKIP_FRONTMATTER_PREFIXES = (
    "archive/",
    "_meta/",
    "briefs/",
    "design/audio/audio_sheets/",
    "ops/sprints/",
    "ops/agents/automation_prompts/",
)


def split_by_h2(text: str) -> tuple[str, list[tuple[str, str]]]:
    """Return (preamble before first H2, [(heading_line, body_including_heading), ...])."""
    lines = text.splitlines(keepends=True)
    preamble: list[str] = []
    sections: list[tuple[str, str]] = []
    current_heading = ""
    current_body: list[str] = []
    seen_h2 = False
    for line in lines:
        if line.startswith("## "):
            if seen_h2:
                sections.append((current_heading, "".join(current_body)))
            else:
                # drop trailing blank lines from preamble
                while preamble and preamble[-1].strip() == "":
                    preamble.pop()
                preamble.append("\n")
            seen_h2 = True
            current_heading = line.strip()
            current_body = [line]
        elif not seen_h2:
            preamble.append(line)
        else:
            current_body.append(line)
    if seen_h2:
        sections.append((current_heading, "".join(current_body)))
    return "".join(preamble), sections


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not content.endswith("\n"):
        content += "\n"
    path.write_text(content, encoding="utf-8")
    print(f"write {path.relative_to(ROOT)} ({len(content)} bytes)")


def slug_heading(heading: str) -> str:
    h = re.sub(r"^##\s+", "", heading)
    h = re.sub(r"^\d+\.\s*", "", h)
    h = h.lower()
    # Keep both sides of em/en dash for uniqueness ("Install — X")
    h = h.replace("—", "-").replace("–", "-")
    h = re.sub(r"[^a-z0-9]+", "-", h).strip("-")
    return h[:64] or "section"


def split_ai_testing_spec() -> None:
    src = DOCS / "ops/qa/AI_TESTING_SPEC.md"
    text = src.read_text(encoding="utf-8")
    # Strip existing frontmatter if any
    if text.startswith("---"):
        text = re.sub(r"^---\n.*?\n---\n", "", text, count=1, flags=re.S)
    preamble, sections = split_by_h2(text)
    by_num: dict[str, tuple[str, str]] = {}
    for heading, body in sections:
        m = re.match(r"##\s+(\d+)", heading)
        if m:
            by_num[m.group(1)] = (heading, body)

    pack_dir = DOCS / "ops/qa/testing"
    packs = {
        "l0": ("2", "L0 — Data validation"),
        "l1": ("3", "L1 — Unit tests"),
        "l2": ("4", "L2 — Smoke tests"),
        "l3": ("5", "L3 — GDAI editor verify"),
        "l4": ("6", "L4 — AI integration tests"),
        "l5": ("7", "L5 — AI E2E playthrough"),
        "l6": ("8", "L6 — Human QA"),
        "toolkit": ("11", "GDAI MCP playtesting toolkit"),
    }
    for name, (num, title) in packs.items():
        heading, body = by_num[num]
        content = (
            f"# {title}\n\n"
            f"**Hub:** [`AI_TESTING_SPEC.md`](../AI_TESTING_SPEC.md)\n\n"
            f"{body}"
        )
        write(pack_dir / f"{name}.md", content)

    # Extra packs: phases/report/related
    extras = []
    for num in ("9", "10", "12", "13"):
        if num in by_num:
            extras.append(by_num[num][1])
    write(
        pack_dir / "phases_and_report.md",
        "# Phase map, report template & related\n\n"
        "**Hub:** [`AI_TESTING_SPEC.md`](../AI_TESTING_SPEC.md)\n\n"
        + "".join(extras),
    )

    # Slim hub: preamble + golden rule + summary + TOC of packs + keep 0,1,9 short links
    hub_parts = [preamble.rstrip() + "\n"]
    for num in ("0", "1"):
        hub_parts.append(by_num[num][1])
    hub_parts.append(
        "## Layer packs (progressive disclosure)\n\n"
        "Load only the layer you are running — do not preload this whole bible.\n\n"
        "| Layer | Pack |\n"
        "|-------|------|\n"
        "| L0 | [testing/l0.md](testing/l0.md) |\n"
        "| L1 | [testing/l1.md](testing/l1.md) |\n"
        "| L2 | [testing/l2.md](testing/l2.md) |\n"
        "| L3 | [testing/l3.md](testing/l3.md) |\n"
        "| L4 | [testing/l4.md](testing/l4.md) |\n"
        "| L5 | [testing/l5.md](testing/l5.md) |\n"
        "| L6 | [testing/l6.md](testing/l6.md) |\n"
        "| Toolkit | [testing/toolkit.md](testing/toolkit.md) |\n"
        "| Phases / report | [testing/phases_and_report.md](testing/phases_and_report.md) |\n\n"
    )
    if "9" in by_num:
        hub_parts.append(by_num["9"][1])
    write(src, "".join(hub_parts))


def split_mcp_stack() -> None:
    src = DOCS / "ops/agents/MCP_STACK.md"
    text = src.read_text(encoding="utf-8")
    if text.startswith("---"):
        text = re.sub(r"^---\n.*?\n---\n", "", text, count=1, flags=re.S)
    preamble, sections = split_by_h2(text)
    # Map by heading slug
    mapped = {slug_heading(h): (h, b) for h, b in sections}

    pack_dir = DOCS / "ops/agents/mcp"
    groups = {
        "install.md": [
            "install-godot-mcp-plugins",
            "install-cursor-mcp-servers",
            "ports-defaults",
            "godot-editor-plugins-enable-all",
        ],
        "art_tools.md": ["art-design-tools"],
        "testing.md": ["testing-qa-workflow"],
        "setup_and_cost.md": [
            "explicitly-rejected-do-not-adopt",
            "licenses-cost",
            "user-setup-checklist-purchase-secrets",
            "troubleshooting",
            "related",
        ],
    }
    for fname, keys in groups.items():
        bodies = []
        title = fname.replace(".md", "").replace("_", " ").title()
        for key in keys:
            if key not in mapped:
                hits = [k for k in mapped if k == key or k.startswith(key) or key in k]
                if not hits:
                    print(f"WARN mcp missing section {key}; have {sorted(mapped)}", file=sys.stderr)
                    continue
                key = hits[0]
            bodies.append(mapped[key][1])
        write(
            pack_dir / fname,
            f"# MCP — {title}\n\n**Hub:** [`MCP_STACK.md`](../MCP_STACK.md)\n\n" + "".join(bodies),
        )

    keep = [
        "full-r-r-map",
        "role-split-conflict-rules",
        "session-startup-every-agent-run",
    ]
    hub = [preamble.rstrip() + "\n"]
    for key in keep:
        if key in mapped:
            hub.append(mapped[key][1])
        else:
            hits = [k for k in mapped if key in k]
            if hits:
                hub.append(mapped[hits[0]][1])
    hub.append(
        "## Packs (progressive disclosure)\n\n"
        "| Topic | Pack |\n"
        "|-------|------|\n"
        "| Install / ports / plugins | [mcp/install.md](mcp/install.md) |\n"
        "| Art & design tools | [mcp/art_tools.md](mcp/art_tools.md) |\n"
        "| Testing & QA workflow | [mcp/testing.md](mcp/testing.md) |\n"
        "| Cost, checklist, troubleshooting | [mcp/setup_and_cost.md](mcp/setup_and_cost.md) |\n\n"
    )
    write(src, "".join(hub))


def slim_coding_standards_hub() -> None:
    """Keep hub; replace deep language sections with links to existing style guides."""
    src = DOCS / "engineering/technical/CODING_STANDARDS_HUB.md"
    text = src.read_text(encoding="utf-8")
    if text.startswith("---"):
        text = re.sub(r"^---\n.*?\n---\n", "", text, count=1, flags=re.S)
    preamble, sections = split_by_h2(text)
    keep_nums = {"1", "2", "9", "10", "11", "12"}
    hub = [preamble.rstrip() + "\n"]
    deep_replaced = False
    for heading, body in sections:
        m = re.match(r"##\s+(\d+)", heading)
        num = m.group(1) if m else ""
        if num in keep_nums:
            hub.append(body)
        elif not deep_replaced and num in {"3", "4", "5", "6", "7", "8"}:
            hub.append(
                "## 3–8. Language deep dives (packs)\n\n"
                "Do not preload language bibles from this hub — open the guide for the file you are editing.\n\n"
                "| Topic | Guide |\n"
                "|-------|-------|\n"
                "| GDScript | [GDSCRIPT_STYLE.md](GDSCRIPT_STYLE.md) · [CODE_STYLE.md](CODE_STYLE.md) |\n"
                "| Shaders | [SHADER_STYLE.md](SHADER_STYLE.md) |\n"
                "| Data / JSON | [JSON_DATA_STYLE.md](JSON_DATA_STYLE.md) · [DATA_ARCHITECTURE.md](DATA_ARCHITECTURE.md) |\n"
                "| Python | [PYTHON_STYLE.md](PYTHON_STYLE.md) |\n"
                "| Shell | [BASH_STYLE.md](BASH_STYLE.md) |\n"
                "| TypeScript | [TYPESCRIPT_STYLE.md](TYPESCRIPT_STYLE.md) |\n"
                "| Scenes | [SCENE_STYLE.md](SCENE_STYLE.md) |\n"
                "| Errors | [ERROR_HANDLING.md](ERROR_HANDLING.md) |\n\n"
            )
            deep_replaced = True
        elif num in {"3", "4", "5", "6", "7", "8"}:
            continue
        else:
            hub.append(body)
    write(src, "".join(hub))


def slim_rr_cheatsheet() -> None:
    src = DOCS / "ops/cheat-sheets/RR_CHEATSHEET.md"
    text = src.read_text(encoding="utf-8")
    if text.startswith("---"):
        text = re.sub(r"^---\n.*?\n---\n", "", text, count=1, flags=re.S)
    preamble, sections = split_by_h2(text)
    pack_dir = DOCS / "ops/cheat-sheets/rr"
    # Pack long sections
    long_slugs = {
        "session-startup-every-run": "session.md",
        "how-to-pick-work-dev-qa": "pick_work.md",
        "performance-review-required-not-code-review": "performance_review.md",
        "qa-gate-layers": "qa_gates.md",
    }
    mapped = {slug_heading(h): (h, b) for h, b in sections}
    for slug, fname in long_slugs.items():
        hits = [k for k in mapped if slug[:16] in k or k.startswith(slug[:12])]
        if not hits:
            print(f"WARN rr missing {slug}", file=sys.stderr)
            continue
        write(
            pack_dir / fname,
            f"# R&R — {hits[0]}\n\n**Hub:** [`RR_CHEATSHEET.md`](../RR_CHEATSHEET.md)\n\n"
            + mapped[hits[0]][1],
        )

    hub = [preamble.rstrip() + "\n"]
    for heading, body in sections:
        slug = slug_heading(heading)
        matched = None
        for key, fname in long_slugs.items():
            if key[:12] in slug or slug.startswith(key[:10]):
                matched = fname
                break
        if matched:
            hub.append(
                f"{heading}\n\n"
                f"> Full detail: [`rr/{matched}`](rr/{matched}) — load only when needed.\n\n"
            )
        else:
            hub.append(body)
    write(src, "".join(hub))


def slim_ai_dev_workflow() -> None:
    src = DOCS / "ops/workflow/AI_DEV_WORKFLOW.md"
    text = src.read_text(encoding="utf-8")
    if text.startswith("---"):
        text = re.sub(r"^---\n.*?\n---\n", "", text, count=1, flags=re.S)
    preamble, sections = split_by_h2(text)
    pack_dir = DOCS / "ops/workflow/ai_dev"
    mapped = {slug_heading(h): (h, b) for h, b in sections}
    packs = {
        "testing_policy.md": ["ai-testing-policy", "unit-tests"],
        "phase_acceptance.md": ["acceptance-criteria-by-phase"],
        "commands.md": ["command-cheat-sheet", "related-docs"],
    }
    for fname, keys in packs.items():
        bodies = []
        for key in keys:
            if key in mapped:
                bodies.append(mapped[key][1])
                continue
            hits = [k for k in mapped if key in k or k.startswith(key)]
            if hits:
                bodies.append(mapped[hits[0]][1])
            else:
                print(f"WARN ai_dev missing {key}; have {sorted(mapped)}", file=sys.stderr)
        write(
            pack_dir / fname,
            f"# AI Dev Workflow — {fname.replace('.md','').replace('_',' ')}\n\n"
            f"**Hub:** [`AI_DEV_WORKFLOW.md`](../AI_DEV_WORKFLOW.md)\n\n"
            + "".join(bodies),
        )
    hub = [preamble.rstrip() + "\n"]
    # Keep section 1 in hub
    if "ai-build-policy" in mapped:
        hub.append(mapped["ai-build-policy"][1])
    else:
        for heading, body in sections:
            if "build policy" in heading.lower():
                hub.append(body)
                break
    hub.append(
        "## Packs (progressive disclosure)\n\n"
        "| Topic | Pack |\n"
        "|-------|------|\n"
        "| Testing policy + unit tests | [ai_dev/testing_policy.md](ai_dev/testing_policy.md) |\n"
        "| Phase acceptance | [ai_dev/phase_acceptance.md](ai_dev/phase_acceptance.md) |\n"
        "| Commands + related | [ai_dev/commands.md](ai_dev/commands.md) |\n\n"
    )
    write(src, "".join(hub))


def infer_frontmatter(rel: str) -> dict[str, object]:
    stem = Path(rel).stem.lower().replace("_", "-")
    parts = rel.split("/")
    audience: list[str] = []
    authority = parts[1] if len(parts) > 1 else "docs"
    doc_type = "reference"

    if rel.startswith("design/vision"):
        audience, authority, doc_type = ["narrative"], "vision", "explanation"
    elif rel.startswith("design/art"):
        audience, authority = ["visual", "builder"], "art"
        doc_type = "how-to" if "PIPELINE" in rel or "QA" in rel else "reference"
    elif rel.startswith("design/audio"):
        audience, authority = ["audio"], "audio"
    elif rel.startswith("design/gameplay") or rel.startswith("design/world") or rel.startswith("design/ui"):
        audience, authority = ["builder", "architect"], parts[1]
    elif rel.startswith("engineering/"):
        audience, authority = ["architect", "builder"], "engineering"
    elif rel.startswith("ops/qa"):
        audience, authority = ["qa", "flow"], "qa"
        doc_type = "how-to" if "REMEDIATION" in rel or "FLOW" in rel else "reference"
    elif rel.startswith("ops/agents"):
        audience, authority = ["pm", "builder"], "agents"
        doc_type = "tutorial" if "SETUP" in rel or "LAUNCH" in rel else "how-to"
    elif rel.startswith("ops/workflow"):
        audience, authority = ["pm", "architect"], "workflow"
        doc_type = "explanation" if "DECISION" in rel else "how-to"
    elif rel.startswith("ops/ci-cd"):
        audience, authority = ["release"], "ci-cd"
    elif rel.startswith("ops/cheat-sheets"):
        audience, authority, doc_type = ["pm", "builder", "qa"], "ops", "reference"

    if "QA" in Path(rel).stem or rel.endswith("_QA.md"):
        doc_type = "how-to"
    if "ADR" in Path(rel).stem or "DECISION" in Path(rel).stem:
        doc_type = "explanation"

    tokens_est = max(400, Path(DOCS / rel).stat().st_size // 4)

    return {
        "id": stem,
        "type": doc_type,
        "audience": audience or ["builder"],
        "status": "active",
        "authority": authority,
        "tokens_est": int(tokens_est),
    }


def format_frontmatter(meta: dict[str, object]) -> str:
    lines = ["---"]
    for key in ("id", "type", "audience", "phase", "status", "authority", "tokens_est"):
        if key not in meta:
            continue
        val = meta[key]
        if isinstance(val, list):
            inner = ", ".join(str(x) for x in val)
            lines.append(f"{key}: [{inner}]")
        else:
            lines.append(f"{key}: {val}")
    lines.append("---")
    lines.append("")
    return "\n".join(lines)


def stamp_frontmatter() -> tuple[int, int]:
    stamped = 0
    skipped = 0
    for path in sorted(DOCS.rglob("*.md")):
        rel = path.relative_to(DOCS).as_posix()
        if path.name in SKIP_FRONTMATTER_NAMES or any(rel.startswith(p) for p in SKIP_FRONTMATTER_PREFIXES):
            skipped += 1
            continue
        text = path.read_text(encoding="utf-8")
        if text.startswith("---\n"):
            # refresh tokens_est only if already present
            skipped += 1
            continue
        meta = infer_frontmatter(rel)
        path.write_text(format_frontmatter(meta) + text, encoding="utf-8")
        stamped += 1
    return stamped, skipped


def write_pack_readmes() -> None:
    for folder, blurb in (
        ("ops/qa/testing", "AI testing layer packs — load one layer at a time."),
        ("ops/agents/mcp", "MCP stack packs — install, art tools, testing, cost."),
        ("ops/cheat-sheets/rr", "R&R cheat-sheet deep packs."),
        ("ops/workflow/ai_dev", "AI_DEV_WORKFLOW packs."),
    ):
        write(
            DOCS / folder / "README.md",
            f"# {folder}\n\n{blurb}\n\nHub: parent `*.md` one level up · Router: [`docs/INDEX.yaml`](../../../INDEX.yaml)\n",
        )


def main() -> int:
    split_ai_testing_spec()
    split_mcp_stack()
    slim_coding_standards_hub()
    slim_rr_cheatsheet()
    slim_ai_dev_workflow()
    write_pack_readmes()
    stamped, skipped = stamp_frontmatter()
    print(f"frontmatter stamped={stamped} skipped={skipped}")
    # sizes
    for rel in (
        "ops/qa/AI_TESTING_SPEC.md",
        "ops/agents/MCP_STACK.md",
        "engineering/technical/CODING_STANDARDS_HUB.md",
        "ops/cheat-sheets/RR_CHEATSHEET.md",
        "ops/workflow/AI_DEV_WORKFLOW.md",
    ):
        p = DOCS / rel
        print(f"size {rel}: {p.stat().st_size} bytes")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
