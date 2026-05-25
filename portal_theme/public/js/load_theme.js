/**
 * load_theme.js — Single source of truth for all theme CSS.
 * Calls get_active_theme_css() once, caches the result,
 * and re-injects on every Frappe SPA navigation.
 */

(function () {
    "use strict";

    let _cssCache = null;

    /* ── Boot ───────────────────────────────────────────────── */
    frappe.after_ajax(function () {
        fetchAndApply();
        hookRouter();
    });

    /* ── 1. Fetch (once) and apply ──────────────────────────── */
    function fetchAndApply() {
        if (_cssCache) {
            applyCSS(_cssCache);
            return;
        }
        frappe.call({
            method: "portal_theme.api.get_active_theme_css",
            callback: function (r) {
                if (!r?.message?.css) return;
                _cssCache = r.message.css;
                applyCSS(_cssCache);
            },
        });
    }

    /* ── 2. Hook SPA router ─────────────────────────────────── */
    function hookRouter() {
        $(document).on("page-change", function () {
            if (_cssCache) applyCSS(_cssCache);
        });
        if (frappe.router) {
            frappe.router.on("change", function () {
                if (_cssCache) applyCSS(_cssCache);
            });
        }
    }

    /* ── 3. Apply CSS (fonts + styles) ─────────────────────── */
    function applyCSS(css) {
        var importRegex = /@import url\(["']([^"']+)["']\);?/g;
        var match;
        while ((match = importRegex.exec(css)) !== null) {
            var url = match[1];
            var id = "gf-" + (url.split("family=")[1]?.split(":")[0]?.replace(/\+/g, "-") || "font");
            if (!document.getElementById(id)) {
                var link = document.createElement("link");
                link.id = id;
                link.rel = "stylesheet";
                link.href = url;
                document.head.appendChild(link);
            }
        }
        var clean = css.replace(/@import url\(["'][^"']+["']\);?/g, "").trim();
        var tag = document.getElementById("dynamic-ui-theme");
        if (!tag) {
            tag = document.createElement("style");
            tag.id = "dynamic-ui-theme";
            document.head.appendChild(tag);
        }
        tag.textContent = clean;
    }

})();