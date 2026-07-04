# presentation-maker

一个专为「讲给人听」设计的 Claude 技能：一键生成**教学科普型、自包含 HTML 演示稿**，无需联网、不依赖外部资源，打开即用。默认采用手绘纸感 16:9 演示文稿风格，像一套精致的纸质手写讲义。

## 快速安装

```bash
npx skills add https://github.com/Liliane0310/presentation-maker -g -y
```

装完在 Claude Code 里说「做一份关于 X 的 slides」即可触发。

## 特性

✨ 特性亮点：
- 📄 单个 `.html` 文件（双击就能看，支持手机/电脑）
- 🎤 内置演讲者模式（按 `S` 键开启，含计时器+逐字稿+下一页预览）
- ⌨️ 全键盘操作：`←→` 翻页、`Home/End` 跳首尾、`F` 全屏
- 🌟 温暖纸感设计：16:9 大版心 + 暖色系 + 微纹理背景，专注内容不刺眼
- 🔤 中英文字体分工：英文/数字优先西文字体，中文保留小赖字体回退
- 🖌️ **小赖字体自动内嵌**：生成的 HTML 自带 GB2312 子集小赖字体（base64），别人打开也能看到手写感
- 🧩 内置类比页模板：支持菜谱动效等生活化解释方式
- 🗣️ Notes 专为「讲出来」优化（不是写论文，是写说话节奏）

📁 本包已包含：
- `SKILL.md`：完整行为规范与工作流
- `references/`：视觉系统、页面结构规则、讲稿写法指南、HTML 骨架模板
- `scripts/`：字体子集化脚本 + 字体注入脚本
- `assets/xiaolai.woff2`：子集化后的小赖字体（GB2312 6763 字，约 1.39MB）
- `examples/`：可直接打开参考的成品样例（已注入字体）

## 字体说明（重要）

为了让别人打开你生成的 HTML 也能看到小赖字体，skill 采用「base64 内嵌 woff2」方案：

- `assets/xiaolai.woff2` 是从 `xiaolai.ttf` 子集化而来，只保留 GB2312 一级+二级 6763 字 + 常用标点 + ASCII，体积 1.39MB（原始 ttf 21MB）
- 生成 HTML 后，必须运行 `python scripts/embed-font.py <html路径>` 把字体以 base64 内嵌进 `@font-face`
- 注入后 HTML 体积约 +1.85MB，是真正单文件自包含
- 缺字（超出 GB2312 范围的生僻字）会自动回退系统字体，不会出方块

重新生成 woff2（仅当原始字体更新时）：

```bash
pip install fonttools brotli
python scripts/subset-font.py   # 默认读 D:/讯飞实习/xiaolai.ttf，输出到 assets/xiaolai.woff2
```

## 安装

### 方式一：一键安装（推荐）

```bash
npx skills add https://github.com/Liliane0310/presentation-maker -g -y
```

- `-g` 全局安装（用户级，所有项目可用，装到 `~/.claude/skills/`）
- `-y` 跳过确认
- 不加 `-g` 则装到当前项目级（`.claude/skills/`）

装完后，在 Claude Code 里说「做一份 slides」「生成 PPT」「演示一下 X」等触发词就会自动调用。

更新到最新版：

```bash
npx skills update presentation-maker -g
```

卸载：

```bash
npx skills remove presentation-maker -g
```

### 方式二：手动 git clone

如果 `npx skills` 不可用或网络受限：

```bash
git clone https://github.com/Liliane0310/presentation-maker.git ~/.claude/skills/presentation-maker
```

## 使用

在 Claude Code 中直接说需求即可，例如：

- 「做一份关于 MCP 的 15 页 slides，听众是产品经理」
- 「生成一个 PPT 讲 RAG，要带案例」
- 「做份演示稿讲提示词工程」

Claude 会先出大纲和你确认，确认后生成完整 HTML，并自动运行字体注入脚本把小赖字体以 base64 内嵌进 HTML。

如果你手动修改了生成的 HTML（比如改了内容），需要重新跑一次注入：

```bash
python scripts/embed-font.py path/to/your-deck.html
```

注入是幂等的，重复运行会自动跳过。

依赖：Python 3.8+（仅生成阶段需要，看 HTML 不需要）。

🎯 适合场景：新人培训、技术分享、产品讲解、课堂教案、内部汇报。

📄 License：MIT
