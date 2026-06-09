"""
玄品心决 · 静态站编译器
用法: python build.py

posts/interview-*.md  → content/*.html
posts/notes/*.md      → content/*.html
data/tools.json       → content/toolbox.html
data/*.json           → data/manifest.json（首页与 reader 的数据源）
"""
from __future__ import annotations

import html
import json
import re
from pathlib import Path

import markdown

ROOT = Path(__file__).parent
POSTS = ROOT / "posts"
NOTES = POSTS / "notes"
CONTENT = ROOT / "content"
DATA = ROOT / "data"


def parse_frontmatter(text: str) -> tuple[dict[str, str], str]:
    if not text.startswith("---"):
        return {}, text
    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}, text
    meta: dict[str, str] = {}
    for line in parts[1].strip().split("\n"):
        line = line.strip()
        if ":" in line:
            key, _, value = line.partition(":")
            meta[key.strip()] = value.strip().strip("\"'")
    return meta, parts[2].strip()


def md_body_to_html(body: str, *, interview: bool) -> str:
    cta_list: list[str] = []

    def extract_cta(m: re.Match[str]) -> str:
        cta_list.append(m.group(0))
        return f"\n<!--CTA:{len(cta_list) - 1}-->\n"

    body = re.sub(r"\[cta\].*?\[/cta\]", extract_cta, body, flags=re.DOTALL)
    html_out = markdown.Markdown(extensions=["extra"]).convert(body)

    if interview:
        for role in ("问", "答"):
            html_out = re.sub(
                rf'<p><strong>{role}[：:]?\s*</strong>\s*(.*?)</p>',
                lambda m, r=role: (
                    f'<p class="speaker">{r}</p>\n<p>{m.group(1).strip()}</p>'
                    if m.group(1).strip()
                    else f'<p class="speaker">{r}</p>'
                ),
                html_out,
            )

    html_out = re.sub(
        r"<li>\[ \] (.+?)</li>",
        r'<li><label><input type="checkbox"> \1</label></li>',
        html_out,
    )
    html_out = re.sub(
        r'<a href="reader:([^"]+)">([^<]+)</a>',
        r'<button type="button" class="reader-inline-link" data-reader-open="\1">\2</button>',
        html_out,
    )

    for i, raw in enumerate(cta_list):
        html_out = html_out.replace(f"<!--CTA:{i}-->", _render_cta(raw))
    return html_out


def _render_cta(raw: str) -> str:
    cta: dict[str, str] = {}
    inner = re.sub(r"^\s*\[cta\]\s*|\s*\[/cta\]\s*$", "", raw, flags=re.DOTALL).strip()
    for line in inner.split("\n"):
        if ":" in line:
            k, _, v = line.partition(":")
            cta[k.strip()] = v.strip()
    return (
        f'<div class="cta-band">\n'
        f'  <p class="cta-band__title">{html.escape(cta.get("title", ""))}</p>\n'
        f'  <p class="cta-band__text">{html.escape(cta.get("text", ""))}</p>\n'
        f'  <button type="button" class="btn btn--primary" data-reader-open="'
        f'{html.escape(cta.get("target", "calculator"))}">'
        f'{html.escape(cta.get("button", "打开"))}</button>\n'
        f"</div>"
    )


def render_interview(meta: dict[str, str], body_html: str) -> str:
    quote = meta.get("quote", meta.get("title", ""))
    meta_line = (
        f"{meta.get('category', '')} · Temu 运营{meta.get('years', '')}"
        f" · 采访日期 {meta.get('date', '')} · 口述整理 · 发布前已过目"
    )
    return (
        f'<header class="reader-article-header">\n'
        f'  <blockquote class="article-quote">{html.escape(quote)}</blockquote>\n'
        f'  <p class="article-meta">{html.escape(meta_line)}</p>\n'
        f"</header>\n"
        f'<div class="reader-article-body">\n{body_html}\n</div>'
    )


def render_note(meta: dict[str, str], body_html: str) -> str:
    meta_line = f"{meta.get('category', '选品手记')} · {meta.get('date', '')} · 个人记录"
    return (
        f'<header class="reader-article-header">\n'
        f'  <h1 class="reader-note-title">{html.escape(meta.get("title", ""))}</h1>\n'
        f'  <p class="article-meta">{html.escape(meta_line)}</p>\n'
        f"</header>\n"
        f'<div class="reader-article-body">\n{body_html}\n</div>'
    )


def compile_md(path: Path, *, kind: str) -> dict:
    meta, body = parse_frontmatter(path.read_text(encoding="utf-8"))
    article_id = meta.get("id", path.stem)
    body_html = md_body_to_html(body, interview=(kind == "interview"))
    fragment = render_interview(meta, body_html) if kind == "interview" else render_note(meta, body_html)
    (CONTENT / f"{article_id}.html").write_text(fragment, encoding="utf-8")

    entry: dict = {
        "id": article_id,
        "status": meta.get("status", "draft"),
        "title": meta.get("title", ""),
        "date": meta.get("date", ""),
        "category": meta.get("category", ""),
        "content": f"content/{article_id}.html",
    }
    if kind == "interview":
        entry["meta"] = f"{meta.get('category', '')} · {meta.get('years', '')} · {meta.get('date', '')}"
        entry["years"] = meta.get("years", "")
        entry["role"] = meta.get("role", "个人卖家")
    else:
        entry["meta"] = f"{meta.get('category', '选品手记')} · {meta.get('date', '')}"
        entry["tags"] = [t.strip() for t in meta.get("tags", "").strip("[]").split(",") if t.strip()]

    for key in ("contrast_q", "contrast_label", "contrast_answer"):
        if meta.get(key):
            entry[key] = meta[key]
    return entry


def load_json(name: str, default: dict | list) -> dict | list:
    path = DATA / name
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding="utf-8"))


def merge_seeds(compiled: list[dict], seeds: list[dict]) -> list[dict]:
    by_id = {item["id"]: item for item in compiled}
    for seed in seeds:
        if seed["id"] not in by_id:
            by_id[seed["id"]] = seed
    return sorted(by_id.values(), key=lambda x: x.get("date", x.get("meta", "")), reverse=True)


def build_contrasts(entries: list[dict]) -> list[dict]:
    cfg = load_json("contrast.json", {"questions": {}, "pending": []})
    questions: dict[str, str] = cfg.get("questions", {})
    groups: dict[str, list[dict]] = {}

    for item in entries:
        q = item.get("contrast_q")
        if not q or not item.get("contrast_answer"):
            continue
        groups.setdefault(q, []).append({
            "label": item.get("contrast_label", item.get("title", "")),
            "text": item["contrast_answer"],
            "source": item["id"],
            "status": item.get("status", "draft"),
        })

    for voice in cfg.get("pending", []):
        q = voice.get("q")
        if not q:
            continue
        source = voice.get("source", "")
        existing = groups.get(q, [])
        if source and any(v.get("source") == source for v in existing):
            continue
        groups.setdefault(q, []).append({
            "label": voice.get("label", ""),
            "text": voice.get("text") or voice.get("answer", ""),
            "source": source,
            "status": voice.get("status", "draft"),
        })

    result = []
    for qid, voices in groups.items():
        seen: set[str] = set()
        unique: list[dict] = []
        for v in voices:
            key = v.get("source") or v.get("label", "")
            if key in seen:
                continue
            seen.add(key)
            unique.append(v)
        result.append({
            "id": qid,
            "question": questions.get(qid, qid),
            "voices": unique,
        })
    return result


def render_toolbox(tools_cfg: dict) -> None:
    links_html = []
    for link in tools_cfg.get("links", []):
        name = html.escape(link.get("name", ""))
        url = html.escape(link.get("url", "#"))
        note = html.escape(link.get("note", ""))
        badge = " *" if link.get("affiliate") else ""
        tested = "亲测" if link.get("tested") else "待验证"
        links_html.append(
            f'<li class="tool-list__item">\n'
            f'  <a href="{url}" target="_blank" rel="noopener noreferrer">{name}{badge}</a>\n'
            f'  <span class="tool-list__meta">{tested} · {html.escape(link.get("category", ""))}</span>\n'
            f'  <p class="tool-list__note">{note}</p>\n'
            f"</li>"
        )

    waitlist = tools_cfg.get("waitlist") or ""
    waitlist_block = (
        f'<p class="tool-waitlist"><a href="{html.escape(waitlist)}" target="_blank" rel="noopener">'
        f"留下邮箱，选品助手内测优先通知</a></p>"
        if waitlist
        else '<p class="tool-waitlist">选品助手内测筹备中。粗算器下方可留反馈。</p>'
    )

    fragment = (
        '<header class="reader-article-header">\n'
        '  <h1 class="section__title" style="font-size:1.5rem;margin-bottom:0.5rem;">选品工具箱</h1>\n'
        '  <p class="article-meta">推荐链接 + 毛利粗算 · 带 * 为联盟链接（当前未启用）</p>\n'
        "</header>\n"
        '<div class="reader-article-body">\n'
        '  <h2 class="reader-section-label">推荐工具</h2>\n'
        f'  <ul class="tool-list">{"".join(links_html)}</ul>\n'
        '  <h2 class="reader-section-label">毛利粗算</h2>\n'
        '  <p class="section__desc">在站内粗算毛利率，判断值不值得往下挖。</p>\n'
        '  <button type="button" class="btn btn--primary" data-reader-open="calculator">打开毛利粗算</button>\n'
        f"  {waitlist_block}\n"
        "</div>"
    )
    (CONTENT / "toolbox.html").write_text(fragment, encoding="utf-8")


def write_manifest(
    interviews: list[dict],
    notes: list[dict],
    contrasts: list[dict],
    tools_cfg: dict,
) -> None:
    site = load_json("site.json", {})
    subscribe = load_json("subscribe.json", {"enabled": False, "hint": "简报邮件筹备中，可先关注抖音口播。"})

    manifest = {
        "site": site,
        "notes": sorted(notes, key=lambda x: x.get("date", ""), reverse=True),
        "interviews": interviews,
        "contrasts": contrasts,
        "briefs": [
            {
                "id": "brief-01",
                "type": "evening",
                "title": "晚报样例：轻克重品运费模板变动",
                "meta": "2026-06-05 · 免费样例",
                "content": "content/brief-01.html",
            },
            {
                "id": "brief-02",
                "type": "evening",
                "title": "晚报样例：$4.9 售价带的百货压力",
                "meta": "2026-06-04 · 免费样例",
                "content": "content/brief-02.html",
            },
        ],
        "tools": [
            {"id": "toolbox", "title": "选品工具箱", "content": "content/toolbox.html"},
            {"id": "calculator", "title": "毛利粗算", "content": "content/calculator.html"},
        ],
        "subscribe": subscribe,
    }
    (DATA / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    (DATA / "manifest.js").write_text(
        "// 自动生成 · build.py · file:// 预览兜底\n"
        "window.XJ_MANIFEST = "
        + json.dumps(manifest, ensure_ascii=False, indent=2)
        + ";\n",
        encoding="utf-8",
    )


def main() -> None:
    print("玄品心决 · 编译器\n")
    CONTENT.mkdir(exist_ok=True)
    NOTES.mkdir(exist_ok=True)

    interviews: list[dict] = []
    for path in sorted(POSTS.glob("interview-*.md")):
        print(f"采访: {path.name}")
        interviews.append(compile_md(path, kind="interview"))
        print(f"  → {path.stem}.html")

    notes: list[dict] = []
    for path in sorted(NOTES.glob("*.md")):
        if path.name.startswith("."):
            print(f"跳过: notes/{path.name}")
            continue
        print(f"手记: {path.name}")
        notes.append(compile_md(path, kind="note"))
        print(f"  → content/{notes[-1]['id']}.html")

    seeds = load_json("seeds.json", {"interviews": []})
    interviews = merge_seeds(interviews, seeds.get("interviews", []))

    contrasts = build_contrasts(interviews + notes)
    tools_cfg = load_json("tools.json", {"links": [], "waitlist": ""})
    render_toolbox(tools_cfg)
    print("工具箱: content/toolbox.html")

    write_manifest(interviews, notes, contrasts, tools_cfg)
    print(f"\nmanifest.json + manifest.js 已更新（手记 {len(notes)} · 采访 {len(interviews)} · 同题 {len(contrasts)}）\n完成！")


if __name__ == "__main__":
    main()
