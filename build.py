#!/usr/bin/env python3
"""Build the static poetry site from src/poems.json into docs/ (GitHub Pages: main branch, /docs)."""
import html
import json
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).parent
SRC = ROOT / "src"
OUT = ROOT / "docs"
DOMAIN = "wangyukun.net"

data = json.loads((SRC / "poems.json").read_text(encoding="utf-8"))
SITE = data["collection"]
AUTHOR = data["author"]
POEMS = data["poems"]

esc = html.escape


def phrases(line: str) -> str:
    """Split a line after each punctuation mark so wrapping only happens between phrases."""
    parts = re.findall(r"[^，。、；？！：,.]+[，。、；？！：,.]*", line) or [line]
    return "".join(f'<span class="ph">{esc(p)}</span>' for p in parts)


def page(title: str, body: str, depth: int, desc: str) -> str:
    up = "../" * depth
    return f"""<!doctype html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta name="theme-color" content="#f6f1e7" media="(prefers-color-scheme: light)">
<meta name="theme-color" content="#1c1a17" media="(prefers-color-scheme: dark)">
<link rel="stylesheet" href="{up}style.css">
</head>
<body>
{body}
<footer class="foot"><a href="{up}">{esc(SITE)}</a> · {esc(AUTHOR)}</footer>
</body>
</html>
"""


def full_title(p: dict) -> str:
    return f"{p['form']}·{p['title']}" if p["form"] else p["title"]


def build():
    if OUT.exists():
        shutil.rmtree(OUT)
    (OUT / "poems").mkdir(parents=True)
    shutil.copy(SRC / "style.css", OUT / "style.css")
    (OUT / "CNAME").write_text(DOMAIN + "\n")
    (OUT / ".nojekyll").write_text("")

    # index
    items = []
    for i, p in enumerate(POEMS, 1):
        first = p["stanzas"][0][0]
        form = esc(p["form"] or "新诗")
        items.append(
            f'<li><a href="poems/{i}/"><span class="no">{i:02d}</span>'
            f'<span class="t">{esc(p["title"])}</span><span class="form">{form}</span>'
            f'<span class="first">{esc(first)}</span></a></li>'
        )
    body = f"""<header class="cover">
<h1>{esc(SITE)}</h1>
<p class="by">{esc(AUTHOR)} 著</p>
<p class="count">共 {len(POEMS)} 首</p>
</header>
<main><ol class="toc">{''.join(items)}</ol></main>"""
    (OUT / "index.html").write_text(
        page(f"{SITE} · {AUTHOR} 诗集", body, 0, f"{AUTHOR} 诗词集《{SITE}》"), encoding="utf-8"
    )

    # poems
    n = len(POEMS)
    for i, p in enumerate(POEMS, 1):
        modern = not p["form"]
        st = "".join(
            '<p class="stanza">' + "".join(f'<span class="ln">{phrases(l)}</span>' for l in s) + "</p>"
            for s in p["stanzas"]
        )
        prev_l = f'<a class="prev" href="../{i-1}/">‹ {esc(POEMS[i-2]["title"])}</a>' if i > 1 else "<span></span>"
        next_l = f'<a class="next" href="../{i+1}/">{esc(POEMS[i]["title"])} ›</a>' if i < n else "<span></span>"
        form = f'<p class="form-tag">{esc(p["form"])}</p>' if p["form"] else '<p class="form-tag">新诗</p>'
        body = f"""<nav class="top"><a href="../../">‹ 目录</a><span>{i} / {n}</span></nav>
<main class="poem{' modern' if modern else ''}">
<article>
<h1>{esc(p["title"])}</h1>
{form}
<div class="body">{st}</div>
<p class="sig">— {esc(AUTHOR)}</p>
</article>
</main>
<nav class="pager">{prev_l}{next_l}</nav>"""
        d = OUT / "poems" / str(i)
        d.mkdir()
        desc = " ".join(p["stanzas"][0][:2])
        (d / "index.html").write_text(
            page(f"{full_title(p)} · {SITE}", body, 2, desc), encoding="utf-8"
        )

    (OUT / "404.html").write_text(
        page(f"未找到 · {SITE}", '<main class="nf"><h1>此页不存</h1><p><a href="/">回到目录</a></p></main>', 0, SITE),
        encoding="utf-8",
    )
    print(f"built {n} poems -> {OUT}")


if __name__ == "__main__":
    build()
