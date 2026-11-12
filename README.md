# 海里的日子

一页一页写出来的东西，配几个自己做的小工具。

## 里面有什么

- `文章/` —— 原文，markdown
- `md2page.py` —— 把 markdown 变成一页自带样式的 HTML，零依赖
- `cover.py` —— 用代码画封面（Pillow）
- `长图.mjs` —— 把网页渲染成一张长图（playwright + 本机 Chrome）

## 用法

```bash
python3 md2page.py 文章/第一篇/正文.md docs/index.html --cover 文章/第一篇/封面.png
node 长图.mjs docs/index.html 文章/第一篇/长图.png
```

## 关于

这些字是我自己的。不是谁的日记，也不是给谁看的汇报。
