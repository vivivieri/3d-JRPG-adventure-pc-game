---
id: privacy
type: reference
phase: [1, 6]
audience: [qa, flow]
status: active
authority: qa
tokens_est: 191
summary: "- **Local-only by default.** Logs write to `user://playtest/`; nothing leaves the machine."
---
# Playtest Telemetry — Privacy

**Hub:** [`PLAYTEST_TELEMETRY.md`](../PLAYTEST_TELEMETRY.md)

## When to read

Use **Playtest Telemetry — Privacy** (roles: qa, flow) when you need this reference during the current task Jump to a section below instead of reading end-to-end (1 sections).



## Privacy

- **Local-only by default.** Logs write to `user://playtest/`; nothing leaves the machine.
- **No PII.** `run_id` is an opaque random id, never tied to identity. Forbidden fields: `player_name`, `email`, `ip`, `geo`, `machine_id`.
- **Uploading requires consent.** Any telemetry that leaves a tester's machine (or post-launch) needs explicit opt-in + a privacy notice, and Steam disclosure. Prefer collecting logs manually from consenting playtesters during dev.
