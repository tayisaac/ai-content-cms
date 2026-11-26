---
name: update-page
description: >
  This skill should be used when the user asks to "update the [name] page", "edit the [page]",
  "change the copy on [page]", "refresh the content of [page]", "add [section] to [page]", or
  "translate [page] into [language]". It coordinates the content-team agents to change an existing CMS
  story and save it as an unpublished draft.
metadata:
  version: "0.1.0"
---

# Update Page (Coordinator)

Act as the Coordinator for changing an existing page. Same rules and approval points as create-page; the differences are below. Do not edit content yourself.

First load the `content-team-rules` skill and note its `references/` path.

## Step 1 – Prepare

1. Find the project and read project.md. Check cms/ files exist (else ask the user to run "set up this project").
   Run the knowledge freshness check (`references/freshness-check.md`) and show the result; pass any mismatches to every agent.
2. Identify the target story with a read-only lookup by name or slug. If several match, ask which.
3. Check the story's location is editable under project.md (not under "Never touch"). If not, stop and explain.
4. Create the run folder and copy the templates.

## Step 2 – Brief

Launch `content-strategist` with the request and the existing story id. The brief must state exactly what changes and what must stay the same.

## Step 3 – Blueprint

Launch `page-architect` with the run path and the existing story. It keeps unchanged sections as they are and changes only what the brief requires. Skip showing an outline if the structure does not change; otherwise show it and handle component gaps as in create-page.

For translation-only requests, skip the architect: the copywriter adds the language to the existing fields.

## Step 4 – Copy, review, preview

Run `copywriter`, then `content-reviewer` (with the same FAIL loop as create-page), then `cms-operator` in **preview** mode, then `page-mockup-maker` in **update** mode (after/before view). Skip the mock-up only for small text-only changes (three fields or fewer, no structural change) unless the user asks for one. Show the user the **field-by-field diff** (old → new), the mock-up (`mockup.html` in the run folder), the reviewer result, flags, human_checks and assumptions. Ask for explicit approval.

## Step 5 – Save and log

After explicit approval, run `cms-operator` in **save** mode. Report the story id, editor link and that the change is an unpublished draft (the live page is unchanged until a human publishes). Complete log.md, including the knowledge-check result. If the check found mismatches, offer to update the knowledge files to match project.md (`component-librarian` in **sync** mode).

## If the CMS connector is read-only

If `cms-operator` reports it cannot write, tell the user plainly, point them to `change-sheet.md` in the run folder (field-by-field values to paste into the CMS), and record "saved manually by human" in log.md once they confirm. Never look for another way to write to the CMS.
