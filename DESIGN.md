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

**方案A（已实施）**
- hero-eyebrow: "玄品心决"（品牌先行）
- hero-title: "Temu 选品笔记"（品类定位）
- hero-tagline: "写给Temu卖家的选品判断力"（价值主张替代原氛围描述"记录选品路上那杆秤"）
- hero-extend: "算克重·懂毛利·不踩坑"（精简，去"当前从Temu写起"）

**设计理由**
将hero信息层级从"抒情→描述"改为"声明→定位→价值→可信度"。eyebrow明确品牌名，tagline直接说明受众和提供什么价值，extend用密集点(·)代替间隔点以匹配Tokyo-style紧凑感。hero-quote保留原引文作为信用锚点（用户亲述），位于价值声明之后。

**CSS改动**
新tagline"写给Temu卖家的选品判断力"比原tagline长一倍，需在窄屏自动换行。以下CSS已确认不需改动：`.hero-tagline`无white-space限制，`.hero-split`在<768px时自动转为1列，文本正常折行。若后续添加强制不换行（white-space: nowrap），需同时设置`overflow-wrap: break-word`。
