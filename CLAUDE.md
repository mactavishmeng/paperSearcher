# CLAUDE.md

本文件为 Claude Code (claude.ai/code) 在此仓库中工作时提供指导。

## 概述

这是一个基于 Flask 的 Web 应用，用于搜索网络安全和计算机网络领域的学术论文。它作为一个本地搜索界面，连接包含顶级会议和期刊（CCS、S&P、USENIX Security、NDSS 等）论文的 SQLite 数据库。

## 运行应用

```bash
# 首次设置：解压数据库
unzip paper.db.zip

# 安装依赖
pip3 install -r requirements.txt

# 运行服务器（默认为 127.0.0.1:5000）
python3 website.py

# 使用自定义 host/port 运行
python3 website.py 0.0.0.0 8080
```

## 架构

应用结构简单：

- **[website.py](website.py)**: Flask 后端，包含两个主要 endpoints：
  - `/search` - 关键词搜索，支持分页，可按来源（会议）和年份筛选
  - `/abstract/<q>` - 根据 ID 获取特定论文的摘要

- **[static/](static/)**: 前端资源（HTML、CSS、JS），通过 Flask 的 `send_static_file()` 提供服务

- **Database**: SQLite 数据库（`paper.db`），包含单个 `PAPER` 表，字段如下：
  - `id`, `conf` (会议), `year`, `cat` (类别), `title`, `href`, `abstract`, `bib`

## 搜索查询语法

搜索支持通过特殊分隔符实现布尔逻辑：
- `+` 表示 AND（两个关键词都必须匹配）
- `|` 表示 OR（任一关键词匹配即可）

示例：
- `blockchain+security` → 在 title/abstract 中同时包含 "blockchain" AND "security" 的论文
- `security|iot` → 包含 "security" OR "iot" 中任一关键词的论文

搜索使用 `LIKE` 查询同时匹配 `TITLE` 和 `ABSTRACT` 列。

## 安全提示

README 明确警告存在 SQL 注入漏洞。[website.py:10-21](website.py#L10-L21) 中的 `sqlinjection()` 函数尝试进行基本的转义，但应用应仅在本地（`127.0.0.1`）运行，不要暴露到公网。
