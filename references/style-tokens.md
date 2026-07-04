# Style Tokens

`presentation-maker` 的默认视觉系统是“手绘纸感（Paper & Hand-drawn）”16:9 演示文稿风格。它像一套精致的纸质手写讲义：温暖、克制、有手作感，但首先服务投影阅读和现场讲述。

## 设计目标

- 每页都要充分利用 16:9 画布，避免内容缩在中央小卡片里。
- 页面要有明确的标题区、主体内容区和视觉重点。
- 风格像纸质讲义，不像网页 landing page，也不像深色科技大屏。
- 纸张质感来自暖底色、极细描边、弥散大阴影和轻微线性纹理。
- 装饰只服务信息层级，不能抢过正文。

## 核心 CSS Tokens

```css
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
  --slide-x:clamp(68px,7vw,112px);
  --slide-y:clamp(42px,6vh,72px);
}
```

## 背景

```css
background:
  radial-gradient(circle at top left, rgba(202,141,107,.18), transparent 28%),
  linear-gradient(135deg,#f4ede4 0%,#efe7db 40%,#f7f2eb 100%);
```

叠加纸张纹理：

```css
body::before{
  background:
    repeating-linear-gradient(90deg, rgba(143,77,46,.028) 0 1px, transparent 1px 18px),
    repeating-linear-gradient(180deg, rgba(143,77,46,.020) 0 1px, transparent 1px 22px);
  opacity:.62;
  mix-blend-mode:multiply;
}
```

## 字体策略

英文、数字和 UI 字母不要使用小赖字体。默认字体栈：

```css
--font:"Segoe UI",Roboto,Arial,"Helvetica Neue","XiaoLai","Xiaolai","小赖字体","Microsoft YaHei",system-ui,-apple-system,sans-serif;
--mono:ui-monospace,SFMono-Regular,Menlo,Monaco,Consolas,"Liberation Mono","Courier New",monospace;
```

规则：

- 英文/数字优先使用 `Segoe UI`、`Roboto`、`Arial`、`Helvetica Neue`。
- 中文再回退到 `XiaoLai` / `Xiaolai` / `小赖字体`，以保留手绘感。
- 代码、命令、按键和页码使用 `--mono`。
- 不强制绑定外部字体文件；如果生成环境没有小赖，自动回退系统中文字体。

## 小赖字体注入机制

模板里 `--font` 把 `XiaoLai` 放在第 5 位作为回退，但用户机器几乎都没装小赖，会直接回退到微软雅黑——手绘感丢失。

为了让别人打开生成的 HTML 也能看到小赖字体，**生成 HTML 后必须运行**：

```bash
python scripts/embed-font.py <html路径>
```

脚本会：

1. 读取 `assets/xiaolai.woff2`（GB2312 6763 字子集，约 1.39MB）
2. 转 base64，注入到 `</style>` 之前的 `@font-face`
3. 重新声明 `:root --font`，把 `XiaoLai` 提到字体栈最前
4. 注入是幂等的，重复运行会自动跳过

注入后 HTML 体积约 +1.85MB，是真正单文件自包含——发给任何人双击打开都能看到小赖字体。缺字（超出 GB2312 范围）会自动回退系统字体，不会出方块。

`assets/xiaolai.woff2` 由 `scripts/subset-font.py` 从 `xiaolai.ttf` 子集化生成，正常使用无需重新生成；只有当原始字体更新或要扩大字符覆盖时才重跑。

## 类型层级

- H1：约 `3.3rem`，用于封面和强结论页。
- H2：约 `2.35rem`，使用 `--accent`，左侧带渐变小胶囊。
- 正文：约 `1.32rem` 到 `1.48rem`，投影优先，行高 `1.5` 左右。
- 表格/代码：可略小，但必须保持可投影阅读。
- 每页最多 3 个明显字体层级。

H2 胶囊装饰：

```css
h2::before{
  content:"";
  width:22px;
  height:10px;
  border-radius:999px;
  background:linear-gradient(90deg,var(--accent),#d2a384);
}
```

## 组件规则

- `blockquote`：左侧 `6px` 主强调色边框，背景 `rgba(143,77,46,.06)`，圆角 `12px`。
- `ul.emoji`：去掉默认黑点，使用 Emoji 或编号作为引导符。
- `.card`：只用于重点信息、并列概念、流程节点，不要把整页都塞进内层卡片。
- `.center-content`：内容较少时让纸张内文字垂直居中；内容多时不要使用。
- `.brand-mark`：封面署名/品牌胶囊，不用于操作说明。

## 动效规则

- 默认只使用轻量动效：翻页淡入、箭头流动、热气、简单执行动作。
- 文字不做悬浮、跳动、闪烁等干扰阅读的动效。
- 类比动效页应根据主题临时设计结构，不固定套用某个具体生活场景。
- 必须提供 `prefers-reduced-motion: reduce` 降级。

## 禁止项

- 不做成网页 Hero 页。
- 不让左右两侧出现大面积空白。
- 不让整页只有一个孤立的小卡片。
- 不在封面写“操作：← / → / Space 翻页”这类观众提示。
- 不让英文和数字使用小赖字体。
- 不使用深色主题、霓虹紫、科技蓝或大面积玻璃拟态作为默认风格。
