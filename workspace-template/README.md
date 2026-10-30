# [Team name] content workspace

One workspace per development team. It holds the team's projects (one folder per site) and uses the shared
**content-team** plugin from https://github.com/tayisaac/ai-content-cms. Do not copy the agents or skills
in here: they come from the plugin and are updated centrally.

```
CLAUDE.md                 tells Claude this workspace uses the content-team plugin
.mcp.json                 CMS connection (server name "Storyblok")
.claude/settings.json     registers the marketplace, enables the plugin, CMS permissions (shared)
.claude/settings.local.json   your personal overrides (not committed)
_template/                copy this to start a project
_example/project.md       a filled-in project.md (fictional brand)
<Project>/                one folder per site: project.md, extras/, learned/, cms/, runs/
```

## First-time setup (each person)

1. Make sure git is installed. The plugin repository tayisaac/ai-content-cms is public, so no GitHub login
   is needed for the plugin itself (your team's workspace repository may still need one).
   If installs fail on a machine without a GitHub SSH key, set `CLAUDE_CODE_PLUGIN_PREFER_HTTPS=1`.
2. Clone this workspace and open Claude Code in it. Accept the trust prompt: Claude Code registers the
   `aicontentteam` marketplace and offers to install `content-team`. If it doesn't, run:
   `/plugin marketplace add tayisaac/ai-content-cms` then `/plugin install content-team@aicontentteam`.
3. Approve the `Storyblok` server from `.mcp.json`, run `/mcp` and sign in. Choose only your team's spaces,
   with read and write for stories. If the desktop app's sign-in is refused, sign in once from Terminal:
   `claude`, then `/mcp`.
   Use only this `.mcp.json` server. If Storyblok is also connected as a connector in the Claude app or on
   claude.ai, switch that connector off: its tools have a different name, so the workspace's permission
   rules and the agents' tool lists don't recognise them.
4. Check: ask "list the subagents and skills available in this session" (seven `content-team:` agents, six
   skills) and "try to publish a test story" (must be blocked by the content-team safety check). Saving a
   draft must show a confirmation prompt labelled `[plugin:content-team]`.
5. Requirements: python3 (the safety check needs it); a browser tool (Claude in Chrome or a Playwright
   server) for "build the mock-up kit".

## Start a project

Copy `_template/` to e.g. `MySite/`, fill in `MySite/project.md` (see `_example/project.md`), then say
**"set up the MySite project"**. Review the drafted `learned/` and `cms/` files and mark them
`Status: reviewed`. Pilot with a read-only job, then a small update.

## Updates

The plugin is versioned centrally. Get the latest with `/plugin marketplace update aicontentteam`, or turn on
auto-update in `/plugin` → Marketplaces → aicontentteam. Problems or ideas: open an issue or pull request
on tayisaac/ai-content-cms; don't edit the plugin locally.
