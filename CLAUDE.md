# Working in this repository

This repository holds the `content-team` agents, skills and safety check that every team copies into its
workspace. A change here reaches every team that runs the update script, so keep changes small and reviewed.

## Folders

- `workspace-template/`: what a team copies to make its own workspace.
  - `.claude/agents/`: the seven agents. Only `cms-operator.md` may list CMS write tools.
  - `.claude/skills/`: the workflows (`create-page`, `update-page`, `setup-project`, `refresh-catalogue`,
    `build-mockup-kit`) and `content-team-rules`, which holds the shared rules, defaults, formats and
    run templates under `references/`.
  - `.claude/hooks/guard-cms-writes.py`: the draft-only safety check. The `hooks` block in
    `.claude/settings.json` runs it.
  - `.claude/content-team-version`: the version.
  - `CLAUDE.md`, `README.md`, `.mcp.json`, `_template/`, `_example/`: the rest of a new workspace. Teams copy
    changes to these by hand; the update script doesn't touch them.
- `docs/`: guides for maintainers and teams (onboarding, maintaining, guardrails, the workflow graph, the
  agent and skill tables in `agents-and-skills.md`).
- `scripts/`: `validate.py` (release checks and safety check tests, also run in CI),
  `update-workspace.sh` (copies the agents, skills and safety check into a team workspace) and
  `build-eval-plugin.sh` (builds the throwaway eval plugin).
- `evals/`: the `claude plugin eval` suite for the agents, with fictional fixtures. It loads a throwaway
  plugin built into `.build/` (git-ignored). Not shipped to teams.
- `.github/`: the CI workflows, CODEOWNERS, and the pull request and issue templates.
- `CHANGELOG.md`: one section per version.
- `AI Content Team for CMS — Setup Guide.docx`: the setup guide for teams. Edit it with the docx
  skill, never as raw XML.

## Before opening a pull request

1. Run `python3 scripts/validate.py`, then `scripts/build-eval-plugin.sh` and
   `claude plugin validate --strict .build/content-team`. All must pass.
2. If anything under `workspace-template/.claude/` changed: bump `.claude/content-team-version`, add a
   `## content-team x.y.z (date)` section to `CHANGELOG.md`, and set the `Template version` line in
   `workspace-template/CLAUDE.md` to the same version.
3. Fill in every item of the pull request template. Say why any item is left unticked.

## Keep in step

When a change alters a workflow, an agent's inputs or outputs, or a rule, update these in the same
pull request:
- `docs/graph.md` (nodes, shared state, edges, routing rules)
- `docs/agents-and-skills.md` (skill and agent tables)
- `workspace-template/CLAUDE.md`, `workspace-template/README.md` and the setup guide, if teams need to act
  on the change. Say so in the changelog.

## Never

Git:
- Never commit on `main`. Create a branch for every change and open a pull request into `main`.
- Ask before every `git push`, including tag pushes, even when the change was already approved.
- Never force-push, delete a branch on GitHub, or delete the repository.
- Never push all tags at once (`git push --tags`). Push only the release tag by name.

Safety:
- Never weaken the safety check or the permission rules (`workspace-template/.claude/hooks/`, the `hooks`
  block and the `ask` and `deny` rules in `workspace-template/.claude/settings.json` and
  `docs/managed-settings.example.json`) unless the user asks for that specific change. Explain the risk in
  the pull request.
- Never give any agent `execute_destructive` or `upload_asset` tools, or give CMS write tools to any
  agent other than `cms-operator`.
- Never add a rule or step that lets the team publish, unpublish, delete, or change components or
  settings in the CMS.
- Never make `update-workspace.sh` edit a team's `settings.json`, `settings.local.json`, `CLAUDE.md` or
  project folders.

Releases:
- Never release a change to `workspace-template/.claude/` without a version bump; teams can't tell they're
  behind.
- Never ship or publish the eval build (`.build/`) or bring back a marketplace without the user
  asking for it.

Content:
- Never commit project data, credentials, `settings.local.json` or personal settings. Example
  content stays fictional (`workspace-template/_example/`).
