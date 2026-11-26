---
name: refresh-catalogue
description: >
  This skill should be used when the user asks to "refresh the component catalogue", "update the
  catalogue", "developers changed the components", "re-scan the CMS components", or when a content-team
  workflow finds that cms/component-catalogue.md is older than recent component changes.
metadata:
  version: "0.1.0"
---

# Refresh Catalogue

Re-read the CMS components and report what changed. Coordinate the `component-librarian` agent.

1. Load the `content-team-rules` skill. Find the project per `references/folder-layout.md`.
2. Launch `component-librarian` in **refresh** mode with the project folder path and the format file paths.
3. Report to the user: components added, removed or changed; mapping entries and page patterns affected; whether the new catalogue replaced a draft or was written as `.new.md` beside a reviewed file.
4. If cms/cms-mapping.md is affected, recommend the user reviews it with a developer before the next page is saved.
5. Run the knowledge freshness check (`references/freshness-check.md`). A component refresh does not pick up permission changes in project.md, so report any mismatches and offer `component-librarian` in **sync** mode.
