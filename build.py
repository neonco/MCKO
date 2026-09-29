import html
import re
import struct
import sys
from pathlib import Path
from urllib.parse import quote

# (название таба, id, акцент, [ (путь, заголовок раздела, якорь, актуальный) ])
GRADES = [
    ("7 класс", "g7", "amber", [
        ("7 класс/moko_k6", "k6", "k7", True),
    ]),
    ("10 класс", "g10", "blue", [
        ("10 класс/moko_k6", "k6", "k6", True),
        ("10 класс/mcko_2025_11", "МЦКО 2025-11", "m202511", False),
        ("10 класс/mcko_24-25_uglublenka", "Углублёнка 24-25", "m2425", False),
        ("10 класс/mcko_23-24_ITclass", "ИТ-класс 23-24", "m2324", False),
        ("10 класс/sstepik.org_lesson_969847", "Степик", "sstepik", False),
    ]),
    ("Шпаргалки", "cards", "neutral", [
        ("NADO ZNAT", "Шпаргалки", "cheats", True),
    ]),
]

IMG_EXTS = {".png", ".jpg", ".jpeg", ".webp", ".gif"}
SKIP_NAMES = {"main.py", "build.py", "index.html"}


def stem_key(stem):
    if stem.isdigit():
        return (0, int(stem), "")
    return (1, 0, stem.lower())


def task_label(stem):
    m = re.match(r"(?:task)?(\d+)$", stem, re.IGNORECASE)
    return f"Задача {int(m.group(1))}" if m else stem


def esc(s):
    return html.escape(s, quote=True)


def esc_code(s):
    return html.escape(s, quote=False)


def png_size(path):
    try:
        with open(path, "rb") as fh:
            head = fh.read(24)
        if head[:8] == b"\x89PNG\r\n\x1a\n" and head[12:16] == b"IHDR":
            return struct.unpack(">II", head[16:24])
    except OSError:
        pass
    return None


def collect(folder):
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


def card_html(folder_path, stem, imgs, pys, section_title):
    label = task_label(stem)
    parts = []
    for img in imgs.get(stem, []):
        src = quote(f"{folder_path}/{img.name}", safe="/._")
        dim = png_size(img)
        size = f' width="{dim[0]}" height="{dim[1]}"' if dim else ""
        alt = esc(f"Условие — {label} ({section_title})")
        parts.append(f'<img loading="lazy"{size} src="{src}" alt="{alt}">')
    if stem in pys:
        py = pys[stem]
        code = py.read_text(encoding="utf-8", errors="replace")
        parts.append(
            '<div class="codebox"><div class="codebar">'
            f'<span>{esc(py.name)}</span>'
            '<button type="button" class="copy">Копировать</button></div>'
            f"<pre><code>{esc_code(code)}</code></pre></div>"
        )
    elif section_title != "Шпаргалки":
        parts.append('<div class="soon">Решение скоро</div>')
    return (
        f'<article class="card"><h4>{esc(label)}</h4>' + "\n".join(parts) + "</article>"
    )


def build():
    root = Path(__file__).parent
    tabs, panels, total = [], [], 0

    for grade, gid, accent, sections in GRADES:
        for i, (_, _, _, current) in enumerate(sections):
            if current and i:
                sections.insert(0, sections.pop(i))
                break
        secs = []
        for path, stitle, anchor, current in sections:
            folder = root / path
            stems, imgs, pys = collect(folder)
            cards = [
                card_html(path, stem, imgs, pys, stitle) for stem in stems
            ]
            badge = ' <span class="badge">актуальное</span>' if current else ""
            secs.append(
                f'<section id="{anchor}"><div class="sec-head">'
                f"<h3>{esc(stitle)}</h3>{badge}</div>\n"
                + "\n".join(cards) + "\n</section>"
            )
            total += len(cards)
        tabs.append(
            f'<button class="tab" role="tab" id="tab-{gid}" aria-controls="{gid}"'
            f' aria-selected="false" tabindex="-1" data-panel="{gid}"'
            f' data-accent="{accent}"><span class="dot dot-{accent}"></span>'
            f"{esc(grade)}</button>"
        )
        panels.append(
            f'<div id="{gid}" class="panel" role="tabpanel" aria-labelledby="tab-{gid}"'
            f' tabindex="0"><h2 class="sr-only">{esc(grade)}</h2>\n'
            + "\n".join(secs) + "\n</div>"
        )

    page = TEMPLATE.replace("@TABS@", "".join(tabs)).replace(
        "@MAIN@", "\n".join(panels)
    )
    (root / "index.html").write_text(page, encoding="utf-8")
    print(f"OK: {total} cards -> index.html")
    for _, _, _, sections in GRADES:
        for path, stitle, _, current in sections:
            st, im, py = collect(root / path)
            print(f"  {path}: {len(im)} img, {len(py)} py"
                  + ("  [актуальное]" if current else ""))


TEMPLATE = r"""<!doctype html>
<html lang="ru">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>МЦКО — разборы задач</title>
<script>document.documentElement.className="js";</script>
<style>
:root{
  color-scheme:light dark;
  --font-ui:system-ui,-apple-system,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif;
  --font-mono:ui-monospace,"Cascadia Mono",Consolas,"SF Mono",Menlo,monospace;
  --bg:#ffffff; --surface:#f6f8fa; --surface-2:#eef1f4;
  --fg:#14171a; --muted:#5b6572; --border:#e2e6eb;
  --accent:#2f5fd0; --accent-fg:#ffffff; --ok:#1a7f37; --warn:#9a6700;
  --r-lg:16px; --r-md:10px; --r-sm:8px;
  --ease-out:cubic-bezier(.23,1,.32,1);
  --shadow-1:0 1px 2px rgba(16,24,40,.04),0 1px 3px rgba(16,24,40,.06);
  --shadow-2:0 2px 4px rgba(16,24,40,.05),0 8px 20px rgba(16,24,40,.10);
  --z-sticky:20; --z-overlay:40; --z-modal:100;
  --head-h:54px;
}
@media (prefers-color-scheme:dark){
  :root{
    --bg:#0e1116; --surface:#161a21; --surface-2:#1c212a;
    --fg:#e6eaf0; --muted:#98a2b3; --border:#262c36;
    --accent:#7aa2ff; --accent-fg:#0e1116; --ok:#3fb950; --warn:#d29922;
    --shadow-1:0 1px 2px rgba(0,0,0,.4);
    --shadow-2:0 4px 14px rgba(0,0,0,.55);
  }
}
body[data-accent="blue"]{--accent:#2f5fd0;--accent-fg:#fff}
body[data-accent="amber"]{--accent:#b4550a;--accent-fg:#fff}
body[data-accent="neutral"]{--accent:#5b6572;--accent-fg:#fff}
@media (prefers-color-scheme:dark){
  body[data-accent="blue"]{--accent:#7aa2ff;--accent-fg:#0e1116}
  body[data-accent="amber"]{--accent:#e0a458;--accent-fg:#0e1116}
  body[data-accent="neutral"]{--accent:#98a2b3;--accent-fg:#0e1116}
}
*{box-sizing:border-box}
html{scroll-behavior:smooth}
body{
  margin:0; background:var(--bg); color:var(--fg);
  font:16px/1.55 var(--font-ui);
  -webkit-font-smoothing:antialiased; -moz-osx-font-smoothing:grayscale;
  text-rendering:optimizeLegibility;
}
h1,h2,h3,h4{text-wrap:balance}
.sr-only{position:absolute;width:1px;height:1px;padding:0;margin:-1px;
  overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap;border:0}
:focus-visible{outline:2px solid var(--accent);outline-offset:2px;border-radius:4px}
a{color:var(--accent)}

header{
  position:sticky; top:0; z-index:var(--z-sticky); min-height:var(--head-h);
  display:flex; align-items:center; gap:12px; flex-wrap:wrap;
  padding:6px clamp(10px,1.4vw,20px);
  background:var(--bg);
  border-bottom:1px solid var(--border);
}
h1{font-size:15px; font-weight:700; letter-spacing:.01em; margin:0; white-space:nowrap}
h1 a{color:var(--fg); text-decoration:none}
.tabs{
  display:flex; gap:2px; margin-left:auto; padding:2px;
  background:var(--surface-2); border:1px solid var(--border); border-radius:999px;
}
.tab{
  position:relative; display:inline-flex; align-items:center; gap:6px;
  min-height:30px; padding:3px 11px; border:0; border-radius:999px;
  background:transparent; color:var(--muted); font:inherit; font-size:13.5px;
  cursor:pointer; transition:color .12s,background .12s;
}
.tab::before{content:""; position:absolute; inset:-7px -3px}
.tab:hover{color:var(--fg)}
.tab[aria-selected="true"]{background:var(--bg); color:var(--fg); box-shadow:var(--shadow-1)}
.dot{width:7px; height:7px; border-radius:50%; background:var(--muted); flex:none}
.dot-amber{background:#b4550a}.dot-blue{background:#2f5fd0}.dot-neutral{background:#5b6572}
@media (prefers-color-scheme:dark){
  .dot-amber{background:#e0a458}.dot-blue{background:#7aa2ff}.dot-neutral{background:#98a2b3}
}

main{padding:12px clamp(10px,1.4vw,20px) 72px}
.hint{max-width:75ch; margin:0 0 14px; color:var(--muted); font-size:13.5px}

.panel{display:block; outline:none}
html.js .panel{display:none}
html.js .panel.active{display:block}

section{scroll-margin-top:calc(var(--head-h) + 8px)}
.sec-head{
  display:flex; align-items:center; gap:10px;
  border-bottom:2px solid var(--accent);
  padding:6px 0; margin:0 0 14px;
}
.sec-head h3{margin:0; font-size:15px; font-weight:650; letter-spacing:.01em}
section + section{margin-top:30px}
.badge{
  font-size:10.5px; font-weight:700; letter-spacing:.05em; text-transform:uppercase;
  color:var(--accent-fg); background:var(--accent);
  padding:2px 8px; border-radius:999px;
}
@media (min-width:820px){
  .sec-head{
    position:sticky; top:var(--head-h); z-index:var(--z-sticky);
    background:var(--bg); padding:8px 0;
  }
}

.card{
  margin:0 0 16px; padding:10px;
  background:var(--bg); border:1px solid var(--border);
  border-radius:var(--r-lg); box-shadow:var(--shadow-1);
}
.card h4{
  margin:0 0 8px; color:var(--muted);
  font-size:11.5px; font-weight:700; letter-spacing:.07em; text-transform:uppercase;
  font-variant-numeric:tabular-nums;
}
.card img{
  display:block; width:100%; height:auto; max-width:100%;
  border:1px solid var(--border); border-radius:var(--r-md);
  background:var(--surface); cursor:zoom-in;
}
.card img + img{margin-top:8px}
@media (hover:hover) and (pointer:fine){
  .card:hover{box-shadow:var(--shadow-2)}
  .card img:hover{border-color:var(--accent)}
}

.codebox{margin-top:10px; border:1px solid var(--border); border-radius:var(--r-md); overflow:hidden}
.codebar{
  display:flex; align-items:center; justify-content:space-between;
  padding:4px 10px; background:var(--surface-2);
  border-bottom:1px solid var(--border);
}
.codebar span{color:var(--muted); font:12px var(--font-mono)}
.copy{
  position:relative; font:inherit; font-size:12.5px; padding:3px 11px;
  color:var(--accent); background:var(--bg);
  border:1px solid var(--border); border-radius:var(--r-sm); cursor:pointer;
  transition:color .12s,border-color .12s,transform .1s;
}
.copy::before{content:""; position:absolute; inset:-6px -3px}
.copy:hover{border-color:var(--accent)}
.copy:active{transform:scale(.97)}
.copy.ok{color:var(--ok); border-color:var(--ok)}
pre{margin:0; padding:10px 12px; overflow:auto; max-height:70vh; background:var(--bg)}
code{
  font-family:var(--font-mono); font-size:clamp(12.5px,.5vw + 11px,13.5px);
  line-height:1.6; tab-size:4;
}
.soon{
  display:flex; align-items:center; gap:8px; margin-top:10px;
  padding:7px 12px; border:1px dashed var(--border); border-radius:var(--r-sm);
  color:var(--muted); font-size:13.5px;
}
.soon::before{
  content:""; width:7px; height:7px; border-radius:50%; background:var(--warn);
  animation:pulse 1.8s var(--ease-out) infinite; flex:none;
}
@keyframes pulse{0%,100%{opacity:.35}50%{opacity:1}}

footer{
  padding:18px clamp(10px,1.4vw,20px) 40px; color:var(--muted);
  font-size:12.5px; border-top:1px solid var(--border);
}

#top-btn{
  position:fixed; right:14px; bottom:14px; z-index:var(--z-overlay);
  width:40px; height:40px; border-radius:50%;
  border:1px solid var(--border); background:var(--bg); color:var(--fg);
  box-shadow:var(--shadow-2); font-size:17px; cursor:pointer; display:none;
}
#top-btn.show{display:grid; place-items:center}
#top-btn:active{transform:scale(.96)}

#lb{
  position:fixed; inset:0; z-index:var(--z-modal); display:grid; place-items:center;
  background:rgba(8,10,14,.88); backdrop-filter:blur(3px);
  touch-action:none; animation:fadeIn .18s var(--ease-out);
}
#lb[hidden]{display:none}
@keyframes fadeIn{from{opacity:0}to{opacity:1}}
.lb-controls{position:fixed; top:12px; right:12px; display:flex; gap:6px}
.lb-btn{
  width:40px; height:40px; display:grid; place-items:center; cursor:pointer;
  border:1px solid rgba(255,255,255,.22); border-radius:10px;
  background:rgba(22,26,33,.72); color:#fff; font-size:17px; line-height:1;
}
.lb-btn:active{transform:scale(.96)}
#lbimg{
  max-width:96vw; max-height:92vh; transform-origin:center;
  cursor:grab; touch-action:none; user-select:none; -webkit-user-drag:none;
  box-shadow:0 0 0 1px rgba(255,255,255,.15),0 10px 44px rgba(0,0,0,.6);
}

@media (prefers-reduced-motion:reduce){
  html{scroll-behavior:auto}
  *,*::before,*::after{animation-duration:.01ms !important;transition-duration:.01ms !important}
  .soon::before{animation:none; opacity:.6}
}
</style>
</head>
<body data-accent="blue">
<a class="sr-only" href="#content">К содержимому</a>
<header>
  <h1><a href="#content">МЦКО — разборы задач</a></h1>
  <div class="tabs" role="tablist" aria-label="Разделы">@TABS@</div>
</header>
<main id="content">
  <p class="hint">Клик по картинке — на весь экран (колесо/пинч — зум, двойной клик — сброс, Esc — закрыть). «Копировать» — забрать код решения.</p>
@MAIN@
</main>
<footer>Материалы: demo.mcko.ru · страница собирается скриптом build.py из репозитория</footer>
<button id="top-btn" aria-label="Наверх" title="Наверх">↑</button>
<div id="lb" hidden role="dialog" aria-modal="true" aria-label="Просмотр условия">
  <div class="lb-controls">
    <button class="lb-btn" data-act="out" aria-label="Уменьшить">−</button>
    <button class="lb-btn" data-act="in" aria-label="Увеличить">+</button>
    <button class="lb-btn" data-act="reset" aria-label="Сбросить масштаб">⤢</button>
    <button class="lb-btn" data-act="close" aria-label="Закрыть">✕</button>
  </div>
  <img id="lbimg" alt="">
</div>
<script>
(function(){
  var tabs=[].slice.call(document.querySelectorAll('.tab'));
  var panels=[].slice.call(document.querySelectorAll('.panel'));
  function byId(id){for(var i=0;i<tabs.length;i++)if(tabs[i].dataset.panel===id)return tabs[i];return null;}
  function activate(id,scroll){
    panels.forEach(function(p){p.classList.toggle('active',p.id===id);});
    tabs.forEach(function(t){var on=t.dataset.panel===id;t.setAttribute('aria-selected',on?'true':'false');t.tabIndex=on?0:-1;});
    var t=byId(id); if(t) document.body.dataset.accent=t.dataset.accent||'blue';
    try{localStorage.setItem('mcko-tab',id);}catch(e){}
    if(scroll) window.scrollTo(0,0);
  }
  tabs.forEach(function(t,i){
    t.addEventListener('click',function(){activate(t.dataset.panel,true);});
    t.addEventListener('keydown',function(e){
      var j=null;
      if(e.key==='ArrowRight')j=(i+1)%tabs.length;
      else if(e.key==='ArrowLeft')j=(i-1+tabs.length)%tabs.length;
      else if(e.key==='Home')j=0;
      else if(e.key==='End')j=tabs.length-1;
      if(j!==null){e.preventDefault();tabs[j].focus();activate(tabs[j].dataset.panel,false);}
    });
  });
  var start=null, hash=decodeURIComponent(location.hash.slice(1));
  if(hash){
    var el=document.getElementById(hash);
    if(el){ if(el.classList.contains('panel')) start=hash; else { var p=el.closest('.panel'); if(p) start=p.id; } }
  }
  if(!start){try{start=localStorage.getItem('mcko-tab');}catch(e){start=null;}}
  if(!start||!byId(start)) start='g10';
  activate(start,false);
  if(hash){var tgt=document.getElementById(hash); if(tgt&&!tgt.classList.contains('panel')) tgt.scrollIntoView();}
})();

(function(){
  var lb=document.getElementById('lb'), img=document.getElementById('lbimg');
  var btns=[].slice.call(lb.querySelectorAll('.lb-btn'));
  var focs=[img].concat(btns);
  var s=1,tx=0,ty=0,ptr=new Map(),drag=null,pinchD=0,pinchS=1,lastFocus=null;
  function draw(){img.style.transform='translate('+tx+'px,'+ty+'px) scale('+s+')';}
  function setZoom(v){s=Math.min(12,Math.max(1,v)); if(s===1){tx=0;ty=0;} draw();}
  function open(src,alt,from){lastFocus=from||null; img.src=src; img.alt=alt||''; s=1; tx=0; ty=0; draw();
    lb.hidden=false; document.body.style.overflow='hidden';
    var c=lb.querySelector('[data-act="close"]'); if(c)c.focus();}
  function close(){lb.hidden=true; img.removeAttribute('src'); document.body.style.overflow='';
    if(lastFocus&&lastFocus.focus)lastFocus.focus();}
  [].slice.call(document.querySelectorAll('.card img')).forEach(function(im){
    im.setAttribute('tabindex','0');
    im.addEventListener('click',function(){open(im.src,im.alt,im);});
    im.addEventListener('keydown',function(e){if(e.key==='Enter'||e.key===' '){e.preventDefault();open(im.src,im.alt,im);}});
  });
  lb.addEventListener('click',function(e){if(e.target===lb)close();});
  document.addEventListener('keydown',function(e){if(!lb.hidden&&e.key==='Escape')close();});
  btns.forEach(function(b){b.addEventListener('click',function(){
    var a=b.dataset.act;
    if(a==='close')close(); else if(a==='in')setZoom(s*1.25);
    else if(a==='out')setZoom(s/1.25); else if(a==='reset')setZoom(1);
  });});
  lb.addEventListener('keydown',function(e){
    if(e.key!=='Tab')return; var i=focs.indexOf(document.activeElement); if(i===-1)return;
    e.preventDefault(); var n=(i+(e.shiftKey?-1:1)+focs.length)%focs.length; focs[n].focus();
  });
  img.addEventListener('wheel',function(e){
    e.preventDefault();
    var f=e.deltaY<0?1.15:1/1.15, ns=Math.min(12,Math.max(1,s*f));
    if(ns===s)return;
    var r=img.getBoundingClientRect(), cx=e.clientX-r.left-r.width/2, cy=e.clientY-r.top-r.height/2;
    tx=cx-(cx-tx)*(ns/s); ty=cy-(cy-ty)*(ns/s); s=ns; draw();
  },{passive:false});
  img.addEventListener('pointerdown',function(e){
    img.setPointerCapture(e.pointerId); ptr.set(e.pointerId,e);
    if(ptr.size===1)drag={x:e.clientX,y:e.clientY,tx:tx,ty:ty};
    else if(ptr.size===2){var a=[].slice.call(ptr.values());
      pinchD=Math.hypot(a[0].clientX-a[1].clientX,a[0].clientY-a[1].clientY); pinchS=s;}
  });
  img.addEventListener('pointermove',function(e){
    if(!ptr.has(e.pointerId))return; ptr.set(e.pointerId,e);
    if(ptr.size===2){
      var a=[].slice.call(ptr.values());
      var d=Math.hypot(a[0].clientX-a[1].clientX,a[0].clientY-a[1].clientY);
      s=Math.min(12,Math.max(1,pinchS*d/pinchD)); draw();
    }else if(drag){ tx=drag.tx+e.clientX-drag.x; ty=drag.ty+e.clientY-drag.y; draw(); }
  });
  function up(e){ptr.delete(e.pointerId);
    if(ptr.size===1){var p=[].slice.call(ptr.values())[0];drag={x:p.clientX,y:p.clientY,tx:tx,ty:ty};}
    else if(ptr.size===0)drag=null;}
  img.addEventListener('pointerup',up);
  img.addEventListener('pointercancel',up);
  img.addEventListener('dblclick',function(e){e.preventDefault(); if(s>1){setZoom(1);}else{setZoom(2.5);}});
})();

(function(){
  function copyText(text){
    if(navigator.clipboard&&window.isSecureContext) return navigator.clipboard.writeText(text);
    return new Promise(function(res,rej){
      var ta=document.createElement('textarea'); ta.value=text;
      ta.style.position='fixed'; ta.style.opacity='0'; document.body.appendChild(ta); ta.select();
      try{document.execCommand('copy')?res():rej();}catch(err){rej(err);}finally{ta.remove();}
    });
  }
  document.querySelectorAll('.copy').forEach(function(b){
    b.addEventListener('click',function(){
      var code=b.closest('.codebox').querySelector('code').textContent;
      copyText(code).then(function(){
        b.textContent='Скопировано'; b.classList.add('ok');
        setTimeout(function(){b.textContent='Копировать'; b.classList.remove('ok');},1500);
      }).catch(function(){
        b.textContent='Не вышло';
        setTimeout(function(){b.textContent='Копировать';},1500);
      });
    });
  });
})();

(function(){
  var btn=document.getElementById('top-btn');
  addEventListener('scroll',function(){btn.classList.toggle('show',scrollY>700);},{passive:true});
  btn.addEventListener('click',function(){scrollTo({top:0,behavior:'smooth'});});
})();
</script>
</body>
</html>
"""


if __name__ == "__main__":
    sys.exit(build())
