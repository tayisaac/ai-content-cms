# Folder layout and conventions

The working folder (the folder Claude Code was opened in, or the folder connected in Cowork; usually named
ContentTeam or a team workspace) contains one subfolder per project:

```
ContentTeam/
  _template/   _example/   _shared/   _archive/      (ignore unless asked)
  <Project>/
    project.md     facts the human wrote; the top authority
    extras/        documents the human dropped in (PDF, Word, Excel, Markdown); read-only for agents
    learned/       content-model.md, page-patterns/*.md, voice-notes.md   (Librarian drafts)
                   mockup-kit/ (site.css, header/footer, component snippets; built by build-mockup-kit)
    cms/           component-catalogue.md, cms-mapping.md                  (Librarian drafts)
    runs/<YYYY-MM-DD>-<slug>/  brief.md, blueprint.json, review.md, preview.md, mockup.html, log.md
```

## Finding the project
- If the working folder itself contains project.md, that is the project.
- Otherwise list subfolders that contain project.md (skip names starting with "_").
  One match: use it. Several: ask the user which. None: tell the user to copy _template/ and fill project.md.

## Authority order (highest first)
1. The user's instruction in this conversation
2. project.md
3. extras/ documents referenced by project.md
4. Files marked "Status: reviewed" in learned/ and cms/
5. The team defaults in this skill's references/defaults/
6. Files marked "Status: draft" (suggestions only)

## Status markers
- Generated files start with "Status: draft". The human changes it to "Status: reviewed".
- Agents may rely on draft files but must list that in the blueprint "assumptions".
- Agents never change a file from draft to reviewed.

## Run folders
- Name: runs/<YYYY-MM-DD>-<short-slug>/ (today's date). Never overwrite an existing run folder; add -2, -3.
- Every run ends with log.md filled from references/run-templates/log.md.
