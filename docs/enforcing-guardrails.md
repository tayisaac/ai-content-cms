# Enforcing the guardrails (optional, needs IT)

Without this, the safety check runs from the hook in each workspace's `.claude/settings.json`. A team member
could edit or delete that hook, or add their own permissions. Claude Code's managed settings, deployed by IT
to company machines, make the guardrails non-negotiable. Managed settings override user, project and local
settings.

File location: macOS `/Library/Application Support/ClaudeCode/managed-settings.json`, Linux/WSL
`/etc/claude-code/managed-settings.json`, Windows `C:\Program Files\ClaudeCode\managed-settings.json`.

See [managed-settings.example.json](managed-settings.example.json). What it does:

- Runs the safety check hook for every session, whatever a workspace's settings say. It runs
  `.claude/hooks/guard-cms-writes.py` from the folder Claude Code was opened in. Outside a content-team
  workspace that file doesn't exist, so the hook fails and **every** matching CMS write is blocked (it fails
  closed). That's intended: CMS writes belong in a workspace.
- `strictKnownMarketplaces: []`: no plugin marketplaces may be added. Content-team no longer needs one. Add
  entries if people use other marketplaces, or remove the key.
- Denies the Storyblok destructive and upload tools for every session, whatever a workspace says. The rules
  use `mcp__*__…`, so they also match a Storyblok connector named by an ID or `mcp__claude_ai_…`, whose ID
  can differ between accounts.

The managed hook still runs the script from the workspace, so someone who edits
`.claude/hooks/guard-cms-writes.py` itself could weaken it. If that matters, IT can install the script at a
fixed path on each machine and point the managed hook's command there instead.

Stronger options, only if every hook and permission rule should come from IT:
`allowManagedHooksOnly` (only managed hooks run, so the workspace hook is ignored and the managed one above
does the job) and `allowManagedPermissionRulesOnly`. Test on one machine before rolling out.

Reference: https://code.claude.com/docs/en/managed-settings
