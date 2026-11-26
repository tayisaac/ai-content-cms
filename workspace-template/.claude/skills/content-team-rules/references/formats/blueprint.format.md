# Page blueprint format (runs/<run>/blueprint.json)

The single hand-off file between agents. CMS-neutral: section and field names come from
learned/content-model.md and cms/component-catalogue.md, never invented.

- action: "create" | "update"
- existing_story_id: CMS story id when action is "update", else null
- page_type, folder, slug: must match project.md writable folders and the content model
- languages: list of language codes; first is the default. Every text field is an object keyed by language
- sections: ordered list. Each has id, section (neutral name), component (catalogue name),
  variant (or null), purpose (one line), fields (only fields the catalogue lists for that component)
- Images: never invent asset URLs. Give "brief" (what to show) and "alt"; "asset" stays null unless the
  user supplied an existing CMS asset
- component_gaps: sections no catalogue component can serve; the Coordinator asks the human to decide
- assumptions: every default or inference used (e.g. "SEO defaults applied")
- human_checks: items that need a human per project.md "Always needs a human" (e.g. treatment claim in s3)
- Unknown facts (prices, dates, figures, names) are written as [TODO: ...], never invented

Who writes what:
- Page Architect: everything except copy (text fields left as "" or a short note in purpose)
- Copywriter: fills text fields and image alt text; adds languages if requested
- Reviewer: does not edit; writes review.md and sets review.result
- CMS Operator: fills saved.story_id and saved.preview after saving
