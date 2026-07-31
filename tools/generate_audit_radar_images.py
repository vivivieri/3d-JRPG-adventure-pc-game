#!/usr/bin/env python3
"""Generate spec/build radar PNGs from alignment audit report data.

Slide-quality presentation visuals — muted coastal palette
(docs/design/art/ART_DIRECTION.md). Includes exec summary card.

Authority: docs/ops/qa/ALIGNMENT_AUDIT.md
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
    draw_callout_card,
    draw_domain_bars,
    draw_na_panel,
    draw_panel_frame,
    style_polar_axis,
    wrap_label,
)

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_VISUALS_DIR = ROOT / "docs/archive/compliance/alignment_audit_visuals"
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

DPI = 200


def _domain_label(dom_id: str) -> str:
    return dom_id.replace("_", " ").title()


def _signal_label(sig_id: str) -> str:
    raw = sig_id.replace("_", " ")
    if raw.lower().startswith("l0 "):
        return "L0·" + raw[3:].title()
    return raw.title()


def _load_catalog() -> dict[str, Any]:
    return json.loads(CATALOG_PATH.read_text(encoding="utf-8"))


def _domain_title(catalog: dict[str, Any], dom_id: str) -> str:
    for row in catalog.get("domains", []):
        if row.get("id") == dom_id:
            return str(row.get("label", dom_id))
    return _domain_label(dom_id)


def _save_fig(fig: plt.Figure, out_path: Path) -> None:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(
        out_path,
        dpi=DPI,
        facecolor=PALETTE["void"],
        bbox_inches="tight",
        pad_inches=0.28,
    )
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
    figsize: tuple[float, float] = (10, 9),
    label_fs: float = 10,
) -> plt.Figure:
    configure_matplotlib()
    fig = plt.figure(figsize=figsize)
    apply_void_gradient(fig, alpha_top=0.28)
    draw_brand_header(
        fig,
        title=title,
        subtitle=subtitle or GAME_SUBTITLE,
        verdict=verdict,
        meta=f"Score {stream_score:.2f} / 10",
        y=0.95,
    )
    ax = fig.add_axes([0.12, 0.08, 0.76, 0.68], projection="polar")
    draw_panel_frame(ax, accent=accent)
    style_polar_axis(
        ax,
        labels=labels,
        values=values,
        accent=accent,
        title="",
        score_line=f"{stream_score:.1f}",
        label_fs=label_fs,
        callout_weak=True,
    )
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
    fig = plt.figure(figsize=(10, 9))
    apply_void_gradient(fig, alpha_top=0.26)
    meta = f"Branch · {_short_branch(branch)}"
    draw_brand_header(
        fig,
        title=title,
        subtitle="Development & shipping stream",
        verdict="N/A",
        meta=meta,
        y=0.96,
    )
    ax = fig.add_axes([0.1, 0.12, 0.8, 0.66])
    draw_na_panel(ax, title=title, reason=reason, branch=branch, accent=PALETTE["fog"])
    _save_fig(fig, out_path)


def _short_branch(branch: str, max_len: int = 36) -> str:
    b = str(branch or "?")
    if len(b) <= max_len:
        return b
    return b[: max_len - 1] + "…"


def _combined_radar_report(report: dict[str, Any], out_path: Path) -> None:
    configure_matplotlib()
    streams = report.get("streams", {})
    branch = report.get("branch", "?")
    verdict = str(report.get("verdict", "?"))
    spec = streams.get("spec_readiness", {})
    build = streams.get("build_readiness", {})
    gen_at = str(report.get("generated_at", ""))[:10]

    fig = plt.figure(figsize=(16, 9))
    apply_void_gradient(fig, alpha_top=0.26)
    draw_brand_header(
        fig,
        title="Alignment Radar Report",
        subtitle="Spec vs build · two-stream view",
        verdict=verdict,
        meta=f"{_short_branch(branch)} · {gen_at}",
        y=0.96,
    )

    # Stream labels sit above panels (not polar titles — avoids header collision)
    fig.text(
        0.26,
        0.78,
        "Design & Preparation",
        ha="center",
        fontsize=12,
        fontweight="bold",
        color=PALETTE["biolume"],
    )
    fig.text(
        0.74,
        0.78,
        "Development & Shipping",
        ha="center",
        fontsize=12,
        fontweight="bold",
        color=PALETTE["lantern"],
    )

    ax_spec = fig.add_axes([0.05, 0.08, 0.42, 0.64], projection="polar")
    draw_panel_frame(ax_spec, accent=PALETTE["biolume"])
    spec_domains = spec.get("domains") or {}
    if spec_domains:
        labels = [wrap_label(_domain_label(k), 11) for k in SPEC_DOMAIN_ORDER if k in spec_domains]
        values = [float(spec_domains[k]) for k in SPEC_DOMAIN_ORDER if k in spec_domains]
        style_polar_axis(
            ax_spec,
            labels=labels,
            values=values,
            accent=PALETTE["biolume"],
            title="",
            score_line=f"{float(spec.get('score') or 0):.1f}",
            label_fs=9,
            callout_weak=True,
        )

    if build.get("status") == "not_applicable" or build.get("score") is None:
        ax_build = fig.add_axes([0.55, 0.1, 0.4, 0.62])
        draw_na_panel(
            ax_build,
            title="Build stream",
            reason=str(build.get("na_reason") or "Not applicable on this branch"),
            branch=_short_branch(branch, 28),
            accent=PALETTE["lantern"],
        )
    else:
        ax_build = fig.add_axes([0.55, 0.08, 0.4, 0.64], projection="polar")
        draw_panel_frame(ax_build, accent=PALETTE["coral_gold"])
        build_domains = build.get("domains") or {}
        if build_domains:
            labels = [
                wrap_label(_domain_label(k), 11)
                for k in BUILD_DOMAIN_ORDER
                if k in build_domains
            ]
            values = [float(build_domains[k]) for k in BUILD_DOMAIN_ORDER if k in build_domains]
            style_polar_axis(
                ax_build,
                labels=labels,
                values=values,
                accent=PALETTE["coral_gold"],
                title="",
                score_line=f"{float(build.get('score') or 0):.1f}",
                label_fs=9,
                callout_weak=True,
            )

    _save_fig(fig, out_path)


def _pick_callouts(report: dict[str, Any]) -> list[tuple[str, str, str]]:
    """Three presentation callouts: strength, gap, next."""
    domain_scores = report.get("domain_scores") or {}
    signal_scores = report.get("signal_scores") or {}
    streams = report.get("streams") or {}
    build = streams.get("build_readiness") or {}

    # Strongest domain
    ranked = sorted(
        ((k, float(v)) for k, v in domain_scores.items() if k in SPEC_DOMAIN_ORDER),
        key=lambda kv: kv[1],
        reverse=True,
    )
    strongest = ranked[0] if ranked else ("data_alignment", 10.0)
    weakest = ranked[-1] if ranked else ("ux_controls", 0.0)

    # Weakest signal under weakest domain
    weak_signals = signal_scores.get(weakest[0]) or {}
    weak_sig = None
    if weak_signals:
        weak_sig = min(weak_signals.items(), key=lambda kv: float(kv[1]))

    strength_body = f"{_domain_label(strongest[0])} at {strongest[1]:.1f}/10 — design truth locked."
    if weak_sig:
        gap_body = (
            f"{_domain_label(weakest[0])} {weakest[1]:.1f}/10 — "
            f"softest signal {_signal_label(weak_sig[0])} ({float(weak_sig[1]):.1f})."
        )
    else:
        gap_body = f"{_domain_label(weakest[0])} is the softest axis at {weakest[1]:.1f}/10."

    if build.get("status") == "not_applicable" or build.get("score") is None:
        next_body = "Build stream awaits game/development — keep specs green, then prove runtime."
        next_accent = PALETTE["lantern"]
    else:
        next_body = (
            f"Build {float(build.get('score') or 0):.1f}/10 — "
            "close runtime/Steam gaps before ship."
        )
        next_accent = PALETTE["coral_gold"]

    return [
        ("Strength", strength_body, PALETTE["seaweed"]),
        ("Gap", gap_body, PALETTE["weak"]),
        ("Next", next_body, next_accent),
    ]


def _exec_summary(report: dict[str, Any], out_path: Path) -> None:
    """Widescreen exec slide: radar + domain bars + three callouts."""
    configure_matplotlib()
    streams = report.get("streams", {})
    branch = report.get("branch", "?")
    verdict = str(report.get("verdict", "?"))
    spec = streams.get("spec_readiness", {})
    build = streams.get("build_readiness", {})
    spec_domains = spec.get("domains") or {}
    domain_scores = report.get("domain_scores") or {}

    build_score = build.get("score")
    build_txt = (
        "N/A"
        if build.get("status") == "not_applicable" or build_score is None
        else f"{float(build_score):.2f}"
    )
    gen_at = str(report.get("generated_at", ""))[:10]
    meta = (
        f"Spec {float(spec.get('score') or 0):.2f}/10 · Build {build_txt}/10 · "
        f"{_short_branch(branch)} · {gen_at}"
    )

    fig = plt.figure(figsize=(16, 9))
    apply_void_gradient(fig, alpha_top=0.24)
    draw_brand_header(
        fig,
        title="Alignment Exec Summary",
        subtitle="Design readiness for dispatch",
        verdict=verdict,
        meta=meta,
        y=0.96,
    )

    # Left: hero radar
    ax_radar = fig.add_axes([0.04, 0.22, 0.38, 0.58], projection="polar")
    draw_panel_frame(ax_radar, accent=PALETTE["biolume"])
    if spec_domains:
        labels = [wrap_label(_domain_label(k), 11) for k in SPEC_DOMAIN_ORDER if k in spec_domains]
        values = [float(spec_domains[k]) for k in SPEC_DOMAIN_ORDER if k in spec_domains]
        style_polar_axis(
            ax_radar,
            labels=labels,
            values=values,
            accent=PALETTE["biolume"],
            title="",
            score_line=f"{float(spec.get('score') or 0):.1f}",
            label_fs=9,
            callout_weak=True,
        )

    # Right: domain bars
    ax_bars = fig.add_axes([0.48, 0.42, 0.48, 0.4])
    bar_labels = []
    bar_values = []
    bar_accents = []
    for dom_id in SPEC_DOMAIN_ORDER:
        if dom_id not in domain_scores and dom_id not in spec_domains:
            continue
        bar_labels.append(_domain_label(dom_id))
        bar_values.append(float(domain_scores.get(dom_id, spec_domains.get(dom_id, 0))))
        bar_accents.append(DOMAIN_ACCENT.get(dom_id, PALETTE["biolume"]))
    draw_domain_bars(ax_bars, labels=bar_labels, values=bar_values, accents=bar_accents)

    # Bottom: three callouts
    callouts = _pick_callouts(report)
    for i, (title, body, accent) in enumerate(callouts):
        ax_c = fig.add_axes([0.05 + i * 0.31, 0.04, 0.29, 0.16])
        draw_callout_card(ax_c, title=title, body=body, accent=accent)

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
    fig = plt.figure(figsize=(16, 9) if grid_cols == 2 else (16, 10))
    apply_void_gradient(fig, alpha_top=0.24)
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
        if grid_cols == 3:
            bottom = 0.48 - row * 0.40
            height = 0.30
            left = 0.04 + col * 0.32
            width = 0.28
        else:
            bottom = 0.08
            height = 0.62
            left = 0.05 + col * (panel_w + 0.02)
            width = panel_w - 0.02
        ax = fig.add_axes([left, bottom, width, height], projection="polar")
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
                title="",
                score_line=f"{float(domain_scores.get(dom_id, 0)):.1f}",
                label_fs=6 if n > 2 else 9,
                tick_fs=5 if n > 2 else 8,
                callout_weak=False,
            )
            # Domain name below panel (avoids colliding with brand header)
            fig.text(
                left + width / 2,
                bottom - 0.022,
                _domain_title(catalog, dom_id),
                ha="center",
                va="top",
                fontsize=9,
                fontweight="bold",
                color=accent,
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
        breakdown_subtitle="Six design axes · signal-level detail",
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
        breakdown_subtitle="Runtime proof & Steam ship",
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

    # Exec summary first — primary presentation slide
    exec_path = out_dir / "audit_exec_summary.png"
    _exec_summary(report, exec_path)
    written["audit_exec_summary.png"] = str(exec_path)

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
    parser = argparse.ArgumentParser(description="Generate slide-quality Urashima audit radar PNGs")
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
