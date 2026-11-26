## What changes and why

## Checklist
- [ ] Version bumped in `workspace-template/.claude/content-team-version` and the `Template version` line
- [ ] `CHANGELOG.md` section added
- [ ] `python3 scripts/validate.py` passes
- [ ] Agents or skills changed? `scripts/build-eval-plugin.sh` then the eval suite run (see `evals/README.md`), scores noted above
- [ ] Tested in a scratch workspace (one read-only job; publishing still blocked)
- [ ] Safety check or permissions changed? Explain the risk above
- [ ] No project data, credentials or personal settings in this pull request
