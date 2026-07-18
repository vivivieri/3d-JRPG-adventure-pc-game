#!/usr/bin/env python3
"""Generate spec/build audit radar PNGs — legacy GameLab-style presentation.

Composites live scores onto layouts referenced from committed legacy art:
  tides_audit_radar_updated.png, audit_radar_6axis.png, tides_audit_alignment_radar.png

Authority: docs/qa/ALIGNMENT_AUDIT.md
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from audit_radar_legacy_style import (
    LEGACY_REFERENCES,
    apply_legacy_watermark,
    draw_gold_frame,
    draw_legacy_title_block,
    draw_scale_legend,
    render_legacy_breakdown_grid,
    render_legacy_combined_report,
    render_legacy_hero_radar,
    render_legacy_subdomain_radar,
)
from audit_radar_theme import PALETTE, configure_matplotlib

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


def _load_catalog() -> dict[str, Any]:
    return json.loads(CATALOG_PATH.read_text(encoding="utf-8"))


def _domain_title(catalog: dict[str, Any], dom_id: str) -> str:
    for row in catalog.get("domains", []):
        if row.get("id") == dom_id:
            return str(row.get("label", dom_id))
    return dom_id.replace("_", " ").title()


def _na_card(*, title: str, reason: str, branch: str, out_path: Path) -> None:
    import matplotlib.pyplot as plt
    from matplotlib.patches import FancyBboxPatch

    configure_matplotlib()
    fig = plt.figure(figsize=(10, 10))
    fig.patch.set_facecolor(PALETTE["void"])
    apply_legacy_watermark(fig, LEGACY_REFERENCES["hero_bg"], alpha=0.12)
    draw_gold_frame(fig)
    draw_legacy_title_block(fig, title=title.upper(), subtitle="Development & shipping", meta=f"Branch · {branch}", verdict="N/A")
    draw_scale_legend(fig)
    ax = fig.add_axes([0.1, 0.14, 0.8, 0.68])
    ax.axis("off")
    frame = FancyBboxPatch(
        (0.08, 0.1),
        0.84,
        0.8,
        boxstyle="round,pad=0.02",
        transform=ax.transAxes,
        facecolor=(0.08, 0.1, 0.16, 0.8),
        edgecolor=PALETTE["coral_gold"],
        linewidth=2,
    )
    ax.add_patch(frame)
    ax.plot([0.2, 0.8], [0.78, 0.78], color=PALETTE["wood"], linewidth=3, transform=ax.transAxes)
    ax.plot([0.28, 0.28], [0.68, 0.78], color=PALETTE["wood"], linewidth=2.5, transform=ax.transAxes)
    ax.plot([0.72, 0.72], [0.68, 0.78], color=PALETTE["wood"], linewidth=2.5, transform=ax.transAxes)
    ax.text(0.5, 0.58, "AWAITING TIDE", ha="center", fontsize=22, color=PALETTE["muted"], transform=ax.transAxes, fontstyle="italic")
    ax.text(0.5, 0.42, reason[:100], ha="center", fontsize=9, color=PALETTE["sand"], transform=ax.transAxes, wrap=True)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_path, dpi=200, facecolor=PALETTE["void"], bbox_inches="tight", pad_inches=0.18)
    plt.close(fig)


def generate_spec_subdomain_radars(
    report: dict[str, Any], output_dir: Path, catalog: dict[str, Any] | None = None
) -> dict[str, str]:
    cat = catalog or _load_catalog()
    signal_scores = report.get("signal_scores", {})
    domain_scores = report.get("domain_scores", {})
    written: dict[str, str] = {}

    domain_titles = {d["id"]: d.get("label", d["id"]) for d in cat.get("domains", [])}

    for dom_id in SPEC_DOMAIN_ORDER:
        signals = signal_scores.get(dom_id, {})
        if not signals:
            continue
        fname = f"audit_radar_spec_{dom_id}.png"
        out_path = output_dir / fname
        render_legacy_subdomain_radar(
            domain_id=dom_id,
            signal_ids=list(signals.keys()),
            values=[float(v) for v in signals.values()],
            domain_score=float(domain_scores.get(dom_id, 0)),
            title=_domain_title(cat, dom_id),
            out_path=out_path,
        )
        written[fname] = str(out_path)

    breakdown_path = output_dir / "audit_radar_spec_breakdown.png"
    render_legacy_breakdown_grid(report, domain_titles, SPEC_DOMAIN_ORDER, breakdown_path)
    written["audit_radar_spec_breakdown.png"] = str(breakdown_path)
    return written


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
        dom_ids = list(spec_domains.keys())
        vals = [float(v) for v in spec_domains.values()]
        spec_path = out_dir / "audit_radar_spec.png"
        render_legacy_hero_radar(
            domain_ids=dom_ids,
            values=vals,
            title="PROJECT AUDIT",
            subtitle="Design & preparation · spec readiness",
            stream_score=float(spec.get("score") or 0),
            verdict=str(spec.get("verdict", "?")),
            meta=spec.get("question", ""),
            out_path=spec_path,
            background=LEGACY_REFERENCES["hero_bg"],
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
            dom_ids = list(build_domains.keys())
            vals = [float(v) for v in build_domains.values()]
            render_legacy_hero_radar(
                domain_ids=dom_ids,
                values=vals,
                title="BUILD AUDIT",
                subtitle="Development & shipping",
                stream_score=float(build.get("score") or 0),
                verdict=str(build.get("verdict", "?")),
                meta=build.get("question", ""),
                out_path=build_path,
                background=LEGACY_REFERENCES["six_axis_bg"],
            )
    written["audit_radar_build.png"] = str(build_path)

    report_path = out_dir / "audit_radar_report.png"
    render_legacy_combined_report(report, report_path)
    written["audit_radar_report.png"] = str(report_path)

    written.update(generate_spec_subdomain_radars(report, out_dir))
    return written


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Generate legacy-style Urashima audit radar PNGs")
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
