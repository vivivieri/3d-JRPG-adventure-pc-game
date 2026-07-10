#!/usr/bin/env python3
"""Generate a timestamped compliance audit report (proof of license review).

Outputs:
  docs/compliance/COMPLIANCE_REPORT.md   — human-readable audit
  docs/compliance/COMPLIANCE_REPORT.json — machine-readable audit

Usage:
  python3 tools/generate_compliance_report.py
  python3 tools/generate_compliance_report.py --credits   # print credits draft
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MANIFEST_PATH = ROOT / "docs" / "asset_manifest.license.json"
OUT_DIR = ROOT / "docs" / "compliance"
OUT_MD = OUT_DIR / "COMPLIANCE_REPORT.md"
OUT_JSON = OUT_DIR / "COMPLIANCE_REPORT.json"


def run_verify() -> tuple[int, str]:
    script = ROOT / "tools" / "verify_asset_licenses.py"
    result = subprocess.run(
        [sys.executable, str(script)],
        capture_output=True,
        text=True,
        cwd=ROOT,
    )
    output = (result.stdout or "") + (result.stderr or "")
    return result.returncode, output.strip()


def scan_media_counts(manifest: dict) -> dict:
  sys.path.insert(0, str(ROOT / "tools"))
  from verify_asset_licenses import iter_media_files, load_manifest, lookup_entry, build_coverage

  m = load_manifest()
  coverage, allowed, banned = build_coverage(m)
  files = iter_media_files(m)
  by_license: dict[str, int] = {}
  unlisted = 0
  for rel in files:
    entry = lookup_entry(rel, coverage)
    if entry:
      lic = entry.get("license", "?")
      by_license[lic] = by_license.get(lic, 0) + 1
    else:
      unlisted += 1
  return {
    "total_media_files": len(files),
    "by_license": by_license,
    "unlisted": unlisted,
    "allowed_license_types": sorted(allowed),
    "banned_license_types": sorted(banned),
  }


def credits_draft(manifest: dict) -> str:
    lines = [
        "# Credits (draft — paste into game credits scene)",
        "",
        "## Engine & tools",
        "- Godot Engine — MIT License — https://godotengine.org",
        "- GodotSteam — MIT License — https://codeberg.org/godotsteam/godotsteam",
        "",
        "## Fonts",
    ]
    seen: set[str] = set()
    for entry in manifest.get("assets", []):
        if entry.get("license") == "OFL-1.1" and entry.get("attribution"):
            text = entry["attribution"]
            if text not in seen:
                lines.append(f"- {text}")
                seen.add(text)

    lines.extend(["", "## Third-party assets (attribution required)"])
    attributions = [
        e for e in manifest.get("assets", [])
        if e.get("attribution") and e.get("license") not in ("OFL-1.1",)
    ]
    if attributions:
        for e in attributions:
            path = e.get("glob") or e.get("path", "")
            lines.append(f"- {e['attribution']} — {path}")
    else:
        lines.append("- (none requiring attribution beyond fonts/engine)")

    lines.extend(["", "## CC0 appreciation (optional)"])
    for e in manifest.get("assets", []):
        if e.get("license") == "CC0-1.0":
            src = e.get("source", "")
            if src and src not in seen:
                lines.append(f"- {src}")
                seen.add(src)

    lines.extend([
        "",
        "## Story",
        "- Adapted from Urashima Tarō (Japanese folklore, public domain)",
        "",
        "## Original work",
        "- Game code, procedural art/audio tools — MIT (this repository)",
    ])
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--credits", action="store_true", help="Print credits draft only")
    args = parser.parse_args()

    with open(MANIFEST_PATH, encoding="utf-8") as f:
        manifest = json.load(f)

    if args.credits:
        print(credits_draft(manifest))
        return 0

    exit_code, verify_output = run_verify()
    stats = scan_media_counts(manifest)
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")

    report = {
        "generated_at": now,
        "policy": manifest.get("policy"),
        "manifest": str(MANIFEST_PATH.relative_to(ROOT)),
        "verify_exit_code": exit_code,
        "verify_passed": exit_code == 0,
        "verify_output": verify_output,
        "statistics": stats,
        "manifest_entry_count": len(manifest.get("assets", [])),
    }

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    with open(OUT_JSON, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
        f.write("\n")

    status = "PASSED" if exit_code == 0 else "FAILED"
    md_lines = [
        "# Asset Compliance Report",
        "",
        f"**Generated:** {now}  ",
        f"**Status:** {status}  ",
        f"**Policy:** [{manifest.get('policy')}](../ASSET_COMPLIANCE.md)  ",
        f"**Manifest:** `{MANIFEST_PATH.relative_to(ROOT)}`",
        "",
        "## Verification output",
        "",
        "```",
        verify_output or "(no output)",
        "```",
        "",
        "## Statistics",
        "",
        f"| Metric | Value |",
        f"|--------|-------|",
        f"| Media files on disk | {stats['total_media_files']} |",
        f"| Unlisted files | {stats['unlisted']} |",
        f"| Manifest entries | {report['manifest_entry_count']} |",
        "",
        "### Files by license",
        "",
    ]
    if stats["by_license"]:
        md_lines.append("| License | File count |")
        md_lines.append("|---------|------------|")
        for lic, count in sorted(stats["by_license"].items()):
            md_lines.append(f"| {lic} | {count} |")
    else:
        md_lines.append("_No media files on disk (docs-only branch or pre-asset phase)._")

    md_lines.extend([
        "",
        "## Allowed license types",
        "",
        ", ".join(f"`{x}`" for x in stats["allowed_license_types"]),
        "",
        "## Banned license types",
        "",
        ", ".join(f"`{x}`" for x in stats["banned_license_types"]),
        "",
        "## Credits draft",
        "",
        "Run `python3 tools/generate_compliance_report.py --credits` for in-game credits text.",
        "",
        "---",
        "",
        "*This report is generated proof of an automated license audit. Re-run before each Steam upload.*",
    ])

    OUT_MD.write_text("\n".join(md_lines) + "\n", encoding="utf-8")
    print(f"Report written: {OUT_MD.relative_to(ROOT)}")
    print(f"JSON written:  {OUT_JSON.relative_to(ROOT)}")
    print(f"Status: {status}")
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
