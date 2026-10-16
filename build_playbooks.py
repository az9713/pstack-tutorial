"""Build playbooks.html from src/playbooks/*.md.

Usage: python build_playbooks.py [path to the pstack folder of a cursor/plugins clone]
The pstack folder is only used to link `/skill` names that exist there.
"""
import html, re, sys
from pathlib import Path
import markdown

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
from shell import page

SRC = HERE / "src/playbooks"
OUT = HERE / "playbooks.html"
GH = "https://github.com/cursor/plugins/blob/main/pstack/"
PSTACK = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else None

GROUPS = [
    ("Start", [("how", "How to use this page", "00-how-to-use")]),
    ("Understand and diagnose", [
        ("investigation", "Investigation", None),
        ("runtime-forensics", "Runtime forensics", None),
        ("trace-forensics", "Trace forensics", None)]),
    ("Fix and improve", [
        ("bug-fix", "Bug fix", None),
        ("perf-issue", "Perf issue", None),
        ("hillclimb", "Hillclimb", None)]),
    ("Design and build", [
        ("feature", "Feature", None),
        ("refactoring", "Refactoring", None),
        ("prototype", "Prototype", None),
        ("visual-parity", "Visual parity", None),
        ("multi-phase-plan", "Multi-phase plan", None)]),
    ("Skills", [
        ("authoring-a-skill", "Authoring a skill", None),
        ("eval", "Eval", None)]),
    ("Ship", [
        ("opening-a-pr", "Opening a PR", None),
        ("babysit", "Babysit", None),
        ("shipping", "Shipping", None),
        ("autopilot-stack", "Autopilot: stack", None),
        ("autopilot-full", "Autopilot: full", None)]),
    ("Operate", [
        ("autonomous-run", "Autonomous run", None),
        ("orchestrate", "Orchestrate", None),
        ("session-pickup", "Session pickup", None),
        ("pause-safely", "Pause safely", None),
        ("worktree-cleanup", "Worktree cleanup", None)]),
]

skills = {p.parent.name for p in (PSTACK / "skills").glob("*/SKILL.md")} if PSTACK else set()


def blank_before_lists(text):
    """Python-Markdown needs a blank line before a list. Skip fenced code."""
    item = re.compile(r"\s*([-*]|\d+\.)\s")
    out, fenced = [], False
    for line in text.split("\n"):
        if line.startswith("```"):
            fenced = not fenced
        if not fenced and item.match(line) and out and out[-1].strip() and not item.match(out[-1]):
            out.append("")
        out.append(line)
    return "\n".join(out)


def convert(pid, stem):
    path = SRC / f"{stem}.md"
    if not path.exists():
        return f"<h1>{html.escape(pid)}</h1><p>Missing source: {stem}.md</p>"
    h = markdown.markdown(blank_before_lists(path.read_text(encoding="utf-8")), extensions=["extra", "sane_lists"])
    h = re.sub(r'href="tab:([^"]+)"', lambda m: f'href="#{m[1]}" data-go="{m[1]}:"', h)
    h = re.sub(
        r"<code>/([a-z0-9-]+)</code>",
        lambda m: f'<a href="{GH}skills/{m[1]}/SKILL.md" target="_blank" rel="noopener"><code>/{m[1]}</code></a>'
        if m[1] in skills else m[0],
        h,
    )
    h = h.replace("<table>", '<div class="tw"><table>').replace("</table>", "</table></div>")
    if pid != "how":
        h += (f'<p class="src">Source playbook: <a href="{GH}skills/poteto-mode/playbooks/{stem}.md" '
              'target="_blank" rel="noopener">view on GitHub</a>.</p>')
    return h


side, panels = [], []
for title, items in GROUPS:
    side.append(f'<div class="grp">{html.escape(title)}</div>')
    for pid, label, stem in items:
        side.append(f'<button role="tab" id="t-{pid}" data-tab="{pid}" aria-controls="p-{pid}">{html.escape(label)}</button>')
        panels.append(f'<section role="tabpanel" id="p-{pid}" aria-labelledby="t-{pid}" hidden><article>{convert(pid, stem or pid)}</article></section>')

extra = '<a class="xl" href="index.html">&larr; Back to the tutorial</a>'
doc = page("pstack playbooks", "".join(side), "".join(panels), extra, mermaid=False, default="how")
OUT.write_text(doc, encoding="utf-8")
print(OUT, OUT.stat().st_size // 1024, "KB")
