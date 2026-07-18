#!/usr/bin/env python3
"""Generate spec/build radar PNGs from alignment audit report data.

Writes to docs/compliance/alignment_audit_visuals/ by default:
  - audit_radar_spec.png  — spec stream domains (live scores)
  - audit_radar_build.png — build stream radar OR N/A card on main

Authority: docs/qa/ALIGNMENT_AUDIT.md
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_VISUALS_DIR = ROOT / "docs/compliance/alignment_audit_visuals"

STYLE = {
    "bg": "#1a1f2e",
    "fg": "#e8ecf0",
    "cyan": "#4ae8d8",
    "gold": "#d4a880",
    "muted": "#8b9daf",
    "grid": "#3a4556",
}


def _domain_label(dom_id: str) -> str:
    return dom_id.replace("_", " ").title()


def _radar_chart(
    *,
    labels: list[str],
    values: list[float],
    title: str,
    subtitle: str,
    stream_score: float,
    verdict: str,
    out_path: Path,
) -> None:
    n = len(labels)
    angles = np.linspace(0, 2 * np.pi, n, endpoint=False).tolist()
    values_loop = values + values[:1]
    angles_loop = angles + angles[:1]

    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw={"projection": "polar"})
    fig.patch.set_facecolor(STYLE["bg"])
    ax.set_facecolor(STYLE["bg"])

    ax.plot(angles_loop, values_loop, color=STYLE["cyan"], linewidth=2.5, label="Current")
    ax.fill(angles_loop, values_loop, color=STYLE["cyan"], alpha=0.22)
    target_loop = [10.0] * (n + 1)
    ax.plot(
        angles_loop,
        target_loop,
        color=STYLE["gold"],
        linewidth=1.2,
        linestyle="--",
        alpha=0.55,
        label="Target (10)",
    )

    ax.set_xticks(angles)
    ax.set_xticklabels(labels, color=STYLE["fg"], fontsize=9)
    ax.set_ylim(0, 10)
    ax.set_yticks([2, 4, 6, 8, 10])
    ax.set_yticklabels(["2", "4", "6", "8", "10"], color=STYLE["muted"], fontsize=7)
    ax.grid(color=STYLE["grid"], alpha=0.45)
    ax.spines["polar"].set_color(STYLE["grid"])

    fig.suptitle(title, color=STYLE["fg"], fontsize=15, fontweight="bold", y=0.98)
    ax.set_title(
        f"{stream_score:.2f}/10 · {verdict}\n{subtitle}",
        color=STYLE["muted"],
        fontsize=10,
        pad=24,
    )
    ax.legend(loc="upper right", bbox_to_anchor=(1.15, 1.12), fontsize=8, framealpha=0.2)

    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_path, dpi=150, facecolor=STYLE["bg"], bbox_inches="tight")
    plt.close(fig)


def _na_card(*, title: str, reason: str, branch: str, out_path: Path) -> None:
    fig, ax = plt.subplots(figsize=(8, 8))
    fig.patch.set_facecolor(STYLE["bg"])
    ax.set_facecolor(STYLE["bg"])
    ax.axis("off")
    ax.text(
        0.5,
        0.64,
        title,
        ha="center",
        va="center",
        color=STYLE["fg"],
        fontsize=17,
        fontweight="bold",
        transform=ax.transAxes,
    )
    ax.text(
        0.5,
        0.48,
        "N/A",
        ha="center",
        va="center",
        color=STYLE["muted"],
        fontsize=52,
        fontweight="bold",
        transform=ax.transAxes,
    )
    ax.text(
        0.5,
        0.36,
        f"Branch: {branch}",
        ha="center",
        va="center",
        color=STYLE["cyan"],
        fontsize=11,
        transform=ax.transAxes,
    )
    wrapped = reason[:120] + ("…" if len(reason) > 120 else "")
    ax.text(
        0.5,
        0.26,
        wrapped,
        ha="center",
        va="center",
        color=STYLE["muted"],
        fontsize=10,
        transform=ax.transAxes,
    )
    ax.text(
        0.5,
        0.12,
        "Not a failure — build stream starts on game/development",
        ha="center",
        va="center",
        color=STYLE["gold"],
        fontsize=9,
        transform=ax.transAxes,
    )
    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_path, dpi=150, facecolor=STYLE["bg"], bbox_inches="tight")
    plt.close(fig)


def generate_audit_radars(
    report: dict[str, Any], output_dir: Path | None = None
) -> dict[str, str]:
    """Generate audit_radar_spec.png and audit_radar_build.png. Returns filename → path."""
    out_dir = output_dir or DEFAULT_VISUALS_DIR
    streams = report.get("streams", {})
    branch = report.get("branch", "?")
    written: dict[str, str] = {}

    spec = streams.get("spec_readiness", {})
    spec_domains = spec.get("domains") or {}
    if spec_domains:
        labels = [_domain_label(k) for k in spec_domains]
        values = [float(v) for v in spec_domains.values()]
        spec_path = out_dir / "audit_radar_spec.png"
        _radar_chart(
            labels=labels,
            values=values,
            title="Spec Readiness — Design & Preparation",
            subtitle=spec.get("question", ""),
            stream_score=float(spec.get("score") or 0),
            verdict=str(spec.get("verdict", "?")),
            out_path=spec_path,
        )
        written["audit_radar_spec.png"] = str(spec_path)

    build = streams.get("build_readiness", {})
    build_path = out_dir / "audit_radar_build.png"
    if build.get("status") == "not_applicable" or build.get("score") is None:
        _na_card(
            title="Build Readiness — Development & Shipping",
            reason=str(build.get("na_reason") or "Not applicable on this branch"),
            branch=branch,
            out_path=build_path,
        )
    else:
        build_domains = build.get("domains") or {}
        if build_domains:
            labels = [_domain_label(k) for k in build_domains]
            values = [float(v) for v in build_domains.values()]
            _radar_chart(
                labels=labels,
                values=values,
                title="Build Readiness — Development & Shipping",
                subtitle=build.get("question", ""),
                stream_score=float(build.get("score") or 0),
                verdict=str(build.get("verdict", "?")),
                out_path=build_path,
            )
    written["audit_radar_build.png"] = str(build_path)
    return written


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Generate spec/build audit radar PNGs")
    parser.add_argument(
        "--report",
        default=str(ROOT / "artifacts/alignment_audits/latest.json"),
        help="Audit report JSON path",
    )
    parser.add_argument(
        "--output-dir",
        default=str(DEFAULT_VISUALS_DIR),
        help="Directory for audit_radar_spec.png and audit_radar_build.png",
    )
    args = parser.parse_args(argv)

    report_path = Path(args.report)
    if not report_path.is_file():
        print(f"MISSING: {report_path}", file=sys.stderr)
        return 1

    report = json.loads(report_path.read_text(encoding="utf-8"))
    written = generate_audit_radars(report, Path(args.output_dir))
    for name, path in written.items():
        print(f"Wrote {path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
