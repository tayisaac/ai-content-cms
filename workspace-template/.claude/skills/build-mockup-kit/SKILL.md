---
name: build-mockup-kit
description: >
  This skill should be used when the user asks to "build the mock-up kit", "refresh the mock-up kit",
  "capture the site design for mock-ups", or when a create-page or update-page run finds that the
  project has no learned/mockup-kit or that it is out of date.
metadata:
  version: "0.1.0"
---

# Build Mock-up Kit

Capture the site's look so `page-mockup-maker` can show proposed pages realistically. The Coordinator
does this itself, because it needs a browser and agents have none. It writes only into
`<project>/learned/mockup-kit/`. It never writes to the CMS.

First load the `content-team-rules` skill and read `references/formats/mockup.format.md`.

## Step 1 – Prepare

1. Find the project and read project.md (site URL), learned/site-notes.md and learned/page-patterns/*.md.
2. If the site is a local dev server, ask the user for the current URL or port (it changes between runs).
3. Check that a browser tool is available (Cowork's built-in browser, or Claude in Chrome / Playwright in
   Claude Code). If none is available, say so and stop: mock-ups will use generic styling until a kit exists.

## Step 2 – Choose pages

Pick the fewest pages that together show every component in cms/component-catalogue.md that appears on the
site (use site-notes.md and the page patterns to see which page shows which component). Include the home page
for the header and footer.

## Step 3 – Capture (run JavaScript in each page)

- **CSS:** concatenate the text of every same-origin stylesheet rule (document.styleSheets -> cssRules) plus
  inline style tags. Skip rules that fail to read. Capture once; reuse across pages.
- **Header and footer:** outerHTML of the site header and footer.
- **Sections:** outerHTML of each direct child of the main element, in order.
- **Clean every snippet:** remove script, noscript, iframe and form action attributes, inline event handlers
  (on*), data-* tracking attributes and srcset; replace image sources with an empty placeholder.
- Map each section to its component using the page pattern for that page (sections appear in the same order
  as the pattern). Where a component contains repeating items (team members, stats, cards), keep the
  container plus one or two items.

## Step 4 – Write the kit

Write `site.css`, `header.html`, `footer.html` and `components/<component>.html` (one per component; prefer
the most complete example), then `kit.md` per the format, starting with `Status: draft` and the Generated
line. List components with no snippet (not shown on any page) so mock-ups mark them as approximate.

## Step 5 – Check and report

Build a quick test page from the kit (header, two components, footer) as a run-free `mockup-kit/kit-preview.html`
and look at it in the browser if possible. Report: pages captured, components with snippets, components
without, and anything that didn't capture well (fonts, icons). Remind the user the kit is a draft to glance
over, and to rebuild it when the site design changes.
