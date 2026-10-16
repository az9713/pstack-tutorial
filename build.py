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

CSS = """
:root{--bg:#0f172a;--card:#1e293b;--tx:#e2e8f0;--tx2:#cbd5e1;--mut:#94a3b8;--a1:#fb923c;--a2:#2dd4bf;--bd:#334155;--side:250px}
*{box-sizing:border-box}html{scroll-padding-top:64px}
body{margin:0;background:var(--bg);color:var(--tx2);font:16px/1.65 system-ui,-apple-system,"Segoe UI",sans-serif}
.layout{display:flex;max-width:1180px;margin:0 auto}
aside{width:var(--side);flex:none;position:sticky;top:0;height:100vh;overflow-y:auto;padding:20px 12px;border-right:1px solid var(--bd);background:var(--bg)}
.brand{display:block;color:var(--a1);font-weight:700;font-size:1.1rem;padding:0 10px 12px}
.grp{color:var(--mut);font-size:12px;letter-spacing:.08em;text-transform:uppercase;padding:12px 10px 4px}
aside button{display:block;width:100%;text-align:left;background:none;border:0;border-left:3px solid transparent;color:var(--tx2);padding:5px 10px;border-radius:0 8px 8px 0;font:inherit;font-size:14.5px;cursor:pointer}
aside button:hover{background:var(--card);color:var(--tx)}
aside button[aria-selected=true]{background:var(--card);color:var(--a2);border-left-color:var(--a1);font-weight:600}
main{flex:1;min-width:0;max-width:860px;padding:28px 24px 80px}
#bar{display:none}
h1,h2,h3,h4{color:var(--tx);line-height:1.25}h1{font-size:2rem;margin-top:0}h2{margin-top:2.2em;padding-bottom:.3em;border-bottom:1px solid var(--bd)}
a{color:var(--a2)}a:hover{color:var(--a1)}strong{color:var(--tx)}
code{background:var(--card);border:1px solid var(--bd);border-radius:4px;padding:1px 5px;font-size:.88em;color:var(--a1)}
pre{background:var(--card);border:1px solid var(--bd);border-radius:8px;padding:14px 16px;overflow-x:auto}pre code{background:none;border:0;padding:0;color:var(--tx)}
pre.mermaid{text-align:center;color:var(--mut)}
.tw{overflow-x:auto;margin:1em 0}table{border-collapse:collapse;width:100%;font-size:.93rem}
th,td{border:1px solid var(--bd);padding:8px 10px;text-align:left;vertical-align:top}th{background:var(--card);color:var(--tx)}
img{max-width:100%;height:auto;border-radius:10px;border:1px solid var(--bd)}
details{background:var(--card);border:1px solid var(--bd);border-radius:8px;padding:8px 14px;margin:1em 0}summary{cursor:pointer;color:var(--a1)}
blockquote{margin:1em 0;padding:.1em 1em;border-left:3px solid var(--a1);color:var(--mut)}hr{border:0;border-top:1px solid var(--bd);margin:2em 0}
@media(max-width:820px){
 #bar{display:flex;align-items:center;gap:12px;position:sticky;top:0;z-index:6;background:var(--bg);border-bottom:1px solid var(--bd);padding:8px 16px}
 #bar button{background:var(--card);color:var(--tx);border:1px solid var(--bd);border-radius:8px;padding:6px 12px;font:inherit;font-size:14px;cursor:pointer}
 #bar span{color:var(--a1);font-weight:700}
 aside{position:fixed;z-index:7;left:0;top:0;width:min(280px,85vw);transform:translateX(-100%);transition:transform .2s;border-right:1px solid var(--bd)}
 body.open aside{transform:none}
 #scrim{display:none;position:fixed;inset:0;z-index:6;background:rgba(0,0,0,.5)}body.open #scrim{display:block}
 .layout{display:block}main{padding:20px 16px 80px}
}
"""
JS = """
if(window.mermaid)mermaid.initialize({startOnLoad:false,theme:'dark'});
const tabs=[...document.querySelectorAll('[role=tab]')];
const menu=document.getElementById('menu');
function setOpen(o){document.body.classList.toggle('open',o);menu.setAttribute('aria-expanded',o)}
function show(id,anchor){
 if(!document.getElementById('p-'+id))id='overview';
 tabs.forEach(t=>t.setAttribute('aria-selected',t.dataset.tab===id));
 document.querySelectorAll('[role=tabpanel]').forEach(p=>p.hidden=p.id!=='p-'+id);
 document.getElementById('t-'+id).scrollIntoView({block:'nearest'});
 try{history.replaceState(null,'','#'+id)}catch(e){}
 setOpen(false);
 renderMermaid(document.getElementById('p-'+id));
 const el=anchor&&document.getElementById(anchor);
 if(el)el.scrollIntoView();else window.scrollTo(0,0);
}
async function renderMermaid(panel){
 if(!window.mermaid)return;
 const nodes=[...panel.querySelectorAll('pre.mermaid:not([data-processed])')];
 if(nodes.length)try{await mermaid.run({nodes})}catch(e){}
}
tabs.forEach(t=>t.addEventListener('click',()=>show(t.dataset.tab)));
menu.addEventListener('click',()=>setOpen(!document.body.classList.contains('open')));
document.getElementById('scrim').addEventListener('click',()=>setOpen(false));
document.addEventListener('keydown',e=>{if(e.key==='Escape')setOpen(false)});
document.addEventListener('click',e=>{const a=e.target.closest('a[data-go]');if(!a)return;e.preventDefault();const[i,an]=a.dataset.go.split(':');show(i,an)});
window.addEventListener('load',()=>show(location.hash.slice(1)||'overview'));
"""
doc = (
    '<!doctype html><html lang="en"><head><meta charset="utf-8">'
    '<meta name="viewport" content="width=device-width,initial-scale=1">'
    '<meta name="color-scheme" content="dark"><title>pstack Tutorial</title>'
    f"<style>{CSS}</style></head><body>"
    '<div id="bar"><button id="menu" aria-expanded="false" aria-controls="side">Contents</button><span>pstack tutorial</span></div>'
    '<div id="scrim"></div>'
    f'<div class="layout"><aside id="side"><span class="brand">pstack tutorial</span><nav role="tablist" aria-orientation="vertical">{side}</nav></aside>'
    f"<main>{panels}</main></div>"
    '<script src="https://cdn.jsdelivr.net/npm/mermaid@10.9.1/dist/mermaid.min.js" integrity="sha384-WmdflGW9aGfoBdHc4rRyWzYuAjEmDwMdGdiPNacbwfGKxBW/SO6guzuQ76qjnSlr" crossorigin="anonymous"></script>'
    f"<script>{JS}</script></body></html>"
)
OUT.write_text(doc, encoding="utf-8")
print(OUT, len(doc) // 1024, "KB")
