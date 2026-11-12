#!/usr/bin/env python3
"""一条命令发一篇：md → 页面 + 封面图位置 + 长图，再更新目录页。

用法：
  python3 发稿.py 文章/第三篇/正文.md              # 只出页面，更新目录
  python3 发稿.py 文章/第三篇/正文.md --long       # 同时出一张长图
"""
import io
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
LONG = os.path.join(ROOT, "长图.mjs")


def main() -> int:
    argv = sys.argv[1:]
    args = [a for a in argv if not a.startswith("--")]
    if not args:
        print(__doc__)
        return 2
    md = os.path.abspath(args[0])
    if not os.path.isfile(md):
        print("找不到", md)
        return 2

    art_dir = os.path.dirname(md)
    name = os.path.basename(art_dir)
    cover = os.path.join(art_dir, "封面.png")

    # 1) 页面
    title, _ = None, None
    for line in io.open(md, encoding="utf-8"):
        if line.startswith("# "):
            title = line[2:].strip()
            break
    subprocess.run([sys.executable, os.path.join(ROOT, "build.py")], check=True, cwd=ROOT)

    # 2) 长图
    if "--long" in argv:
        page = os.path.join(ROOT, "docs", name, "index.html")
        out = os.path.join(art_dir, "长图.png")
        if os.path.isfile(LONG):
            subprocess.run(["node", LONG, page, out, "900"], check=True, cwd=ROOT)
        else:
            print("没有 长图.mjs，跳过长图")

    print(f"\n✓ {title or name}")
    print(f"  页面：docs/{name}/index.html")
    if os.path.isfile(cover):
        print(f"  封面：{cover}")
    if "--long" in argv:
        print(f"  长图：{os.path.join(art_dir, '长图.png')}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
