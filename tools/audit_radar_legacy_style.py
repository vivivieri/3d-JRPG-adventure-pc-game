"""Legacy audit radar presentation — matches GameLab-era stakeholder art.

Reference frames (committed):
  - tides_audit_radar_updated.png — hero spec radar layout
  - audit_radar_6axis.png — 6-domain gold-icon radar
  - tides_audit_alignment_radar.png — sub-domain signal radar
"""
from __future__ import annotations

from pathlib import Path
from typing import Any

import matplotlib.pyplot as plt
import numpy as np
from matplotlib import patheffects as pe
from matplotlib.figure import Figure
from matplotlib.patches import Circle, FancyBboxPatch, Rectangle
from matplotlib.axes import Axes
from PIL import Image

from audit_radar_theme import PALETTE, configure_matplotlib, verdict_color, wrap_label

ROOT = Path(__file__).resolve().parents[1]
VISUALS_DIR = ROOT / "docs/compliance/alignment_audit_visuals"

LEGACY_REFERENCES = {
    "hero_bg": VISUALS_DIR / "tides_audit_radar_updated.png",
    "six_axis_bg": VISUALS_DIR / "audit_radar_6axis.png",
    "subdomain_ref": VISUALS_DIR / "tides_audit_alignment_radar.png",
    "mega_ref": VISUALS_DIR / "tides_mega_dashboard_all_radars.png",
}

# Single-letter glyphs in gold discs (DejaVu-safe; legacy art uses illustrated icons)
DOMAIN_GLYPH = {
    "data_alignment": "D",
    "narrative": "N",
    "gameplay": "G",
    "visual_spec": "V",
    "ux_controls": "U",
    "pm_workflow": "P",
    "runtime_proof": "R",
    "steam_ship": "S",
}

DOMAIN_LABEL_CAPS = {
    "data_alignment": "DATA ALIGNMENT",
    "narrative": "NARRATIVE",
    "gameplay": "GAMEPLAY",
    "visual_spec": "VISUAL SPEC",
    "ux_controls": "UX & CONTROLS",
    "pm_workflow": "PM WORKFLOW",
    "runtime_proof": "RUNTIME PROOF",
    "steam_ship": "STEAM SHIP",
}


def _domain_caps(dom_id: str) -> str:
    return DOMAIN_LABEL_CAPS.get(dom_id, dom_id.replace("_", " ").upper())


def apply_legacy_watermark(fig: Figure, image_path: Path, *, alpha: float = 0.16) -> None:
    if not image_path.is_file():
        return
    img = Image.open(image_path).convert("RGBA")
    dpi = fig.dpi
    w = int(fig.get_figwidth() * dpi)
    h = int(fig.get_figheight() * dpi)
    img = img.resize((w, h), Image.Resampling.LANCZOS)
    arr = np.asarray(img).astype(float) / 255.0
    ax_bg = fig.add_axes([0, 0, 1, 1], zorder=-30)
    ax_bg.imshow(arr, aspect="auto", extent=[0, 1, 0, 1], transform=fig.transFigure, alpha=alpha)
    ax_bg.axis("off")


def draw_gold_frame(fig: Figure, *, inset: float = 0.03) -> None:
    """Ornate double-line border like legacy dashboards."""
    for pad, lw, alpha in ((inset, 2.2, 0.95), (inset + 0.012, 0.8, 0.45)):
        rect = Rectangle(
            (pad, pad),
            1 - 2 * pad,
            1 - 2 * pad,
            transform=fig.transFigure,
            fill=False,
            edgecolor=PALETTE["coral_gold"],
            linewidth=lw,
            alpha=alpha,
            zorder=20,
        )
        fig.add_artist(rect)
    # Corner flourishes
    corners = [(inset, inset), (1 - inset, inset), (inset, 1 - inset), (1 - inset, 1 - inset)]
    for x, y in corners:
        fig.add_artist(
            Circle(
                (x, y),
                0.012,
                transform=fig.transFigure,
                facecolor=PALETTE["coral_gold"],
                edgecolor="none",
                alpha=0.85,
                zorder=21,
            )
        )


def draw_legacy_title_block(
    fig: Figure,
    *,
    eyebrow: str = "TIDES OF URASHIMA",
    title: str = "PROJECT AUDIT",
    subtitle: str = "",
    meta: str = "",
    verdict: str = "",
) -> None:
    fig.text(
        0.07,
        0.93,
        eyebrow,
        ha="left",
        va="top",
        fontsize=22,
        fontweight="bold",
        color=PALETTE["coral_gold"],
        family="serif",
    )
    fig.text(
        0.07,
        0.885,
        title,
        ha="left",
        va="top",
        fontsize=13,
        fontweight="bold",
        color=PALETTE["biolume"],
        family="sans-serif",
    )
    fig.add_artist(
        Rectangle((0.07, 0.868), 0.28, 0.003, transform=fig.transFigure, color=PALETTE["coral_gold"], zorder=5)
    )
    if subtitle:
        fig.text(0.07, 0.845, subtitle, ha="left", va="top", fontsize=9, color=PALETTE["ethereal"], style="italic")
    if meta:
        fig.text(0.07, 0.822, meta, ha="left", va="top", fontsize=8, color=PALETTE["muted"])
    if verdict:
        vc = verdict_color(verdict)
        fig.text(
            0.93,
            0.93,
            verdict.replace("_", " "),
            ha="right",
            va="top",
            fontsize=11,
            fontweight="bold",
            color=vc,
            bbox={
                "boxstyle": "round,pad=0.4",
                "facecolor": (0.1, 0.12, 0.2, 0.85),
                "edgecolor": vc,
                "linewidth": 1.5,
            },
        )


def draw_scale_legend(fig: Figure, *, x: float = 0.07, y: float = 0.12) -> None:
    box = FancyBboxPatch(
        (x, y),
        0.22,
        0.14,
        boxstyle="round,pad=0.012,rounding_size=0.01",
        transform=fig.transFigure,
        facecolor=(0.08, 0.1, 0.16, 0.82),
        edgecolor=PALETTE["coral_gold"],
        linewidth=1.6,
        zorder=25,
    )
    fig.add_artist(box)
    fig.text(x + 0.02, y + 0.115, "SCALE", fontsize=9, fontweight="bold", color=PALETTE["coral_gold"], transform=fig.transFigure)
    for i, line in enumerate(
        [
            "0 = Not started / not proven",
            "5 = In progress / partial",
            "10 = Complete / locked",
        ]
    ):
        fig.text(
            x + 0.02,
            y + 0.085 - i * 0.028,
            line,
            fontsize=7,
            color=PALETTE["ethereal"],
            transform=fig.transFigure,
        )


def style_polar_legacy(
    ax: Axes,
    *,
    labels: list[str],
    values: list[float],
    domain_ids: list[str] | None = None,
    glyphs: list[str] | None = None,
    title: str = "",
    show_scale: bool = False,
    label_radius: float = 11.8,
    score_radius: float = 10.6,
) -> None:
    """Legacy GameLab-style polar: teal polygon, gold icons, scores on axes."""
    n = len(labels)
    domain_ids = domain_ids or [""] * n
    glyphs = glyphs or [DOMAIN_GLYPH.get(d, "●") for d in domain_ids]
    angles = np.linspace(0, 2 * np.pi, n, endpoint=False)
    values_loop = np.concatenate([values, values[:1]])
    angles_loop = np.concatenate([angles, angles[:1]])

    ax.set_theta_offset(np.pi / 2)
    ax.set_theta_direction(-1)
    ax.set_facecolor((0, 0, 0, 0))

    for r in [2, 4, 6, 8, 10]:
        ax.plot(
            np.concatenate([angles, angles[:1]]),
            [r] * (n + 1),
            color=PALETTE["biolume"],
            linewidth=0.55,
            alpha=0.22,
        )

    ax.fill(angles_loop, values_loop, color=PALETTE["biolume"], alpha=0.38)
    line = ax.plot(angles_loop, values_loop, color=PALETTE["biolume"], linewidth=2.8, zorder=5)[0]
    line.set_path_effects(
        [pe.withStroke(linewidth=5.5, foreground=PALETTE["biolume"], alpha=0.35), pe.Normal()]
    )

    for ang, val in zip(angles, values, strict=False):
        ax.scatter([ang], [val], s=55, color=PALETTE["biolume"], edgecolors=PALETTE["ethereal"], linewidths=1.2, zorder=6)

    ax.set_ylim(0, 12.5)
    ax.set_yticks([2, 4, 6, 8, 10])
    ax.set_yticklabels(["2", "4", "6", "8", "10"], color=PALETTE["muted"], fontsize=7)
    ax.set_xticks([])
    ax.grid(False)
    ax.spines["polar"].set_visible(False)

    for ang, label, val, dom_id, glyph in zip(angles, labels, values, domain_ids, glyphs, strict=False):
        # Gold icon disc
        ix = ang
        ax.scatter(
            [ix],
            [label_radius - 0.6],
            s=420,
            color=PALETTE["coral_gold"],
            alpha=0.92,
            zorder=7,
            transform=ax.transData,
        )
        ax.text(
            ix,
            label_radius - 0.6,
            glyph,
            ha="center",
            va="center",
            fontsize=11,
            color=PALETTE["void"],
            fontweight="bold",
            zorder=8,
        )
        caps = _domain_caps(dom_id) if dom_id else wrap_label(label, 14).upper()
        label_txt = caps if dom_id and len(domain_ids) == len(set(domain_ids)) else wrap_label(label, 12).upper()
        ax.text(
            ix,
            label_radius - 1.35,
            label_txt,
            ha="center",
            va="center",
            fontsize=7.5 if n <= 6 else 6.5,
            color=PALETTE["ethereal"],
            fontweight="bold",
            zorder=8,
        )
        ax.text(
            ix,
            score_radius,
            f"{val:.1f}",
            ha="center",
            va="center",
            fontsize=13 if n <= 6 else 10,
            fontweight="bold",
            color=PALETTE["coral_gold"],
            zorder=8,
        )

    if title:
        ax.set_title(title, color=PALETTE["biolume"], fontsize=14, fontweight="bold", pad=28, y=1.08)

    if show_scale:
        pass  # scale drawn at figure level via draw_scale_legend


def render_legacy_hero_radar(
    *,
    domain_ids: list[str],
    values: list[float],
    title: str,
    subtitle: str,
    stream_score: float,
    verdict: str,
    meta: str,
    out_path: Path,
    background: Path | None = None,
) -> None:
    configure_matplotlib()
    fig = plt.figure(figsize=(12, 12))
    fig.patch.set_facecolor(PALETTE["void"])
    apply_legacy_watermark(fig, background or LEGACY_REFERENCES["hero_bg"], alpha=0.14)
    draw_gold_frame(fig)
    draw_legacy_title_block(
        fig,
        title=title,
        subtitle=subtitle,
        meta=meta,
        verdict=verdict,
    )
    draw_scale_legend(fig)
    fig.text(
        0.5,
        0.06,
        f"Stream score {stream_score:.2f} / 10",
        ha="center",
        fontsize=10,
        color=PALETTE["sand"],
    )

    ax = fig.add_axes([0.12, 0.16, 0.76, 0.68], projection="polar")
    labels = [_domain_caps(d) for d in domain_ids]
    style_polar_legacy(
        ax,
        labels=labels,
        values=values,
        domain_ids=domain_ids,
        title="",
        show_scale=True,
    )
    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_path, dpi=200, facecolor=PALETTE["void"], bbox_inches="tight", pad_inches=0.2)
    plt.close(fig)


def render_legacy_subdomain_radar(
    *,
    domain_id: str,
    signal_ids: list[str],
    values: list[float],
    domain_score: float,
    title: str,
    out_path: Path,
) -> None:
    configure_matplotlib()
    fig = plt.figure(figsize=(10, 10))
    fig.patch.set_facecolor(PALETTE["void"])
    apply_legacy_watermark(fig, LEGACY_REFERENCES["subdomain_ref"], alpha=0.12)
    draw_gold_frame(fig, inset=0.04)
    draw_legacy_title_block(fig, title=title.upper(), subtitle="Signal breakdown", meta=f"{domain_score:.1f} / 10")
    draw_scale_legend(fig, x=0.06, y=0.1)

    ax = fig.add_axes([0.1, 0.14, 0.8, 0.7], projection="polar")
    labels = [s.replace("_", " ").upper() for s in signal_ids]
    sig_glyphs = [s[0].upper() if s else "•" for s in signal_ids]
    style_polar_legacy(
        ax,
        labels=labels,
        values=values,
        domain_ids=[""] * len(labels),
        glyphs=sig_glyphs,
        title="",
    )
    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_path, dpi=200, facecolor=PALETTE["void"], bbox_inches="tight", pad_inches=0.18)
    plt.close(fig)


def render_legacy_breakdown_grid(
    report: dict[str, Any],
    catalog_domains: dict[str, str],
    spec_domain_order: list[str],
    out_path: Path,
) -> None:
    signal_scores = report.get("signal_scores", {})
    domain_scores = report.get("domain_scores", {})
    spec = report.get("streams", {}).get("spec_readiness", {})

    configure_matplotlib()
    fig = plt.figure(figsize=(18, 11))
    fig.patch.set_facecolor(PALETTE["void"])
    apply_legacy_watermark(fig, LEGACY_REFERENCES["six_axis_bg"], alpha=0.1)
    draw_gold_frame(fig, inset=0.02)
    draw_legacy_title_block(
        fig,
        title="SPEC DOMAIN BREAKDOWN",
        subtitle="Six design axes · signal-level sub-radars",
        meta=f"Stream {spec.get('score', '?')} / 10",
        verdict=str(spec.get("verdict", "")),
    )

    for idx, dom_id in enumerate(spec_domain_order):
        row, col = divmod(idx, 3)
        left = 0.06 + col * 0.31
        bottom = 0.52 - row * 0.44
        ax = fig.add_axes([left, bottom, 0.27, 0.38], projection="polar")
        signals = signal_scores.get(dom_id, {})
        if not signals:
            ax.axis("off")
            continue
        sids = list(signals.keys())
        vals = [float(v) for v in signals.values()]
        title = catalog_domains.get(dom_id, dom_id)
        sig_glyphs = [g[0].upper() if g else "•" for g in sids]
        style_polar_legacy(
            ax,
            labels=[s.replace("_", " ") for s in sids],
            values=vals,
            domain_ids=[""] * len(sids),
            glyphs=sig_glyphs,
            title=title,
            label_radius=11.2,
            score_radius=9.8,
        )

    fig.text(
        0.5,
        0.03,
        "Reference style: legacy stakeholder radars (tides_audit_radar_updated · audit_radar_6axis)",
        ha="center",
        fontsize=7,
        color=PALETTE["muted"],
        style="italic",
    )
    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_path, dpi=200, facecolor=PALETTE["void"], bbox_inches="tight", pad_inches=0.15)
    plt.close(fig)


def render_legacy_combined_report(report: dict[str, Any], out_path: Path) -> None:
    streams = report.get("streams", {})
    spec = streams.get("spec_readiness", {})
    build = streams.get("build_readiness", {})
    branch = report.get("branch", "?")
    verdict = str(report.get("verdict", "?"))

    configure_matplotlib()
    fig = plt.figure(figsize=(16, 9))
    fig.patch.set_facecolor(PALETTE["void"])
    apply_legacy_watermark(fig, LEGACY_REFERENCES["mega_ref"], alpha=0.08)
    draw_gold_frame(fig)
    draw_legacy_title_block(
        fig,
        title="ALIGNMENT RADAR REPORT",
        subtitle="Design & preparation · development & shipping",
        meta=f"{branch} · {report.get('generated_at', '')}",
        verdict=verdict,
    )

    ax_spec = fig.add_axes([0.06, 0.12, 0.42, 0.72], projection="polar")
    spec_domains = spec.get("domains") or {}
    if spec_domains:
        dom_ids = list(spec_domains.keys())
        vals = [float(v) for v in spec_domains.values()]
        style_polar_legacy(
            ax_spec,
            labels=[_domain_caps(d) for d in dom_ids],
            values=vals,
            domain_ids=dom_ids,
            title="Design & Preparation",
        )

    if build.get("status") == "not_applicable" or build.get("score") is None:
        ax_na = fig.add_axes([0.54, 0.18, 0.4, 0.6])
        ax_na.axis("off")
        frame = FancyBboxPatch(
            (0.05, 0.05),
            0.9,
            0.9,
            boxstyle="round,pad=0.02",
            transform=ax_na.transAxes,
            facecolor=(0.08, 0.1, 0.16, 0.75),
            edgecolor=PALETTE["coral_gold"],
            linewidth=1.8,
        )
        ax_na.add_patch(frame)
        ax_na.text(0.5, 0.65, "DEVELOPMENT & SHIPPING", ha="center", fontsize=14, fontweight="bold", color=PALETTE["coral_gold"], transform=ax_na.transAxes)
        ax_na.text(0.5, 0.45, "AWAITING TIDE", ha="center", fontsize=20, color=PALETTE["muted"], transform=ax_na.transAxes)
        ax_na.text(0.5, 0.28, str(build.get("na_reason", "")), ha="center", fontsize=8, color=PALETTE["sand"], transform=ax_na.transAxes, wrap=True)
    else:
        ax_build = fig.add_axes([0.54, 0.12, 0.42, 0.72], projection="polar")
        build_domains = build.get("domains") or {}
        if build_domains:
            dom_ids = list(build_domains.keys())
            vals = [float(v) for v in build_domains.values()]
            style_polar_legacy(
                ax_build,
                labels=[_domain_caps(d) for d in dom_ids],
                values=vals,
                domain_ids=dom_ids,
                title="Development & Shipping",
            )

    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_path, dpi=200, facecolor=PALETTE["void"], bbox_inches="tight", pad_inches=0.15)
    plt.close(fig)
