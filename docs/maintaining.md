# Maintaining the team

## Who changes what

| Change | Where | Who |
| --- | --- | --- |
| Agents, skills, rules, defaults, formats | `workspace-template/.claude/agents/` and `skills/` in this repository | Pull request, approved by the maintainer |
| Safety check and permissions | `workspace-template/.claude/hooks/`, `workspace-template/.claude/settings.json`, `docs/managed-settings.example.json` | Pull request, maintainer approval required (CODEOWNERS) |
| A site's facts, permissions, voice | `<Project>/project.md` in the team's workspace | That team |
| A site's knowledge (catalogue, mapping, patterns, mock-up kit) | `<Project>/learned/`, `<Project>/cms/` | Drafted by the team's agents, reviewed by that team |

Teams get the agents, skills and safety check as copies in their workspace's `.claude/`. They should not edit
those files: `scripts/update-workspace.sh` overwrites them on the next update. If a team needs different
behaviour, make it configurable through `project.md` instead. Files a team adds itself in `.claude/agents/`
or `.claude/skills/` are left alone by updates, as long as their names don't clash with ours.

## Release a new version

1. Branch, make the change in `workspace-template/.claude/`.
2. Bump the version (x.y.z) in `workspace-template/.claude/content-team-version` and in the
   `Template version` line of `workspace-template/CLAUDE.md`.
3. Add a `## content-team x.y.z (date)` section at the top of `CHANGELOG.md`. If teams must change something
   the update script doesn't touch (`CLAUDE.md`, `.claude/settings.json`, `.mcp.json`), say so there.
4. Run `python3 scripts/validate.py`, then `scripts/build-eval-plugin.sh` and
   `claude plugin validate --strict .build/content-team` locally (the GitHub Action runs all three on the
   pull request).
5. If agents or skills changed, run the eval suite (see `evals/README.md`). Add a case when you add a rule an
   agent must follow. The suite has no CMS, so also test by hand: make a scratch workspace with
   `scripts/update-workspace.sh <scratch folder>`, open it in Claude Code, connect a sandbox Storyblok space,
   then run one read-only job and the publish-blocked check.
6. Merge, then tag the release and push only that tag:
   `git tag content-team--vX.Y.Z && git push origin content-team--vX.Y.Z`.
7. Tell the teams: they `git pull` this repository and run `scripts/update-workspace.sh <workspace>`, then
   commit the result in their workspace.

Version guide: patch (0.x.y) for wording and fixes, minor (0.x.0) for new skills, agents or workflow steps,
or changes teams must act on, major once the team is stable and something breaks existing workspaces
(renamed agents, new required project.md fields).

## Rename or remove an agent or skill

The update script removes files an earlier version shipped and this one doesn't, using
`.claude/content-team-files` in each workspace. So deleting or renaming a file here reaches teams on their next
update. Say in the changelog what was renamed, because anything that called it by its old name stops working.

## Adding a CMS

Keep one set of agents. Add the new CMS's tool names to the Librarian, CMS Operator and Strategist, its allowed draft
calls to the safety check, and a CMS line to `project.md` so each project picks its CMS. Bump the minor
version.
