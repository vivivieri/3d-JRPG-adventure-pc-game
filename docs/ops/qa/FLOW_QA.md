---
id: flow-qa
type: how-to
audience: [flow, qa, builder]
status: active
authority: qa
tokens_est: 199
summary: "Story soft-lock / quest / combat hang gates — load the layer you need"
---
# Flow QA

**Hub** — load only the pack for your current pass.

| Pack | Topic |
|------|-------|
| [`standards_layers.md`](flow_qa/standards_layers.md) | Industry standards + defense layers |
| [`scenarios_levers.md`](flow_qa/scenarios_levers.md) | L4 scenarios + lever taxonomy |
| [`workflow_report.md`](flow_qa/workflow_report.md) | Agent workflow, iteration, smoke, report, tools |
**Version:** 1.0
**Problem:** An agent can wire a scene “done” while the **main story soft-locks**, a **quest never advances**, or **combat hangs** — then patch the same trigger logic repeatedly without fixing root cause.

