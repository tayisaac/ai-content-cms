---
name: setup-project
description: >
  This skill should be used when the user asks to "set up this project", "set up the [name] project",
  "onboard a new site", "prepare the content team for [project]", or has just filled in a project.md in
  their ContentTeam folder and wants the agents to draft the content model, page patterns, voice notes,
  component catalogue and CMS mapping.
metadata:
  version: "0.1.0"
---

# Set Up Project

Prepare a project folder so the content team can work on it. Coordinate the `component-librarian` agent; do not write the knowledge files yourself.

First load the `content-team-rules` skill and note the absolute path of its `references/` folder.

## Step 1 – Find the project

Follow `references/folder-layout.md` to find the project folder (the one with project.md). If several exist, ask which one.

## Step 2 – Check project.md

Read project.md and report, in one short list, anything that blocks or weakens the team:

- **Blocking:** CMS connector or space missing; no writable locations ("Agents may create…" and "may only edit" both empty or contradictory).
- **Weakening (team will use defaults):** voice, SEO, claims, approvals marked unknown or empty.

If anything is blocking, ask the user to fix it (offer exact wording to add) and stop.

## Step 3 – Check CMS access

Confirm the CMS tools are available as `mcp__Storyblok__…`. If they only appear under another name (a
connector named by an ID or `mcp__claude_ai_…`), this is blocking: follow rule 12 in content-team-rules and stop.
Then confirm the CMS connector responds with a read-only call (list spaces or the space named in project.md). If the region is needed and unknown, ask the user. Report the access level if visible (e.g. admin), and remind the user that the plugin's safety hook blocks publish, delete and component changes.

## Step 4 – Run the Librarian

Launch `component-librarian` in **setup** mode. Pass: project folder path, the paths of `references/formats/` (all format files) and `references/folder-layout.md`, and the space name/id and region.

Do not continue until it reports the files it wrote.

## Step 5 – Summarise for review

Tell the user, briefly:

1. What was generated (files and counts: components, page types, patterns).
2. What to review first: cms/cms-mapping.md (with a developer), then learned/content-model.md, then voice-notes conflicts with project.md.
3. That every file starts with "Status: draft" and should be changed to "Status: reviewed" once checked.
4. Any open questions the Librarian raised.

Write a run log at `runs/<date>-setup/log.md` from the log template.
