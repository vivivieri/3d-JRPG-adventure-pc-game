#!/usr/bin/env python3
"""Analyze gameplay/playtest JSONL logs against Tides of Urashima QA thresholds.

Reads one or more JSONL playtest logs (one event object per line, schema:
game/data/qa/playtest_analytics_schema.json), rolls them into pacing / combat /
progression / ending metrics, and reports each metric against the thresholds in
the schema (cross-referenced to docs/ACCEPTANCE_CRITERIA.md gates). This is a
development QA aid — a red metric opens a remediation item
(docs/QA_REMEDIATION_LOOP.md), it does not by itself block ship.

Usage:
  python3 tools/analyze_playtest_logs.py <log.jsonl | logs_dir>
  python3 tools/analyze_playtest_logs.py <logs_dir> --json report.json --strict
  python3 tools/analyze_playtest_logs.py --emit-sample <out_dir> [--runs N]

Exit codes:
  0  analysis ran; no malformed events (and, unless --strict, regardless of FAILs)
  1  malformed events found, or --strict and one or more metrics FAILed
  2  bad invocation / missing schema
"""
from __future__ import annotations

import argparse
import json
import random
import statistics
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "game/data/qa/playtest_analytics_schema.json"

PASS = "PASS"
WARN = "WARN"
FAIL = "FAIL"


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


# --------------------------------------------------------------------------- #
# Log loading + validation
# --------------------------------------------------------------------------- #
def iter_log_files(target: Path) -> list[Path]:
    if target.is_dir():
        return sorted(target.glob("*.jsonl"))
    return [target]


def load_events(files: list[Path], schema: dict[str, Any]) -> tuple[list[dict], list[str]]:
    known = {et["name"]: et for et in schema["event_types"]}
    events: list[dict] = []
    errors: list[str] = []
    for f in files:
        for lineno, raw in enumerate(f.read_text(encoding="utf-8").splitlines(), 1):
            raw = raw.strip()
            if not raw:
                continue
            try:
                obj = json.loads(raw)
            except json.JSONDecodeError as exc:
                errors.append(f"{f.name}:{lineno} invalid JSON ({exc.msg})")
                continue
            name = obj.get("event")
            if name not in known:
                errors.append(f"{f.name}:{lineno} unknown event '{name}'")
                continue
            for field in known[name]["required"]:
                if field not in obj:
                    errors.append(f"{f.name}:{lineno} event '{name}' missing required field '{field}'")
            obj["_src"] = f.name
            events.append(obj)
    return events, errors


def group_runs(events: list[dict]) -> dict[str, list[dict]]:
    runs: dict[str, list[dict]] = {}
    for e in events:
        runs.setdefault(e.get("run_id", "?"), []).append(e)
    for evs in runs.values():
        evs.sort(key=lambda e: e.get("t", 0.0))
    return runs


# --------------------------------------------------------------------------- #
# Metric computation
# --------------------------------------------------------------------------- #
def analyze_run(events: list[dict], schema: dict[str, Any]) -> dict[str, Any]:
    beats = {b["id"]: b for b in schema["scene_beats"]}
    thr = schema["thresholds"]
    stuck_seconds = thr["stuck_seconds"]["value"]
    progress_events = set(schema["progress_events"])

    times = [e["t"] for e in events if "t" in e]
    t0 = min(times) if times else 0.0
    t_last = max(times) if times else 0.0

    ending = None
    session_reason = None
    scene_arrival: dict[str, float] = {}
    combats: list[dict] = []
    deaths: dict[str, int] = {}
    first_combat_t: float | None = None
    choices: list[dict] = []

    prog_ts: list[tuple[float, str]] = []
    for e in events:
        name = e["event"]
        t = e.get("t", 0.0)
        if name in progress_events:
            prog_ts.append((t, name))
        if name == "scene_beat" and e.get("scene") not in scene_arrival:
            scene_arrival[e.get("scene")] = t
        elif name == "ending_reached":
            ending = e.get("ending")
        elif name == "session_end":
            session_reason = e.get("reason")
        elif name == "combat_start" and first_combat_t is None:
            first_combat_t = t
        elif name == "combat_end":
            combats.append(e)
        elif name == "player_death":
            deaths[e.get("encounter", "unknown")] = deaths.get(e.get("encounter", "unknown"), 0) + 1
        elif name == "choice_made":
            choices.append({"choice_id": e.get("choice_id"), "option": e.get("option")})

    # Stuck gaps between consecutive progress events.
    stuck: list[dict] = []
    prog_ts.sort()
    for (ta, na), (tb, nb) in zip(prog_ts, prog_ts[1:]):
        gap = tb - ta
        if gap > stuck_seconds:
            stuck.append({"from": na, "to": nb, "gap_s": round(gap, 1), "at_t": round(ta, 1)})

    completed = ending is not None or session_reason == "completed"

    # No-combat-before-SC-05 rule.
    combat_before_gate = False
    gate_scene = thr["no_combat_before_scene"]["value"]
    if first_combat_t is not None:
        gate_t = scene_arrival.get(gate_scene)
        if gate_t is None or first_combat_t < gate_t:
            combat_before_gate = True

    return {
        "playtime_min": round((t_last - t0) / 60.0, 1),
        "completed": completed,
        "ending": ending,
        "session_reason": session_reason,
        "scene_arrival_min": {k: round(v / 60.0, 1) for k, v in scene_arrival.items()},
        "combats": combats,
        "deaths": deaths,
        "combat_before_gate": combat_before_gate,
        "choices": choices,
        "stuck": stuck,
    }


def aggregate(runs: dict[str, list[dict]], schema: dict[str, Any]) -> dict[str, Any]:
    per_run = {rid: analyze_run(evs, schema) for rid, evs in runs.items()}
    thr = schema["thresholds"]
    beats = {b["id"]: b for b in schema["scene_beats"]}
    drift_tol = thr["scene_beat_drift_tolerance_min"]["value"]
    turn_max = thr["combat_turn_resolve_max_s"]["value"]
    death_flag = thr["encounter_avg_deaths_flag"]["value"]

    total = len(per_run)
    completed = sum(1 for r in per_run.values() if r["completed"])
    completion_rate = round(100.0 * completed / total, 1) if total else 0.0

    endings_seen: dict[str, int] = {}
    for r in per_run.values():
        if r["ending"]:
            endings_seen[r["ending"]] = endings_seen.get(r["ending"], 0) + 1

    playtimes = [r["playtime_min"] for r in per_run.values() if r["playtime_min"] > 0]
    avg_playtime = round(statistics.mean(playtimes), 1) if playtimes else 0.0

    # Scene pacing drift: avg arrival vs target.
    scene_drift: list[dict] = []
    for sid, beat in beats.items():
        arrivals = [r["scene_arrival_min"][sid] for r in per_run.values() if sid in r["scene_arrival_min"]]
        if not arrivals:
            continue
        avg_arr = statistics.mean(arrivals)
        delta = avg_arr - beat["target_min"]
        if abs(delta) > drift_tol:
            scene_drift.append({"scene": sid, "label": beat["label"], "target_min": beat["target_min"],
                                "avg_arrival_min": round(avg_arr, 1), "delta_min": round(delta, 1)})

    # Combat difficulty: avg deaths per encounter across runs.
    death_totals: dict[str, int] = {}
    for r in per_run.values():
        for enc, n in r["deaths"].items():
            death_totals[enc] = death_totals.get(enc, 0) + n
    death_spikes = [{"encounter": enc, "avg_deaths": round(n / total, 2)}
                    for enc, n in death_totals.items() if total and (n / total) > death_flag]

    # Combat turn-resolve feel violations.
    slow_turns = []
    for rid, r in per_run.items():
        for c in r["combats"]:
            mtr = c.get("max_turn_resolve_s")
            if isinstance(mtr, (int, float)) and mtr > turn_max:
                slow_turns.append({"run": rid, "encounter": c.get("encounter"), "max_turn_resolve_s": mtr})

    combat_before_gate_runs = [rid for rid, r in per_run.items() if r["combat_before_gate"]]

    # Stuck hotspots aggregated by location.
    hotspots: dict[str, int] = {}
    for r in per_run.values():
        for s in r["stuck"]:
            hotspots[f"{s['from']} -> {s['to']}"] = hotspots.get(f"{s['from']} -> {s['to']}", 0) + 1

    return {
        "per_run": per_run,
        "totals": {
            "runs": total,
            "completed": completed,
            "completion_rate_percent": completion_rate,
            "avg_playtime_min": avg_playtime,
            "endings_seen": endings_seen,
        },
        "scene_drift": scene_drift,
        "death_spikes": death_spikes,
        "slow_turns": slow_turns,
        "combat_before_gate_runs": combat_before_gate_runs,
        "stuck_hotspots": hotspots,
    }


# --------------------------------------------------------------------------- #
# Reporting
# --------------------------------------------------------------------------- #
def evaluate(agg: dict[str, Any], schema: dict[str, Any]) -> list[dict]:
    thr = schema["thresholds"]
    t = agg["totals"]
    checks: list[dict] = []

    def add(name: str, status: str, detail: str, ref: str) -> None:
        checks.append({"metric": name, "status": status, "detail": detail, "design_ref": ref})

    # Completion rate (L6).
    min_comp = thr["completion_rate_min_percent"]["value"]
    add("completion_rate",
        PASS if t["completion_rate_percent"] >= min_comp else FAIL,
        f"{t['completion_rate_percent']}% completed ({t['completed']}/{t['runs']} runs), min {min_comp}%",
        thr["completion_rate_min_percent"]["design_ref"])

    # Ending coverage (L5).
    required = set(thr["endings_required_coverage"]["value"])
    seen = set(t["endings_seen"])
    missing = required - seen
    add("ending_coverage",
        PASS if not missing else FAIL,
        f"seen {sorted(seen)}; missing {sorted(missing)}" if missing else f"all endings reached {t['endings_seen']}",
        thr["endings_required_coverage"]["design_ref"])

    # Playtime vs pacing target.
    target = thr["target_playtime_minutes"]["value"]
    tol = thr["target_playtime_minutes"]["tolerance"]
    within = abs(t["avg_playtime_min"] - target) <= tol
    add("avg_playtime",
        PASS if within else WARN,
        f"avg {t['avg_playtime_min']} min (target {target}±{tol})",
        thr["target_playtime_minutes"]["design_ref"])

    # No combat before SC-05 (hard pacing rule).
    add("no_combat_before_gate",
        PASS if not agg["combat_before_gate_runs"] else FAIL,
        "ok" if not agg["combat_before_gate_runs"] else f"combat before {thr['no_combat_before_scene']['value']} in runs {agg['combat_before_gate_runs']}",
        thr["no_combat_before_scene"]["design_ref"])

    # Pacing drift per scene.
    add("scene_pacing_drift",
        PASS if not agg["scene_drift"] else WARN,
        "within tolerance" if not agg["scene_drift"] else f"{len(agg['scene_drift'])} beat(s) drift: " + ", ".join(f"{d['scene']} {d['delta_min']:+}min" for d in agg["scene_drift"]),
        thr["scene_beat_drift_tolerance_min"]["design_ref"])

    # Combat difficulty spikes.
    add("combat_difficulty",
        PASS if not agg["death_spikes"] else WARN,
        "no spikes" if not agg["death_spikes"] else "; ".join(f"{d['encounter']} {d['avg_deaths']} deaths/run" for d in agg["death_spikes"]),
        thr["encounter_avg_deaths_flag"]["design_ref"])

    # Combat turn-resolve feel.
    add("combat_turn_resolve",
        PASS if not agg["slow_turns"] else WARN,
        "within feel budget" if not agg["slow_turns"] else f"{len(agg['slow_turns'])} encounter(s) over {thr['combat_turn_resolve_max_s']['value']}s",
        thr["combat_turn_resolve_max_s"]["design_ref"])

    # Stuck / confusion hotspots.
    add("stuck_hotspots",
        PASS if not agg["stuck_hotspots"] else WARN,
        "none" if not agg["stuck_hotspots"] else "; ".join(f"{loc} ×{n}" for loc, n in agg["stuck_hotspots"].items()),
        thr["stuck_seconds"]["design_ref"])

    return checks


def print_report(agg: dict[str, Any], checks: list[dict]) -> None:
    t = agg["totals"]
    print("=" * 68)
    print("Tides of Urashima — Playtest log analysis")
    print("=" * 68)
    print(f"Runs: {t['runs']}  |  Completed: {t['completed']}  |  Completion: {t['completion_rate_percent']}%")
    print(f"Avg playtime: {t['avg_playtime_min']} min  |  Endings: {t['endings_seen'] or '(none)'}")
    print("-" * 68)
    icon = {PASS: "[PASS]", WARN: "[WARN]", FAIL: "[FAIL]"}
    for c in checks:
        print(f"{icon[c['status']]} {c['metric']}: {c['detail']}")
        print(f"        ref: {c['design_ref']}")
    print("-" * 68)
    n_fail = sum(1 for c in checks if c["status"] == FAIL)
    n_warn = sum(1 for c in checks if c["status"] == WARN)
    print(f"Summary: {len(checks) - n_fail - n_warn} PASS, {n_warn} WARN, {n_fail} FAIL")
    if n_fail or n_warn:
        print("On WARN/FAIL: open a remediation item (docs/QA_REMEDIATION_LOOP.md) — change one lever, re-measure.")


# --------------------------------------------------------------------------- #
# Sample generator (for demos / testing the pipeline)
# --------------------------------------------------------------------------- #
def emit_sample(out_dir: Path, runs: int, schema: dict[str, Any]) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    beats = schema["scene_beats"]
    endings = ["rewind", "anchor", "drift"]
    heartbeat_s = 45.0  # game emits a periodic progress heartbeat; a > stuck_seconds gap = real inactivity
    rng = random.Random(42)

    for i in range(runs):
        rid = f"run{i:03d}"
        lines: list[dict] = []
        # One run (the last) is abandoned early to exercise drop-off/completion.
        abandoned = i == runs - 1 and runs > 1
        # run000 sits stuck on the caves puzzle to demonstrate a real hotspot.
        stuck_window: tuple[float, float] | None = None

        def ev(t: float, event: str, **kw: Any) -> None:
            lines.append({"run_id": rid, "event": event, "t": round(t, 1), **kw})

        ev(0.0, "session_start", build="0.1.0-dev", locale="en")
        cutoff = beats[4]["target_min"] if abandoned else beats[-1]["target_min"] + 5
        end_t = 0.0
        for b in beats:
            base_min = b["target_min"]
            if base_min > cutoff:
                break
            arr = max(0.0, base_min + rng.uniform(-2, 4)) * 60.0
            end_t = max(end_t, arr)
            ev(arr, "scene_beat", scene=b["id"])
            if b["id"] == "SC-05":
                ev(arr + 30, "combat_start", encounter="enc_sc05_tutorial")
                ev(arr + 90, "combat_end", encounter="enc_sc05_tutorial", result="win", turns=4, max_turn_resolve_s=1.6)
            if b["id"] == "SC-07":
                ev(arr + 20, "puzzle_start", puzzle_id="caves_tide_gate")
                solve_delay = 430.0 if i == 0 else 200.0  # run000: player gets stuck
                if i == 0:
                    stuck_window = (arr + 40, arr + solve_delay)  # no heartbeats here
                ev(arr + solve_delay, "puzzle_solved", puzzle_id="caves_tide_gate", duration_s=solve_delay - 20, hints_used=1 if i else 3)
                end_t = max(end_t, arr + solve_delay)
            if b["id"] == "SC-15":
                ev(arr + 20, "combat_start", encounter="boss_tide_keeper")
                for _ in range(rng.randint(3, 5)):  # difficulty spike -> WARN
                    ev(arr + 40, "player_death", encounter="boss_tide_keeper")
                ev(arr + 300, "combat_end", encounter="boss_tide_keeper", result="win", turns=18, max_turn_resolve_s=2.4)
                end_t = max(end_t, arr + 300)
            if b["id"] == "SC-16":
                ev(arr + 10, "choice_made", choice_id="ending_choice", option=endings[i % 3])
        if not abandoned:
            end_t = max(end_t, (beats[-1]["target_min"] + rng.uniform(0, 6)) * 60.0)
            ev(end_t, "ending_reached", ending=endings[i % 3])
            ev(end_t + 5, "session_end", reason="completed")
            end_t += 5
        else:
            end_t = cutoff * 60.0 + 30
            ev(end_t, "session_end", reason="quit")

        # Fill periodic heartbeats so normal pacing gaps are not mistaken for "stuck".
        hb = heartbeat_s
        while hb < end_t:
            if not (stuck_window and stuck_window[0] <= hb <= stuck_window[1]):
                ev(hb, "progress", note="heartbeat")
            hb += heartbeat_s

        lines.sort(key=lambda o: o["t"])
        path = out_dir / f"{rid}.jsonl"
        path.write_text("\n".join(json.dumps(o) for o in lines) + "\n", encoding="utf-8")
    print(f"Wrote {runs} sample run log(s) to {out_dir}")


# --------------------------------------------------------------------------- #
def main() -> int:
    ap = argparse.ArgumentParser(description="Analyze playtest JSONL logs against QA thresholds.")
    ap.add_argument("logs", nargs="?", help="JSONL file or directory of *.jsonl logs")
    ap.add_argument("--schema", default=str(SCHEMA_PATH), help="analytics schema JSON")
    ap.add_argument("--json", dest="json_out", help="write full report JSON to this path")
    ap.add_argument("--strict", action="store_true", help="exit non-zero if any metric FAILs")
    ap.add_argument("--emit-sample", dest="emit_sample", metavar="OUT_DIR", help="generate synthetic sample logs and exit")
    ap.add_argument("--runs", type=int, default=5, help="number of runs for --emit-sample (default 5)")
    args = ap.parse_args()

    schema_path = Path(args.schema)
    if not schema_path.is_file():
        print(f"Missing schema: {schema_path}", file=sys.stderr)
        return 2
    schema = load_json(schema_path)

    if args.emit_sample:
        emit_sample(Path(args.emit_sample), args.runs, schema)
        return 0

    if not args.logs:
        print("error: provide a log file/dir, or use --emit-sample OUT_DIR", file=sys.stderr)
        return 2
    target = Path(args.logs)
    if not target.exists():
        print(f"No such log path: {target}", file=sys.stderr)
        return 2

    files = iter_log_files(target)
    if not files:
        print(f"No .jsonl logs found in {target}", file=sys.stderr)
        return 2

    events, parse_errors = load_events(files, schema)
    runs = group_runs(events)
    if not runs:
        print("No valid events parsed.", file=sys.stderr)
        return 1

    agg = aggregate(runs, schema)
    checks = evaluate(agg, schema)
    print_report(agg, checks)

    if parse_errors:
        print("-" * 68)
        print(f"Malformed events: {len(parse_errors)} (showing up to 10)")
        for e in parse_errors[:10]:
            print(f"  - {e}")

    if args.json_out:
        Path(args.json_out).write_text(
            json.dumps({"totals": agg["totals"], "checks": checks, "detail": {k: agg[k] for k in ("scene_drift", "death_spikes", "slow_turns", "combat_before_gate_runs", "stuck_hotspots")}, "parse_errors": parse_errors}, indent=2),
            encoding="utf-8",
        )
        print(f"Wrote report JSON: {args.json_out}")

    n_fail = sum(1 for c in checks if c["status"] == FAIL)
    if parse_errors:
        return 1
    if args.strict and n_fail:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
