#!/usr/bin/env python3
"""Apply skim aids (summary + When to read + Jump to) across active doc leaves.

Policy: docs/_meta/DOC_LIBRARY_ADR.md § Amendment — Docs pack thinning.
Prefer skim aids over new pack splits. Idempotent — safe to re-run.
"""
from __future__ import annotations

import argparse
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"

SKIP_NAMES = {
    "README.md",
    "BOOT.md",
    "INDEX.md",
    "COMPLIANCE_REPORT.md",
    "AGENTS.md",
    "FRONTMATTER.md",
    "DOC_LIBRARY_ADR.md",
    "DOCS_READ_LOG.md",
    "ARTIFACTS.md",
    "DOCS_PACK_SCHEMA.md",
}
SKIP_PREFIXES = (
    "archive/",
    "briefs/",
    "design/audio/audio_sheets/",  # never_autoload sheets — not in resolve packs
)  # relative to docs/


def strip_fm(text: str) -> tuple[str, str]:
    if not text.startswith("---\n"):
        return "", text
    end = text.find("\n---\n", 4)
    if end < 0:
        return "", text
    return text[: end + 5], text[end + 5 :]


def parse_fm(fm_block: str) -> dict[str, str]:
    meta: dict[str, str] = {}
    for line in fm_block.splitlines():
        if ":" not in line or line.strip() in ("---",):
            continue
        k, v = line.split(":", 1)
        meta[k.strip()] = v.strip().strip("\"'")
    return meta


def is_hub(body: str) -> bool:
    return "| Pack | Topic |" in body or "## Packs" in body


def github_anchor(heading: str) -> str:
    text = re.sub(r"^#{1,6}\s+", "", heading).strip().lower()
    text = text.replace("`", "")
    # keep letters, digits, spaces, hyphens
    text = re.sub(r"[^\w\s\-]", "", text, flags=re.UNICODE)
    text = re.sub(r"\s+", "-", text.strip())
    text = re.sub(r"-+", "-", text)
    return text


def headings(body: str) -> list[tuple[int, str, str]]:
    """Return (level, raw_line, anchor) for ## / ### excluding skim sections."""
    out: list[tuple[int, str, str]] = []
    seen: dict[str, int] = {}
    for line in body.splitlines():
        m = re.match(r"^(#{2,3})\s+(.+)$", line)
        if not m:
            continue
        title = m.group(2).strip()
        if title in ("When to read", "Jump to", "Packs", "Related packs"):
            continue
        if title.startswith("Pack |"):
            continue
        level = len(m.group(1))
        base = github_anchor(title)
        n = seen.get(base, 0)
        seen[base] = n + 1
        anchor = base if n == 0 else f"{base}-{n}"
        out.append((level, title, anchor))
    return out


def summary_weak(raw: str) -> bool:
    s = (raw or "").strip().strip("\"'")
    if not s or len(s) < 40:
        return True
    low = s.lower()
    if low.endswith(" summary") or low.startswith("see `"):
        return True
    if s.startswith(("**Hub", "**Version", "**Authority", "[")):
        return True
    # Truncated / broken frontmatter leftovers
    if s.count("`") % 2 == 1:
        return True
    if s.endswith(("_", "-", "…", "—")):
        return True
    # Very short ellipsis clamps are usually mid-thought cuts
    if s.endswith("...") and len(s) < 90:
        return True
    # Mid-sentence cut (common after 160-char clamp)
    if s.endswith((" the", " a", " an", " to", " of", " for", " and", " or", " with")):
        return True
    return False


def _clamp_summary(text: str, limit: int = 160) -> str:
    """Clamp without breaking backticks or mid-word when possible."""
    s = text.replace("\n", " ").replace('"', "'").strip()
    if len(s) <= limit:
        return s
    cut = s[:limit]
    if " " in cut:
        cut = cut.rsplit(" ", 1)[0]
    if cut.count("`") % 2 == 1:
        cut = cut.rsplit("`", 1)[0].rstrip()
    cut = cut.rstrip(".,;: —-")
    if not cut.endswith("."):
        cut += "."
    return cut[:limit]


def first_prose(body: str) -> str:
    for line in body.splitlines():
        s = line.strip()
        if not s or s.startswith("#") or s.startswith("|") or s.startswith("```"):
            continue
        if s.startswith(("**Hub", "**Hub**", "> ", "---")):
            continue
        if s.startswith("| Pack"):
            continue
        if s.startswith(("- [ ]", "- [x]", "* [ ]")):
            continue
        # strip markdown bold/links lightly
        s = re.sub(r"\*\*([^*]+)\*\*", r"\1", s)
        s = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", s)
        s = s.strip().strip("`")
        if len(s) < 20:
            continue
        return s
    return ""


def derive_summary(title: str, body: str, meta: dict[str, str], hs: list[tuple[int, str, str]]) -> str:
    prose = first_prose(body)
    audience = meta.get("audience", "").strip("[]")
    # Prefer section topics when first prose is a fragment / code / diagram label
    prose_bad = False
    if prose:
        low = prose.lower()
        if "`" in prose or prose.startswith(("[", "|", "-", "*")):
            prose_bad = True
        if low.startswith(
            ("runner:", "location:", "scene:", "source of truth:", "policy:", "from ")
        ):
            prose_bad = True
        if prose.startswith("Scope:") and len(prose) < 80:
            prose_bad = True
    if prose and not prose_bad and not prose.lower().startswith("hub"):
        tip = prose
        if "open when" not in tip.lower() and " — " not in tip and not tip.lower().startswith(
            title.lower()[:12]
        ):
            tip = f"{title} — {tip}"
        return _clamp_summary(tip)
    if hs:
        topics = "; ".join(h[1] for h in hs[:4])
        return _clamp_summary(f"{title} — covers {topics}")
    if audience:
        return _clamp_summary(f"{title} — for {audience}")
    return _clamp_summary(f"{title} — project reference")


def ensure_frontmatter(fm_block: str, body: str, title: str) -> tuple[str, str]:
    """Guarantee a summary field exists (create minimal FM when missing)."""
    if fm_block:
        return fm_block, body
    slug = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")[:48] or "doc"
    fm = (
        "---\n"
        f"id: {slug}\n"
        "type: reference\n"
        "status: active\n"
        f'summary: "{title} — project reference"\n'
        "---\n"
    )
    return fm, body


def derive_when(title: str, meta: dict[str, str], hs: list[tuple[int, str, str]]) -> str:
    doc_type = meta.get("type", "reference")
    audience = meta.get("audience", "").strip("[]")
    bits = [f"Use **{title}**"]
    if audience:
        bits.append(f"(roles: {audience})")
    if doc_type == "how-to":
        bits.append("when executing this procedure")
    elif doc_type == "tutorial":
        bits.append("when learning/setup for the first time")
    else:
        bits.append("when you need this reference during the current task")
    if hs:
        bits.append(f"Jump to a section below instead of reading end-to-end ({len(hs)} sections).")
    else:
        bits.append("Short leaf — skim the body if the summary matches your task.")
    return " ".join(bits)


def strip_existing_skim(body: str) -> str:
    """Remove prior When to read / Jump to blocks (idempotent)."""
    # Remove from ## When to read through end of Jump to list (until next ##/### content heading)
    body = re.sub(
        r"\n## When to read\n.*?(?=\n## (?!When to read|Jump to)|\n### |\Z)",
        "\n",
        body,
        count=1,
        flags=re.S,
    )
    body = re.sub(
        r"\n## Jump to\n.*?(?=\n## (?!When to read|Jump to)|\n### |\Z)",
        "\n",
        body,
        count=1,
        flags=re.S,
    )
    return body


def build_jump(hs: list[tuple[int, str, str]]) -> str:
    lines = ["## Jump to", ""]
    for _level, title, anchor in hs:
        lines.append(f"- [{title}](#{anchor})")
    lines.append("")
    return "\n".join(lines)


def set_fm_field(fm_block: str, key: str, value: str) -> str:
    safe = _clamp_summary(value.replace("\n", " ").replace('"', "'").strip())
    if re.search(rf"(?m)^{key}:", fm_block):
        return re.sub(rf"(?m)^{key}:\s*.*$", f'{key}: "{safe}"', fm_block, count=1)
    if fm_block.rstrip().endswith("---"):
        return fm_block.rstrip()[:-3] + f'{key}: "{safe}"\n---\n'
    return fm_block


def retokens(fm_block: str, body: str) -> str:
    tokens = max(180, len(body) // 4)
    if re.search(r"(?m)^tokens_est:", fm_block):
        return re.sub(r"(?m)^tokens_est:\s*\d+", f"tokens_est: {tokens}", fm_block, count=1)
    if fm_block.rstrip().endswith("---"):
        return fm_block.rstrip()[:-3] + f"tokens_est: {tokens}\n---\n"
    return fm_block


def process_file(path: Path, *, min_tokens: int, summary_only_below: int, dry_run: bool) -> str | None:
    rel = path.relative_to(DOCS).as_posix()
    if any(rel.startswith(p) for p in SKIP_PREFIXES):
        return None
    if path.name in SKIP_NAMES:
        return None

    raw = path.read_text(encoding="utf-8")
    fm_block, body = strip_fm(raw)
    if is_hub(body):
        return None

    tok = max(1, len(body) // 4)
    if tok < min_tokens:
        return None

    title_m = re.search(r"(?m)^#\s+(.+)$", body)
    title = title_m.group(1).strip() if title_m else path.stem.replace("_", " ")
    fm_block, body = ensure_frontmatter(fm_block, body, title)
    meta = parse_fm(fm_block)

    body2 = strip_existing_skim(body)
    hs = headings(body2)

    old_sum = meta.get("summary", "")
    new_sum = old_sum
    if summary_weak(old_sum):
        new_sum = derive_summary(title, body2, meta, hs)

    add_jump = tok >= summary_only_below and len(hs) >= 2
    when = derive_when(title, meta, hs) if add_jump or tok >= summary_only_below else ""

    # Build insertion
    insert = ""
    if when:
        insert += f"## When to read\n\n{when}\n\n"
    if add_jump:
        insert += build_jump(hs)

    if not insert and new_sum == old_sum:
        return None

    # Place after Hub line or after H1
    if insert:
        m = re.search(r"(?m)^\*\*Hub:\*\*.+\n", body2)
        if m:
            body2 = body2[: m.end()] + "\n" + insert + body2[m.end() :]
        else:
            m = re.search(r"(?m)^# .+\n", body2)
            if m:
                body2 = body2[: m.end()] + "\n" + insert + body2[m.end() :]
            else:
                body2 = insert + "\n" + body2

    fm_block = set_fm_field(fm_block, "summary", new_sum)
    fm_block = retokens(fm_block, body2)
    # fix tokens_est if quoted wrongly
    fm_block = re.sub(r'(?m)^tokens_est:\s*"(\d+)"', r"tokens_est: \1", fm_block)
    out = fm_block + body2
    if not out.endswith("\n"):
        out += "\n"

    if out == raw:
        return None
    if dry_run:
        return f"DRY {rel} sum_weak={summary_weak(old_sum)} jump={add_jump} hs={len(hs)}"
    path.write_text(out, encoding="utf-8")
    return f"OK {rel} jump={add_jump} hs={len(hs)} tok~{len(body2)//4} weak_fix={summary_weak(old_sum)}"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--min-tokens", type=int, default=0, help="Skip leaves smaller than this (0=all active leaves)")
    ap.add_argument(
        "--summary-only-below",
        type=int,
        default=0,
        help="Legacy alias; jump threshold is --full-skim-at",
    )
    ap.add_argument(
        "--full-skim-at",
        type=int,
        default=0,
        help="At/above this size with ≥2 headings, add When to read + Jump to (0=all)",
    )
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--limit", type=int, default=0, help="Max files to change (0=all)")
    args = ap.parse_args()

    # Use full_skim_at as summary_only_below for jump threshold
    summary_only_below = args.full_skim_at

    changed = 0
    for path in sorted(DOCS.rglob("*.md")):
        msg = process_file(
            path,
            min_tokens=args.min_tokens,
            summary_only_below=summary_only_below,
            dry_run=args.dry_run,
        )
        if not msg:
            continue
        print(msg)
        changed += 1
        if args.limit and changed >= args.limit:
            break
    print(f"done — {changed} file(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
