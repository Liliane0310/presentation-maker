# presentation-maker

一个专为「讲给人听」设计的 Claude 技能：一键生成**教学科普型、自包含 HTML 演示稿**，无需联网、不依赖外部资源，打开即用。默认采用手绘纸感 16:9 演示文稿风格，像一套精致的纸质手写讲义。

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

## 安装与使用

作为 Claude Code skill，把整个目录放到 `~/.claude/skills/presentation-maker/` 即可。Claude 会在你说「做一份 slides」「生成 PPT」等触发词时自动调用。

生成演示稿后，Claude 会自动运行字体注入脚本。如果你手动生成或修改了 HTML，需要手动运行：

```bash
python scripts/embed-font.py path/to/your-deck.html
```

依赖：Python 3.8+（仅生成阶段需要，运行阶段不需要）。

🎯 适合场景：新人培训、技术分享、产品讲解、课堂教案、内部汇报。

📄 License：MIT
