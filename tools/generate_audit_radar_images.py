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
CATALOG_PATH = ROOT / "game/data/qa/alignment_audit_catalog.json"

SPEC_DOMAIN_ORDER = [
    "data_alignment",
    "narrative",
    "gameplay",
    "visual_spec",
    "ux_controls",
    "pm_workflow",
]

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


def _signal_label(sig_id: str) -> str:
    return sig_id.replace("_", " ").title()


def _load_catalog() -> dict[str, Any]:
    return json.loads(CATALOG_PATH.read_text(encoding="utf-8"))


def _domain_title(catalog: dict[str, Any], dom_id: str) -> str:
    for row in catalog.get("domains", []):
        if row.get("id") == dom_id:
            return str(row.get("label", dom_id))
    return _domain_label(dom_id)


def _mini_radar_on_axis(
    ax: Any,
    *,
    labels: list[str],
    values: list[float],
    title: str,
    domain_score: float,
) -> None:
    n = len(labels)
    if n < 3:
        ax.axis("off")
        ax.text(0.5, 0.5, f"{title}\n(insufficient signals)", ha="center", va="center", color=STYLE["muted"])
        return
    angles = np.linspace(0, 2 * np.pi, n, endpoint=False).tolist()
    values_loop = values + values[:1]
    angles_loop = angles + angles[:1]
    ax.plot(angles_loop, values_loop, color=STYLE["cyan"], linewidth=1.8)
    ax.fill(angles_loop, values_loop, color=STYLE["cyan"], alpha=0.2)
    target_loop = [10.0] * (n + 1)
    ax.plot(angles_loop, target_loop, color=STYLE["gold"], linewidth=0.9, linestyle="--", alpha=0.5)
    ax.set_xticks(angles)
    ax.set_xticklabels(labels, color=STYLE["fg"], fontsize=6)
    ax.set_ylim(0, 10)
    ax.set_yticks([2, 4, 6, 8, 10])
    ax.set_yticklabels(["2", "4", "6", "8", "10"], color=STYLE["muted"], fontsize=5)
    ax.grid(color=STYLE["grid"], alpha=0.4)
    ax.spines["polar"].set_color(STYLE["grid"])
    ax.set_title(f"{title}\n{domain_score:.2f}/10", color=STYLE["fg"], fontsize=9, pad=10)


def generate_spec_subdomain_radars(
    report: dict[str, Any], output_dir: Path, catalog: dict[str, Any] | None = None
) -> dict[str, str]:
    """Generate per-domain signal sub-radars + 2×3 breakdown grid for spec stream."""
    cat = catalog or _load_catalog()
    out_dir = output_dir
    signal_scores = report.get("signal_scores", {})
    domain_scores = report.get("domain_scores", {})
    written: dict[str, str] = {}

    for dom_id in SPEC_DOMAIN_ORDER:
        signals = signal_scores.get(dom_id, {})
        if not signals:
            continue
        labels = [_signal_label(sid) for sid in signals]
        values = [float(v) for v in signals.values()]
        fname = f"audit_radar_spec_{dom_id}.png"
        out_path = out_dir / fname
        _radar_chart(
            labels=labels,
            values=values,
            title=_domain_title(cat, dom_id),
            subtitle="Signal breakdown",
            stream_score=float(domain_scores.get(dom_id, 0)),
            verdict="",
            out_path=out_path,
        )
        written[fname] = str(out_path)

    fig, axes = plt.subplots(2, 3, figsize=(16, 10), subplot_kw={"projection": "polar"})
    fig.patch.set_facecolor(STYLE["bg"])
    spec = report.get("streams", {}).get("spec_readiness", {})
    fig.suptitle(
        f"Spec Sub-Radar Breakdown — {spec.get('score', '?')}/10 · {spec.get('verdict', '')}",
        color=STYLE["fg"],
        fontsize=14,
        fontweight="bold",
        y=0.98,
    )
    for idx, dom_id in enumerate(SPEC_DOMAIN_ORDER):
        ax = axes.flat[idx]
        ax.set_facecolor(STYLE["bg"])
        signals = signal_scores.get(dom_id, {})
        if signals:
            labels = [_signal_label(sid) for sid in signals]
            values = [float(v) for v in signals.values()]
            _mini_radar_on_axis(
                ax,
                labels=labels,
                values=values,
                title=_domain_title(cat, dom_id),
                domain_score=float(domain_scores.get(dom_id, 0)),
            )
        else:
            ax.axis("off")
    breakdown_path = out_dir / "audit_radar_spec_breakdown.png"
    breakdown_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(breakdown_path, dpi=150, facecolor=STYLE["bg"], bbox_inches="tight")
    plt.close(fig)
    written["audit_radar_spec_breakdown.png"] = str(breakdown_path)
    return written


    return dom_id.replace("_", " ").title()

def _draw_radar_on_axis(
    ax: Any,
    *,
    labels: list[str],
    values: list[float],
    title: str,
    stream_score: float,
    verdict: str,
) -> None:
    n = len(labels)
    angles = np.linspace(0, 2 * np.pi, n, endpoint=False).tolist()
    values_loop = values + values[:1]
    angles_loop = angles + angles[:1]

    ax.plot(angles_loop, values_loop, color=STYLE["cyan"], linewidth=2.2)
    ax.fill(angles_loop, values_loop, color=STYLE["cyan"], alpha=0.22)
    target_loop = [10.0] * (n + 1)
    ax.plot(
        angles_loop,
        target_loop,
        color=STYLE["gold"],
        linewidth=1.0,
        linestyle="--",
        alpha=0.55,
    )
    ax.set_xticks(angles)
    ax.set_xticklabels(labels, color=STYLE["fg"], fontsize=8)
    ax.set_ylim(0, 10)
    ax.set_yticks([2, 4, 6, 8, 10])
    ax.set_yticklabels(["2", "4", "6", "8", "10"], color=STYLE["muted"], fontsize=6)
    ax.grid(color=STYLE["grid"], alpha=0.45)
    ax.spines["polar"].set_color(STYLE["grid"])
    ax.set_title(
        f"{title}\n{stream_score:.2f}/10 · {verdict}",
        color=STYLE["fg"],
        fontsize=10,
        pad=16,
    )


def _draw_na_on_axis(ax: Any, *, title: str, reason: str, branch: str) -> None:
    ax.axis("off")
    ax.text(0.5, 0.72, title, ha="center", va="center", color=STYLE["fg"], fontsize=12, fontweight="bold")
    ax.text(0.5, 0.5, "N/A", ha="center", va="center", color=STYLE["muted"], fontsize=36, fontweight="bold")
    ax.text(0.5, 0.36, f"Branch: {branch}", ha="center", va="center", color=STYLE["cyan"], fontsize=9)
    wrapped = reason[:90] + ("…" if len(reason) > 90 else "")
    ax.text(0.5, 0.24, wrapped, ha="center", va="center", color=STYLE["muted"], fontsize=8)


def _combined_radar_report(report: dict[str, Any], out_path: Path) -> None:
    streams = report.get("streams", {})
    branch = report.get("branch", "?")
    verdict = report.get("verdict", "?")
    spec = streams.get("spec_readiness", {})
    build = streams.get("build_readiness", {})

    fig = plt.figure(figsize=(14, 7))
    fig.patch.set_facecolor(STYLE["bg"])
    fig.suptitle(
        f"Tides of Urashima — Alignment Radar Report · {verdict}",
        color=STYLE["fg"],
        fontsize=16,
        fontweight="bold",
        y=0.98,
    )
    fig.text(
        0.5,
        0.93,
        f"{branch} · {report.get('generated_at', '')} · Spec + Build streams",
        ha="center",
        color=STYLE["muted"],
        fontsize=10,
    )

    ax_spec = fig.add_subplot(1, 2, 1, projection="polar")
    ax_spec.set_facecolor(STYLE["bg"])
    spec_domains = spec.get("domains") or {}
    if spec_domains:
        labels = [_domain_label(k) for k in spec_domains]
        values = [float(v) for v in spec_domains.values()]
        _draw_radar_on_axis(
            ax_spec,
            labels=labels,
            values=values,
            title="Spec — Design & Preparation",
            stream_score=float(spec.get("score") or 0),
            verdict=str(spec.get("verdict", "?")),
        )
    else:
        ax_spec.axis("off")

    if build.get("status") == "not_applicable" or build.get("score") is None:
        ax_build = fig.add_subplot(1, 2, 2)
        ax_build.set_facecolor(STYLE["bg"])
        _draw_na_on_axis(
            ax_build,
            title="Build — Development & Shipping",
            reason=str(build.get("na_reason") or "Not applicable on this branch"),
            branch=branch,
        )
    else:
        ax_build = fig.add_subplot(1, 2, 2, projection="polar")
        ax_build.set_facecolor(STYLE["bg"])
        build_domains = build.get("domains") or {}
        if build_domains:
            labels = [_domain_label(k) for k in build_domains]
            values = [float(v) for v in build_domains.values()]
            _draw_radar_on_axis(
                ax_build,
                labels=labels,
                values=values,
                title="Build — Development & Shipping",
                stream_score=float(build.get("score") or 0),
                verdict=str(build.get("verdict", "?")),
            )

    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_path, dpi=150, facecolor=STYLE["bg"], bbox_inches="tight")
    plt.close(fig)


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
        f"{stream_score:.2f}/10{f' · {verdict}' if verdict else ''}\n{subtitle}",
        color=STYLE["muted"],
        fontsize=10,
        pad=24,
    )
    if verdict:
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

    report_path = out_dir / "audit_radar_report.png"
    _combined_radar_report(report, report_path)
    written["audit_radar_report.png"] = str(report_path)

    written.update(generate_spec_subdomain_radars(report, out_dir))

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
