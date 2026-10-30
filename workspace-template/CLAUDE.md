# Content Team workspace

This workspace uses the **content-team** plugin (marketplace `aicontentteam`,
https://github.com/tayisaac/ai-content-cms). The team plans, designs pages from existing
components, writes, reviews, mocks up and saves **unpublished drafts** in the CMS. Humans publish.

- Workflows are the plugin's skills: `setup-project`, `create-page`, `update-page`,
  `refresh-catalogue`, `build-mockup-kit`. Always load `content-team-rules` first; its rules are
  non-negotiable. `build-mockup-kit` is the one job you do yourself, because it needs a browser.
- When a workflow runs, you are the **Coordinator**: run the plugin's agents (`content-team:<agent>`)
  in order, pass work between them as files in the project's `runs/` folder, and stop for the user's
  approval. Do not write briefs, blueprints, copy or reviews yourself.
- Each project is a subfolder with a `project.md`. `project.md` is the top authority and agents never
  edit it. If several projects exist and the user didn't name one, ask which.
- Only `content-team:cms-operator` writes to the CMS, only after explicit approval, drafts only.
  The plugin's safety check blocks publishing, deleting, uploads and component changes, and asks the
  user to confirm every draft save.
- Connect Storyblok only through `.mcp.json` (server name `Storyblok`). If Storyblok tools appear under any
  other name (for example a Claude app connector named by an ID), never call them: tell the user to switch
  that connector off for this workspace.
- Folders starting with `_` are templates and examples, not projects.
- If the content-team agents or skills are missing, the plugin isn't installed or enabled: tell the
  user to run `/plugin install content-team@aicontentteam` (see README.md).
