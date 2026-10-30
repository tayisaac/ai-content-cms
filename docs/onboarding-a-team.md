# Onboarding a development team

About an hour for the team lead, then about 15 minutes per person.

## 1. Before you start (maintainer)

- Nothing to grant: `tayisaac/ai-content-cms` is public, so anyone can install the plugin. Changes still
  need the maintainer's approval (branch protection on `main`).
- Agree who on the team approves and publishes in the CMS.
- Confirm the team's CMS is supported (Storyblok today). Another CMS needs a CMS variant of the plugin first.

## 2. Create the team's workspace repository (team lead)

1. Create an empty private repository, e.g. `your-org/contentteam-<team>`.
2. Copy everything in `workspace-template/` into it, including the hidden `.claude/`, `.mcp.json` and
   `.gitignore`. Replace `[Team name]` in README.md.
3. If the team's Storyblok MCP server is not the hosted one, change `.mcp.json`. Keep the server name
   `Storyblok`, because the agents' tool lists and the workspace permissions use it. This is the only
   supported connection in Claude Code: people should switch off any Storyblok connector they added in the
   Claude app or on claude.ai, whose tools are named differently and aren't covered by those rules.
4. Commit and push.

## 3. Set up each person

Follow "First-time setup" in the workspace README: GitHub credential, open in Claude Code, accept the trust
prompt and the plugin, sign in to Storyblok, run the two checks (agents listed; publishing blocked).

## 4. First project

1. Copy `_template/` to `<Project>/` and fill in `project.md`. The CMS permissions (where agents may create
   and edit, what they never touch), approvers and site URL matter most; "unknown" is fine elsewhere.
2. Ask the CMS admin for a Storyblok role that can't publish, if the plan allows custom roles.
3. Say "set up the <Project> project". Review `learned/` and `cms/`, then mark them `Status: reviewed`.
4. Optional: "build the mock-up kit" while the site is running (needs Claude in Chrome or a Playwright server).
5. Pilot: "refresh the component catalogue" (read-only), then one small update, then one new page. Check the
   drafts and the `runs/` log before anyone publishes.

## 5. Ongoing

- Commit `runs/` folders: they are the audit trail of who approved what.
- Get updates with `/plugin marketplace update aicontentteam` (or turn on auto-update in `/plugin` →
  Marketplaces).
- Report problems or ideas as issues on `tayisaac/ai-content-cms`.
