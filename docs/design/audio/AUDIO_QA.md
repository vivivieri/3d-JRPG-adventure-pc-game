---
id: audio-qa
type: how-to
phase: [1, 5]
audience: [audio, qa]
status: active
authority: audio
tokens_est: 240
summary: "BGM/VO QA gates — load layers, smoke, or tools"
---
# Audio QA

**Hub** — load only the pack for your current pass.

| Pack | Topic |
|------|-------|
| [`automate_layers.md`](audio_qa/automate_layers.md) | Automate vs human + defense layers |
| [`smoke_workflow.md`](audio_qa/smoke_workflow.md) | L2 smoke, agent workflow, report template |
| [`tools_vs_visual.md`](audio_qa/tools_vs_visual.md) | Tools + vs Visual QA |
**Version:** 1.1
**Problem:** An agent can register `bgm_village.ogg` or `sc00_urashima_01.ogg` without listening — often a **procedural sine placeholder**, wrong loudness, or off-direction VO that ships everywhere.

**Rule:** Audio tasks pass **catalog + technical checks** first. **Hero BGM** and **P0 VO** use optional **multi-LLM listen jury** (scoped — not every SFX). Human **L6** still owns in-game mix feel.

