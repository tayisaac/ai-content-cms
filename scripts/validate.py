#!/usr/bin/env python3
"""Checks the content-team files in workspace-template/.claude before a release. Run: python3 scripts/validate.py
Exit 0 = all good. Exit 1 = problems listed. Used by the GitHub Action and by maintainers locally."""
import json, re, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
errors = []
def err(msg): errors.append(msg)

def load_json(p):
    try:
        return json.loads(Path(p).read_text())
    except Exception as e:
        err(f"{p.relative_to(ROOT)}: invalid JSON ({e})"); return None

def frontmatter(p):
    t = p.read_text()
    m = re.match(r"^---\n(.*?)\n---\n", t, re.S)
    if not m: err(f"{p.relative_to(ROOT)}: missing frontmatter"); return {}
    fm, key = {}, None
    for line in m.group(1).splitlines():
        km = re.match(r"^([A-Za-z_-]+):\s*(.*)$", line)
        if km: key = km.group(1); fm[key] = km.group(2)
        elif key: fm[key] += "\n" + line
    return fm

T = ROOT / "workspace-template/.claude"
rel = lambda p: p.relative_to(ROOT)

# 1. Version: one number in content-team-version, the template CLAUDE.md and the changelog
ver = (T / "content-team-version").read_text().strip() if (T / "content-team-version").exists() else ""
if not re.match(r"^\d+\.\d+\.\d+$", ver): err(f"{rel(T)}/content-team-version: '{ver}' is not x.y.z")
changelog = (ROOT / "CHANGELOG.md").read_text() if (ROOT / "CHANGELOG.md").exists() else ""
if f"## content-team {ver} " not in changelog: err(f"CHANGELOG.md: no '## content-team {ver} (date)' section")
ws_claude = (ROOT / "workspace-template/CLAUDE.md").read_text() if (ROOT / "workspace-template/CLAUDE.md").exists() else ""
tv = re.search(r"^Template version: content-team (\S+)$", ws_claude, re.M)
if not tv: err("workspace-template/CLAUDE.md: missing 'Template version: content-team x.y.z' line")
elif tv.group(1) != ver: err(f"workspace-template/CLAUDE.md: template version {tv.group(1)} != content-team-version {ver}")
for gone in (".claude-plugin", "plugins"):
    if (ROOT / gone).exists(): err(f"{gone}/ is back: content-team ships as workspace-template/.claude, not as a plugin")

# 2. Skills
skills = sorted((T / "skills").glob("*/SKILL.md"))
for s in skills:
    fm = frontmatter(s)
    if fm.get("name", "").strip() != s.parent.name: err(f"{rel(s)}: name must equal folder '{s.parent.name}'")
    if not fm.get("description", "").strip(): err(f"{rel(s)}: missing description")
    if re.search(r"[<>]", fm.get("description", "").replace(">\n", "\n", 1) if fm.get("description","").startswith(">") else fm.get("description", "")):
        err(f"{rel(s)}: description contains < or > (Claude Code rejects it)")

# 3. Agents and tool limits
agents = sorted((T / "agents").glob("*.md"))
writers = []
for a in agents:
    fm = frontmatter(a)
    for k in ("name", "description", "tools"):
        if not fm.get(k, "").strip(): err(f"{rel(a)}: missing '{k}'")
    tools = fm.get("tools", "")
    if re.search(r"execute_destructive|upload_asset", tools): err(f"{rel(a)}: agents must never get destructive or upload tools")
    if "execute_mutating" in tools: writers.append(a.stem)
if writers != ["cms-operator"]: err(f"only cms-operator may have write tools (and it must have them), found: {writers}")
# Agents and skills now load under their bare names; a 'content-team:' prefix would point at nothing
for f in [*agents, *skills, ROOT / "workspace-template/CLAUDE.md", ROOT / "workspace-template/README.md"]:
    if re.search(r"content-team:[a-z<]", f.read_text()): err(f"{rel(f)}: uses the old plugin name 'content-team:<name>'")

# 4. Safety check: wired in settings.json (template and managed example) and behaving as expected
HOOK_MATCHER = "mcp__.*__(execute_mutating|execute_destructive|upload_asset|upload_asset_finish)"
HOOK_COMMAND = 'python3 "$CLAUDE_PROJECT_DIR/.claude/hooks/guard-cms-writes.py" || exit 2'
def has_hook(settings):
    return any(h.get("matcher") == HOOK_MATCHER and any(x.get("type") == "command" and x.get("command") == HOOK_COMMAND
               for x in h.get("hooks", [])) for h in settings.get("hooks", {}).get("PreToolUse", []))
ws = load_json(T / "settings.json") or {}
ms = load_json(ROOT / "docs/managed-settings.example.json") or {}
if not has_hook(ws): err("workspace-template settings: PreToolUse hook must run the safety check with the exact matcher and command")
if not has_hook(ms): err("managed-settings example: PreToolUse hook must run the safety check with the exact matcher and command")
guard = T / "hooks/guard-cms-writes.py"
cases = [  # (tool_name, tool_input, expected exit code)
    ("mcp__Storyblok__execute_mutating", {"operation": "createStory", "parameters": {"story": {"name": "x", "content": {"publish": 1}}}}, 0),
    ("mcp__Storyblok__execute_mutating", {"operation": "updateStory", "parameters": {"story_id": 1, "story": {}}}, 0),
    ("mcp__Storyblok__execute_mutating", {"operation": "updateStory", "parameters": {"publish": 1}}, 2),
    ("mcp__Storyblok__execute_mutating", {"operation": "updateStory", "parameters": {"force_update": True}}, 2),
    ("mcp__Storyblok__execute_mutating", {"operation": "publishStory", "parameters": {}}, 2),
    ("mcp__Storyblok__execute_mutating", {"operation": "updateComponent", "parameters": {}}, 2),
    ("mcp__Storyblok__execute_destructive", {"operation": "deleteStory"}, 2),
    ("mcp__Storyblok__upload_asset", {}, 2),
    ("mcp__68a2506e-d22d__execute_destructive", {"operation": "deleteStory"}, 2),
    ("mcp__68a2506e-d22d__execute_mutating", {"operation": "createStory", "parameters": {"story": {"name": "x"}}}, 0),
    ("mcp__68a2506e-d22d__execute_mutating", {"operation": "updateStory", "parameters": {"publish": "1"}}, 2),
    # Every other publish-like option, nested anywhere outside story content
    ("mcp__Storyblok__execute_mutating", {"operation": "updateStory", "parameters": {"story_id": 1, "unpublish": 1}}, 2),
    ("mcp__Storyblok__execute_mutating", {"operation": "updateStory", "parameters": {"story": {"publish_at": "2026-12-01"}}}, 2),
    ("mcp__Storyblok__execute_mutating", {"operation": "updateStory", "parameters": {"release_id": 7}}, 2),
    ("mcp__Storyblok__execute_mutating", {"operation": "updateStory", "parameters": {"lang": "zh"}}, 2),
    ("mcp__Storyblok__execute_mutating", {"operation": "createStory", "parameters": {"story": {"name": "x"}, "ai_translate_language": "zh"}}, 2),
    ("mcp__Storyblok__execute_mutating", {"operation": "createStory", "parameters": {"story": {"name": "x"}, "publish": "false"}}, 0),
    # Missing or unexpected operations, other write-ish operations, the second upload step
    ("mcp__Storyblok__execute_mutating", {"parameters": {}}, 2),
    ("mcp__Storyblok__execute_mutating", {"operation": "updateSpace", "parameters": {}}, 2),
    ("mcp__Storyblok__execute_mutating", {"operation": "createDatasource", "parameters": {}}, 2),
    ("mcp__Storyblok__upload_asset_finish", {}, 2),
    # Tools that don't write pass through untouched (no ask)
    ("mcp__Storyblok__execute_readonly", {"operation": "getStory"}, 0),
]
for tool, inp, want in cases:
    r = subprocess.run([sys.executable, str(guard)], input=json.dumps({"tool_name": tool, "tool_input": inp}),
                       capture_output=True, text=True)
    if r.returncode != want: err(f"safety check: {tool} {inp.get('operation','')} returned {r.returncode}, expected {want}")
    elif want == 0 and tool.endswith("execute_mutating"):  # allowed draft saves must still ask the user
        try: decision = json.loads(r.stdout)["hookSpecificOutput"]["permissionDecision"]
        except Exception: decision = None
        if decision != "ask": err(f"safety check: {tool} {inp.get('operation','')} must return permissionDecision 'ask', got {decision}")
r = subprocess.run([sys.executable, str(guard)], input="not json", capture_output=True, text=True)
if r.returncode != 2: err("safety check: unreadable input must be blocked (fail closed)")

# 5. Workspace template
for k in ("extraKnownMarketplaces", "enabledPlugins"):
    if k in ws: err(f"workspace-template settings: remove '{k}' (the plugin is retired)")
load_json(ROOT / "workspace-template/.mcp.json")
if (T / "settings.local.json").exists(): err("workspace-template must not contain settings.local.json")
# Wildcard server names, so the rules also match connectors named by an ID
DENY_ANY = {"mcp__*__execute_destructive", "mcp__*__upload_asset", "mcp__*__upload_asset_finish"}
perms = ws.get("permissions", {})
if not DENY_ANY <= set(perms.get("deny", [])): err(f"workspace-template settings: deny must include {sorted(DENY_ANY)}")
if "mcp__*__execute_mutating" not in perms.get("ask", []): err("workspace-template settings: ask must include mcp__*__execute_mutating")
if not DENY_ANY <= set(ms.get("permissions", {}).get("deny", [])): err(f"managed-settings example: deny must include {sorted(DENY_ANY)}")

if errors:
    print("Validation failed:"); [print(" -", e) for e in errors]; sys.exit(1)
print(f"OK: content-team {ver}, {len(agents)} agents, {len(skills)} skills, safety check {len(cases)+1} cases passed.")
