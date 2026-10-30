# Enforcing the guardrails (optional, needs IT)

Without this, the safety check runs from the plugin, but a determined user could disable the plugin or add
their own permissions. Claude Code's managed settings, deployed by IT to company machines, make the
guardrails non-negotiable. Managed settings override user, project and local settings.

File location: macOS `/Library/Application Support/ClaudeCode/managed-settings.json`, Linux/WSL
`/etc/claude-code/managed-settings.json`, Windows `C:\Program Files\ClaudeCode\managed-settings.json`.

See [managed-settings.example.json](managed-settings.example.json). What it does:

- Registers this marketplace for everyone, turns on auto-update and enables `content-team`.
- `strictKnownMarketplaces`: only this marketplace may be added (remove it if people use other marketplaces).
- Denies the Storyblok destructive and upload tools for every session, whatever a workspace says. The rules
  use `mcp__*__…`, so they also match a Storyblok connector named by an ID or `mcp__claude_ai_…`, whose ID
  can differ between accounts.

Stronger options, only if every hook and permission rule should come from IT:
`allowManagedHooksOnly` (only managed hooks run; the safety check would then need to be deployed as a managed
hook too) and `allowManagedPermissionRulesOnly`. Test on one machine before rolling out.

Reference: https://code.claude.com/docs/en/managed-settings and
https://code.claude.com/docs/en/plugins/org
