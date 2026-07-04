# subset-font.py
# 把 xiaolai.ttf 子集化为 GB2312 常用字 + 标点 + ASCII，并转 woff2。
# 用法：python scripts/subset-font.py [输入ttf路径] [输出woff2路径]
# 默认输入：D:/讯飞实习/xiaolai.ttf（可改成你自己的路径）
# 默认输出：assets/xiaolai.woff2

import sys
import os
from pathlib import Path

try:
    from fontTools import subset
except ImportError:
    print("fonttools missing. run: pip install fonttools brotli", file=sys.stderr)
    sys.exit(1)

# GB2312 常用字（3755 字）+ 全角标点 + ASCII + 常用中文标点
# 这里用 Unicode 范围 + GB2312 字表的方式，确保覆盖演示稿常用字符
def build_charset():
    """返回 GB2312 一级+二级常用字 + ASCII + 常用标点的码点集合。
    优先读同目录的 gb2312-codes.txt（预生成），失败则现场计算。
    GB2312 共 6763 字，覆盖中文演示稿 99%+ 场景；缺字时 CSS 字体栈自动回退系统字体。
    """
    codes_file = Path(__file__).resolve().parent / "gb2312-codes.txt"
    if codes_file.exists():
        text = codes_file.read_text(encoding="utf-8").strip()
        return set(int(x) for x in text.split(",") if x)

    # 兜底：现场计算
    cps = set()
    for cp in range(0x20, 0x7F):
        cps.add(cp)
    puncts = "，。、；：？！（）【】《》—…·「」『』〈〉．／｜～－＝＋×÷＜＞≤≥\"\""
    for ch in puncts:
        cps.add(ord(ch))
    for qu in range(16, 88):
        for wei in range(1, 95):
            try:
                code = bytes([0xA0 + qu, 0xA0 + wei])
                ch = code.decode("gb2312")
                cps.add(ord(ch))
            except (UnicodeDecodeError, ValueError):
                pass
    return cps

def main():
    here = Path(__file__).resolve().parent.parent
    in_path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(r"D:/讯飞实习/xiaolai.ttf")
    out_path = Path(sys.argv[2]) if len(sys.argv) > 2 else here / "assets" / "xiaolai.woff2"

    if not in_path.exists():
        print(f"input font not found: {in_path}", file=sys.stderr)
        print("put xiaolai.ttf at the path above, or pass it as argv[1].", file=sys.stderr)
        sys.exit(1)

    out_path.parent.mkdir(parents=True, exist_ok=True)

    chars = build_charset()
    print(f"subsetting charset size: {len(chars)}")

    # 用 subset.Options 控制子集化行为
    opt = subset.Options()
    opt.layout_features = ["*"]
    opt.name_IDs = ["*"]
    opt.glyph_names = True
    opt.notdef_outline = True
    opt.recalc_bounds = True
    opt.drop_tables = ["DSIG", "MVAR", "cvar", "STAT"]

    font = subset.load_font(str(in_path), opt)
    subsetter = subset.Subsetter(options=opt)
    subsetter.populate(unicodes=chars)
    subsetter.subset(font)

    # woff2 需要 brotli
    try:
        import brotli  # noqa: F401
    except ImportError:
        print("brotli missing, woff2 unavailable. run: pip install brotli", file=sys.stderr)
        sys.exit(1)

    font.flavor = "woff2"
    font.save(str(out_path))

    in_size = in_path.stat().st_size
    out_size = out_path.stat().st_size
    print(f"input  ttf : {in_size/1024/1024:.2f} MB  <-  {in_path}")
    print(f"output woff2: {out_size/1024/1024:.2f} MB  ->  {out_path}")
    print(f"ratio: {out_size/in_size*100:.1f}%")

if __name__ == "__main__":
    main()
