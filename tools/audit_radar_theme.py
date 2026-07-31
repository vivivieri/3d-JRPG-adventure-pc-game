"""Tides of Urashima — audit radar visual theme (slide / presentation quality).

Palette authority: docs/design/art/ART_DIRECTION.md §1, docs/design/art/RENDERING_GUIDE.md
Presentation goal: readable on projector — sans-serif, high contrast, less ornament.
"""
from __future__ import annotations

import textwrap

import matplotlib.pyplot as plt
import numpy as np
from matplotlib import patheffects as pe
from matplotlib.axes import Axes
from matplotlib.figure import Figure
from matplotlib.patches import Circle, FancyBboxPatch

# Hub + caves + palace void — muted coastal JRPG (not bright anime)
PALETTE = {
    "void": "#12182A",
    "deep_teal": "#1A3A4A",
    "panel": "#1E2636",
    "panel_edge": "#4A5568",
    "fog": "#A8B8C8",
    "wood": "#6B5748",
    "sand": "#D4C4A8",
    "seaweed": "#4A7A5C",
    "biolume": "#4AE8D8",
    "lantern": "#E0B890",
    "coral_gold": "#E0B86A",
    "crimson": "#C04858",
    "ethereal": "#F2F0EA",
    "muted": "#9AABBC",
    "weak": "#E8A060",
}

DOMAIN_ACCENT = {
    "data_alignment": PALETTE["fog"],
    "narrative": PALETTE["lantern"],
    "gameplay": PALETTE["crimson"],
    "visual_spec": PALETTE["biolume"],
    "ux_controls": PALETTE["sand"],
    "pm_workflow": PALETTE["seaweed"],
    "runtime_proof": PALETTE["biolume"],
    "steam_ship": PALETTE["coral_gold"],
}

VERDICT_COLORS = {
    "ALIGNED": "#5CB87A",
    "AT_RISK": PALETTE["lantern"],
    "AT-RISK": PALETTE["lantern"],
    "FAIL": PALETTE["crimson"],
    "N/A": PALETTE["fog"],
}

GAME_TITLE = "Tides of Urashima"
GAME_SUBTITLE = "Alignment status"


def configure_matplotlib() -> None:
    plt.rcParams.update(
        {
            "font.family": "sans-serif",
            "font.sans-serif": [
                "DejaVu Sans",
                "Noto Sans",
                "Liberation Sans",
                "Arial",
                "sans-serif",
            ],
            "axes.edgecolor": PALETTE["panel_edge"],
            "axes.labelcolor": PALETTE["ethereal"],
            "text.color": PALETTE["ethereal"],
            "figure.facecolor": PALETTE["void"],
            "savefig.facecolor": PALETTE["void"],
        }
    )


def wrap_label(text: str, width: int = 12) -> str:
    return textwrap.fill(text, width=width, break_long_words=False)


def verdict_color(verdict: str) -> str:
    return VERDICT_COLORS.get(str(verdict).upper().replace("_", "-"), PALETTE["fog"])


def apply_void_gradient(fig: Figure, *, alpha_top: float = 0.22) -> None:
    """Subtle depth wash — keep slides readable (not heavy fog)."""
    grad = np.linspace(0, 1, 256).reshape(256, 1)
    cmap = plt.matplotlib.colors.LinearSegmentedColormap.from_list(
        "urashima_slide",
        [(PALETTE["void"], 0.0), (PALETTE["deep_teal"], 0.55), (PALETTE["panel"], 1.0)],
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
    y: float = 0.94,
) -> None:
    fig.text(
        0.06,
        y,
        GAME_TITLE.upper(),
        ha="left",
        va="top",
        fontsize=10,
        color=PALETTE["biolume"],
        fontweight="bold",
    )
    fig.text(
        0.06,
        y - 0.038,
        title,
        ha="left",
        va="top",
        fontsize=20,
        fontweight="bold",
        color=PALETTE["ethereal"],
    )
    if subtitle:
        fig.text(
            0.06,
            y - 0.072,
            subtitle,
            ha="left",
            va="top",
            fontsize=11,
            color=PALETTE["muted"],
        )
    if meta:
        fig.text(
            0.06,
            y - 0.098 if subtitle else y - 0.072,
            meta,
            ha="left",
            va="top",
            fontsize=10,
            color=PALETTE["sand"],
        )
    if verdict:
        badge_color = verdict_color(verdict)
        fig.text(
            0.94,
            y - 0.01,
            verdict.replace("_", " ").upper(),
            ha="right",
            va="top",
            fontsize=11,
            fontweight="bold",
            color=PALETTE["ethereal"],
            bbox={
                "boxstyle": "round,pad=0.45",
                "facecolor": badge_color,
                "edgecolor": "none",
                "alpha": 0.95,
            },
        )


def draw_panel_frame(ax: Axes, *, accent: str | None = None) -> None:
    """Soft card behind polar plot — minimal chrome."""
    accent = accent or PALETTE["biolume"]
    frame = FancyBboxPatch(
        (-0.06, -0.06),
        1.12,
        1.12,
        boxstyle="round,pad=0.02,rounding_size=0.03",
        transform=ax.transAxes,
        facecolor=PALETTE["panel"],
        edgecolor=accent,
        linewidth=1.0,
        alpha=0.45,
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
    label_fs: float = 10,
    tick_fs: float = 8,
    callout_weak: bool = True,
    weak_threshold: float = 9.5,
) -> None:
    n = len(labels)
    angles = np.linspace(0, 2 * np.pi, n, endpoint=False).tolist()
    values_loop = values + values[:1]
    angles_loop = angles + angles[:1]

    ax.set_theta_offset(np.pi / 2)
    ax.set_theta_direction(-1)
    ax.set_facecolor((0, 0, 0, 0))

    for r in [2, 4, 6, 8, 10]:
        ring = [r] * (n + 1)
        ax.plot(
            angles_loop,
            ring,
            color=PALETTE["panel_edge"],
            linewidth=0.8 if r < 10 else 1.2,
            alpha=0.45 if r < 10 else 0.65,
            linestyle="-",
        )

    ax.fill(angles_loop, values_loop, color=accent, alpha=0.32)
    line = ax.plot(
        angles_loop,
        values_loop,
        color=accent,
        linewidth=2.8,
        solid_capstyle="round",
        zorder=4,
    )[0]
    line.set_path_effects(
        [pe.withStroke(linewidth=5.0, foreground=PALETTE["void"], alpha=0.4)]
    )

    # Soft target ring (ceiling) — not a competing dashed triangle
    ax.plot(
        angles_loop,
        [10.0] * (n + 1),
        color=PALETTE["coral_gold"],
        linewidth=1.0,
        linestyle=(0, (3, 4)),
        alpha=0.35,
        zorder=3,
    )

    # Vertex markers
    ax.scatter(
        angles,
        values,
        s=36,
        c=accent,
        zorder=5,
        edgecolors=PALETTE["void"],
        linewidths=1.2,
    )

    if callout_weak:
        for ang, val, lab in zip(angles, values, labels):
            if val < weak_threshold:
                ax.annotate(
                    f"{val:.1f}",
                    xy=(ang, val),
                    xytext=(ang, min(10.2, val + 1.35)),
                    textcoords="data",
                    ha="center",
                    va="bottom",
                    fontsize=9,
                    fontweight="bold",
                    color=PALETTE["weak"],
                    arrowprops={
                        "arrowstyle": "-",
                        "color": PALETTE["weak"],
                        "lw": 0.8,
                        "alpha": 0.7,
                    },
                    zorder=7,
                )

    wrapped = [wrap_label(lb, width=9 if n > 5 else (10 if n > 3 else 14)) for lb in labels]
    ax.set_xticks(angles)
    ax.set_xticklabels(wrapped, color=PALETTE["ethereal"], fontsize=label_fs)
    for tick in ax.get_xticklabels():
        tick.set_fontweight("normal")
        tick.set_path_effects([pe.withStroke(linewidth=3, foreground=PALETTE["void"])])
        tick.set_clip_on(False)

    ax.set_ylim(0, 10.6)
    ax.set_yticks([2, 4, 6, 8, 10])
    ax.set_yticklabels(
        ["2", "4", "6", "8", "10"], color=PALETTE["muted"], fontsize=tick_fs
    )
    ax.grid(False)
    ax.spines["polar"].set_visible(False)

    if title:
        ax.set_title(
            title,
            color=PALETTE["ethereal"],
            fontsize=12,
            fontweight="bold",
            pad=16,
        )
    if score_line:
        ax.text(
            0.5,
            0.5,
            score_line,
            transform=ax.transAxes,
            ha="center",
            va="center",
            fontsize=16,
            fontweight="bold",
            color=accent,
            bbox={
                "boxstyle": "circle,pad=0.4",
                "facecolor": PALETTE["void"],
                "edgecolor": accent,
                "alpha": 0.92,
                "linewidth": 1.6,
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
        (0.06, 0.1),
        0.88,
        0.8,
        boxstyle="round,pad=0.03,rounding_size=0.04",
        transform=ax.transAxes,
        facecolor=PALETTE["panel"],
        edgecolor=accent,
        linewidth=1.4,
        alpha=0.75,
    )
    ax.add_patch(frame)
    ax.text(
        0.5,
        0.72,
        title,
        ha="center",
        va="center",
        color=PALETTE["ethereal"],
        fontsize=14,
        fontweight="bold",
        transform=ax.transAxes,
    )
    ax.text(
        0.5,
        0.52,
        "AWAITING TIDE",
        ha="center",
        va="center",
        color=PALETTE["lantern"],
        fontsize=13,
        fontweight="bold",
        transform=ax.transAxes,
    )
    ax.text(
        0.5,
        0.38,
        f"Branch · {branch}",
        ha="center",
        va="center",
        color=PALETTE["biolume"],
        fontsize=10,
        transform=ax.transAxes,
    )
    wrapped = wrap_label(reason, width=40)
    ax.text(
        0.5,
        0.22,
        wrapped,
        ha="center",
        va="center",
        color=PALETTE["sand"],
        fontsize=9,
        transform=ax.transAxes,
        alpha=0.95,
    )


def draw_domain_bars(
    ax: Axes,
    *,
    labels: list[str],
    values: list[float],
    accents: list[str] | None = None,
) -> None:
    """Horizontal domain score bars for exec summary."""
    ax.set_facecolor((0, 0, 0, 0))
    n = len(labels)
    y = np.arange(n)[::-1]
    accents = accents or [PALETTE["biolume"]] * n
    ax.barh(
        y,
        [10] * n,
        height=0.55,
        color=PALETTE["panel"],
        edgecolor=PALETTE["panel_edge"],
        linewidth=0.8,
        zorder=1,
    )
    ax.barh(
        y,
        values,
        height=0.55,
        color=accents,
        edgecolor="none",
        zorder=2,
        alpha=0.9,
    )
    for yi, val, lab in zip(y, values, labels):
        ax.text(
            0.15,
            yi,
            lab,
            va="center",
            ha="left",
            fontsize=10,
            color=PALETTE["ethereal"],
            fontweight="normal",
            zorder=3,
        )
        ax.text(
            9.7,
            yi,
            f"{val:.1f}",
            va="center",
            ha="right",
            fontsize=11,
            color=PALETTE["ethereal"],
            fontweight="bold",
            zorder=3,
        )
    ax.set_xlim(0, 10)
    ax.set_ylim(-0.6, n - 0.4)
    ax.axis("off")


def draw_callout_card(
    ax: Axes,
    *,
    title: str,
    body: str,
    accent: str,
) -> None:
    ax.set_facecolor((0, 0, 0, 0))
    ax.axis("off")
    frame = FancyBboxPatch(
        (0.02, 0.08),
        0.96,
        0.84,
        boxstyle="round,pad=0.02,rounding_size=0.03",
        transform=ax.transAxes,
        facecolor=PALETTE["panel"],
        edgecolor=accent,
        linewidth=1.2,
        alpha=0.8,
    )
    ax.add_patch(frame)
    ax.add_patch(
        Circle(
            (0.1, 0.72),
            0.045,
            transform=ax.transAxes,
            facecolor=accent,
            edgecolor="none",
            zorder=2,
        )
    )
    ax.text(
        0.18,
        0.72,
        title,
        ha="left",
        va="center",
        fontsize=11,
        fontweight="bold",
        color=PALETTE["ethereal"],
        transform=ax.transAxes,
    )
    ax.text(
        0.08,
        0.38,
        wrap_label(body, width=28),
        ha="left",
        va="center",
        fontsize=9,
        color=PALETTE["muted"],
        transform=ax.transAxes,
        linespacing=1.35,
    )
