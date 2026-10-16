"""Shared page shell for the tutorial and the playbooks reference."""

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
pre{position:relative}.cp{position:absolute;top:6px;right:6px;background:var(--bg);color:var(--mut);border:1px solid var(--bd);border-radius:6px;padding:2px 9px;font:inherit;font-size:12px;cursor:pointer}.cp:hover{color:var(--a2);border-color:var(--a2)}
.xl{display:block;margin:18px 10px 0;padding-top:12px;border-top:1px solid var(--bd);font-size:14px}
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
document.querySelectorAll('pre:not(.mermaid)').forEach(pre=>{const c=pre.querySelector('code');if(!c)return;const b=document.createElement('button');b.className='cp';b.textContent='Copy';b.addEventListener('click',async()=>{const t=c.innerText;try{await navigator.clipboard.writeText(t)}catch(e){const a=document.createElement('textarea');a.value=t;document.body.appendChild(a);a.select();try{document.execCommand('copy')}catch(_){}a.remove()}b.textContent='Copied';setTimeout(()=>b.textContent='Copy',1500)});pre.appendChild(b)});
tabs.forEach(t=>t.addEventListener('click',()=>show(t.dataset.tab)));
menu.addEventListener('click',()=>setOpen(!document.body.classList.contains('open')));
document.getElementById('scrim').addEventListener('click',()=>setOpen(false));
document.addEventListener('keydown',e=>{if(e.key==='Escape')setOpen(false)});
document.addEventListener('click',e=>{const a=e.target.closest('a[data-go]');if(!a)return;e.preventDefault();const[i,an]=a.dataset.go.split(':');show(i,an)});
window.addEventListener('load',()=>show(location.hash.slice(1)||'overview'));
"""

MERMAID = (
    '<script src="https://cdn.jsdelivr.net/npm/mermaid@10.9.1/dist/mermaid.min.js" '
    'integrity="sha384-WmdflGW9aGfoBdHc4rRyWzYuAjEmDwMdGdiPNacbwfGKxBW/SO6guzuQ76qjnSlr" crossorigin="anonymous"></script>'
)


def page(title, side, panels, extra_side="", mermaid=True, default="overview"):
    return (
        '<!doctype html><html lang="en"><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width,initial-scale=1">'
        f'<meta name="color-scheme" content="dark"><title>{title}</title>'
        f"<style>{CSS}</style></head><body>"
        f'<div id="bar"><button id="menu" aria-expanded="false" aria-controls="side">Contents</button><span>{title}</span></div>'
        '<div id="scrim"></div>'
        f'<div class="layout"><aside id="side"><span class="brand">{title}</span>'
        f'<nav role="tablist" aria-orientation="vertical">{side}</nav>{extra_side}</aside>'
        f"<main>{panels}</main></div>"
        + (MERMAID if mermaid else "")
        + f"<script>{JS.replace(chr(39) + 'overview' + chr(39), chr(39) + default + chr(39))}</script></body></html>"
    )
