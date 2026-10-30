# content-team

A seven-agent content team for a headless CMS (built for Storyblok, designed to swap). It plans, designs pages
from existing components, writes, reviews and saves **unpublished drafts**. Humans publish.

## Install (Claude Code)

```
/plugin marketplace add tayisaac/ai-content-cms
/plugin install content-team@aicontentteam
```

Or open a workspace made from `workspace-template/`: its `.claude/settings.json` registers the marketplace and
enables the plugin. In Claude Code the agents are named `content-team:<agent>`.

## Skills (ask in plain words)

| Say | Skill | What happens |
| --- | --- | --- |
| "Set up the MySite project" | setup-project | Checks project.md and CMS access; Librarian drafts the catalogue, mapping, content model, page patterns and voice notes |
| "Create a page for …" | create-page | Brief → blueprint → copy → review → preview → your approval → draft saved |
| "Update the … page" / "Translate … into Italian" | update-page | Same, with a field-by-field diff of the existing page |
| "Build the mock-up kit" | build-mockup-kit | Captures the site's look (CSS, header, footer, one snippet per component) so mock-ups look like the site |
| "Refresh the component catalogue" | refresh-catalogue | Re-reads components after developer changes and reports what changed |
| (used automatically) | content-team-rules | Shared rules, defaults, formats and folder conventions |

## Agents

| Agent | Job | CMS access |
| --- | --- | --- |
| content-strategist | Brief: new vs update, goal, audience, messages, location | Read |
| page-architect | Blueprint from existing components; flags component gaps | None |
| copywriter | Copy in brand voice, all languages | None |
| content-reviewer | Structure, facts, compliance, voice, SEO, accessibility; PASS/FAIL | None |
| component-librarian | Drafts cms/ and learned/ files from the CMS | Read |
| page-mockup-maker | Self-contained HTML mock-up of the proposed page (before/after for updates) | None |
| cms-operator | Preview diff; saves drafts after explicit approval | Read + draft write |

## Safety

- A safety check (hooks/guard-cms-writes.py) runs before every write, delete or upload call on any
  connected server, including Storyblok connectors whose tools are named by an ID. It allows only
  `createStory` / `updateStory` without publish, force-update, AI-translate or per-language publish options, and blocks publishing, deleting, asset uploads and
  component or settings changes. It fails closed. Every draft save it allows still shows the user a
  confirmation prompt (labelled `[plugin:content-team]`), whatever the server is called.
- The workspace template's permission rules back this up: draft saves ask and deletes and uploads are
  denied on any server (`mcp__*__execute_mutating`, `mcp__*__execute_destructive`, `mcp__*__upload_asset*`),
  so they also cover connectors named by an ID. Reads are pre-approved only for the `Storyblok` server,
  because allow rules can't use a wildcard for the server name.
- If the connector is read-only, the CMS Operator writes `change-sheet.md` for a human to paste instead.

## Requirements

- Claude Code (opened in a team workspace folder) or Cowork (with a connected folder). The workspace holds one
  subfolder per project with a project.md (see the content-team-rules skill and workspace-template/ in the repo).
- A Storyblok MCP server named `Storyblok`: in Claude Code, the workspace's `.mcp.json` (the only supported
  connection; switch off any Storyblok connector added in the Claude app or on claude.ai); in Cowork, the
  Storyblok connector (Settings → Connectors). Agent tool lists and the workspace permissions use the names
  `mcp__Storyblok__search`, `…__describe`, `…__execute_readonly`, `…__execute_mutating`. If the CMS tools
  appear under any other name (for example a connector named by an ID), the workflows stop and ask you to
  fix the connection instead of using them.
- python3 for the safety check (if missing, all CMS writes are blocked).

## Swapping CMS

Connect the new CMS, update the tool names in component-librarian.md, cms-operator.md and content-strategist.md,
adjust the hook matcher and allowed operations, then run "set up this project" to regenerate cms/.
