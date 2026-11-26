# Knowledge freshness check

Run by the Coordinator at the start of every create-page, update-page and refresh-catalogue run,
right after reading project.md. Read-only. project.md is the authority; the knowledge files in
cms/ and learned/ can fall behind when the human changes project.md.

## What to compare

| project.md says | Check that these agree |
| --- | --- |
| CMS: "Agents may create and edit drafts in" | cms/cms-mapping.md access rules; learned/content-model.md "Agents may create from scratch" for each page type |
| CMS: "Agents may only edit" | cms/cms-mapping.md access rules; learned/content-model.md (edit only) |
| CMS: "Never touch" (and any edit-only global blocks such as the menu) | cms/cms-mapping.md access rules and page-type table; learned/content-model.md global blocks; cms/component-catalogue.md notes such as "never touch" |
| Markets / languages, and Notes on translation | cms/cms-mapping.md locales section |
| Voice: approved CTAs | learned/voice-notes.md CTA list and conflicts |
| CMS: tag for agent stories | cms/cms-mapping.md conventions |
| Site: URL | learned/site-notes.md and learned/page-patterns/*.md (live URLs, port) |
| Pages listed in project.md | learned/content-model.md "Existing pages" |
| (no project.md section) | learned/mockup-kit/kit.md exists and its Generated date is not older than cms/component-catalogue.md; otherwise say mock-ups may be generic or out of date and suggest "build the mock-up kit" |

Also note each knowledge file's Status (draft / reviewed) and its Generated / Updated date.

## What to do with the result

1. **Up to date:** say "Knowledge check: up to date" in one line and continue.
2. **Mismatches:** show one short list before the first agent starts:
   `<file>: says <X>; project.md says <Y>`.
   - Continue the run. project.md wins. Pass the list to every agent and record each item in the
     blueprint `assumptions` ("knowledge file out of date: ...; followed project.md").
   - If a mismatch changes what this run may do (a permission, a never-touch item), state that
     clearly before the Content Strategist starts.
3. **At the end of the run,** offer: "update the knowledge files to match project.md". On a yes, run
   `component-librarian` in **sync** mode with the mismatch list.
4. **project.md looks wrong** (e.g. it lists a page or folder that doesn't exist in the CMS): raise it
   as a question for the human. Never edit project.md.
