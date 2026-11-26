# Changelog

Each release bumps `workspace-template/.claude/content-team-version`. Teams get a release by running
`scripts/update-workspace.sh` and compare their `.claude/content-team-version` with this file to see if they
are behind. (Up to 0.1.11 the version was in the plugin's `plugin.json`.)

## content-team 0.2.0 (2026-11-26)
- **No more plugin.** The `aicontentteam` marketplace and the `content-team` plugin are gone. The agents,
  skills and safety check now live in `workspace-template/.claude/` and each team keeps a copy in its
  workspace's `.claude/`. Agents and skills go by their plain names (`cms-operator`, `create-page`) instead
  of `content-team:<name>`. Their behaviour hasn't changed.
- New `scripts/update-workspace.sh <workspace>`: copies or updates the agents, skills and safety check, and
  removes files a release drops (tracked in `.claude/content-team-files`). It never edits `settings.json`,
  `CLAUDE.md` or project folders. It warns if the safety check hook is missing or the old plugin is still
  enabled.
- The safety check now runs from a `hooks` block in the workspace's `.claude/settings.json` instead of the
  plugin. The check itself, its matcher and the permission rules haven't changed. Risk: a team member can
  edit or delete that block, which was harder with the plugin. The update script warns when it's missing,
  validate.py checks the template, and the managed-settings example now deploys the same hook (and sets
  `strictKnownMarketplaces` to `[]` instead of listing the retired marketplace).
- Cowork is no longer supported (it needs a `.plugin` file); `build-cowork-plugin.sh` is removed.
- Evals: `scripts/build-eval-plugin.sh` builds a throwaway plugin from `workspace-template/.claude/` into
  `.build/` (git-ignored, never shipped) so `claude plugin eval` and `claude plugin validate` still
  run. CI builds it first.
- **Teams must act** (see "Moving a workspace off the old plugin" in docs/onboarding-a-team.md): in
  `.claude/settings.json` remove `extraKnownMarketplaces` and `enabledPlugins` and add the `hooks` block;
  replace `CLAUDE.md` above Team notes; run `update-workspace.sh`; each person uninstalls the plugin and
  removes the marketplace. Plugin installs stay at 0.1.11.

## content-team 0.1.11 (2026-11-11)
- content-reviewer can now Edit, and sets only `review.result` in blueprint.json with it, instead of having to
  rewrite the whole file with Write. It sets the result even when the caller says not to change the copy.
- content-reviewer finds the team defaults and review template when called outside a workflow: its
  description tells the caller to load content-team-rules and pass the paths, and the agent searches for them
  if they are missing. Without them it says so in review.md and flags the SEO and accessibility checks.
- Found by the new eval suite (`evals/`). Existing workspaces need no changes.

## content-team 0.1.10 (2026-10-30)
- Workspace template's CLAUDE.md rewritten into four sections: Folders, Sources, Never, and If a file cannot
  be read. The Never rules apply even when the user asks otherwise. When a file can't be read, Claude stops
  and explains instead of guessing, says which part of a partly read file it used, and covers read-only CMS
  connections and a missing python3.
- The file says the `content-team-rules` skill wins if the two disagree, starts with a
  `Template version: content-team x.y.z` line (validate.py checks it matches plugin.json), and ends with a
  Team notes section that teams keep when updating.
- Existing workspaces: copy the new `workspace-template/CLAUDE.md` into your workspace by hand (see
  docs/onboarding-a-team.md). Plugin agents and skills are unchanged.

## content-team 0.1.9 (2026-10-30)
- Safety check asks the user to confirm every draft save it allows (`[plugin:content-team]` prompt), so the
  prompt appears even when Storyblok is connected under another name, such as a connector named by an ID,
  that the workspace's permission rules don't match.
- One CMS connection: in Claude Code, Storyblok is connected only through the workspace's `.mcp.json`
  (server `Storyblok`). New rule 12 in content-team-rules and a check in setup-project: if the CMS tools
  appear under any other name, the workflow stops instead of using them. README, workspace template and
  onboarding docs updated.
- Workspace template and managed-settings example: the ask and deny rules now use `mcp__*__…`
  (`execute_mutating` asks; `execute_destructive`, `upload_asset`, `upload_asset_finish` are denied), so they
  match Storyblok under any server name, including connectors named by an ID that differs per account.
  Read allow rules stay on `mcp__Storyblok__…`. validate.py checks these rules.

## content-team 0.1.8 (2026-10-16)
- Repository renamed to tayisaac/ai-content-cms: links, install commands, the workspace template's
  marketplace source and the managed-settings example now use the new name. No behaviour change.
  The marketplace (aicontentteam) and plugin (content-team) names are unchanged.

## content-team 0.1.7 (2026-10-14)
- First release from this marketplace (aicontentteam). Same behaviour as 0.1.6.
- Wording made host-neutral (Claude Code or Cowork) in the README, folder layout and catalogue format.
- Plugin description now says seven agents.

## content-team 0.1.6 (2026-10-09)
- New agent page-mockup-maker: self-contained HTML mock-up of the proposed page (before/after for updates).
- New skill build-mockup-kit: captures the site's CSS, header, footer and one snippet per component.
- create-page and update-page show the mock-up at the approval step.

## content-team 0.1.5 (2026-10-08)
- Tagging rule: every story agents create or edit gets the ai-draft tag; existing tags are kept.

## content-team 0.1.4 (2026-10-08)
- Knowledge freshness check at the start of every run; Librarian sync mode. Agents never edit project.md.

## content-team 0.1.3 (2026-10-08)
- Safety check also covers connectors whose tools are named by an ID.

## content-team 0.1.0 – 0.1.2 (2026-10-07)
- Initial team: strategist, page architect, copywriter, reviewer, component librarian, CMS operator;
  setup-project, create-page, update-page, refresh-catalogue; draft-only safety check.
