#!/usr/bin/env bash
# Builds a throwaway plugin at .build/content-team from workspace-template/.claude, so
# `claude plugin eval` and `claude plugin validate` can load the agents and skills.
# The build is git-ignored and never shipped: teams get the files through scripts/update-workspace.sh.
set -euo pipefail
root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
src="$root/workspace-template/.claude"
out="$root/.build/content-team"

rm -rf "$root/.build"
mkdir -p "$out/.claude-plugin" "$out/hooks"
cp -R "$src/agents" "$src/skills" "$out/"
cp "$src/hooks/guard-cms-writes.py" "$out/hooks/"
find "$out" -name .DS_Store -delete

# plugin.json and hooks.json, with the hook matcher and timeout taken from the template's settings.json
python3 - "$src" "$out" <<'EOF'
import json, sys
from pathlib import Path
src, out = Path(sys.argv[1]), Path(sys.argv[2])
ver = (src / "content-team-version").read_text().strip()
(out / ".claude-plugin/plugin.json").write_text(json.dumps({
    "name": "content-team",
    "version": ver,
    "description": "Eval build of the content-team agents and skills. Not for installing.",
    "author": {"name": "Isaac Tay"},
    "license": "UNLICENSED",
}, indent=2) + "\n")
h = json.loads((src / "settings.json").read_text())["hooks"]["PreToolUse"][0]
(out / "hooks/hooks.json").write_text(json.dumps({"hooks": {"PreToolUse": [{
    "matcher": h["matcher"],
    "hooks": [{"type": "command",
               "command": "python3 \"${CLAUDE_PLUGIN_ROOT}/hooks/guard-cms-writes.py\" || exit 2",
               "timeout": h["hooks"][0]["timeout"]}],
}]}}, indent=2) + "\n")
print(f"Built {out} (content-team {ver})")
EOF
