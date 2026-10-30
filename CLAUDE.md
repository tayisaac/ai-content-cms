# Working in this repository

This repository is the `aicontentteam` marketplace. It holds the `content-team` plugin, which every
team receives. A change here reaches every team that updates the plugin, so keep changes small and
reviewed.

## Folders

- `.claude-plugin/marketplace.json`: the marketplace catalogue. Lists plugins and their source folders.
- `plugins/content-team/`: the plugin itself.
  - `agents/`: the seven agents. Only `cms-operator.md` may list CMS write tools.
  - `skills/`: the workflows (`create-page`, `update-page`, `setup-project`, `refresh-catalogue`,
    `build-mockup-kit`) and `content-team-rules`, which holds the shared rules, defaults, formats and
    run templates under `references/`.
  - `hooks/`: `hooks.json` and `guard-cms-writes.py`, the draft-only safety check.
  - `.claude-plugin/plugin.json`: the plugin's name and version.
- `workspace-template/`: what a team copies to make its own workspace. Changes here don't reach
  existing workspaces; teams copy them by hand.
- `docs/`: guides for maintainers and teams (onboarding, maintaining, guardrails, the workflow graph).
- `scripts/`: `validate.py` (release checks, also run in CI) and `build-cowork-plugin.sh`.
- `.github/`: the CI workflow, CODEOWNERS, and the pull request and issue templates.
- `CHANGELOG.md`: one section per plugin version.
- `AI Content Team for CMS — Setup Guide.docx`: the setup guide for teams. Edit it with the docx
  skill, never as raw XML.

## Before opening a pull request

1. Run `python3 scripts/validate.py` and `claude plugin validate --strict .`. Both must pass.
2. If anything under `plugins/content-team/` changed: bump `version` in `plugin.json`, add a
   `## content-team x.y.z (date)` section to `CHANGELOG.md`, and set the `Template version` line in
   `workspace-template/CLAUDE.md` to the same version.
3. Fill in every item of the pull request template. Say why any item is left unticked.

## Keep in step

When a change alters a workflow, an agent's inputs or outputs, or a rule, update these in the same
pull request:
- `docs/graph.md` (nodes, shared state, edges, routing rules)
- `plugins/content-team/README.md` (skill and agent tables)
- `workspace-template/CLAUDE.md` and the setup guide, if teams need to act on the change.
  Say so in the changelog.

## Never

Git:
- Never commit on `main`. Create a branch for every change and open a pull request into `main`.
- Ask before every `git push`, including tag pushes, even when the change was already approved.
- Never force-push, delete a branch on GitHub, or delete the repository.
- Never push all tags at once (`git push --tags`). Push only the release tag by name.

Plugin safety:
- Never weaken the safety check or the permission rules (`hooks/`, the `ask` and `deny` rules in
  `workspace-template/.claude/settings.json` and `docs/managed-settings.example.json`) unless the
  user asks for that specific change. Explain the risk in the pull request.
- Never give any agent `execute_destructive` or `upload_asset` tools, or give CMS write tools to any
  agent other than `cms-operator`.
- Never add a rule or step that lets the team publish, unpublish, delete, or change components or
  settings in the CMS.

Releases:
- Never change the plugin's `name` or set `version` in `marketplace.json`. `plugin.json` holds the
  version.
- Never release a change to `plugins/content-team/` without a version bump; teams won't receive it.

Content:
- Never commit project data, credentials, `settings.local.json` or personal settings. Example
  content stays fictional (`workspace-template/_example/`).
