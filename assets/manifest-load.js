(function () {
    "use strict";

    window.XJ = window.XJ || {};

    window.XJ.loadManifest = function () {
        if (window.XJ._manifestPromise) {
            return window.XJ._manifestPromise;
        }
        window.XJ._manifestPromise = fetch("data/manifest.json")
            .then(function (r) {
                if (!r.ok) throw new Error("manifest fetch " + r.status);
                return r.json();
            })
            .catch(function () {
                if (window.XJ_MANIFEST) {
                    return window.XJ_MANIFEST;
                }
                throw new Error("manifest unavailable");
            });
        return window.XJ._manifestPromise;
    };

    window.XJ.applyContentMap = function (contentMap, data) {
        (data.notes || []).forEach(function (item) {
            if (item.content) contentMap[item.id] = item.content;
        });
        (data.interviews || []).forEach(function (item) {
            if (item.content) contentMap[item.id] = item.content;
        });
        (data.briefs || []).forEach(function (item) {
            if (item.content) contentMap[item.id] = item.content;
        });
        (data.tools || []).forEach(function (item) {
            if (item.content) contentMap[item.id] = item.content;
        });
        return contentMap;
    };
})();
