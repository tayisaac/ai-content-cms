#!/usr/bin/env bash
# Copies the content-team agents, skills and safety check into a team workspace, or updates them.
# Usage: scripts/update-workspace.sh <path to the team workspace>
#
# Overwrites .claude/agents, .claude/skills and .claude/hooks files that come from this repository, and
# removes files an earlier version shipped that this one doesn't (tracked in .claude/content-team-files).
# Never touches settings.json (except to create it in a new workspace), settings.local.json, CLAUDE.md,
# files the team added itself, or project folders. Commit the result in the workspace repository.
set -euo pipefail

[ $# -eq 1 ] || { echo "Usage: $0 <path to the team workspace>" >&2; exit 1; }
[ -d "$1" ] || { echo "Not a folder: $1" >&2; exit 1; }

repo="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
src="$repo/workspace-template/.claude"
ws="$(cd "$1" && pwd)"
dest="$ws/.claude"
[ "$ws" != "$repo/workspace-template" ] || { echo "That is the template itself; pass a team workspace." >&2; exit 1; }

old_ver="$(cat "$dest/content-team-version" 2>/dev/null || echo "none")"
new_ver="$(cat "$src/content-team-version")"
manifest="$dest/content-team-files"
new_list="$(cd "$src" && find agents skills hooks -type f ! -name .DS_Store | LC_ALL=C sort)"

mkdir -p "$dest"

# Remove files an earlier version shipped that this version doesn't
if [ -f "$manifest" ]; then
  LC_ALL=C comm -23 <(LC_ALL=C sort "$manifest") <(printf '%s\n' "$new_list") | while IFS= read -r f; do
    case "$f" in
      *..*) echo "skipped suspicious manifest entry: $f" >&2 ;;
      agents/*|skills/*|hooks/*) rm -f "$dest/$f" && echo "removed .claude/$f" ;;
    esac
  done
fi

# Copy this version's files
printf '%s\n' "$new_list" | while IFS= read -r f; do
  mkdir -p "$dest/$(dirname "$f")"
  rm -f "$dest/$f"   # some files are read-only on purpose; replace rather than overwrite
  cp "$src/$f" "$dest/$f"
done
cp "$src/content-team-version" "$dest/content-team-version"
printf '%s\n' "$new_list" > "$manifest"
find "$dest/agents" "$dest/skills" "$dest/hooks" -type d -empty -delete 2>/dev/null || true

# A new workspace gets the template's settings.json; an existing one is only checked
if [ ! -f "$dest/settings.json" ]; then
  cp "$src/settings.json" "$dest/settings.json"
  echo "created .claude/settings.json from the template"
fi

python3 - "$src/settings.json" "$dest" "$HOME/.claude/settings.json" <<'EOF'
import json, sys
from pathlib import Path
template, dest, user = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
def load(p):
    try: return json.loads(p.read_text())
    except FileNotFoundError: return {}
    except Exception as e: print(f"WARNING: {p} is not valid JSON ({e})"); return {}
want = load(template)["hooks"]["PreToolUse"][0]
want_cmd = want["hooks"][0]["command"]
have = load(dest / "settings.json").get("hooks", {}).get("PreToolUse", [])
ok = any(h.get("matcher") == want["matcher"] and any(x.get("command") == want_cmd for x in h.get("hooks", []))
         for h in have)
if not ok:
    print("WARNING: .claude/settings.json does not run the safety check. Copy the \"hooks\" block from")
    print("         workspace-template/.claude/settings.json into it. Until then publish and delete calls")
    print("         are NOT blocked by the content-team safety check.")
for p in (dest / "settings.json", dest / "settings.local.json", user):
    s = load(p)
    if any(k.startswith("content-team@") and v for k, v in s.get("enabledPlugins", {}).items()):
        print(f"WARNING: {p} still enables the old content-team plugin, so every agent and skill loads twice.")
        print("         Remove it from enabledPlugins (and aicontentteam from extraKnownMarketplaces),")
        print("         then run /plugin uninstall content-team@aicontentteam in Claude Code.")
EOF

echo "content-team $old_ver -> $new_ver in $dest"
echo "Review the changes and commit them in the workspace repository."
