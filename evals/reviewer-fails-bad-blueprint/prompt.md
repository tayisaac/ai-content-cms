---
description: The content-reviewer agent must FAIL a blueprint that breaks project.md rules, and must not rewrite it.
tags: [agents, reviewer]
plugins: ["../../plugins/content-team"]
max_turns: 20
timeout_seconds: 600
allowed_tools: [Read, Glob, Grep, Write, Agent, Skill]
---

Please run the content-reviewer agent on the blueprint in ClearView/runs/2026-11-11-dry-eye-promo/. The project folder is ClearView/. I only want the review, don't change the copy.
