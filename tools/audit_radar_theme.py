"""Tides of Urashima — audit radar visual theme.

Palette authority: docs/art/ART_DIRECTION.md §1, docs/art/RENDERING_GUIDE.md
"""
from __future__ import annotations

import textwrap
from typing import Any

import matplotlib.pyplot as plt
import numpy as np
from matplotlib import patheffects as pe
from matplotlib.figure import Figure
from matplotlib.patches import FancyBboxPatch, Rectangle
from matplotlib.axes import Axes

# Hub + caves + palace void — muted coastal JRPG (not bright anime)
PALETTE = {
    "void": "#1A1A3A",
    "deep_teal": "#1A4A5A",
    "panel": "#242B3A",
    "panel_edge": "#3A4556",
    "fog": "#8B9DAF",
    "wood": "#5C4A3A",
    "sand": "#C9B89A",
    "seaweed": "#3D5C4A",
    "biolume": "#4AE8D8",
    "lantern": "#D4A880",
    "coral_gold": "#D4A55A",
    "crimson": "#8B2A3A",
    "ethereal": "#E8E4DC",
    "muted": "#8B9DAF",
}

DOMAIN_ACCENT = {
    "data_alignment": PALETTE["fog"],
    "narrative": PALETTE["lantern"],
    "gameplay": PALETTE["crimson"],
    "visual_spec": PALETTE["biolume"],
    "ux_controls": PALETTE["sand"],
    "pm_workflow": PALETTE["seaweed"],
}

VERDICT_COLORS = {
    "ALIGNED": PALETTE["seaweed"],
    "AT_RISK": PALETTE["lantern"],
    "AT-RISK": PALETTE["lantern"],
    "FAIL": PALETTE["crimson"],
    "N/A": PALETTE["fog"],
}

GAME_TITLE = "Tides of Urashima"
GAME_SUBTITLE = "Coastal alignment · muted tide readiness"


def configure_matplotlib() -> None:
    plt.rcParams.update(
        {
            "font.family": "serif",
            "font.serif": ["DejaVu Serif", "Noto Serif", "Times New Roman", "serif"],
            "axes.edgecolor": PALETTE["panel_edge"],
            "axes.labelcolor": PALETTE["ethereal"],
            "text.color": PALETTE["ethereal"],
            "figure.facecolor": PALETTE["void"],
            "savefig.facecolor": PALETTE["void"],
        }
    )


def wrap_label(text: str, width: int = 11) -> str:
    return textwrap.fill(text, width=width, break_long_words=False)


def verdict_color(verdict: str) -> str:
    return VERDICT_COLORS.get(str(verdict).upper().replace("_", "-"), PALETTE["fog"])


def apply_void_gradient(fig: Figure, *, alpha_top: float = 0.35) -> None:
    """Coastal fog wash over void sky — subtle vertical gradient."""
    grad = np.linspace(0, 1, 256).reshape(256, 1)
    cmap = plt.matplotlib.colors.LinearSegmentedColormap.from_list(
        "urashima_fog",
        [(PALETTE["void"], 0.0), (PALETTE["deep_teal"], 0.45), (PALETTE["fog"], 1.0)],
    )
    ax_bg = fig.add_axes([0, 0, 1, 1], zorder=-10)
    ax_bg.imshow(
        grad,
        aspect="auto",
        cmap=cmap,
        alpha=alpha_top,
        extent=[0, 1, 0, 1],
        transform=fig.transFigure,
    )
    ax_bg.axis("off")


def draw_brand_header(
    fig: Figure,
    *,
    title: str,
    subtitle: str = "",
    verdict: str = "",
    meta: str = "",
    y: float = 0.96,
) -> None:
    fig.text(
        0.5,
        y,
        GAME_TITLE,
        ha="center",
        va="top",
        fontsize=11,
        color=PALETTE["fog"],
        fontstyle="italic",
        alpha=0.9,
    )
    fig.text(
        0.5,
        y - 0.045,
        title,
        ha="center",
        va="top",
        fontsize=17,
        fontweight="bold",
        color=PALETTE["ethereal"],
    )
    # Ink-wash rule
    fig.add_artist(
        Rectangle(
            (0.18, y - 0.055),
            0.64,
            0.004,
            transform=fig.transFigure,
            facecolor=PALETTE["wood"],
            alpha=0.65,
            zorder=5,
        )
    )
    if subtitle:
        fig.text(
            0.5,
            y - 0.075,
            subtitle,
            ha="center",
            va="top",
            fontsize=9,
            color=PALETTE["muted"],
        )
    if meta:
        fig.text(
            0.5,
            y - 0.095 if subtitle else y - 0.075,
            meta,
            ha="center",
            va="top",
            fontsize=8,
            color=PALETTE["sand"],
            alpha=0.85,
        )
    if verdict:
        badge_color = verdict_color(verdict)
        fig.text(
            0.92,
            y - 0.02,
            verdict.replace("_", " "),
            ha="right",
            va="top",
            fontsize=9,
            fontweight="bold",
            color=badge_color,
            bbox={
                "boxstyle": "round,pad=0.35",
                "facecolor": PALETTE["panel"],
                "edgecolor": badge_color,
                "linewidth": 1.2,
                "alpha": 0.95,
            },
        )


def draw_panel_frame(ax: Axes, *, accent: str | None = None) -> None:
    """Card frame behind polar plot."""
    accent = accent or PALETTE["biolume"]
    frame = FancyBboxPatch(
        (-0.08, -0.08),
        1.16,
        1.16,
        boxstyle="round,pad=0.02,rounding_size=0.04",
        transform=ax.transAxes,
        facecolor=PALETTE["panel"],
        edgecolor=accent,
        linewidth=1.4,
        alpha=0.55,
        zorder=-1,
    )
    ax.add_patch(frame)


def style_polar_axis(
    ax: Axes,
    *,
    labels: list[str],
    values: list[float],
    accent: str,
    title: str = "",
    score_line: str = "",
    label_fs: float = 8,
    tick_fs: float = 7,
) -> None:
    n = len(labels)
    angles = np.linspace(0, 2 * np.pi, n, endpoint=False).tolist()
    values_loop = values + values[:1]
    angles_loop = angles + angles[:1]

    ax.set_theta_offset(np.pi / 2)
    ax.set_theta_direction(-1)
    ax.set_facecolor((0, 0, 0, 0))

    # Stepped fog rings (toon-like bands)
    for r in [2, 4, 6, 8, 10]:
        ring = [r] * (n + 1)
        ax.plot(
            angles_loop,
            ring,
            color=PALETTE["panel_edge"],
            linewidth=0.6,
            alpha=0.35,
            linestyle="-",
        )

    # Score fill + stroke
    ax.fill(angles_loop, values_loop, color=accent, alpha=0.28)
    line = ax.plot(
        angles_loop,
        values_loop,
        color=accent,
        linewidth=2.4,
        solid_capstyle="round",
        zorder=4,
    )[0]
    line.set_path_effects([pe.withStroke(linewidth=4.2, foreground=PALETTE["void"], alpha=0.35)])

    target_loop = [10.0] * (n + 1)
    ax.plot(
        angles_loop,
        target_loop,
        color=PALETTE["coral_gold"],
        linewidth=1.3,
        linestyle=(0, (4, 3)),
        alpha=0.75,
        zorder=3,
    )

    wrapped = [wrap_label(lb, width=10 if n > 5 else 12) for lb in labels]
    ax.set_xticks(angles)
    ax.set_xticklabels(wrapped, color=PALETTE["ethereal"], fontsize=label_fs)
    for tick in ax.get_xticklabels():
        tick.set_path_effects([pe.withStroke(linewidth=2, foreground=PALETTE["void"])])

    ax.set_ylim(0, 10.5)
    ax.set_yticks([2, 4, 6, 8, 10])
    ax.set_yticklabels(["2", "4", "6", "8", "10"], color=PALETTE["muted"], fontsize=tick_fs)
    ax.grid(color=PALETTE["panel_edge"], alpha=0.2, linewidth=0.5)
    ax.spines["polar"].set_color(PALETTE["wood"])
    ax.spines["polar"].set_linewidth(1.2)

    if title:
        ax.set_title(
            title,
            color=PALETTE["ethereal"],
            fontsize=11,
            fontweight="bold",
            pad=18,
        )
    if score_line:
        ax.text(
            0.5,
            0.5,
            score_line,
            transform=ax.transAxes,
            ha="center",
            va="center",
            fontsize=13,
            fontweight="bold",
            color=accent,
            bbox={
                "boxstyle": "circle,pad=0.35",
                "facecolor": PALETTE["void"],
                "edgecolor": accent,
                "alpha": 0.88,
                "linewidth": 1.2,
            },
            zorder=6,
        )


def draw_na_panel(
    ax: Axes,
    *,
    title: str,
    reason: str,
    branch: str,
    accent: str = PALETTE["fog"],
) -> None:
    ax.set_facecolor((0, 0, 0, 0))
    ax.axis("off")
    frame = FancyBboxPatch(
        (0.06, 0.08),
        0.88,
        0.84,
        boxstyle="round,pad=0.03,rounding_size=0.05",
        transform=ax.transAxes,
        facecolor=PALETTE["panel"],
        edgecolor=accent,
        linewidth=1.6,
        alpha=0.7,
    )
    ax.add_patch(frame)
    # Torii-inspired top bar
    ax.plot([0.22, 0.78], [0.82, 0.82], color=PALETTE["wood"], linewidth=3.2, transform=ax.transAxes)
    ax.plot([0.28, 0.28], [0.72, 0.82], color=PALETTE["wood"], linewidth=2.4, transform=ax.transAxes)
    ax.plot([0.72, 0.72], [0.72, 0.82], color=PALETTE["wood"], linewidth=2.4, transform=ax.transAxes)

    ax.text(
        0.5,
        0.66,
        title,
        ha="center",
        va="center",
        color=PALETTE["ethereal"],
        fontsize=13,
        fontweight="bold",
        transform=ax.transAxes,
    )
    ax.text(
        0.5,
        0.48,
        "—",
        ha="center",
        va="center",
        color=accent,
        fontsize=42,
        fontweight="light",
        transform=ax.transAxes,
        alpha=0.9,
    )
    ax.text(
        0.5,
        0.36,
        "AWAITING TIDE",
        ha="center",
        va="center",
        color=PALETTE["muted"],
        fontsize=10,
        fontstyle="italic",
        transform=ax.transAxes,
    )
    ax.text(
        0.5,
        0.26,
        f"Branch · {branch}",
        ha="center",
        va="center",
        color=PALETTE["biolume"],
        fontsize=9,
        transform=ax.transAxes,
    )
    wrapped = wrap_label(reason, width=42)
    ax.text(
        0.5,
        0.14,
        wrapped,
        ha="center",
        va="center",
        color=PALETTE["sand"],
        fontsize=8,
        transform=ax.transAxes,
        alpha=0.9,
    )
