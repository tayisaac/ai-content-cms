# Eval suite for the content-team agents

Behaviour tests for the `content-team` plugin, run with `claude plugin eval`. They live at the repository
root, not in `plugins/content-team/`, so they never ship to teams and changing them needs no version bump.

Each case starts in an empty workspace, seeds it with the fictional ClearView project from `_fixtures/`,
runs one request, and grades the files the agents wrote. No CMS is connected, so nothing reaches Storyblok.

| Case | What it checks |
| --- | --- |
| `reviewer-fails-bad-blueprint` | The reviewer writes FAIL for a blueprint with banned words, a competitor, an unknown component, an invented asset URL and no disclaimer, and leaves the copy alone |
| `reviewer-passes-clean-blueprint` | The reviewer doesn't FAIL a blueprint that follows the rules (PASS or PASS WITH FLAGS) |
| `copywriter-fills-outline` | The copywriter fills the copy with approved CTAs, the promotion disclaimer and the ® mark, keeps all five sections, and invents no prices or banned words |
| `refuses-to-publish` | Asked to publish an approved page, the team says a person publishes in the CMS |

The safety check (`hooks/guard-cms-writes.py`) is tested separately and for free by `scripts/validate.py`.

## Run it

Log in first (`claude` then `/login`) if your session has expired. From the repository root:

```bash
claude plugin eval . --scaffold --allow-tools Write Edit Agent --runs 1 --ablation none --no-publish
```

- `--scaffold` runs each case's `scaffold.sh`, which copies the fixtures in. Only these files we wrote.
- `--allow-tools Write Edit Agent` lets the agents write `review.md` and fill `blueprint.json`.
- `--runs 1 --ablation none` is the cheap check while editing. Before a release, drop both flags to get
  three runs per case plus the no-plugin baseline (`Δ` shows what the plugin adds).
- One case: add `--case copywriter-fills-outline`. One area: `--tag reviewer`.

Results go to `evals/results/` (ignored by git). Open `report.html` there to see each grader's verdict.

## Add a case

Copy a case folder, change `prompt.md` and the graders, and point `scaffold.sh` at a fixture in
`_fixtures/runs/`. Keep fixtures fictional. Prefer `regex` graders on the files the agents write; keep
`llm` graders for short replies. See https://code.claude.com/docs/en/plugin-evals for every option.

Not covered yet: the `cms-operator` agent and the full `create-page`/`update-page` workflows, which need
Storyblok. Test those by hand in a sandbox space (docs/maintaining.md, step 5).
