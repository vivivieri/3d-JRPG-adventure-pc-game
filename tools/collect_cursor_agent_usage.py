#!/usr/bin/env python3
"""Fetch token usage from Cursor Cloud Agents API.

GET https://api.cursor.com/v1/agents/{bcId}/usage

Auth: HTTP Basic with CURSOR_API_KEY as username (empty password).
Docs: https://cursor.com/docs/cloud-agent/api/endpoints#get-agent-usage

Authority: docs/qa/AGENT_SESSION_TELEMETRY.md
"""
from __future__ import annotations

import json
import os
import sys
import time
import urllib.error
import urllib.request
from base64 import b64encode
from pathlib import Path
from typing import Any

API_BASE = "https://api.cursor.com/v1/agents"
DEFAULT_RETRIES = 3
DEFAULT_RETRY_DELAY_S = 8.0


def resolve_bc_id(explicit: str | None = None) -> str | None:
    """Resolve cloud agent bcId from argument or environment."""
    if explicit:
        return explicit.strip()
    for key in (
        "CURSOR_CONVERSATION_ID",
        "CURSOR_AGENT_BC_ID",
        "CURSOR_CLOUD_AGENT_BC_ID",
        "CURSOR_BC_ID",
    ):
        val = os.environ.get(key, "").strip()
        if val:
            return val
    return None


def resolve_api_key() -> str | None:
    for key in ("CURSOR_API_KEY", "CURSOR_API_TOKEN"):
        val = os.environ.get(key, "").strip()
        if val:
            return val
    return None


def _auth_header(api_key: str) -> str:
    token = b64encode(f"{api_key}:".encode("utf-8")).decode("ascii")
    return f"Basic {token}"


def fetch_agent_usage(
    bc_id: str,
    *,
    api_key: str | None = None,
    run_id: str | None = None,
    timeout_s: float = 30.0,
) -> dict[str, Any]:
    """Call Cursor usage API. Raises on HTTP error."""
    key = api_key or resolve_api_key()
    if not key:
        raise RuntimeError("CURSOR_API_KEY not set — see docs/agents/CURSOR_SECRETS_SETUP.md §8")

    url = f"{API_BASE}/{bc_id}/usage"
    if run_id:
        url += f"?runId={run_id}"

    req = urllib.request.Request(
        url,
        headers={
            "Authorization": _auth_header(key),
            "Accept": "application/json",
            "User-Agent": "tides-of-urashima-agent-telemetry/1.0",
        },
        method="GET",
    )
    with urllib.request.urlopen(req, timeout=timeout_s) as resp:
        return json.loads(resp.read().decode("utf-8"))


def usage_to_telemetry_fields(usage_payload: dict[str, Any]) -> dict[str, Any]:
    """Map API response to agent_session_telemetry fields."""
    total = usage_payload.get("totalUsage") or {}
    runs = usage_payload.get("runs") or []
    input_t = int(total.get("inputTokens") or 0)
    output_t = int(total.get("outputTokens") or 0)
    cache_read = int(total.get("cacheReadTokens") or 0)
    cache_write = int(total.get("cacheWriteTokens") or 0)
    total_t = int(total.get("totalTokens") or (input_t + output_t + cache_read + cache_write))

    fields: dict[str, Any] = {
        "tokens_input": input_t,
        "tokens_output": output_t,
        "tokens_cache_read": cache_read,
        "tokens_cache_write": cache_write,
        "tokens_total": total_t,
        "tokens_source": "cursor_api",
        "cursor_usage_raw": usage_payload,
        "cursor_run_count": len(runs),
    }
    if runs:
        fields["cursor_run_ids"] = [r.get("id") for r in runs if r.get("id")]
        latest = runs[-1]
        if latest.get("id"):
            fields["cursor_latest_run_id"] = latest["id"]
    return fields


def usage_delta(
    end_payload: dict[str, Any],
    start_payload: dict[str, Any] | None,
) -> dict[str, Any]:
    """Compute per-session token delta when baseline was captured at session_start."""
    end_fields = usage_to_telemetry_fields(end_payload)
    if not start_payload:
        return end_fields

    start_total = usage_to_telemetry_fields(start_payload)
    delta: dict[str, Any] = {
        "tokens_source": "cursor_api_delta",
        "cursor_usage_raw_end": end_payload,
        "cursor_usage_raw_start": start_payload,
        "cursor_run_count": end_fields.get("cursor_run_count"),
    }
    for key in (
        "tokens_input",
        "tokens_output",
        "tokens_cache_read",
        "tokens_cache_write",
        "tokens_total",
    ):
        end_v = int(end_fields.get(key) or 0)
        start_v = int(start_total.get(key) or 0)
        delta[key] = max(0, end_v - start_v)
    return delta


def fetch_with_retry(
    bc_id: str,
    *,
    retries: int = DEFAULT_RETRIES,
    delay_s: float = DEFAULT_RETRY_DELAY_S,
    min_total_tokens: int = 1,
) -> dict[str, Any] | None:
    """Fetch usage with retries — Cursor may lag before usage is recorded."""
    last_err: Exception | None = None
    for attempt in range(1, retries + 1):
        try:
            payload = fetch_agent_usage(bc_id)
            total = int((payload.get("totalUsage") or {}).get("totalTokens") or 0)
            if total >= min_total_tokens or attempt == retries:
                return payload
            time.sleep(delay_s)
        except (urllib.error.URLError, urllib.error.HTTPError, RuntimeError, json.JSONDecodeError) as exc:
            last_err = exc
            if attempt < retries:
                time.sleep(delay_s)
    if last_err:
        return None
    return None


def main() -> int:
    import argparse

    ap = argparse.ArgumentParser(description="Fetch Cursor cloud agent token usage")
    ap.add_argument("--bc-id", help="Cloud agent bcId (default: CURSOR_CONVERSATION_ID)")
    ap.add_argument("--run-id", help="Optional run id scope")
    ap.add_argument("--retries", type=int, default=1)
    ap.add_argument("--json", dest="json_out", help="Write JSON to file")
    args = ap.parse_args()

    bc_id = resolve_bc_id(args.bc_id)
    if not bc_id:
        print("[FAIL] No bcId — set CURSOR_CONVERSATION_ID or pass --bc-id", file=sys.stderr)
        return 1

    try:
        if args.retries > 1:
            payload = fetch_with_retry(bc_id, retries=args.retries)
            if payload is None:
                print("[FAIL] Could not fetch usage after retries", file=sys.stderr)
                return 1
        else:
            payload = fetch_agent_usage(bc_id, run_id=args.run_id)
    except Exception as exc:
        print(f"[FAIL] {exc}", file=sys.stderr)
        return 1

    fields = usage_to_telemetry_fields(payload)
    out = {"bc_id": bc_id, **fields}
    text = json.dumps(out, indent=2, ensure_ascii=False)
    if args.json_out:
        Path(args.json_out).write_text(text + "\n", encoding="utf-8")
    print(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
