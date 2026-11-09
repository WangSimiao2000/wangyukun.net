# 风舞流年 · YK 诗集

网站地址：https://wangyukun.net

- `src/poems.json`：全部诗词（加新诗就往 `poems` 里追加一条）
- `src/style.css`：样式
- `build.py`：只用 Python 标准库，运行 `python3 build.py` 生成 `docs/`
- GitHub Pages 发布来源：`main` 分支的 `/docs` 目录（不依赖 Actions 工作流）

新增一首诗的格式：

```json
{ "form": "七律", "title": "诗题", "stanzas": [["第一句，", "第二句。"], ["下一段……"]] }
```

`form` 留空字符串表示新诗。改完运行 `python3 build.py`，提交并推送即可。
