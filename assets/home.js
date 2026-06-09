(function () {
    "use strict";

    function esc(s) {
        var d = document.createElement("div");
        d.textContent = s || "";
        return d.innerHTML;
    }

    function showFileBanner() {
        if (location.protocol !== "file:") return;
        var bar = document.getElementById("file-protocol-hint");
        if (!bar) {
            bar = document.createElement("div");
            bar.id = "file-protocol-hint";
            bar.className = "file-protocol-hint";
            bar.setAttribute("role", "status");
            document.body.insertBefore(bar, document.body.firstChild);
        }
        bar.innerHTML =
            "当前为本地文件打开，阅读全文请双击 <strong>本地预览-仅开发用.bat</strong>，" +
            "用 <code>http://localhost:8765/</code> 访问。";
    }

    function articleRow(item) {
        var published = item.status === "published" && item.content;
        var titleInner = published
            ? '<button type="button" class="reader-inline-link reader-inline-link--title" data-reader-open="' + esc(item.id) + '">' + esc(item.title) + "</button>"
            : esc(item.title);
        var action = published
            ? '<button type="button" class="article-list__link reader-inline-link" data-reader-open="' + esc(item.id) + '">阅读</button>'
            : '<span class="article-list__link article-list__link--soon">整理中</span>';
        return (
            '<li class="article-list__item" data-reader-row="' + esc(item.id) + '">' +
            "<div><h3 class=\"article-list__title\">" + titleInner + "</h3>" +
            '<p class="article-list__meta">' + esc(item.meta || "") + "</p></div>" +
            action +
            "</li>"
        );
    }

    function renderList(el, items) {
        if (!el) return;
        if (!items.length) {
            el.innerHTML = '<li class="article-list__item article-list__item--empty"><p class="article-list__meta">筹备中，第一篇发布后会出现在这里。</p></li>';
            return;
        }
        el.innerHTML = items.map(articleRow).join("");
    }

    function renderContrasts(el, contrasts) {
        if (!el || !contrasts.length) return;
        var block = contrasts[0];
        var voices = (block.voices || []).map(function (v) {
            var text = v.text || v.answer || "";
            var link = v.source && v.status === "published"
                ? ' <button type="button" class="reader-inline-link" data-reader-open="' + esc(v.source) + '">来源</button>'
                : "";
            return "<li><strong>" + esc(v.label) + "</strong> " + esc(text) + link + "</li>";
        }).join("");
        var cta = block.voices.some(function (v) { return v.source === "interview-01"; })
            ? '<p style="margin-top:1.75rem;"><button type="button" class="btn" data-reader-open="interview-01" data-reader-hash="rules">看采访中的完整判断规则</button></p>'
            : "";
        el.innerHTML =
            '<p class="contrast-block__question">' + esc(block.question) + "</p>" +
            '<ul class="contrast-voices">' + voices + "</ul>" + cta;
    }

    function renderBriefs(el, briefs) {
        if (!el) return;
        el.innerHTML = (briefs || []).map(function (b) {
            return (
                '<li class="brief-list__item" data-reader-row="' + esc(b.id) + '">' +
                '<button type="button" class="reader-inline-link" data-reader-open="' + esc(b.id) + '">' + esc(b.title) + "</button>" +
                '<span class="brief-list__meta">' + esc((b.meta || "").split(" · ")[0]) + "</span></li>"
            );
        }).join("");
    }

    function renderSubscribe(el, sub) {
        if (!el || !sub) return;
        el.innerHTML =
            '<p class="subscribe-box__hint">' + esc(sub.hint) + "</p>" +
            (sub.enabled && sub.action
                ? '<form class="subscribe-box__form" action="' + esc(sub.action) + '" method="post" target="_blank">' +
                  '<label class="subscribe-box__label" for="subscribe-email">简报邮件</label>' +
                  '<input id="subscribe-email" class="subscribe-box__input" type="email" name="email" placeholder="你的邮箱" required>' +
                  '<button type="submit" class="btn btn--primary">订阅</button></form>'
                : "");
    }

    function applySiteMeta(site) {
        if (!site) return;
        document.querySelectorAll("[data-site-name]").forEach(function (n) {
            n.textContent = site.name || "";
        });
        document.querySelectorAll("[data-site-tagline]").forEach(function (n) {
            n.textContent = site.tagline || "";
        });
        if (site.description) {
            var desc = document.querySelector('meta[name="description"]');
            if (desc) desc.setAttribute("content", site.description);
        }
    }

    function renderHome(data) {
        applySiteMeta(data.site);
        renderList(document.getElementById("notes-list"), data.notes || []);
        renderList(document.getElementById("interview-list"), data.interviews || []);
        renderContrasts(document.getElementById("contrast-root"), data.contrasts || []);
        renderBriefs(document.getElementById("brief-list"), data.briefs || []);
        renderSubscribe(document.getElementById("subscribe-box"), data.subscribe);
        showFileBanner();

        var last = sessionStorage.getItem("xj-last-reader-id");
        if (last) {
            var row = document.querySelector('[data-reader-row="' + last + '"]');
            if (row) row.classList.add("is-last-read");
        }
    }

    var loader = window.XJ && window.XJ.loadManifest ? window.XJ.loadManifest() : fetch("data/manifest.json").then(function (r) { return r.json(); });

    loader
        .then(function (data) {
            renderHome(data);
        })
        .catch(function () {
            var hint = document.getElementById("notes-list");
            if (hint) {
                hint.innerHTML = '<li class="article-list__item article-list__item--empty"><p class="article-list__meta">无法加载内容清单。请运行 build.py 后使用本地预览 bat 打开。</p></li>';
            }
        });
})();
