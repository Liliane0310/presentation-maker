# HTML Template

这是 `presentation-maker` 的唯一骨架来源。生成新的 deck 时，复用这里的结构、样式和脚本，只替换标题、页内容、页数和 `.notes`。默认对齐手绘纸感 16:9 演示文稿风格。

## 使用原则

- 保持单个自包含 HTML。
- 保持 `main.deck > section.slide > div.card` 的结构。
- 保持底部导航、进度条、键盘翻页、滚轮/触摸翻页、`F` 全屏和 `S` 演讲者模式。
- 首页不要写快捷键或翻页操作说明；需要署名时使用 `.brand-mark`。
- 内容少的页给 `section.slide` 添加 `.center-content`；内容多的页不加。
- 只在必要时新增局部组件，优先复用模板中的 `grid`、`emoji`、`flow`。
- **模板里的 `--font` 把 `XiaoLai` 放在回退位置，生成 HTML 后必须运行 `scripts/embed-font.py` 注入字体**，否则用户机器看不到小赖。详见 `references/style-tokens.md` 的"小赖字体注入机制"。

## 可替换区域

- `<title>`
- 封面页标题、副标题、总纲句、品牌/署名
- 各个 `section.slide` 的正文内容
- 各个 `section.slide` 中的 `.notes`
- 页面标题和页数

## 模板

```html
<!doctype html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title><!-- 替换为主题标题 --></title>
<style>
  :root{
    --paper:#fffdf8;
    --ink:#1f2937;
    --muted:#5b6470;
    --accent:#8f4d2e;
    --accent-soft:#f3e6da;
    --line:#d8d0c4;
    --shadow:0 24px 60px rgba(88,59,34,.12);
    --h1:3.3rem;
    --h2:2.35rem;
    --p:1.48rem;
    --radius:18px;
    --transition:600ms;
    --slide-x:clamp(68px,7vw,112px);
    --slide-y:clamp(42px,6vh,72px);
    --font:"Segoe UI",Roboto,Arial,"Helvetica Neue","XiaoLai","Xiaolai","小赖字体","Microsoft YaHei",system-ui,-apple-system,sans-serif;
    --mono:ui-monospace,SFMono-Regular,Menlo,Monaco,Consolas,"Liberation Mono","Courier New",monospace;
  }
  *{box-sizing:border-box}
  html,body{height:100%;margin:0;overflow:hidden}
  body{
    color:var(--ink);
    font-family:var(--font);
    background:
      radial-gradient(circle at top left, rgba(202,141,107,.18), transparent 28%),
      linear-gradient(135deg,#f4ede4 0%,#efe7db 40%,#f7f2eb 100%);
  }
  body::before{
    content:"";
    position:fixed;
    inset:0;
    pointer-events:none;
    background:
      repeating-linear-gradient(90deg, rgba(143,77,46,.028) 0 1px, transparent 1px 18px),
      repeating-linear-gradient(180deg, rgba(143,77,46,.020) 0 1px, transparent 1px 22px);
    opacity:.62;
    mix-blend-mode:multiply;
  }
  .deck{width:100vw;height:100vh;position:relative}
  .slide{
    width:100vw;
    height:100vh;
    padding:var(--slide-y) var(--slide-x) calc(var(--slide-y) + 52px);
    display:flex;
    align-items:stretch;
    justify-content:stretch;
    position:absolute;
    inset:0;
    opacity:0;
    transform:translateY(30px);
    transition:opacity var(--transition) ease, transform var(--transition) ease;
    pointer-events:none;
  }
  .slide.is-active{opacity:1;transform:translateY(0);pointer-events:auto}
  .card{
    width:100%;
    min-height:calc(100vh - (var(--slide-y) * 2) - 52px);
    background:var(--paper);
    border:1px solid var(--line);
    box-shadow:var(--shadow);
    border-radius:var(--radius);
    position:relative;
    overflow:hidden;
    padding:clamp(30px,4.6vh,48px) clamp(42px,5vw,70px);
    display:flex;
    flex-direction:column;
    justify-content:flex-start;
  }
  .card::before{
    content:"";
    position:absolute;
    inset:0;
    pointer-events:none;
    background:
      linear-gradient(90deg, rgba(143,77,46,.04), transparent 18%),
      linear-gradient(180deg, rgba(143,77,46,.02), transparent 20%);
    opacity:.9;
  }
  .card::after{
    content:"";
    position:absolute;
    inset:0;
    pointer-events:none;
    background:linear-gradient(180deg, rgba(243,230,218,.55), rgba(255,253,248,.92));
    opacity:.75;
    mix-blend-mode:multiply;
  }
  .card>*{position:relative;z-index:1}
  .slide.center-content .card,
  .slide:first-child .card{justify-content:center}
  h1{margin:0 0 1.05rem;font-size:var(--h1);letter-spacing:1px;line-height:1.1;font-weight:800;color:var(--ink)}
  h2{margin:0 0 1.2rem;font-size:var(--h2);line-height:1.25;font-weight:800;color:var(--accent);display:inline-flex;align-items:center;gap:10px}
  h2::before{content:"";width:22px;height:10px;border-radius:999px;background:linear-gradient(90deg,var(--accent),#d2a384);flex:0 0 auto}
  h3{font-size:1.35rem;margin:1rem 0 .45rem;color:var(--ink)}
  p,li{font-size:var(--p);line-height:1.5;margin:.55rem 0;color:var(--ink)}
  .big{font-size:1.58rem;line-height:1.5}
  .muted{color:var(--muted)}
  .highlight{color:var(--accent);font-weight:800}
  .kicker{letter-spacing:4px;color:var(--accent);font-weight:800;text-transform:uppercase;font-size:1rem;margin-bottom:1rem}
  .brand-mark{margin-top:1.35rem;display:inline-flex;align-items:center;gap:.55rem;width:fit-content;padding:.42rem .82rem;border:1px solid rgba(143,77,46,.22);border-radius:999px;background:rgba(243,230,218,.62);color:var(--accent);font-size:1.18rem;line-height:1;box-shadow:0 12px 30px rgba(88,59,34,.08)}
  .brand-mark::before{content:"";width:22px;height:10px;border-radius:999px;background:linear-gradient(90deg,var(--accent),#d2a384)}
  ul.emoji{list-style:none;padding:0;margin:1rem 0 0;display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:.55rem 1.25rem}
  ul.emoji li{display:flex;gap:.72rem;align-items:flex-start;min-width:0}
  blockquote{margin:1.05rem 0 0;padding:.75rem 1.1rem;border-left:6px solid var(--accent);background:rgba(143,77,46,.06);border-radius:12px}
  code,kbd,pre{font-family:var(--mono)}
  code,kbd{font-size:.95em;background:rgba(31,41,55,.06);padding:.05em .35em;border-radius:8px;color:#5b2e17}
  pre{font-size:1rem;background:rgba(31,41,55,.05);padding:.85rem 1rem;border-radius:12px;overflow-x:auto;line-height:1.45;margin:1rem 0}
  .grid{display:grid;gap:20px}
  .grid.c2{grid-template-columns:repeat(2,minmax(0,1fr))}
  .grid.c3{grid-template-columns:repeat(3,minmax(0,1fr))}
  .cardlet{background:rgba(255,253,248,.72);border:1px solid rgba(143,77,46,.14);border-radius:16px;padding:22px 24px;box-shadow:0 14px 34px rgba(88,59,34,.08)}
  .cardlet h4{margin:0 0 .55rem;color:var(--accent);font-size:1.3rem}
  .cardlet p{margin:0;color:var(--muted)}
  table{width:100%;border-collapse:separate;border-spacing:0;margin:1rem 0;border:1px solid var(--line);border-radius:12px;overflow:hidden;background:rgba(255,253,248,.76)}
  th,td{padding:.62rem .8rem;text-align:left;font-size:1.08rem;border-bottom:1px solid var(--line);vertical-align:top}
  th{background:var(--accent-soft);color:var(--accent);font-weight:800}
  tr:last-child td{border-bottom:none}
  .flow{display:flex;align-items:center;gap:12px;flex-wrap:wrap;margin:1rem 0}
  .node{padding:.7rem 1rem;background:rgba(255,253,248,.76);border:1.5px solid var(--accent);border-radius:14px;color:var(--accent);font-weight:800;box-shadow:0 4px 0 var(--accent-soft)}
  .arrow{color:var(--accent);font-size:1.4rem;font-weight:800}

  .nav{position:fixed;left:0;right:0;bottom:0;padding:14px 18px;display:grid;grid-template-columns:1fr auto 1fr;align-items:center;gap:14px;background:linear-gradient(to top,rgba(247,242,235,.96),rgba(247,242,235,.60),transparent);backdrop-filter:blur(6px);z-index:10}
  .controls{display:flex;gap:10px;justify-content:flex-start}
  .btn{font-family:var(--font);padding:8px 14px;border-radius:999px;border:1px solid var(--line);background:var(--paper);color:var(--ink);cursor:pointer;box-shadow:0 6px 16px rgba(88,59,34,.10);font-size:1rem}
  .btn:hover{border-color:var(--accent);color:var(--accent)}
  .pager{justify-self:center;font-family:var(--mono);color:rgba(31,41,55,.78)}
  .progress{height:8px;border-radius:999px;background:rgba(143,77,46,.14);overflow:hidden;box-shadow:inset 0 0 0 1px rgba(143,77,46,.10);grid-column:1/-1}
  .bar{height:100%;width:0;background:linear-gradient(90deg,rgba(143,77,46,.85),rgba(210,163,132,.95));border-radius:999px;transition:width 260ms ease}
  .notes{display:none}

  @media (max-height:820px) and (min-width:721px){
    :root{--h2:2.12rem;--p:1.32rem;--slide-y:36px}
    .card{padding:28px clamp(40px,4.8vw,64px)}
    h2{margin-bottom:.85rem}
    ul.emoji{gap:.4rem 1.05rem;margin-top:.75rem}
    blockquote{margin-top:.8rem}
    pre{font-size:.92rem;line-height:1.36}
  }
  @media (max-width:720px){
    :root{--h1:2.55rem;--h2:1.85rem;--p:1.16rem;--slide-x:18px;--slide-y:22px}
    .card{padding:24px 20px;min-height:calc(100vh - 96px)}
    ul.emoji,.grid.c2,.grid.c3{grid-template-columns:1fr}
    .flow-labels{grid-template-columns:1fr;font-size:1rem}
    .flow-arrow{display:none}
    .controls .btn{display:none}
  }
  @media (prefers-reduced-motion:reduce){
    .slide,.flow-arrow{animation:none;transition:none}
  }
</style>
</head>
<body>
<main class="deck" id="deck" aria-label="Slide Deck">
  <section class="slide is-active" data-title="封面">
    <div class="card">
      <div class="kicker"><!-- 可选：英文小标题 --></div>
      <h1><!-- 替换为封面主标题 --></h1>
      <p class="big muted"><!-- 替换为封面副标题或导语 --></p>
      <blockquote><!-- 替换为一句总纲或金句 --></blockquote>
      <div class="brand-mark"><!-- 替换为作者/品牌/课程名 --></div>
    </div>
    <div class="notes"><!-- 替换为本页 notes --></div>
  </section>

  <section class="slide center-content" data-title="概念">
    <div class="card">
      <h2><!-- 替换为常规页标题 --></h2>
      <p class="big"><!-- 替换为核心说明 --></p>
      <ul class="emoji">
        <li><span>💡</span><span><!-- 要点 1 --></span></li>
        <li><span>📦</span><span><!-- 要点 2 --></span></li>
      </ul>
      <blockquote><!-- 替换为结论 --></blockquote>
    </div>
    <div class="notes"><!-- 替换为本页 notes --></div>
  </section>
</main>

<footer class="nav" aria-label="Navigation">
  <div class="controls">
    <button class="btn" id="prev">上一页</button>
    <button class="btn" id="next">下一页</button>
  </div>
  <div class="pager" id="pager">1 / 1</div>
  <div></div>
  <div class="progress"><div class="bar" id="bar"></div></div>
</footer>

<script>
(function(){
  const slides = Array.from(document.querySelectorAll('.slide'));
  const prevBtn = document.getElementById('prev');
  const nextBtn = document.getElementById('next');
  const pager = document.getElementById('pager');
  const bar = document.getElementById('bar');
  let index = 0, presenterWin = null;
  function clamp(n,min,max){return Math.max(min,Math.min(max,n))}
  function getTitle(i){const h=slides[i].querySelector('h1,h2');return h?h.textContent.trim():'Slide '+(i+1)}
  function getNotes(i){const n=slides[i].querySelector('.notes');return n?n.innerHTML.trim():'<em style="color:#999">（本页无逐字稿）</em>'}
  function render(){
    slides.forEach((s,i)=>s.classList.toggle('is-active',i===index));
    pager.textContent=(index+1)+' / '+slides.length;
    bar.style.width=(slides.length<=1?100:index/(slides.length-1)*100)+'%';
    location.hash='/' + (index + 1);
    if(presenterWin && !presenterWin.closed) updatePresenter();
  }
  function goTo(i){index=clamp(i,0,slides.length-1);render()}
  function next(){goTo(index+1)}
  function prev(){goTo(index-1)}
  if(prevBtn) prevBtn.onclick=prev;
  if(nextBtn) nextBtn.onclick=next;
  function openPresenter(){
    if(presenterWin && !presenterWin.closed){presenterWin.focus();return}
    presenterWin=window.open('', 'presenter', 'width=900,height=680,scrollbars=yes');
    const d=presenterWin.document;
    d.write(`<!doctype html><html><head><meta charset="UTF-8"><title>演讲者模式</title><style>
    *{box-sizing:border-box}body{margin:0;font-family:"Segoe UI",Roboto,Arial,"Helvetica Neue","XiaoLai","Xiaolai","小赖字体","Microsoft YaHei",system-ui,sans-serif;background:#1f2937;color:#fffdf8;padding:16px;display:grid;grid-template-columns:1fr 1fr;grid-template-rows:auto 1fr auto;gap:12px;height:100vh;overflow:hidden}.card{background:#2d3748;border-radius:14px;overflow:hidden}.card-header{padding:10px 16px;font-size:13px;font-weight:700}.h-current .card-header{background:#8f4d2e}.h-next .card-header{background:#d2a384;color:#1f2937}.h-script .card-header{background:#c4956a;color:#1f2937}.h-timer .card-header{background:#f3e6da;color:#8f4d2e}.card-body{padding:16px}.slide-title{font-size:15px;color:#a0a0b0;margin-bottom:8px}.slide-preview{font-size:20px;font-weight:700;color:#fffdf8}#scriptBody{font-size:17px;line-height:1.85;color:#e8e0d8;overflow-y:auto;padding:16px;flex:1;min-height:0}.timer-display{font-size:28px;font-weight:800;text-align:center;font-family:ui-monospace,SFMono-Regular,Menlo,monospace;color:#d2a384}.timer-btns{display:flex;gap:8px;justify-content:center}.timer-btns button{padding:5px 14px;border:none;border-radius:6px;background:#3d4a5c;color:#fffdf8;font-size:12px;cursor:pointer;font-family:inherit}</style></head><body>
    <div class="card h-current"><div class="card-header">当前</div><div class="card-body"><div class="slide-title" id="pCurTitle"></div><div class="slide-preview" id="pCurPreview"></div></div></div>
    <div class="card h-next"><div class="card-header">下一页</div><div class="card-body"><div class="slide-title" id="pNextTitle"></div><div class="slide-preview" id="pNextPreview"></div></div></div>
    <div class="card h-script" style="grid-column:1/3;display:flex;flex-direction:column;min-height:0"><div class="card-header">逐字稿 / Speaker Script</div><div id="scriptBody"></div></div>
    <div class="card h-timer" style="grid-column:1/3"><div class="card-header">计时器</div><div class="card-body"><div class="timer-display" id="pTimer">00:00</div><div class="timer-btns"><button onclick="prev()">上一页</button><button onclick="resetTimer()">重置</button><button onclick="next()">下一页</button></div></div></div></body></html>`);
    d.close();
    let start=Date.now();
    presenterWin._timerInterval=setInterval(()=>{if(presenterWin.closed){clearInterval(presenterWin._timerInterval);return}const e=Math.floor((Date.now()-start)/1000);const m=String(Math.floor(e/60)).padStart(2,'0');const s=String(e%60).padStart(2,'0');const el=presenterWin.document.getElementById('pTimer');if(el)el.textContent=m+':'+s},500);
    presenterWin.resetTimer=()=>{start=Date.now()};
    presenterWin.prev=prev;
    presenterWin.next=next;
    updatePresenter();
  }
  function updatePresenter(){
    const d=presenterWin.document;
    d.getElementById('pCurTitle').textContent='Slide '+(index+1);
    d.getElementById('pCurPreview').textContent=getTitle(index);
    d.getElementById('pNextTitle').textContent=index<slides.length-1?'Slide '+(index+2):'';
    d.getElementById('pNextPreview').textContent=index<slides.length-1?getTitle(index+1):'— 最后一页 —';
    d.getElementById('scriptBody').innerHTML=getNotes(index);
  }
  document.addEventListener('keydown',e=>{if(e.key==='ArrowRight'||e.key===' '||e.key==='PageDown'){e.preventDefault();next()}else if(e.key==='ArrowLeft'||e.key==='PageUp'){e.preventDefault();prev()}else if(e.key==='Home')goTo(0);else if(e.key==='End')goTo(slides.length-1);else if(e.key==='f'||e.key==='F'){if(!document.fullscreenElement)document.documentElement.requestFullscreen();else document.exitFullscreen()}else if(e.key==='s'||e.key==='S')openPresenter()});
  window.addEventListener('wheel',(()=>{let lock=false;return e=>{if(lock)return;lock=true;if(e.deltaY>0)next();else if(e.deltaY<0)prev();setTimeout(()=>lock=false,420)}})(),{passive:true});
  const hash=parseInt(location.hash.replace('#/',''),10);if(hash>=1&&hash<=slides.length)index=hash-1;
  render();
})();
</script>
</body>
</html>
```
