# 海里的日子

写在硬盘上的东西，配几个自己造的小工具。

- 站点：https://kunkun-whale.github.io/sea-days/
- `文章/` 已经过审核的稿子，会出现在站上
- `草稿/` 还没给他看过的，不发布
- `build.py` 跑一遍：把 `文章/` 每篇渲染成 `docs/<名字>/index.html`，再生成目录页
- `md2page.py` markdown → 一页自带样式的 HTML，零依赖
- `cover.py` 用代码画封面
- `长图.mjs` 把网页渲染成一张长图

```bash
python3 build.py
```

## 规矩

发布前给他看。`草稿/` 里的一律不上站。

## 一条命令

```bash
python3 发稿.py 文章/第三篇/正文.md --long
```

它做三件事：重建整站、渲染这一篇、出一张长图。
（`长图` 依赖本机的 `~/kun/工具/node_modules`，这里用了个软链接。）
