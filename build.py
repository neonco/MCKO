import html
import sys
from pathlib import Path
from urllib.parse import quote

# folder, заголовок, id-якорь
SECTIONS = [
    ("mcko_2025_11", "МЦКО 2025-11", "m202511"),
    ("mcko_24-25_uglublenka", "МЦКО 2024-25 углублёнка", "m2425"),
    ("mcko_23-24_ITclass", "МЦКО 2023-24 ИТ-класс", "m2324"),
    ("moko_k6", "МЦКО k6", "k6"),
    ("sstepik.org_lesson_969847", "Степик — урок 969847", "sstepik"),
    ("NADO ZNAT", "Шпаргалки", "cards"),
]

IMG_EXTS = {".png", ".jpg", ".jpeg", ".webp", ".gif"}
SKIP_NAMES = {"main.py", "build.py", "index.html"}


def stem_key(stem):
    if stem.isdigit():
        return (0, int(stem), "")
    return (1, 0, stem.lower())


def esc(s):
    return html.escape(s, quote=True)


def esc_code(s):
    return html.escape(s, quote=False)


def collect(folder: Path):
    imgs, pys = {}, {}
    for f in sorted(folder.iterdir()):
        if not f.is_file() or f.name in SKIP_NAMES:
            continue
        stem, ext = f.stem, f.suffix.lower()
        if ext in IMG_EXTS:
            imgs.setdefault(stem, []).append(f)
        elif ext == ".py":
            pys[stem] = f
    stems = sorted(set(imgs) | set(pys), key=stem_key)
    return stems, imgs, pys


def build():
    root = Path(__file__).parent
    sections_html, nav_html, total = [], [], 0

    for folder_name, title, anchor in SECTIONS:
        folder = root / folder_name
        stems, imgs, pys = collect(folder)
        cards_html = []
        for stem in stems:
            snum = int(stem) if stem.isdigit() else stem
            task_title = f"Задача {snum}" if stem.isdigit() else stem
            code_part = ""
            if stem in imgs:
                for img in imgs[stem]:
                    src = quote((folder_name + "/" + img.name).replace("\\", "/"),
                                safe="/._")
                    alt = f"Условие — {esc(task_title)} ({esc(folder_name)})"
                    code_part += f'<img loading="lazy" src="{src}" alt="{alt}">\n'
            if stem in pys:
                code = pys[stem].read_text(encoding="utf-8", errors="replace")
                code_box = (
                    '<div class="codebox"><div class="codebar">'
                    f'<span>Python</span>'
                    '<button type="button" class="copy">Копировать</button></div>'
                    f"<pre><code>{esc_code(code)}</code></pre></div>"
                )
            elif not imgs or folder_name != "NADO ZNAT":
                code_box = '<div class="soon">решение скоро</div>'
            else:
                code_box = ""
            cards_html.append(
                f'<article class="card"><h3>Задача {esc(str(snum))}</h3>'
                f'{code_part}{code_box}</article>'
            )
            total += 1
        nav_html.append(f'<a href="#{anchor}">{esc(title)}</a>')
        sections_html.append(
            f'<section id="{anchor}"><h2>{esc(title)}</h2>'
            + "\n".join(cards_html) + "</section>"
        )

    nav = " ".join(nav_html)
    main = "\n".join(sections_html)

    page = """<!doctype html>
<html lang="ru">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>МЦКО — разборы задач</title>
<style>
:root{
  --bg:#fff; --fg:#1f2328; --muted:#59636e; --bd:#d1d9e0;
  --codebg:#f6f8fa; --accent:#0969da; --shadow:rgba(140,152,164,.2);
}
@media (prefers-color-scheme:dark){
  :root{
    --bg:#0d1117; --fg:#e6edf3; --muted:#9198a1; --bd:#30363d;
    --codebg:#151b23; --accent:#4493f8; --shadow:rgba(0,0,0,.6);
  }
}
html{color-scheme:light dark}
*{box-sizing:border-box}
body{
  margin:0; background:var(--bg); color:var(--fg);
  font:16px/1.5 system-ui,-apple-system,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif;
}
header{
  position:sticky; top:0; z-index:10; background:var(--bg);
  border-bottom:1px solid var(--bd); padding:8px 14px;
}
#top{
  font-weight:700; font-size:1.05rem; text-decoration:none;
  color:var(--fg); display:inline-block; margin-bottom:2px;
}
nav{display:flex; flex-wrap:wrap; gap:2px 14px}
nav a{color:var(--accent); text-decoration:none; white-space:nowrap}
main{padding:10px 14px 60px; max-width:none}
h2{
  font-size:1.25rem; border-bottom:2px solid var(--bd);
  padding-bottom:6px; margin:34px 0 14px;
}
.card{margin:0 0 34px}
.card h3{margin:0 0 8px; font-size:1.05rem}
.card img{
  display:block; width:100%; height:auto; max-width:100%;
  border:1px solid var(--bd); cursor:zoom-in; background:var(--codebg);
}
.codebox{border:1px solid var(--bd); border-radius:6px; margin-top:10px}
.codebar{
  display:flex; justify-content:space-between; align-items:center;
  padding:5px 10px; background:var(--codebg);
  border-bottom:1px solid var(--bd);
}
.codebar span{color:var(--muted); font-size:.85rem}
.copy{
  font:inherit; font-size:.85rem; padding:3px 12px; cursor:pointer;
  color:var(--accent); background:transparent;
  border:1px solid var(--bd); border-radius:6px;
}
.copy:hover{border-color:var(--accent)}
.copy.ok{color:#1a7f37; border-color:#1a7f37}
@media (prefers-color-scheme:dark){.copy.ok{color:#3fb950; border-color:#3fb950}}
pre{margin:0; padding:12px 14px; overflow:auto; max-height:70vh}
code{
  font:400 14px/1.5 ui-monospace,"Cascadia Mono",Consolas,"Liberation Mono",Menlo,monospace;
  font-size:clamp(13px,1vw + 9px,15px);
}
.soon{
  margin-top:10px; padding:8px 14px; border:1px dashed var(--bd);
  border-radius:6px; color:var(--muted);
}
#lb{
  position:fixed; inset:0; z-index:100; display:grid;
  place-items:center; background:rgba(0,0,0,.88); touch-action:none;
}
#lb[hidden]{display:none}
#lbimg{
  max-width:98%; max-height:98%; will-change:transform;
  transform-origin:center; cursor:grab; touch-action:none;
  box-shadow:0 0 0 1px rgba(255,255,255,.15),0 8px 40px var(--shadow);
  user-select:none; -webkit-user-drag:none;
}
@media (max-width:720px){
  header,main{padding-left:8px; padding-right:8px}
  pre{padding:10px}
  h2{margin-top:26px}
}
</style>
</head>
<body>
<header>
  <a id="top" href="#top">МЦКО — разборы задач</a>
  <nav>{NAV}</nav>
</header>
<main>
{MAIN}
</main>
<div id="lb" hidden><img id="lbimg" alt=""></div>
<script>
const lb=document.getElementById('lb'),lbimg=document.getElementById('lbimg');
let s=1,tx=0,ty=0,ptr=new Map(),drag=null,pinchD=0,pinchS=1;
function apply(){lbimg.style.transform='translate('+tx+'px,'+ty+'px) scale('+s+')';}
function open(src,alt){lbimg.src=src;lbimg.alt=alt;s=1;tx=0;ty=0;apply();
  lb.hidden=false;document.body.style.overflow='hidden';}
function close(){lb.hidden=true;lbimg.src='';document.body.style.overflow='';}
document.querySelectorAll('.card img').forEach(im=>{
  im.setAttribute('tabindex','0');
  im.addEventListener('click',()=>open(im.src,im.alt));
  im.addEventListener('keydown',e=>{if(e.key==='Enter')open(im.src,im.alt);});
});
lb.addEventListener('click',e=>{if(e.target===lb)close();});
document.addEventListener('keydown',e=>{if(e.key==='Escape'&&!lb.hidden)close();});
lbimg.addEventListener('wheel',e=>{
  e.preventDefault();
  const f=e.deltaY<0?1.15:1/1.15,ns=Math.min(12,Math.max(1,s*f));
  if(ns===s)return;
  const r=lbimg.getBoundingClientRect(),cx=e.clientX-r.left-r.width/2,
        cy=e.clientY-r.top-r.height/2;
  tx=cx-(cx-tx)*(ns/s); ty=cy-(cy-ty)*(ns/s); s=ns; apply();
},{passive:false});
lbimg.addEventListener('pointerdown',e=>{
  lbimg.setPointerCapture(e.pointerId);
  ptr.set(e.pointerId,e);
  if(ptr.size===1)drag={x:e.clientX,y:e.clientY,tx,ty};
  else if(ptr.size===2){const a=[...ptr.values()];
    pinchD=Math.hypot(a[0].clientX-a[1].clientX,a[0].clientY-a[1].clientY);pinchS=s;}
});
lbimg.addEventListener('pointermove',e=>{
  if(!ptr.has(e.pointerId))return;
  ptr.set(e.pointerId,e);
  if(ptr.size===2){
    const a=[...ptr.values()],
          d=Math.hypot(a[0].clientX-a[1].clientX,a[0].clientY-a[1].clientY);
    s=Math.min(12,Math.max(1,pinchS*d/pinchD)); apply();
  }else if(drag){
    tx=drag.tx+e.clientX-drag.x; ty=drag.ty+e.clientY-drag.y; apply();
  }
});
function up(e){
  ptr.delete(e.pointerId);
  if(ptr.size===1){const p=[...ptr.values()][0];drag={x:p.clientX,y:p.clientY,tx,ty};}
  else if(ptr.size===0)drag=null;
}
lbimg.addEventListener('pointerup',up);
lbimg.addEventListener('pointercancel',up);
lbimg.addEventListener('dblclick',e=>{e.preventDefault();
  if(s>1){s=1;tx=0;ty=0;}else{s=2.5;} apply();});

function clipboardCopy(text){
  if(navigator.clipboard&&window.isSecureContext)
    return navigator.clipboard.writeText(text);
  return new Promise((res,rej)=>{
    const ta=document.createElement('textarea');
    ta.value=text; ta.style.position='fixed'; ta.style.opacity='0';
    document.body.appendChild(ta); ta.select();
    try{document.execCommand('copy')?res():rej();}
    catch(err){rej(err);} finally{ta.remove();}
  });
}
document.querySelectorAll('.copy').forEach(b=>{
  b.addEventListener('click',()=>{
    const code=b.closest('.codebox').querySelector('code').textContent;
    clipboardCopy(code).then(()=>{
      b.textContent='Скопировано'; b.classList.add('ok');
      setTimeout(()=>{b.textContent='Копировать';b.classList.remove('ok');},1500);
    }).catch(()=>{b.textContent='Не вышло';setTimeout(()=>b.textContent='Копировать',1500);});
  });
});
</script>
</body>
</html>
"""
    page = page.replace("{NAV}", nav).replace("{MAIN}", main)
    (root / "index.html").write_text(page, encoding="utf-8")
    print(f"OK: {total} cards -> index.html")
    for folder_name, title, _ in SECTIONS:
        st, im, py = collect(root / folder_name)
        print(f"  {folder_name}: {len(im)} img, {len(py)} py")


if __name__ == "__main__":
    sys.exit(build())
