#!/usr/bin/env python3
"""Save-slot HMAC helpers — reference for SaveSystem (docs/qa/SECURITY.md §9)."""
from __future__ import annotations

import hashlib
import hmac
import json
from typing import Any

DEFAULT_SPEC_PATH = "game/data/qa/save_integrity.json"


def load_spec(path: str = DEFAULT_SPEC_PATH) -> dict[str, Any]:
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def canonical_payload(save: dict[str, Any], spec: dict[str, Any]) -> bytes:
    payload = {
        k: save[k]
        for k in spec["signed_payload_fields"]
        if k in save and k not in spec.get("excluded_from_canonical", [])
    }
    cfg = spec["canonical_json"]
    text = json.dumps(
        payload,
        sort_keys=cfg.get("sort_keys", True),
        separators=tuple(cfg.get("separators", [",", ":"])),
        ensure_ascii=cfg.get("ensure_ascii", True),
    )
    return text.encode("utf-8")


def sign_save(save: dict[str, Any], pepper: str, spec: dict[str, Any] | None = None) -> str:
    spec = spec or load_spec()
    digest = hmac.new(
        pepper.encode("utf-8"),
        canonical_payload(save, spec),
        hashlib.sha256,
    ).hexdigest()
    return digest


def verify_save(save: dict[str, Any], pepper: str, spec: dict[str, Any] | None = None) -> bool:
    spec = spec or load_spec()
    field = spec["integrity_field"]
    if field not in save:
        return False
    expected = save[field]
    copy = dict(save)
    copy.pop(field, None)
    actual = sign_save(copy, pepper, spec)
    return hmac.compare_digest(str(expected), actual)


def attach_integrity(save: dict[str, Any], pepper: str, spec: dict[str, Any] | None = None) -> dict[str, Any]:
    spec = spec or load_spec()
    out = dict(save)
    out.pop(spec["integrity_field"], None)
    out[spec["integrity_field"]] = sign_save(out, pepper, spec)
    return out
