# 玄品心决 — Visual Design

Design Read: Editorial / 采访笔记，Temu 老板+新人，手稿语言；原生 CSS；MOTION 4；DENSITY 3。

## Tokens

| Token | Value | 用途 |
|-------|-------|------|
| `--bg` | `#fffff8` | 象牙白主底 |
| `--surface` | `#ffffff` | 卡片/浮层面 |
| `--ink` | `#454545` | 正文 |
| `--accent` | `#9aab8f` | 相邻色点睛（进度、列表点） |
| `--accent-warm` | `#c4a882` | 淡香槟点睛（按钮描边、链接） |

## Bans

无 side-stripe · 无 hero metrics · 无 identical card grid · 无 dashboard footer 链接

## Reader（统一浮层）

采访 / 简报 / 计算器共用 `assets/reader.js` + `#read/{id}` 分享链接。

- 遮罩：blur + 半透明；面板：实底 `#ffffff`
- 左侧「← 返回」；面板内独立滚动 + 细金滚动条
- 关闭恢复首页 scrollY；同篇再开恢复浮层内滚动
- 点遮罩：400ms 后生效，需连点两次关闭（防误触）

## CTA 原则

动词+对象；站内闭环：读采访 → 毛利粗算 → 回采访/简报（均在浮层内）


## 品牌陈述决策 2026-06-09

**方案 A 修订版（已实施）**

| 层级 | 文案 | 作用 |
|------|------|------|
| hero-eyebrow | 玄品心决 | 品牌 |
| hero-title | Temu 选品笔记 | SEO + 当前主战场 |
| hero-tagline | 记录选品路上那杆秤 | 人（不限平台） |
| hero-extend | 算克重 · 懂毛利 · 不踩坑 · 当前从 Temu 写起 | 能力 + 诚实边界 |
| hero-author | by 玉成 · 在职 Temu 选品 | 可信度 |
| hero-quote | 「克重看着轻，毛利一算就穿底。」 | 情境锚点 |

**设计理由**

品牌层（玄品心决）不绑定单一平台；内容层现阶段从 Temu 长出来，extend 末尾诚实标注边界。h1 保留「Temu 选品笔记」以维持 SEO 长尾。meta description 与 tagline 一致，由 `data/site.json` + `home.js` 同步。

**CSS**

`.hero-tagline` 无 white-space 限制；`.hero-split` 在 &lt;768px 单列，长 tagline 自然换行。`.article-tag` 用于采访列表「新手推荐」等 frontmatter 标签。
