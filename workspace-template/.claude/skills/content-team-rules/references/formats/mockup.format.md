# Mock-up kit and mock-up format

## Mock-up kit: <project>/learned/mockup-kit/

Captured from the live or dev site by the `build-mockup-kit` skill. Used by `page-mockup-maker`.

```
mockup-kit/
  kit.md            Status, Generated date, source URL; table of components -> snippet files; notes
  site.css          the site's own CSS as captured (fonts may fall back to system fonts)
  header.html       the site header / navigation as rendered
  footer.html       the site footer as rendered
  components/       one real HTML example per component, e.g. hero.html, page-header.html,
                    leadership.html (with one team-member inside), stats.html
```

kit.md starts with:

```
Status: draft
Generated: <date>, source: <URL>
```

and then a table: component | snippet file | captured from (page) | which element holds which field
(e.g. "h1 = heading_line_1 + heading_line_2; p.lead = body"), plus notes on image placeholders,
fonts and anything that didn't capture well. Scripts, tracking, form actions and event handlers are
removed from every snippet.

## Mock-up: runs/<run>/mockup.html

- Self-contained single file, opens in any browser, no network needed.
- Banner at the top: "Mock-up – not the live design. Images are placeholders."
- Create mode: the full proposed page inside the site's header and footer.
- Update mode: "After (proposed)" with changed sections outlined, then "Before (current)" collapsed.
- [TODO] markers highlighted in yellow.
- It is a likeness, not the real site: spacing, fonts and mobile layout may differ slightly.
