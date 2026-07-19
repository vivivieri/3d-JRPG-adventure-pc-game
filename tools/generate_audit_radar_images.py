#!/usr/bin/env python3
"""Generate spec/build radar PNGs from alignment audit report data.

Themed for Tides of Urashima — muted coastal palette (docs/art/ART_DIRECTION.md).

Authority: docs/qa/ALIGNMENT_AUDIT.md
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

import matplotlib.pyplot as plt

from audit_radar_theme import (
    DOMAIN_ACCENT,
    GAME_SUBTITLE,
    PALETTE,
    apply_void_gradient,
    configure_matplotlib,
    draw_brand_header,
    draw_na_panel,
    draw_panel_frame,
    style_polar_axis,
    wrap_label,
)

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

BUILD_DOMAIN_ORDER = [
    "runtime_proof",
    "steam_ship",
]

DPI = 180


def _domain_label(dom_id: str) -> str:
    return dom_id.replace("_", " ").title()


def _signal_label(sig_id: str) -> str:
    return sig_id.replace("_", " ").replace("L0 ", "L0·").title()


def _load_catalog() -> dict[str, Any]:
    return json.loads(CATALOG_PATH.read_text(encoding="utf-8"))


def _domain_title(catalog: dict[str, Any], dom_id: str) -> str:
    for row in catalog.get("domains", []):
        if row.get("id") == dom_id:
            return str(row.get("label", dom_id))
    return _domain_label(dom_id)


def _save_fig(fig: plt.Figure, out_path: Path) -> None:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_path, dpi=DPI, facecolor=PALETTE["void"], bbox_inches="tight", pad_inches=0.35)
    plt.close(fig)


def _radar_figure(
    *,
    labels: list[str],
    values: list[float],
    title: str,
    subtitle: str,
    stream_score: float,
    verdict: str,
    accent: str,
    figsize: tuple[float, float] = (9, 9),
    label_fs: float = 9,
) -> plt.Figure:
    configure_matplotlib()
    fig = plt.figure(figsize=figsize)
    apply_void_gradient(fig, alpha_top=0.42)
    draw_brand_header(
        fig,
        title=title,
        subtitle=subtitle or GAME_SUBTITLE,
        verdict=verdict,
        meta=f"Score {stream_score:.2f} / 10",
        y=0.97,
    )
    ax = fig.add_subplot(111, projection="polar")
    draw_panel_frame(ax, accent=accent)
    style_polar_axis(
        ax,
        labels=labels,
        values=values,
        accent=accent,
        title="",
        score_line=f"{stream_score:.1f}",
        label_fs=label_fs,
    )
    fig.subplots_adjust(top=0.82, bottom=0.08, left=0.06, right=0.94)
    return fig


def _radar_chart(
    *,
    labels: list[str],
    values: list[float],
    title: str,
    subtitle: str,
    stream_score: float,
    verdict: str,
    out_path: Path,
    accent: str | None = None,
) -> None:
    accent = accent or PALETTE["biolume"]
    fig = _radar_figure(
        labels=labels,
        values=values,
        title=title,
        subtitle=subtitle,
        stream_score=stream_score,
        verdict=verdict,
        accent=accent,
    )
    _save_fig(fig, out_path)


def _na_card(*, title: str, reason: str, branch: str, out_path: Path) -> None:
    configure_matplotlib()
    fig = plt.figure(figsize=(9, 9))
    apply_void_gradient(fig, alpha_top=0.38)
    draw_brand_header(
        fig,
        title=title,
        subtitle="Development & shipping stream",
        verdict="N/A",
        meta=f"Branch · {branch}",
        y=0.97,
    )
    ax = fig.add_axes([0.08, 0.12, 0.84, 0.68])
    draw_na_panel(ax, title=title, reason=reason, branch=branch, accent=PALETTE["fog"])
    _save_fig(fig, out_path)


def _combined_radar_report(report: dict[str, Any], out_path: Path) -> None:
    configure_matplotlib()
    streams = report.get("streams", {})
    branch = report.get("branch", "?")
    verdict = str(report.get("verdict", "?"))
    spec = streams.get("spec_readiness", {})
    build = streams.get("build_readiness", {})

    fig = plt.figure(figsize=(15, 8))
    apply_void_gradient(fig, alpha_top=0.4)
    draw_brand_header(
        fig,
        title="Alignment Radar Report",
        subtitle=GAME_SUBTITLE,
        verdict=verdict,
        meta=f"{branch} · {report.get('generated_at', '')}",
        y=0.97,
    )

    ax_spec = fig.add_axes([0.06, 0.12, 0.4, 0.72], projection="polar")
    draw_panel_frame(ax_spec, accent=PALETTE["biolume"])
    spec_domains = spec.get("domains") or {}
    if spec_domains:
        labels = [wrap_label(_domain_label(k), 10) for k in spec_domains]
        values = [float(v) for v in spec_domains.values()]
        style_polar_axis(
            ax_spec,
            labels=labels,
            values=values,
            accent=PALETTE["biolume"],
            title="Design & Preparation",
            score_line=f"{float(spec.get('score') or 0):.1f}",
            label_fs=8,
        )
    fig.text(
        0.26,
        0.08,
        spec.get("question", ""),
        ha="center",
        fontsize=8,
        color=PALETTE["muted"],
        wrap=True,
    )

    if build.get("status") == "not_applicable" or build.get("score") is None:
        ax_build = fig.add_axes([0.56, 0.12, 0.38, 0.72])
        draw_na_panel(
            ax_build,
            title="Development & Shipping",
            reason=str(build.get("na_reason") or "Not applicable on this branch"),
            branch=branch,
            accent=PALETTE["lantern"],
        )
    else:
        ax_build = fig.add_axes([0.56, 0.12, 0.4, 0.72], projection="polar")
        draw_panel_frame(ax_build, accent=PALETTE["coral_gold"])
        build_domains = build.get("domains") or {}
        if build_domains:
            labels = [wrap_label(_domain_label(k), 10) for k in build_domains]
            values = [float(v) for v in build_domains.values()]
            style_polar_axis(
                ax_build,
                labels=labels,
                values=values,
                accent=PALETTE["coral_gold"],
                title="Development & Shipping",
                score_line=f"{float(build.get('score') or 0):.1f}",
                label_fs=8,
            )

    _save_fig(fig, out_path)


def _generate_subdomain_radars(
    report: dict[str, Any],
    output_dir: Path,
    catalog: dict[str, Any],
    *,
    domain_order: list[str],
    stream_key: str,
    filename_prefix: str,
    breakdown_filename: str,
    breakdown_title: str,
    breakdown_subtitle: str,
    detail_subtitle: str,
    grid_cols: int,
) -> dict[str, str]:
    signal_scores = report.get("signal_scores", {})
    domain_scores = report.get("domain_scores", {})
    written: dict[str, str] = {}

    for dom_id in domain_order:
        signals = signal_scores.get(dom_id, {})
        if not signals:
            continue
        labels = [_signal_label(sid) for sid in signals]
        values = [float(v) for v in signals.values()]
        accent = DOMAIN_ACCENT.get(dom_id, PALETTE["biolume"])
        fname = f"{filename_prefix}_{dom_id}.png"
        _radar_chart(
            labels=labels,
            values=values,
            title=_domain_title(catalog, dom_id),
            subtitle=detail_subtitle,
            stream_score=float(domain_scores.get(dom_id, 0)),
            verdict="",
            out_path=output_dir / fname,
            accent=accent,
        )
        written[fname] = str(output_dir / fname)

    configure_matplotlib()
    stream = report.get("streams", {}).get(stream_key, {})
    fig = plt.figure(figsize=(17, 7) if grid_cols == 2 else (17, 11))
    apply_void_gradient(fig, alpha_top=0.38)
    stream_score = stream.get("score")
    score_meta = (
        "Stream N/A on this branch — domain sub-scores preview"
        if stream.get("status") == "not_applicable"
        else f"Stream score {stream_score} / 10"
    )
    draw_brand_header(
        fig,
        title=breakdown_title,
        subtitle=breakdown_subtitle,
        verdict=str(stream.get("verdict", "")) if stream.get("verdict") != "N/A" else "",
        meta=score_meta,
        y=0.97,
    )

    n = len(domain_order)
    for idx, dom_id in enumerate(domain_order):
        row, col = divmod(idx, grid_cols)
        panel_w = 0.9 / grid_cols
        left = 0.05 + col * (panel_w + 0.02)
        bottom = 0.52 - row * 0.44 if grid_cols == 3 else 0.14
        height = 0.38 if grid_cols == 3 else 0.62
        ax = fig.add_axes([left, bottom, panel_w - 0.02, height], projection="polar")
        accent = DOMAIN_ACCENT.get(dom_id, PALETTE["biolume"])
        draw_panel_frame(ax, accent=accent)
        signals = signal_scores.get(dom_id, {})
        if signals:
            labels = [_signal_label(sid) for sid in signals]
            values = [float(v) for v in signals.values()]
            style_polar_axis(
                ax,
                labels=labels,
                values=values,
                accent=accent,
                title=_domain_title(catalog, dom_id),
                score_line=f"{float(domain_scores.get(dom_id, 0)):.1f}",
                label_fs=6.5 if n > 2 else 8,
                tick_fs=5.5 if n > 2 else 7,
            )
        else:
            ax.axis("off")

    breakdown_path = output_dir / breakdown_filename
    _save_fig(fig, breakdown_path)
    written[breakdown_filename] = str(breakdown_path)
    return written


def generate_spec_subdomain_radars(
    report: dict[str, Any], output_dir: Path, catalog: dict[str, Any] | None = None
) -> dict[str, str]:
    cat = catalog or _load_catalog()
    return _generate_subdomain_radars(
        report,
        output_dir,
        cat,
        domain_order=SPEC_DOMAIN_ORDER,
        stream_key="spec_readiness",
        filename_prefix="audit_radar_spec",
        breakdown_filename="audit_radar_spec_breakdown.png",
        breakdown_title="Spec Domain Breakdown",
        breakdown_subtitle="Six design axes · signal-level sub-radars",
        detail_subtitle="Signal breakdown · design stream",
        grid_cols=3,
    )


def generate_build_subdomain_radars(
    report: dict[str, Any], output_dir: Path, catalog: dict[str, Any] | None = None
) -> dict[str, str]:
    cat = catalog or _load_catalog()
    return _generate_subdomain_radars(
        report,
        output_dir,
        cat,
        domain_order=BUILD_DOMAIN_ORDER,
        stream_key="build_readiness",
        filename_prefix="audit_radar_build",
        breakdown_filename="audit_radar_build_breakdown.png",
        breakdown_title="Build Domain Breakdown",
        breakdown_subtitle="Runtime proof & Steam ship · signal-level sub-radars",
        detail_subtitle="Signal breakdown · build stream",
        grid_cols=2,
    )


def generate_audit_radars(
    report: dict[str, Any], output_dir: Path | None = None
) -> dict[str, str]:
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
            title="Design & Preparation",
            subtitle=spec.get("question", GAME_SUBTITLE),
            stream_score=float(spec.get("score") or 0),
            verdict=str(spec.get("verdict", "?")),
            out_path=spec_path,
            accent=PALETTE["biolume"],
        )
        written["audit_radar_spec.png"] = str(spec_path)

    build = streams.get("build_readiness", {})
    build_path = out_dir / "audit_radar_build.png"
    if build.get("status") == "not_applicable" or build.get("score") is None:
        _na_card(
            title="Development & Shipping",
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
                title="Development & Shipping",
                subtitle=build.get("question", ""),
                stream_score=float(build.get("score") or 0),
                verdict=str(build.get("verdict", "?")),
                out_path=build_path,
                accent=PALETTE["coral_gold"],
            )
    written["audit_radar_build.png"] = str(build_path)

    report_path = out_dir / "audit_radar_report.png"
    _combined_radar_report(report, report_path)
    written["audit_radar_report.png"] = str(report_path)

    written.update(generate_spec_subdomain_radars(report, out_dir))
    written.update(generate_build_subdomain_radars(report, out_dir))
    return written


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Generate themed Urashima audit radar PNGs")
    parser.add_argument(
        "--report",
        default=str(ROOT / "artifacts/alignment_audits/latest.json"),
        help="Audit report JSON path",
    )
    parser.add_argument(
        "--output-dir",
        default=str(DEFAULT_VISUALS_DIR),
        help="Output directory for radar PNGs",
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
