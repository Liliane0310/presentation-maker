# HTML Template

这是 `presentation-maker` 的唯一骨架来源。生成新的 deck 时，复用这里的结构、样式和脚本，只替换标题、页内容、页数和 `.notes`。默认对齐 `Workflow入门.html` 的单页纸张演示风格。

## 使用原则

- 保持单个自包含 HTML
- 保持 `body > .progress + .slide-number + .stage > section.slide` 的整体结构
- 保持顶部进度条、底部翻页控件、键盘翻页和 `S` 键演讲者模式
- 不随意改造底层运行逻辑
- 只在必要时新增局部组件

## 可替换区域

- `<title>`
- 封面页标题、副标题、总纲句
- 各个 `section.slide` 的正文内容
- 各个 `section.slide` 中的 `.notes`
- 页数总数和页面标题

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
    --font:"XiaoLai","Xiaolai","小赖字体","Microsoft YaHei",system-ui,-apple-system,Segoe UI,Roboto,sans-serif;
    --mono:ui-monospace,SFMono-Regular,Menlo,Monaco,Consolas,"Liberation Mono","Courier New",monospace;
  }
  *{box-sizing:border-box}
  html,body{margin:0;padding:0;height:100%;}
  body{
    font-family:var(--font);
    color:var(--ink);
    background:
      radial-gradient(1200px 700px at 0% 0%, rgba(202,141,107,.18), transparent 60%),
      linear-gradient(135deg,#f4ede4 0%,#efe7db 50%,#f7f2eb 100%);
    min-height:100vh;
    overflow-x:hidden;
  }
  body::before{
    content:"";
    position:fixed;inset:0;
    pointer-events:none;
    background-image:
      repeating-linear-gradient(0deg, rgba(143,77,46,.03) 0 1px, transparent 1px 3px),
      repeating-linear-gradient(90deg, rgba(143,77,46,.02) 0 1px, transparent 1px 4px);
    mix-blend-mode:multiply;
    z-index:0;
  }
  .stage{
    position:relative;
    z-index:1;
    min-height:100vh;
    display:flex;
    align-items:center;
    justify-content:center;
    padding:56px 24px 120px;
  }
  .slide{
    display:none;
    width:min(1040px,100%);
    background:var(--paper);
    border:1px solid var(--line);
    border-radius:18px;
    box-shadow:var(--shadow);
    padding:64px 72px;
    position:relative;
  }
  .slide.active{display:block;animation:fade .45s ease both}
  @keyframes fade{from{opacity:0;transform:translateY(8px)}to{opacity:1;transform:none}}

  h1{font-size:3.3rem;line-height:1.1;margin:0 0 18px;font-weight:800;letter-spacing:.5px}
  h2{
    font-size:1.9rem;color:var(--accent);margin:0 0 24px;
    display:flex;align-items:center;gap:14px;font-weight:800;
  }
  h2::before{
    content:"";display:inline-block;width:22px;height:10px;border-radius:6px;
    background:linear-gradient(90deg,var(--accent),#d2a384);
  }
  h3{font-size:1.25rem;margin:18px 0 8px;color:var(--ink)}
  p{font-size:1.08rem;line-height:1.8;color:var(--ink);margin:10px 0}
  .muted{color:var(--muted)}
  .kicker{letter-spacing:6px;color:var(--accent);font-weight:700;text-transform:uppercase;font-size:.85rem;margin-bottom:18px}
  .big{font-size:1.35rem;line-height:1.8}

  ul.emoji{list-style:none;padding:0;margin:8px 0}
  ul.emoji li{
    padding:10px 0 10px 2px;
    border-bottom:1px dashed var(--line);
    font-size:1.05rem;line-height:1.7;
  }
  ul.emoji li:last-child{border-bottom:none}

  blockquote{
    margin:18px 0;padding:16px 20px;
    border-left:6px solid var(--accent);
    background:rgba(143,77,46,.06);
    border-radius:12px;color:var(--ink);
    font-size:1.05rem;line-height:1.75;
  }

  code,kbd{font-family:var(--mono);font-size:.95em;background:var(--accent-soft);padding:2px 8px;border-radius:6px;color:#5b2e17}
  kbd{border:1px solid var(--line);box-shadow:0 2px 0 var(--line)}

  .grid{display:grid;gap:18px}
  .grid.c2{grid-template-columns:1fr 1fr}
  .grid.c3{grid-template-columns:repeat(3,1fr)}
  .card{
    background:#fff;border:1px solid var(--line);border-radius:14px;
    padding:20px 22px;box-shadow:0 6px 18px rgba(88,59,34,.06)
  }
  .card h4{margin:0 0 8px;color:var(--accent);font-size:1.05rem}
  .card p{margin:0;font-size:.98rem;color:var(--muted)}

  table{
    width:100%;border-collapse:separate;border-spacing:0;margin:12px 0;
    border:1px solid var(--line);border-radius:12px;overflow:hidden;background:#fff
  }
  th,td{padding:12px 14px;text-align:left;font-size:1rem;border-bottom:1px solid var(--line)}
  th{background:var(--accent-soft);color:var(--accent);font-weight:700}
  tr:last-child td{border-bottom:none}

  .flow{display:flex;align-items:center;gap:10px;flex-wrap:wrap;margin:14px 0}
  .node{
    padding:12px 18px;background:#fff;border:1.5px solid var(--accent);
    border-radius:14px;color:var(--accent);font-weight:700;
    box-shadow:0 4px 0 var(--accent-soft);
  }
  .arrow{color:var(--accent);font-size:1.4rem;font-weight:700}

  .controls{
    position:fixed;left:0;right:0;bottom:20px;z-index:10;
    display:flex;justify-content:center;align-items:center;gap:14px;
  }
  .btn{
    font-family:var(--font);
    padding:10px 18px;border-radius:999px;border:1px solid var(--line);
    background:var(--paper);color:var(--ink);cursor:pointer;
    box-shadow:0 6px 16px rgba(88,59,34,.1);font-size:1rem;
  }
  .btn:hover{border-color:var(--accent);color:var(--accent)}
  .pager{
    background:var(--paper);border:1px solid var(--line);
    padding:8px 16px;border-radius:999px;font-family:var(--mono);color:var(--muted)
  }
  .progress{
    position:fixed;top:0;left:0;height:3px;background:linear-gradient(90deg,var(--accent),#d2a384);
    width:0;transition:width .3s ease;z-index:20;
  }
  .notes{display:none}
  @media (max-width:720px){
    .slide{padding:40px 24px}
    h1{font-size:2.2rem}
    .grid.c2,.grid.c3{grid-template-columns:1fr}
  }
</style>
</head>
<body>
<div class="progress" id="progress"></div>
<div class="slide-number" id="slideNum" style="position:fixed;bottom:20px;right:30px;font-size:13px;font-family:var(--mono);color:var(--muted);z-index:100"></div>
<div class="stage">

  <section class="slide active">
    <div class="kicker"><!-- 替换为英文小标题 --></div>
    <h1><!-- 替换为封面主标题 --></h1>
    <p class="big muted"><!-- 替换为封面副标题或导语 --></p>
    <blockquote><!-- 替换为一句总纲或金句 --></blockquote>
    <div class="notes"><!-- 替换为本页 notes --></div>
  </section>

  <section class="slide">
    <h2><!-- 替换为常规页标题 --></h2>
    <div class="grid c2">
      <div class="card">
        <h4><!-- 左卡标题 --></h4>
        <p><!-- 左卡内容 --></p>
      </div>
      <div class="card">
        <h4><!-- 右卡标题 --></h4>
        <p><!-- 右卡内容 --></p>
      </div>
    </div>
    <div class="notes"><!-- 替换为本页 notes --></div>
  </section>

</div>

<div class="controls">
  <button class="btn" id="prev">← 上一页</button>
  <div class="pager" id="pager">1 / 2</div>
  <button class="btn" id="next">下一页 →</button>
</div>

<script>
(function(){
  const slides = document.querySelectorAll('.slide');
  const prevBtn = document.getElementById('prev');
  const nextBtn = document.getElementById('next');
  const pager = document.getElementById('pager');
  const progress = document.getElementById('progress');
  const slideNum = document.getElementById('slideNum');
  let current = 0, presenterWin = null;

  function goto(n){
    current = Math.max(0, Math.min(n, slides.length - 1));
    slides.forEach((s, idx) => s.classList.toggle('active', idx === current));
    pager.textContent = (current + 1) + ' / ' + slides.length;
    progress.style.width = ((current + 1) / slides.length * 100) + '%';
    if(slideNum) slideNum.textContent = (current + 1) + ' / ' + slides.length;
    location.hash = '/' + (current + 1);
    if(presenterWin && !presenterWin.closed) updatePresenter();
  }

  prevBtn.onclick = () => goto(current - 1);
  nextBtn.onclick = () => goto(current + 1);

  function getTitle(idx){
    const s = slides[idx];
    const h = s.querySelector('h1') || s.querySelector('h2');
    return h ? h.textContent.trim() : 'Slide ' + (idx + 1);
  }
  function getNotes(idx){
    const n = slides[idx].querySelector('.notes');
    return n ? n.innerHTML.trim() : '<em style="color:#999">（本页无逐字稿）</em>';
  }

  function openPresenter(){
    if(presenterWin && !presenterWin.closed){ presenterWin.focus(); return; }
    presenterWin = window.open('', 'presenter', 'width=900,height=680,scrollbars=yes');
    const doc = presenterWin.document;
    doc.write(`<!DOCTYPE html><html><head><meta charset="UTF-8"><title>演讲者模式</title>
    <style>
      *{margin:0;padding:0;box-sizing:border-box}
      body{font-family:"XiaoLai","Microsoft YaHei",system-ui,sans-serif;background:#1f2937;color:#fffdf8;padding:16px;display:grid;grid-template-columns:1fr 1fr;grid-template-rows:auto 1fr auto;gap:12px;height:100vh;overflow:hidden}
      .card{background:#2d3748;border-radius:14px;overflow:hidden}
      .card-header{padding:10px 16px;font-size:13px;font-weight:700;text-transform:uppercase;letter-spacing:1px}
      .h-current .card-header{background:#8f4d2e}
      .h-next .card-header{background:#d2a384;color:#1f2937}
      .h-script .card-header{background:#c4956a;color:#1f2937}
      .h-timer .card-header{background:#f3e6da;color:#8f4d2e}
      .card-body{padding:16px}
      .slide-title{font-size:15px;color:#a0a0b0;margin-bottom:8px}
      .slide-preview{font-size:20px;font-weight:700;color:#fffdf8}
      #scriptBody{font-size:17px;line-height:1.85;color:#e8e0d8;overflow-y:auto;padding:16px;flex:1;min-height:0}
      #scriptBody strong,#scriptBody b{color:#d2a384}
      .timer-display{font-size:28px;font-weight:800;text-align:center;font-family:ui-monospace,SFMono-Regular,Menlo,monospace;color:#d2a384;padding:4px 0}
      .timer-slide{text-align:center;font-size:13px;color:#a0a0b0;margin-bottom:4px}
      .timer-btns{display:flex;gap:8px;justify-content:center;padding-bottom:4px}
      .timer-btns button{padding:5px 14px;border:none;border-radius:6px;background:#3d4a5c;color:#fffdf8;font-size:12px;cursor:pointer;font-weight:600;font-family:inherit}
    </style></head><body>
      <div class="card h-current" style="grid-column:1"><div class="card-header">当前</div><div class="card-body"><div class="slide-title" id="pCurTitle"></div><div class="slide-preview" id="pCurPreview"></div></div></div>
      <div class="card h-next" style="grid-column:2"><div class="card-header">下一页</div><div class="card-body"><div class="slide-title" id="pNextTitle"></div><div class="slide-preview" id="pNextPreview"></div></div></div>
      <div class="card h-script" style="grid-column:1/3;display:flex;flex-direction:column;min-height:0;overflow:hidden"><div class="card-header">逐字稿 / Speaker Script</div><div id="scriptBody"></div></div>
      <div class="card h-timer" style="grid-column:1/3"><div class="card-header" style="padding:6px 16px;font-size:11px">计时器</div><div class="card-body" style="padding:6px 16px">
        <div class="timer-slide" id="pSlideCount"></div>
        <div class="timer-display" id="pTimer">00:00</div>
        <div class="timer-btns"><button onclick="prev()">上一页</button><button onclick="resetTimer()">重置</button><button onclick="next()">下一页</button></div>
      </div></div>
    </body></html>`);
    doc.close();

    let startTime = Date.now();
    presenterWin._timerInterval = setInterval(() => {
      if(presenterWin.closed){ clearInterval(presenterWin._timerInterval); return; }
      const elapsed = Math.floor((Date.now() - startTime) / 1000);
      const m = String(Math.floor(elapsed / 60)).padStart(2, '0');
      const s = String(elapsed % 60).padStart(2, '0');
      const el = presenterWin.document.getElementById('pTimer');
      if(el) el.textContent = m + ':' + s;
    }, 500);

    presenterWin.resetTimer = () => { startTime = Date.now(); };
    presenterWin.prev = () => { goto(current - 1); };
    presenterWin.next = () => { goto(current + 1); };
    presenterWin.document.addEventListener('keydown', (e) => {
      if(e.key === 'ArrowRight') goto(current + 1);
      else if(e.key === 'ArrowLeft') goto(current - 1);
      else if(e.key === 'r' || e.key === 'R') presenterWin.resetTimer();
      else if(e.key === 'Escape') presenterWin.close();
    });

    updatePresenter();
  }

  function updatePresenter(){
    if(!presenterWin || presenterWin.closed) return;
    const doc = presenterWin.document;
    const cur = doc.getElementById('pCurTitle');
    const curP = doc.getElementById('pCurPreview');
    const nxtT = doc.getElementById('pNextTitle');
    const nxtP = doc.getElementById('pNextPreview');
    const script = doc.getElementById('scriptBody');
    const count = doc.getElementById('pSlideCount');
    if(cur) cur.textContent = 'Slide ' + (current + 1);
    if(curP) curP.textContent = getTitle(current);
    if(current < slides.length - 1){
      if(nxtT) nxtT.textContent = 'Slide ' + (current + 2);
      if(nxtP) nxtP.textContent = getTitle(current + 1);
    } else {
      if(nxtT) nxtT.textContent = '';
      if(nxtP) nxtP.textContent = '— 最后一页 —';
    }
    if(script) script.innerHTML = getNotes(current);
    if(count) count.textContent = 'Slide ' + (current + 1) + ' / ' + slides.length;
  }

  document.addEventListener('keydown', e => {
    if(e.key === 'ArrowRight' || e.key === ' ' || e.key === 'PageDown') { e.preventDefault(); goto(current + 1); }
    else if(e.key === 'ArrowLeft' || e.key === 'PageUp') { e.preventDefault(); goto(current - 1); }
    else if(e.key === 'Home') goto(0);
    else if(e.key === 'End') goto(slides.length - 1);
    else if(e.key === 'f' || e.key === 'F'){
      if(!document.fullscreenElement) document.documentElement.requestFullscreen();
      else document.exitFullscreen();
    }
    else if(e.key === 's' || e.key === 'S') openPresenter();
  });

  const hash = parseInt(location.hash.replace('#/', ''));
  if(hash >= 1 && hash <= slides.length) current = hash - 1;
  goto(current);
})();
</script>
</body>
</html>
```
