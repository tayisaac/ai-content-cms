#!/usr/bin/env python3
"""Checks the marketplace before a release. Run: python3 scripts/validate.py
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

# 1. Marketplace
mp = load_json(ROOT / ".claude-plugin/marketplace.json") or {}
for k in ("name", "owner", "plugins"):
    if k not in mp: err(f"marketplace.json: missing '{k}'")
names = [p.get("name") for p in mp.get("plugins", [])]
if len(names) != len(set(names)): err("marketplace.json: duplicate plugin names")

for entry in mp.get("plugins", []):
    src = entry.get("source", "")
    if not isinstance(src, str) or not src.startswith("./"):
        err(f"plugin {entry.get('name')}: source must be a ./ path in this repo"); continue
    pdir = ROOT / src
    rel = lambda p: p.relative_to(ROOT)
    pj = load_json(pdir / ".claude-plugin/plugin.json") or {}
    if pj.get("name") != entry["name"]: err(f"{rel(pdir)}: plugin.json name '{pj.get('name')}' != marketplace entry '{entry['name']}'")
    ver = pj.get("version", "")
    if not re.match(r"^\d+\.\d+\.\d+$", ver): err(f"{rel(pdir)}: plugin.json version '{ver}' is not x.y.z")
    if "version" in entry: err(f"marketplace entry {entry['name']}: don't set version here; plugin.json wins")
    changelog = (ROOT / "CHANGELOG.md").read_text() if (ROOT / "CHANGELOG.md").exists() else ""
    if f"## {entry['name']} {ver}" not in changelog: err(f"CHANGELOG.md: no '## {entry['name']} {ver}' section")
    if (pdir / "bin").exists(): err(f"{rel(pdir)}: a top-level bin/ breaks Cowork and claude.ai installs")

    # 2. Skills
    for s in sorted((pdir / "skills").glob("*/SKILL.md")):
        fm = frontmatter(s)
        if fm.get("name", "").strip() != s.parent.name: err(f"{rel(s)}: name must equal folder '{s.parent.name}'")
        if not fm.get("description", "").strip(): err(f"{rel(s)}: missing description")
        if re.search(r"[<>]", fm.get("description", "").replace(">\n", "\n", 1) if fm.get("description","").startswith(">") else fm.get("description", "")):
            err(f"{rel(s)}: description contains < or > (installers reject it)")

    # 3. Agents and tool limits
    writers = []
    for a in sorted((pdir / "agents").glob("*.md")):
        fm = frontmatter(a)
        for k in ("name", "description", "tools"):
            if not fm.get(k, "").strip(): err(f"{rel(a)}: missing '{k}'")
        tools = fm.get("tools", "")
        if re.search(r"execute_destructive|upload_asset", tools): err(f"{rel(a)}: agents must never get destructive or upload tools")
        if "execute_mutating" in tools: writers.append(a.stem)
    if writers and writers != ["cms-operator"]: err(f"only cms-operator may have write tools, found: {writers}")

    # 4. Hook
    hj = load_json(pdir / "hooks/hooks.json") or {}
    if "guard-cms-writes.py" not in json.dumps(hj): err(f"{rel(pdir)}: hooks.json does not run guard-cms-writes.py")
    guard = pdir / "hooks/guard-cms-writes.py"
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
ws = load_json(ROOT / "workspace-template/.claude/settings.json") or {}
mpname = mp.get("name")
if mpname not in ws.get("extraKnownMarketplaces", {}): err("workspace-template settings: marketplace not registered")
for n in names:
    if not ws.get("enabledPlugins", {}).get(f"{n}@{mpname}"): err(f"workspace-template settings: {n}@{mpname} not enabled")
load_json(ROOT / "workspace-template/.mcp.json")
if (ROOT / "workspace-template/.claude/settings.local.json").exists(): err("workspace-template must not contain settings.local.json")
# The template's CLAUDE.md names the plugin version it was written for, so teams can tell when their copy is behind
ws_claude = (ROOT / "workspace-template/CLAUDE.md").read_text() if (ROOT / "workspace-template/CLAUDE.md").exists() else ""
tv = re.search(r"^Template version: content-team (\S+)$", ws_claude, re.M)
ct_ver = (load_json(ROOT / "plugins/content-team/.claude-plugin/plugin.json") or {}).get("version")
if not tv: err("workspace-template/CLAUDE.md: missing 'Template version: content-team x.y.z' line")
elif tv.group(1) != ct_ver: err(f"workspace-template/CLAUDE.md: template version {tv.group(1)} != plugin version {ct_ver}")
# Wildcard server names, so the rules also match connectors named by an ID
DENY_ANY = {"mcp__*__execute_destructive", "mcp__*__upload_asset", "mcp__*__upload_asset_finish"}
perms = ws.get("permissions", {})
if not DENY_ANY <= set(perms.get("deny", [])): err(f"workspace-template settings: deny must include {sorted(DENY_ANY)}")
if "mcp__*__execute_mutating" not in perms.get("ask", []): err("workspace-template settings: ask must include mcp__*__execute_mutating")
ms = load_json(ROOT / "docs/managed-settings.example.json") or {}
if not DENY_ANY <= set(ms.get("permissions", {}).get("deny", [])): err(f"managed-settings example: deny must include {sorted(DENY_ANY)}")

if errors:
    print("Validation failed:"); [print(" -", e) for e in errors]; sys.exit(1)
print(f"OK: marketplace '{mpname}', plugins {names}, safety check {len(cases)+1} cases passed.")
