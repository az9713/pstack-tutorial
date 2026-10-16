"""Build index.html from the pstack docs.

Usage: python build.py <path to a cursor/plugins clone's pstack folder>
Pages under src/ live in this repo. All other pages are read from the pstack folder.
"""
import re, base64, html, posixpath, sys
from pathlib import Path
import markdown

HERE = Path(__file__).parent
ROOT = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else sys.exit(__doc__)
OUT = HERE / "index.html"
GH = "https://github.com/cursor/plugins/"
PAGES = [  # (id, label, path relative to ROOT)
    ("overview", "Overview", "README.md"),
    ("start", "Start here", "src/00-start-here.md"),
    ("example", "Worked example", "src/example.md"),
    ("setup", "1 Setup", "docs/guide/01-setup.md"),
    ("mode", "2 poteto-mode", "docs/guide/02-poteto-mode.md"),
    ("understand", "3 Understand", "docs/guide/03-understand.md"),
    ("design", "4 Design", "docs/guide/04-design.md"),
    ("build", "5 Build & clean", "docs/guide/05-build-and-clean.md"),
    ("verify", "6 Verify & ship", "docs/guide/06-verify-and-ship.md"),
    ("overnight", "7 Overnight", "docs/guide/07-overnight.md"),
    ("principles", "8 Principles", "docs/guide/08-principles.md"),
    ("yours", "9 Make it yours", "docs/guide/09-make-it-yours.md"),
    ("recipes", "10 Recipes", "docs/guide/10-recipes-and-pitfalls.md"),
    ("article", "Article: Verification", "src/article.md"),
    ("video", "Video: Six stages", "src/video.md"),
]
BYPATH = {p: i for i, _, p in PAGES}
BYPATH["docs/guide/00-start-here.md"] = "start"
BYPATH["docs/guide/README.md"] = "start"


def slug(pid):
    def f(value, sep):
        s = re.sub(r"[^\w\s-]", "", value.lower()).strip()
        return pid + "--" + re.sub(r"[-\s]+", sep, s)
    return f


def convert(pid, rel):
    ext = rel.startswith("src/")
    text = ((HERE if ext else ROOT) / rel).read_text(encoding="utf-8")
    mer = []

    def hold(m):
        mer.append(m.group(1))
        return f"\n\nMERMAIDHOLD{len(mer)-1}\n\n"

    text = re.sub(r"```mermaid\n(.*?)```", hold, text, flags=re.S)
    text = text.replace("<details>", '<details markdown="1">')
    md = markdown.Markdown(
        extensions=["extra", "md_in_html", "toc", "sane_lists"],
        extension_configs={"toc": {"slugify": slug(pid)}},
    )
    h = md.convert(text)
    for i, src in enumerate(mer):
        h = h.replace(f"<p>MERMAIDHOLD{i}</p>", f'<pre class="mermaid">{html.escape(src)}</pre>')
    base = "docs/guide" if ext else posixpath.dirname(rel)

    def img(m):
        p = (ROOT / base / m.group(1)).resolve()
        return 'src="data:image/jpeg;base64,' + base64.b64encode(p.read_bytes()).decode() + '"'

    h = re.sub(r'src="(\./images/[^"]+)"', img, h)

    def link(m):
        href = m.group(1)
        if re.match(r"(https?:|mailto:)", href):
            return f'href="{href}" target="_blank" rel="noopener"'
        if href.startswith("tab:"):
            t = href[4:]
            return f'href="#{t}" data-go="{t}:"'
        if href.startswith("#"):
            return f'href="#{pid}--{href[1:]}" data-go="{pid}:{pid}--{href[1:]}"'
        path, _, frag = href.partition("#")
        res = posixpath.normpath(posixpath.join(base, path))
        if res in BYPATH:
            t = BYPATH[res]
            anchor = f"{t}--{frag}" if frag else ""
            return f'href="#{t}" data-go="{t}:{anchor}"'
        kind = "tree" if (href.endswith("/") or "." not in posixpath.basename(res)) else "blob"
        return f'href="{GH}{kind}/main/pstack/{res}" target="_blank" rel="noopener"'

    h = re.sub(r'href="([^"]*)"', link, h)
    h = h.replace("<table>", '<div class="tw"><table>').replace("</table>", "</table></div>")
    return h


LABEL = {i: l for i, l, _ in PAGES}
GROUPS = [
    ("Begin here", ["overview", "start", "example"]),
    ("The guide", ["setup", "mode", "understand", "design", "build", "verify", "overnight", "principles", "yours", "recipes"]),
    ("Sources", ["article", "video"]),
]
assert sorted(sum((g for _, g in GROUPS), [])) == sorted(LABEL)
sys.path.insert(0, str(HERE))
from shell import page

side = "".join(
    f'<div class="grp">{html.escape(t)}</div>'
    + "".join(
        f'<button role="tab" id="t-{i}" data-tab="{i}" aria-controls="p-{i}">{html.escape(LABEL[i])}</button>'
        for i in ids
    )
    for t, ids in GROUPS
)
panels = "".join(
    f'<section role="tabpanel" id="p-{i}" aria-labelledby="t-{i}" hidden><article>{convert(i, p)}</article></section>'
    for i, _, p in PAGES
)
extra = '<a class="xl" href="playbooks.html">Playbooks reference &rarr;</a>'
OUT.write_text(page("pstack tutorial", side, panels, extra), encoding="utf-8")
print(OUT, OUT.stat().st_size // 1024, "KB")
