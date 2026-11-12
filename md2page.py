#!/usr/bin/env python3
"""把一个 markdown 文件转成一页自带样式的 HTML（零依赖）。

用法：
  python3 md2page.py 输入.md 输出.html [--title 标题] [--cover 图片]
"""
import html
import io
import re
import sys

TEMPLATE = """<!doctype html>
<html lang="zh-CN">
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title>
<style>
  :root {{ color-scheme: dark; }}
  html, body {{ margin:0; background:#0d1b2a; }}
  body {{ color:#dbe7f3; font:17px/1.95 -apple-system, "PingFang SC", "Songti SC", serif; }}
  main {{ max-width:34rem; margin:0 auto; padding:4.5rem 1.5rem 6rem; }}
  h1 {{ font-size:2rem; letter-spacing:.06em; margin:0 0 2.4rem; font-weight:600; }}
  h2 {{ font-size:1.02rem; letter-spacing:.15em; color:#7fb2d9; margin:3.2rem 0 1rem; font-weight:600;
        scroll-margin-top:2rem; }}
  p {{ margin:0 0 1.2rem; }}
  hr {{ border:0; border-top:1px solid #24384c; margin:2.5rem 0; }}
  em {{ color:#9fc4e0; font-style:normal; }}
  blockquote {{ margin:1.5rem 0; padding-left:1rem; border-left:2px solid #2b5876; color:#a8bfd4; }}
  figure {{ margin:0 0 2.6rem; }}
  figure img {{ width:100%; border-radius:6px; display:block; }}
  nav {{ margin:0 0 3rem; }}
  nav ol {{ margin:0; padding-left:1.2rem; color:#6f96b5; font-size:.92rem; line-height:2.1; }}
  nav a {{ color:#8ab3d1; text-decoration:none; border-bottom:1px solid #24445e; }}
  nav a:hover {{ color:#cfe4f4; }}
  ::selection {{ background:#2b5876; }}
</style>
<main>
{cover}{toc}{body}
</main>
</html>
"""


def inline(text: str) -> str:
    out = html.escape(text)
    out = re.sub(r"\*(.+?)\*", r"<em>\1</em>", out)
    out = re.sub(r"`(.+?)`", r"<code>\1</code>", out)
    return out


def convert(md: str):
    title = ""
    blocks: list[tuple[str, str]] = []   # (类型, 内容)
    for raw in md.split("\n\n"):
        block = raw.strip()
        if not block:
            continue
        if block.startswith("## "):
            blocks.append(("h2", inline(block[3:])))
        elif block.startswith("# "):
            heading = block[2:].strip()
            if not title:
                title = heading
            blocks.append(("h1", inline(heading)))
        elif block.startswith("> "):
            body = "<br>".join(inline(l[2:]) for l in block.splitlines())
            blocks.append(("quote", body))
        elif set(block) <= {"-", " ", "\n"} and block.count("-") >= 3:
            blocks.append(("hr", ""))
        else:
            blocks.append(("p", "<br>".join(inline(l) for l in block.splitlines())))
    return title or "无题", blocks


def render(blocks) -> tuple[str, str]:
    body, items = [], []
    for i, (kind, content) in enumerate(blocks):
        if kind == "h1":
            body.append(f"<h1>{content}</h1>")
        elif kind == "h2":
            body.append(f'<h2 id="s{i}">{content}</h2>')
            items.append(f'<li><a href="#s{i}">{re.sub(r"<[^>]+>", "", content)}</a></li>')
        elif kind == "quote":
            body.append(f"<blockquote>{content}</blockquote>")
        elif kind == "hr":
            body.append("<hr>")
        else:
            body.append(f"<p>{content}</p>")
    nav = "<nav><ol>" + "".join(items) + "</ol></nav>" if len(items) >= 2 else ""
    return "\n".join(body), nav


def main() -> int:
    argv = sys.argv[1:]
    args = [a for a in argv if not a.startswith("--")]
    if len(args) < 2:
        print(__doc__)
        return 2
    src, dst = args[0], args[1]
    md = io.open(src, encoding="utf-8").read()
    title, blocks = convert(md)
    body, nav = render(blocks)

    if "--title" in argv:
        title = argv[argv.index("--title") + 1]
    cover = ""
    if "--cover" in argv:
        rel = argv[argv.index("--cover") + 1]
        cover = f'<figure><img src="{html.escape(rel)}" alt=""></figure>\n'

    io.open(dst, "w", encoding="utf-8").write(
        TEMPLATE.format(title=html.escape(title), cover=cover, toc=nav, body=body)
    )
    print(f"{src} → {dst}  小节 {body.count('<h2')} 个，目录 {'有' if nav else '无'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
