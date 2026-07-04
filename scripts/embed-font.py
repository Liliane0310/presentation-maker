# embed-font.py
# 把 assets/xiaolai.woff2 以 base64 形式内嵌进 HTML 的 @font-face，实现真正单文件自包含。
#
# 用法：python scripts/embed-font.py <html文件路径>
#       python scripts/embed-font.py <html文件路径> --check   (只检查是否已注入，不修改)
#
# 行为：
#   1. 读取 HTML
#   2. 检查是否已含 <!-- xiaolai-font-embedded --> 标记，已注入则跳过
#   3. 读取 assets/xiaolai.woff2，转 base64
#   4. 在 </style> 前插入 @font-face 规则
#   5. 把 --font 变量里的 "XiaoLai" 提到字体栈最前（保证优先使用小赖）
#   6. 写回原文件
#
# 体积影响：HTML 会增加约 1.85MB（1.39MB woff2 → base64 后约 +33%）。

import sys
import base64
from pathlib import Path

FONT_FACE_MARKER = "<!-- xiaolai-font-embedded -->"

# 注入到 </style> 之前的 CSS。
# 1) @font-face 定义 XiaoLai，src 指向 base64 内嵌的 woff2
# 2) 重新声明 :root 的 --font，把 XiaoLai 提到最前，回退链保持不变
#    （CSS 后定义的 :root 会覆盖前面 :root 里的同名变量，无需修改原模板）
# 注意：用 .replace 注入 base64，不用 .format，因为 CSS 里大量花括号会被 format 当占位符
FONT_FACE_CSS = """
/* {MARKER} */
@font-face {
  font-family: "XiaoLai";
  src: url(data:font/woff2;charset=utf-8;base64,{B64}) format("woff2");
  font-display: swap;
  font-weight: 400;
  font-style: normal;
}
:root {
  --font: "XiaoLai","Segoe UI",Roboto,Arial,"Helvetica Neue","Xiaolai","小赖字体","Microsoft YaHei",system-ui,-apple-system,sans-serif;
}
"""


def find_assets_font(skill_root: Path) -> Path:
    font_path = skill_root / "assets" / "xiaolai.woff2"
    if not font_path.exists():
        # 也允许放到 skill 根目录
        alt = skill_root / "xiaolai.woff2"
        if alt.exists():
            return alt
        raise FileNotFoundError(
            f"xiaolai.woff2 not found at {font_path}\n"
            f"run: python scripts/subset-font.py first to generate it."
        )
    return font_path


def embed(html_path: Path, font_path: Path) -> bool:
    html = html_path.read_text(encoding="utf-8")

    if FONT_FACE_MARKER in html:
        print(f"[skip] already embedded: {html_path}")
        return False

    if "</style>" not in html:
        print(f"[warn] no </style> found, cannot inject: {html_path}", file=sys.stderr)
        return False

    font_bytes = font_path.read_bytes()
    b64 = base64.b64encode(font_bytes).decode("ascii")
    print(f"font size: {len(font_bytes)/1024/1024:.2f} MB, base64 size: {len(b64)/1024/1024:.2f} MB")

    css_block = FONT_FACE_CSS.replace("{MARKER}", FONT_FACE_MARKER).replace("{B64}", b64)

    # 在 </style> 前注入
    new_html = html.replace("</style>", css_block + "</style>", 1)

    html_path.write_text(new_html, encoding="utf-8")
    out_size = html_path.stat().st_size
    print(f"[ok] embedded into: {html_path}  (now {out_size/1024/1024:.2f} MB)")
    return True


def check(html_path: Path) -> bool:
    html = html_path.read_text(encoding="utf-8")
    has = FONT_FACE_MARKER in html
    print(f"[check] {html_path}: {'embedded' if has else 'NOT embedded'}")
    return has


def main():
    args = sys.argv[1:]
    if not args:
        print("usage: python scripts/embed-font.py <html-path> [--check]", file=sys.stderr)
        sys.exit(2)

    html_path = Path(args[0]).resolve()
    do_check = "--check" in args

    if not html_path.exists() or not html_path.is_file():
        print(f"html not found: {html_path}", file=sys.stderr)
        sys.exit(1)

    if do_check:
        sys.exit(0 if check(html_path) else 1)

    # skill 根目录 = 脚本所在目录的上一级
    skill_root = Path(__file__).resolve().parent.parent
    font_path = find_assets_font(skill_root)

    embed(html_path, font_path)


if __name__ == "__main__":
    main()
