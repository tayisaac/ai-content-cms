---
name: content-team-rules
description: >
  Shared rules, defaults, file formats and folder conventions for the content-team plugin.
  This skill should be used whenever another content-team skill runs (setup-project, create-page,
  update-page, refresh-catalogue), or when the user asks "what are the content team rules",
  "what defaults does the content team use", or "how is the ContentTeam folder organised".
metadata:
  version: "0.1.0"
---

# Content Team Rules

Apply these rules in every content-team workflow. Pass the absolute paths of the relevant files in this
skill's `references/` folder to every sub-agent, because sub-agents cannot load skills themselves.

## Reference files

| File | Use |
| --- | --- |
| `references/folder-layout.md` | Finding the project, authority order, status markers, run folders |
| `references/formats/mockup.format.md` | Mock-up kit contents and mock-up rules |
| `references/freshness-check.md` | Comparing project.md with the knowledge files at the start of each run |
| `references/defaults/missing-info.md` | What to do when project.md says "unknown" or is silent |
| `references/defaults/seo.md` | SEO rules when project.md has none |
| `references/defaults/writing.md` | Writing rules when project.md has none |
| `references/defaults/accessibility.md` | Always applies |
| `references/formats/*.md` | Shape of every generated file (catalogue, mapping, content model, page patterns, voice notes, blueprint) |
| `references/run-templates/*` | brief.md, blueprint.json, review.md, log.md templates for a run |

## Non-negotiable rules

1. **Drafts only.** Never publish, unpublish, schedule or delete anything in the CMS. Publishing is a human action in the CMS.
2. **One writer.** Only the `cms-operator` agent calls CMS write tools, and only after the user has explicitly approved the exact change in this conversation.
3. **Existing components only.** Never create or modify CMS components, fields, datasources, folders' settings or space settings. A missing component is a "component gap" for developers.
4. **Respect project.md CMS permissions.** Create pages only in "Agents may create and edit drafts in"; edit only where listed; never touch anything under "Never touch". If writable locations are unknown, stop and ask.
5. **No invented facts.** Prices, dates, statistics, names, claims and asset URLs come from project.md, extras/, the CMS, or the user. Otherwise write `[TODO: ...]`.
6. **Human checks.** Anything matching project.md "Always needs a human before saving a draft" is listed in the blueprint `human_checks` and shown to the user before approval.
7. **Strict review when claims are unknown.** If project.md "Must-follow" claims are unknown, the reviewer flags every claim, price, percentage and health or treatment statement for human review.
8. **Say what was assumed.** Every default applied or inference made goes in the blueprint `assumptions` and in the final summary.
9. **Leave a trail.** Every run writes brief.md, blueprint.json, review.md and log.md in its run folder.
10. **Tag** every story created or edited with the tag in project.md (default `ai-draft`), including existing pages and site-wide blocks such as the menu. Add it alongside existing tags; never remove a tag.
11. **Check knowledge freshness.** At the start of every page or catalogue run, compare project.md with the
    knowledge files (`references/freshness-check.md`). project.md always wins; agents never edit project.md.
12. **One CMS connection.** Use only the CMS server named `Storyblok` (tools `mcp__Storyblok__…`). The workspace
    permissions and the agents' tool lists only recognise that name. If the CMS tools appear under any other
    name, such as a connector named by an ID (`mcp__<id>__…`) or `mcp__claude_ai_…`, never call them, even to
    read: stop and tell the user to connect Storyblok through the workspace's `.mcp.json` (Claude Code) or a
    connector named `Storyblok` (Cowork), and to switch the other connection off.

## Language handling

Read project.md "Markets / languages" and the Notes. If the CMS uses field-level translation, write every language into the same story's translated fields; never create separate per-language stories unless project.md says so. Pages in a language marked as needing a human check are listed in `human_checks`.
