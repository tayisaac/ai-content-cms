---
description: The content-reviewer agent must not FAIL a blueprint that follows the rules (PASS or PASS WITH FLAGS).
tags: [agents, reviewer]
plugins: ["../../plugins/content-team"]
max_turns: 20
timeout_seconds: 600
allowed_tools: [Read, Glob, Grep, Write, Agent, Skill]
---

Please run the content-reviewer agent on the blueprint in ClearView/runs/2026-11-11-office-eye-check/. The project folder is ClearView/.
