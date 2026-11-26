---
name: create-page
description: >
  This skill should be used when the user asks to "create a page", "make a new page for [topic]",
  "build a landing page", "add a service page", "draft a new page in the CMS", or "run the content team"
  for new content. It coordinates the content-team agents from brief to a saved, unpublished CMS draft.
metadata:
  version: "0.1.0"
---

# Create Page (Coordinator)

Act as the Coordinator of the content team. Run the agents in order, pass files between them, and stop for the user at the approval points. Do not write the brief, blueprint, copy or review yourself.

First load the `content-team-rules` skill. Every rule in it applies. Note the absolute path of its `references/` folder; pass the relevant file paths to each agent.

## Step 1 – Prepare

1. Find the project (`references/folder-layout.md`). Read project.md.
2. Check that cms/component-catalogue.md and cms/cms-mapping.md exist. If not, tell the user to run "set up this project" first and stop. If they are still "Status: draft", say so once and continue.
3. Run the knowledge freshness check (`references/freshness-check.md`) and show the result: one line if up to date, otherwise a short list. Pass any mismatches to every agent.
4. Create the run folder `runs/<YYYY-MM-DD>-<slug>/` and copy the run templates into it.
5. If the request is missing something only the user can give (topic, key facts, dates, prices), ask once, all in one question.

## Step 2 – Brief

Launch `content-strategist` with the request, project path, run path and the rules paths. If it recommends updating an existing page instead, tell the user and offer to switch to the update-page workflow. If it reports a permission problem, stop and show it.

## Step 3 – Blueprint

Launch `page-architect` with the run path, project path, `references/formats/blueprint.format.md` and `references/run-templates/blueprint.json`.

Show the user a short outline (section → component) and any **component gaps**. For each gap ask the user to choose: use the closest existing component, drop the section, or pause for developers. Record decisions in the blueprint.

## Step 4 – Copy

Launch `copywriter` with the run path, project path and the defaults paths (writing, seo, accessibility).

## Step 5 – Review

Launch `content-reviewer` with the run path, project path and the defaults and review template paths.
- **FAIL:** send the FAIL items back to the copywriter (copy issues) or page-architect (structure issues) once, then review again. If it still fails, stop and show the user.
- **PASS WITH FLAGS / PASS:** continue.

## Step 6 – Preview and approval

Launch `cms-operator` in **preview** mode. Then launch `page-mockup-maker` in **create** mode with the run folder, project folder and `references/formats/mockup.format.md`. If the project has no `learned/mockup-kit/`, the agent uses generic styling; mention once that "build the mock-up kit" makes mock-ups look like the site.

Then show the user, concisely:
- Page title, folder/slug, languages
- Section outline
- Reviewer result and every FLAG and human_check
- Assumptions and [TODO]s
- The mock-up: `mockup.html` in the run folder (open it to see the page), plus any approximations the agent reported
- Where to read the full blueprint and preview in the run folder

Ask for explicit approval to save as a draft. Do not treat silence or general enthusiasm as approval. If the user asks for changes, route them to the right agent and repeat review, preview and the mock-up.

## Step 7 – Save

Only after explicit approval, launch `cms-operator` in **save** mode with the user's approval wording. Then report the story id, slug, editor link, and that it is an unpublished draft for the user to review and publish in the CMS.

## Step 8 – Log

Make sure log.md is complete (request, story id, gaps, review result, approver, link, knowledge-check result).

If the freshness check found mismatches, offer to update the knowledge files to match project.md (`component-librarian` in **sync** mode).

## If the CMS connector is read-only

If `cms-operator` reports it cannot write, tell the user plainly, point them to `change-sheet.md` in the run folder (field-by-field values to paste into the CMS), and record "saved manually by human" in log.md once they confirm. Never look for another way to write to the CMS.
