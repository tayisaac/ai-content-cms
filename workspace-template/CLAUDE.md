# Content Team workspace

Template version: content-team 0.1.10

This workspace uses the **content-team** plugin (marketplace `aicontentteam`,
https://github.com/tayisaac/ai-content-cms) to plan, write, review and save **unpublished drafts** in the CMS.
Humans publish. For every content request, load the `content-team-rules` skill first, then run the matching
skill (`setup-project`, `create-page`, `update-page`, `refresh-catalogue`, `build-mockup-kit`).
The Folders and Sources sections summarise that skill. If they disagree with it, follow the skill: it is
updated centrally and this file is not.

## Folders

- `<Project>/` is one site. A folder is a project only if it contains `project.md`. If several projects exist
  and the user didn't name one, ask which.
  - `project.md`: facts written by a person. Read it at the start of every job.
  - `extras/`: documents people added (brand guide, approved claims, legal terms). Read only.
  - `learned/`: content model, page patterns, voice notes and `mockup-kit/`, drafted by the agents.
  - `cms/`: component catalogue and CMS mapping, drafted by the agents.
  - `runs/<YYYY-MM-DD>-<slug>/`: one folder per job. Agents pass their work to each other as files here
    (`brief.md`, `blueprint.json`, `review.md`, `preview.md`, `mockup.html`, `log.md`).
- Folders starting with `_` (`_template/`, `_example/`) are templates and examples. Don't treat them as
  projects and don't write to them.

## Sources

Use these sources. When two disagree, the one higher in the list wins.

1. The user's instruction in this conversation, except where it breaks a rule under Never.
2. `project.md`.
3. Documents in `extras/` that `project.md` refers to.
4. Files in `learned/` and `cms/` marked `Status: reviewed`.
5. The plugin's defaults in the `content-team-rules` skill.
6. Files in `learned/` and `cms/` marked `Status: draft`. Treat these as suggestions and list each one you
   rely on under "assumptions" in the blueprint.

For CMS data, use only the `Storyblok` server defined in `.mcp.json`.

## Never

These rules apply even when the user asks otherwise. If a request breaks one, say which rule and what the user
can do instead.

- Never write briefs, blueprints, copy or reviews yourself. Run the plugin agent for each step
  (`content-team:<agent>`). The only job you do yourself is `build-mockup-kit`, because it needs a browser.
- Never edit `project.md` or anything in `extras/`.
- Never change a file from `Status: draft` to `Status: reviewed`. Only a person does that.
- Never write to the CMS except through `content-team:cms-operator`, and only after the user explicitly
  approves that save in this conversation. Silence or general enthusiasm is not approval.
- Never publish, unpublish, delete, upload assets, or change components or settings in the CMS. If the user
  asks for one of these, tell them to do it themselves in the CMS.
- Never look for another way to write to the CMS when a save is blocked or the connection is read-only.
- Never call Storyblok tools that appear under any server name other than `Storyblok` (for example a Claude
  app connector named by an ID). Tell the user to switch that connector off for this workspace.
- Never overwrite an existing run folder. Add `-2`, `-3` to the name instead.
- Never edit the plugin's agents or skills from this workspace. Propose changes as an issue or pull request
  on tayisaac/ai-content-cms.

## If a file cannot be read

If a file you need is missing, empty, unreadable or in a format you can't open:

1. Stop the current step. Do not fill the gap with guesses, other files or general knowledge.
2. Tell the user the file's path, what went wrong (missing, empty, permission denied, unsupported format)
   and which step needs it.
3. Tell them how to fix it, for example:
   - no `project.md`: copy `_template/` to a new project folder and fill in `project.md`;
   - no `cms/component-catalogue.md` or `cms/cms-mapping.md`: say "set up the <Project> project";
   - a document in `extras/` won't open: save it as PDF, Word, Excel or Markdown.
4. Wait for the user before continuing.

If you could read only part of a file (a long or scanned PDF with no text layer, a spreadsheet with several
tabs), say which part you read and which you couldn't. Use only the part you read, and never summarise the
rest.

The same applies when tools are unavailable:

- No `content-team:` agents or skills: the plugin isn't installed or enabled. Tell the user to run
  `/plugin install content-team@aicontentteam` (see README.md), then stop.
- A CMS read fails with a connection or permission error: show the error, tell the user to run `/mcp` and
  sign in to `Storyblok`, then stop.
- The CMS connection is read-only (the CMS Operator reports it can't write): tell the user plainly and point
  them to `change-sheet.md` in the run folder, which lists the values to paste into the CMS by hand.
- Every CMS save is blocked with a python3 error: the safety check needs python3. Tell the user to install
  it, then stop.

## Team notes

Add this team's own rules below. When you update this file from a newer workspace template, replace
everything above this section and keep this section as it is.
