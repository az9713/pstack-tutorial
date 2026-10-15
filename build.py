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


tabs = "".join(
    f'<button role="tab" id="t-{i}" data-tab="{i}" aria-controls="p-{i}">{html.escape(l)}</button>'
    for i, l, _ in PAGES
)
panels = "".join(
    f'<section role="tabpanel" id="p-{i}" aria-labelledby="t-{i}" hidden><article>{convert(i, p)}</article></section>'
    for i, _, p in PAGES
)

CSS = """
:root{--bg:#0f172a;--card:#1e293b;--tx:#e2e8f0;--tx2:#cbd5e1;--mut:#94a3b8;--a1:#fb923c;--a2:#2dd4bf;--bd:#334155}
*{box-sizing:border-box}html{scroll-padding-top:64px}
body{margin:0;background:var(--bg);color:var(--tx2);font:16px/1.65 system-ui,-apple-system,"Segoe UI",sans-serif}
header{position:sticky;top:0;z-index:5;background:var(--bg);border-bottom:1px solid var(--bd)}
.bar{display:flex;align-items:center;gap:12px;padding:8px 16px;max-width:1000px;margin:0 auto}
.brand{color:var(--a1);font-weight:700;white-space:nowrap}
nav{display:flex;gap:4px;overflow-x:auto;scrollbar-width:thin}
nav button{background:none;border:1px solid transparent;color:var(--mut);padding:6px 12px;border-radius:8px;font:inherit;font-size:14px;cursor:pointer;white-space:nowrap}
nav button:hover{color:var(--tx)}nav button[aria-selected=true]{background:var(--card);color:var(--a2);border-color:var(--bd)}
main{max-width:860px;margin:0 auto;padding:24px 16px 80px}
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
"""
JS = """
const tabs=[...document.querySelectorAll('[role=tab]')];
function show(id,anchor){
 if(!document.getElementById('p-'+id))id='overview';
 tabs.forEach(t=>t.setAttribute('aria-selected',t.dataset.tab===id));
 document.querySelectorAll('[role=tabpanel]').forEach(p=>p.hidden=p.id!=='p-'+id);
 document.getElementById('t-'+id).scrollIntoView({block:'nearest',inline:'center'});
 try{history.replaceState(null,'','#'+id)}catch(e){}
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
document.addEventListener('click',e=>{const a=e.target.closest('a[data-go]');if(!a)return;e.preventDefault();const[i,an]=a.dataset.go.split(':');show(i,an)});
window.addEventListener('load',()=>{if(window.mermaid)mermaid.initialize({startOnLoad:false,theme:'dark'});show(location.hash.slice(1)||'overview')});
"""
doc = (
    '<!doctype html><html lang="en"><head><meta charset="utf-8">'
    '<meta name="viewport" content="width=device-width,initial-scale=1">'
    '<meta name="color-scheme" content="dark"><title>pstack Docs</title>'
    f"<style>{CSS}</style></head><body>"
    f'<header><div class="bar"><span class="brand">pstack</span><nav role="tablist">{tabs}</nav></div></header>'
    f"<main>{panels}</main>"
    '<script src="https://cdn.jsdelivr.net/npm/mermaid@10.9.1/dist/mermaid.min.js" integrity="sha384-WmdflGW9aGfoBdHc4rRyWzYuAjEmDwMdGdiPNacbwfGKxBW/SO6guzuQ76qjnSlr" crossorigin="anonymous"></script>'
    f"<script>{JS}</script></body></html>"
)
OUT.write_text(doc, encoding="utf-8")
print(OUT, len(doc) // 1024, "KB")
