---
id: qa-remediation-loop
type: how-to
audience: [qa, builder, visual]
status: active
authority: qa
tokens_est: 261
summary: "FAIL → one lever → re-measure — load the section for your domain"
---
# QA Remediation Loop

**Hub** — load only the pack for your current pass.

| Pack | Topic |
|------|-------|
| [`standards_loop.md`](remediation/standards_loop.md) | Industry standards + remediation loop |
| [`levers_commands.md`](remediation/levers_commands.md) | Lever taxonomy + commands |
| [`report_stop_maps.md`](remediation/report_stop_maps.md) | Report template, stop rules, medium maps |
| [`tools_related.md`](remediation/tools_related.md) | Tools, related docs, unified improvement |
**Version:** 1.0
**Problem:** QA gates catch bad assets, but agents often **re-run the same generator with the same prompt** and expect a different result. That loop never ends.

**Rule:** Every FAIL produces a **structured remediation brief** with a **changed lever** before the next build. Same pipeline + same prompt = **blocked** after 2 attempts.

