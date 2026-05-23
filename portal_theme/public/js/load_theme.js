/**
 * load_theme.js — Single source of truth for all theme CSS.
 * Calls get_active_theme_css() once, caches the result,
 * and re-injects on every Frappe SPA navigation.
 * Manually marks active sidebar item since Frappe v16
 * does not add any active class to sidebar items.
 */

(function () {
    "use strict";

    let _cssCache = null;

    /* ── Boot ───────────────────────────────────────────────── */
    frappe.after_ajax(function () {
        fetchAndApply();
        hookRouter();
        markActiveSidebarItem();
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
            markActiveSidebarItem();
        });

        if (frappe.router) {
            frappe.router.on("change", function () {
                if (_cssCache) applyCSS(_cssCache);
                markActiveSidebarItem();
            });
        }
    }

    /* ── 3. Mark active sidebar item ────────────────────────── */
    function markActiveSidebarItem() {
        setTimeout(function () {
            // Remove previous active marks
            document.querySelectorAll('.sidebar-item-container.portal-active')
                .forEach(function(el) { el.classList.remove('portal-active'); });

            var route = frappe.get_route_str() || "";
            // e.g. "List/Font/List" → doctype = "Font"
            // e.g. "Form/Sidebar Theme/Sidebar Theme" → doctype = "Sidebar Theme"
            var parts = route.split("/");
            var doctype = (parts[1] || "").toLowerCase().replace(/ /g, "-");

            if (!doctype) return;

            document.querySelectorAll('.sidebar-item-container').forEach(function (el) {
                var itemName = (el.getAttribute('item-name') || "").toLowerCase().replace(/ /g, "-");
                var href = (el.querySelector('.item-anchor')?.getAttribute('href') || "").toLowerCase();

                if (itemName && (itemName === doctype || href.includes("/" + doctype))) {
                    el.classList.add('portal-active');
                }
            });
        }, 150);
    }

    /* ── 4. Apply CSS (fonts + styles) ─────────────────────── */
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