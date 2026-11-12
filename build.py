#!/usr/bin/env python3
"""把 文章/ 下的每一篇都渲染成 docs/ 里的页面，再生成一个目录页。

用法：python3 build.py
"""
import html
import io
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(ROOT, "文章")
DOCS = os.path.join(ROOT, "docs")

LIST_TPL = """<!doctype html>
<html lang="zh-CN">
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title>
<style>
  :root {{ color-scheme: dark; }}
  html, body {{ margin:0; background:#0d1b2a; }}
  body {{ color:#dbe7f3; font:17px/1.9 -apple-system,"PingFang SC","Songti SC",serif; }}
  main {{ max-width:34rem; margin:0 auto; padding:5rem 1.5rem 6rem; }}
  h1 {{ font-size:1.6rem; letter-spacing:.1em; margin:0 0 3rem; }}
  article {{ margin:0 0 2.6rem; }}
  a {{ color:#9fc4e0; text-decoration:none; }}
  a:hover {{ color:#e6f0f8; }}
  .d {{ display:block; color:#5f849f; font-size:.85rem; letter-spacing:.12em; margin-top:.4rem; }}
</style>
<main>
<h1>{title}</h1>
{items}
</main>
</html>
"""


def slug_dir(path: str) -> str:
    return os.path.basename(path.rstrip("/"))


def main() -> int:
    os.makedirs(DOCS, exist_ok=True)
    items = []
    for name in sorted(os.listdir(SRC)):
        d = os.path.join(SRC, name)
        md = os.path.join(d, "正文.md")
        if not os.path.isfile(md):
            continue
        out_dir = os.path.join(DOCS, name)
        os.makedirs(out_dir, exist_ok=True)
        cover = os.path.join(d, "封面.png")
        cover_arg = ["--cover", "../文章/" + name + "/封面.png"] if os.path.isfile(cover) else []
        out = os.path.join(out_dir, "index.html")
        # 页面里的封面用相对仓库根的路径
        subprocess.run([sys.executable, os.path.join(ROOT, "md2page.py"), md, out] +
                       (["--cover", "../../文章/" + name + "/封面.png"] if os.path.isfile(cover) else []),
                       check=True, cwd=ROOT)
        # 站点根备份一份封面（Pages 只发布 docs/）
        if os.path.isfile(cover):
            subprocess.run(["cp", cover, os.path.join(DOCS, name + ".png")], check=False)
        text = io.open(md, encoding="utf-8").read()
        title = ""
        for line in text.splitlines():
            if line.startswith("# "):
                title = line[2:].strip()
                break
        items.append(
            f'<article><a href="{name}/">{html.escape(title or name)}</a>'
            f'<span class="d">{len(text)} 字</span></article>'
        )
        print("✓", name, title)

    io.open(os.path.join(DOCS, "index.html"), "w", encoding="utf-8").write(
        LIST_TPL.format(title="海里的日子", items="\n".join(items))
    )
    print(f"目录页已写，共 {len(items)} 篇")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
