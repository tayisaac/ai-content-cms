# [Team name] content workspace

One workspace per development team. It holds the team's projects (one folder per site) and a copy of the
shared **content-team** agents, skills and safety check from https://github.com/tayisaac/ai-content-cms.
Don't edit the files in `.claude/agents/`, `.claude/skills/` or `.claude/hooks/`: they are updated centrally
and the update script overwrites local changes.

```
CLAUDE.md                     tells Claude how this workspace uses the content team
.mcp.json                     CMS connection (server name "Storyblok")
.claude/agents/               the content-team agents (copied, don't edit)
.claude/skills/               the content-team skills (copied, don't edit)
.claude/hooks/                the draft-only safety check (copied, don't edit)
.claude/settings.json         CMS permissions and the hook that runs the safety check (shared)
.claude/content-team-version  which content-team version this workspace has
.claude/content-team-files    the files the update script manages
.claude/settings.local.json   your personal overrides (not committed)
_template/                    copy this to start a project
_example/project.md           a filled-in project.md (fictional brand)
<Project>/                    one folder per site: project.md, extras/, learned/, cms/, runs/
```

## First-time setup (each person)

1. Make sure git and python3 are installed (the safety check needs python3).
2. Clone this workspace and open Claude Code in it. Accept the trust prompt: the agents, skills and safety
   check load from `.claude/`. There is nothing to install.
3. Approve the `Storyblok` server from `.mcp.json`, run `/mcp` and sign in. Choose only your team's spaces,
   with read and write for stories. If the desktop app's sign-in is refused, sign in once from Terminal:
   `claude`, then `/mcp`.
   Use only this `.mcp.json` server. If Storyblok is also connected as a connector in the Claude app or on
   claude.ai, switch that connector off: its tools have a different name, so the workspace's permission
   rules and the agents' tool lists don't recognise them.
4. Check: ask "list the subagents and skills available in this session" (seven content-team agents such as
   `cms-operator`, six skills such as `create-page`) and "try to publish a test story" (must be blocked by
   the content-team safety check). Saving a draft must show a confirmation prompt with the reason
   `content-team: … will save … as an unpublished DRAFT`.
5. If you used the old `content-team` plugin, remove it once: `/plugin uninstall content-team@aicontentteam`,
   then `/plugin marketplace remove aicontentteam`. Otherwise every agent and skill loads twice.
6. For "build the mock-up kit": a browser tool (Claude in Chrome or a Playwright server).

## Start a project

Copy `_template/` to e.g. `MySite/`, fill in `MySite/project.md` (see `_example/project.md`), then say
**"set up the MySite project"**. Review the drafted `learned/` and `cms/` files and mark them
`Status: reviewed`. Pilot with a read-only job, then a small update.

## Updates

The content team is versioned centrally. To update, someone on the team runs, from a current clone of
https://github.com/tayisaac/ai-content-cms:

```bash
scripts/update-workspace.sh <path to this workspace>
```

Read its warnings, review the changes, and commit them here. It updates `.claude/agents`, `.claude/skills`,
`.claude/hooks` and `.claude/content-team-version`, and never touches `settings.json`, `CLAUDE.md` or project
folders. The changelog says when a release also needs a hand change. Problems or ideas: open an issue or pull
request on tayisaac/ai-content-cms; don't edit the copied files here.
