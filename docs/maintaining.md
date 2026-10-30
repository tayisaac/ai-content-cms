# Maintaining the team

## Who changes what

| Change | Where | Who |
| --- | --- | --- |
| Agents, skills, rules, defaults, formats | `plugins/content-team/` in this repository | Pull request, approved by the maintainer |
| Safety check and permissions | `plugins/content-team/hooks/`, `workspace-template/.claude/settings.json` | Pull request, maintainer approval required (CODEOWNERS) |
| A site's facts, permissions, voice | `<Project>/project.md` in the team's workspace | That team |
| A site's knowledge (catalogue, mapping, patterns, mock-up kit) | `<Project>/learned/`, `<Project>/cms/` | Drafted by the team's agents, reviewed by that team |

Teams should not override plugin agents with same-named files in their workspace's `.claude/agents/`: a
project agent wins over the plugin's and silently stops receiving updates. If a team needs different
behaviour, make it configurable through `project.md` instead.

## Release a new version

1. Branch, make the change in `plugins/content-team/`.
2. Bump `version` in `plugins/content-team/.claude-plugin/plugin.json` (x.y.z). Without a bump, users never
   receive the change. Don't put `version` in `marketplace.json`.
3. Add a `## content-team x.y.z (date)` section at the top of `CHANGELOG.md`, and set the
   `Template version` line in `workspace-template/CLAUDE.md` to the same version. If the release changes the
   workspace template, say in the changelog that teams must copy it into their workspaces by hand.
4. Run `python3 scripts/validate.py` and `claude plugin validate --strict .` locally (the GitHub Action runs
   both on the pull request).
5. Test it: in a scratch workspace run `/plugin marketplace add <path to your clone>` and
   `/plugin install content-team@aicontentteam`, then run one read-only job and the publish-blocked check.
6. Merge, then tag the release: `git tag content-team--vX.Y.Z && git push --tags`.
7. Tell the teams; they run `/plugin marketplace update aicontentteam` (or receive it via auto-update).
8. Cowork users: run `scripts/build-cowork-plugin.sh` and share the `.plugin` file it builds.

Version guide: patch (0.1.x) for wording and fixes, minor (0.x.0) for new skills, agents or workflow steps,
major for changes teams must act on (renamed agents, new required project.md fields).

## Rename or retire

Never change a plugin's `name`; add a `renames` entry to `marketplace.json` if you must. Removing a plugin:
map it to `null` in `renames`.

## Adding a CMS

Keep one plugin. Add the new CMS's tool names to the Librarian, CMS Operator and Strategist, its allowed draft
calls to the safety check, and a CMS line to `project.md` so each project picks its CMS. Bump the minor
version.
