# AI Content Team for CMS

A multi-agent content team for headless CMS sites. Many development teams use one centrally maintained
team: each team copies its agents, skills and safety check into its own workspace and updates them from
here. It plans pages, designs them from existing CMS components, writes and reviews copy, shows an HTML
mock-up and saves **unpublished drafts**. Humans publish.

| | |
| --- | --- |
| Name | `content-team` (see [CHANGELOG.md](CHANGELOG.md) for the current version) |
| CMS today | Storyblok (CMS-swappable by design) |
| Maintainer | @tayisaac |

## What's in this repository

```
workspace-template/               copy this to create a team's own workspace repository
  .claude/agents/                 the 7 agents
  .claude/skills/                 the 6 skills, including content-team-rules and its references
  .claude/hooks/                  guard-cms-writes.py, the draft-only safety check
  .claude/settings.json           CMS permissions and the hook that runs the safety check
  .claude/content-team-version    the current version
scripts/update-workspace.sh       copies or updates the agents, skills and safety check in a team workspace
scripts/validate.py               release checks (also run by GitHub Actions on every pull request)
scripts/build-eval-plugin.sh      builds a throwaway plugin from workspace-template/.claude for the evals
evals/                            behaviour tests for the agents (not shipped)
docs/                             onboarding, maintaining, enforcing the guardrails, agents and skills
CHANGELOG.md                      one section per release
```

## How it fits together

- **This repository** owns the team: agents, skills, rules, safety check. One version for everyone.
- **Each development team** has its own workspace repository, made from `workspace-template/`. It holds the
  team's projects (one folder per site, each with `project.md`, `extras/`, `learned/`, `cms/`, `runs/`) and
  a copy of the agents, skills and safety check in `.claude/`. Teams change behaviour through their
  `project.md` and knowledge files, not by editing agents.
- **People** install nothing: cloning the team's workspace and opening it in Claude Code is enough.
- **Updates** reach a team when someone runs `scripts/update-workspace.sh <workspace>` from a current copy of
  this repository and commits the result in the workspace. Nothing updates automatically.

## Quick start

- **A new team:** follow [docs/onboarding-a-team.md](docs/onboarding-a-team.md).
- **Updating a team's workspace:**
  ```bash
  git clone https://github.com/tayisaac/ai-content-cms.git   # or git pull in an existing clone
  ai-content-cms/scripts/update-workspace.sh path/to/team-workspace
  ```
  The repository is public, so no GitHub login is needed. Only the maintainer can change it; everyone else
  proposes changes through pull requests.
- **Changing the team:** see [docs/maintaining.md](docs/maintaining.md). All changes go through pull requests.

## Guardrails (all teams)

Drafts only (a safety check blocks publish, unpublish, delete, uploads and component changes) · only the CMS
Operator writes, after explicit approval · existing components only · `project.md` is the top authority and
agents never edit it · every story agents touch gets the `ai-draft` tag.
