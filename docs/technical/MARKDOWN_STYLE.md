# Markdown Style Guide — Tides of Urashima

**Version:** 1.0
**Scope:** `docs/**/*.md`, root `AGENTS.md`, `game/data/README.md`, PR templates
**Hub:** [`CODING_STANDARDS_HUB.md`](CODING_STANDARDS_HUB.md)
**Generated docs:** `docs/compliance/COMPLIANCE_REPORT.md` and `alignment_audit_reports/**` are auto-generated — do not hand-edit.

---

## 1. Industry standards

| Standard | Reference | What it governs |
|----------|-----------|-----------------|
| **CommonMark** | [spec.commonmark.org](https://spec.commonmark.org/) | Portable markdown syntax |
| **Google developer docs** | [styleguide.doc](https://developers.google.com/style) | Clarity, headings, lists |
| **Accessibility** | [WCAG link text](https://www.w3.org/WAI/WCAG21/Understanding/link-purpose-in-context.html) | Descriptive link labels |

---

## 2. File format

| Rule | Detail |
|------|--------|
| Encoding | UTF-8 (no BOM) |
| Line endings | LF |
| Trailing newline | One `\n` at EOF |
| Indentation | Spaces only — **no tabs** in prose |
| Line length | Soft ~100 chars — wrap long tables in source when readable |
| Headings | ATX (`#`) — avoid setext (`===`) underlines |

---

## 3. Structure

| Rule | Detail |
|------|--------|
| Title | One H1 per doc (`# Title`) at top |
| Version block | Technical guides: `**Version:**` + `**Scope:**` after H1 |
| Hub link | Link back to `CODING_STANDARDS_HUB.md` or `docs/README.md` |
| Sections | Increment heading levels by one — no skipped levels (`#` → `##` → `###`) |
| Tables | Pipe tables for matrices; align `|` for diff-friendly edits |

---

## 4. Links & paths

| Do | Don't |
|----|-------|
| `[CI.md](../ci-cd/CI.md)` relative from current file | Broken `IMPLEMENTATION_PLAN.md` without path |
| Full URLs for external specs | Bare `https://` without link text |
| `docs/technical/FOO.md` from hub | Deep links to generated audit HTML |

**CI:** `check_markdown_style.py` verifies relative links resolve (excludes `docs/deprecated/`).

---

## 5. Code & commands

- Fenced blocks with language tag: ` ```bash `, ` ```gdscript `, ` ```json `
- One command per line in copy-paste shells — no `$` prompt prefix
- Gate ids in backticks: `` `L1_python_lint` ``

---

## 6. Voice & content

| Audience | Tone |
|----------|------|
| `docs/technical/` | Precise, imperative, link to authority JSON |
| `docs/vision/` | Evocative but still structured |
| `docs/agents/` | Runbook steps — numbered when order matters |
| `docs/qa/` | Measurable pass/fail — cite gate ids |

Avoid engagement bait, vague "should consider", and duplicate indexes (Notion rejected — `docs/` is authoritative).

---

## 7. CI enforcement

```bash
python3 tools/check_markdown_style.py   # L1_markdown_style
```

Checks: trailing newline, no tabs, no trailing whitespace, ATX headings (level jumps), resolvable relative links.

---

## 8. PR checklist

- [ ] `python3 tools/check_markdown_style.py` green
- [ ] New doc linked from `docs/README.md` or hub when user-facing
- [ ] No tabs; trailing newline present
- [ ] Relative links tested from file location
