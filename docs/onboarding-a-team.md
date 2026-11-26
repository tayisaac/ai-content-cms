# Onboarding a development team

About an hour for the team lead, then about 15 minutes per person.

## 1. Before you start (maintainer)

- Nothing to grant: `tayisaac/ai-content-cms` is public, so anyone can copy the agents and skills. Changes
  still need the maintainer's approval (branch protection on `main`).
- Agree who on the team approves and publishes in the CMS.
- Confirm the team's CMS is supported (Storyblok today). Another CMS needs a CMS variant of the agents first.

## 2. Create the team's workspace repository (team lead)

1. Create an empty private repository on GitHub, e.g. `your-org/contentteam-<team>`. This is the team's
   workspace: everything below goes into it.
2. Clone it, and clone this repository next to it:
   ```bash
   git clone https://github.com/your-org/contentteam-<team>.git
   git clone https://github.com/tayisaac/ai-content-cms.git
   ```
3. Copy everything in `ai-content-cms/workspace-template/` into `contentteam-<team>/`, including the hidden
   `.claude/`, `.mcp.json` and `.gitignore`. Replace `[Team name]` in README.md. Then run
   `ai-content-cms/scripts/update-workspace.sh contentteam-<team>` once: it writes
   `.claude/content-team-files`, the list of shipped files that later updates use to remove files a release
   drops. Keep `.claude/settings.json` as it is: its `hooks` block runs the safety check.
4. If the team's Storyblok MCP server is not the hosted one, change `.mcp.json`. Keep the server name
   `Storyblok`, because the agents' tool lists and the workspace permissions use it. This is the only
   supported connection in Claude Code: people should switch off any Storyblok connector they added in the
   Claude app or on claude.ai, whose tools are named differently and aren't covered by those rules.
5. Commit and push `contentteam-<team>`.

## 3. Set up each person

Follow "First-time setup" in the workspace README: GitHub credential, open in Claude Code, accept the trust
prompt, sign in to Storyblok, run the two checks (agents listed; publishing blocked).

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
- Get updates: in a current clone of `tayisaac/ai-content-cms` (`git pull`), run
  `scripts/update-workspace.sh <workspace>`, read its warnings, then review and commit the changes in the
  workspace. Compare `.claude/content-team-version` with the latest release in `CHANGELOG.md` to see if
  you're behind. The changelog says when a release also needs a hand change.
- The update script doesn't change your `CLAUDE.md` or `.claude/settings.json`. If a release changes either,
  copy the change by hand. For `CLAUDE.md`, replace everything above its "Team notes" section with the new
  `workspace-template/CLAUDE.md`, and keep your Team notes as they are.
- Report problems or ideas as issues on `tayisaac/ai-content-cms`.

## Moving a workspace off the old plugin (0.1.x to 0.2.0)

Until 0.2.0 the agents came from the `content-team` plugin in the `aicontentteam` marketplace. That
marketplace is gone, so plugin installs stay at 0.1.11. To move a workspace:

1. In `.claude/settings.json`, remove `extraKnownMarketplaces` and `enabledPlugins`, and add the `hooks` block
   from `workspace-template/.claude/settings.json`. Keep your permission rules.
2. Replace everything above "Team notes" in `CLAUDE.md` with the new `workspace-template/CLAUDE.md`.
3. Run `scripts/update-workspace.sh <workspace>` and fix anything it warns about. Commit.
4. Each person, once, in Claude Code: `/plugin uninstall content-team@aicontentteam`, then
   `/plugin marketplace remove aicontentteam`. Otherwise every agent and skill loads twice.
5. Check as in "First-time setup": seven agents and six skills listed, publishing blocked, a draft save asks
   for confirmation.
