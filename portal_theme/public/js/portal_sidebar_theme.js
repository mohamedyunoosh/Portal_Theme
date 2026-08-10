/**
 * Portal Sidebar Theme — Dynamic CSS Injector
 * Frappe ERPNext v16 | Global (SPA-aware)
 *
 * Fixes:
 *  1. Hooks into Frappe's SPA router so theme persists on every navigation.
 *  2. Caches the theme locally so re-injections are instant (no extra API call).
 *  3. Uses a MutationObserver as a safety net for lazy-rendered sidebars.
 *  4. Covers all known Frappe v16 sidebar wrappers across desk / form / list /
 *     report / workspace / print screens.
 *  5. Font-family applied correctly only when a value is set.
 */
(function () {
	"use strict";

	/* ── Cache ──────────────────────────────────────────────── */
	let _themeCache = null;       // stores the fetched settings object
	let _cssCache   = null;       // stores the built CSS string
	let _observer   = null;       // MutationObserver instance

	/* ── Entry point ─────────────────────────────────────────── */
	function boot() {
		fetchAndApply();
		hookRouter();
		startObserver();
	}

	if (document.readyState === "loading") {
		document.addEventListener("DOMContentLoaded", boot);
	} else {
		boot();
	}

	/* ── 1. Fetch settings (once) then inject ────────────────── */
	function fetchAndApply() {
		if (_cssCache) {
			// Already built — just make sure the <style> tag is present
			injectCSS(_cssCache);
			return;
		}

		frappe.call({
			method: "portal_theme.api.get_portal_sidebar_theme",
			async: true,
			callback: function (r) {
				if (!r || !r.message) return;
				const s = r.message;
				if (!s.enable_sidebar_theme) return;

				_themeCache = s;
				_cssCache   = buildSidebarCSS(s);
				injectCSS(_cssCache);
			},
		});
	}

	/* ── 2. Hook Frappe SPA router ───────────────────────────── */
	function hookRouter() {
		// Frappe fires this event on every route change
		$(document).on("page-change", function () {
			if (_cssCache) injectCSS(_cssCache);
		});

		// Also hook frappe.router if available (v15/16)
		if (frappe.router) {
			frappe.router.on("change", function () {
				if (_cssCache) injectCSS(_cssCache);
			});
		}
	}

	/* ── 3. MutationObserver safety-net ─────────────────────── */
	// Some sidebar elements are rendered late (workspace, reports).
	// Re-inject when the sidebar DOM node appears or is replaced.
	function startObserver() {
		if (_observer) return;

		_observer = new MutationObserver(function (mutations) {
			for (const m of mutations) {
				for (const node of m.addedNodes) {
					if (
						node.nodeType === 1 &&
						(node.classList.contains("body-sidebar") ||
							node.querySelector?.(".body-sidebar"))
					) {
						if (_cssCache) injectCSS(_cssCache);
						return;
					}
				}
			}
		});

		_observer.observe(document.body, { childList: true, subtree: true });
	}

	/* ── Inject / refresh <style> tag ───────────────────────── */
	function injectCSS(css) {
		let tag = document.getElementById("portal-sidebar-theme-css");
		if (!tag) {
			tag = document.createElement("style");
			tag.id = "portal-sidebar-theme-css";
			document.head.appendChild(tag);
		}
		tag.textContent = css;
	}

	/* ── Helpers ─────────────────────────────────────────────── */
	function v(val, fb) { return val !== undefined && val !== null && val !== "" ? val : fb; }

	/* ── CSS Builder ─────────────────────────────────────────── */
	function buildSidebarCSS(s) {

		/* Background */
		const bgColor = v(s.bg_color, "#0a0e2a");
		const bgValue = s.use_gradient
			? `linear-gradient(${v(s.bg_gradient_direction, "to bottom")}, ${v(s.bg_gradient_start, "#0a0e2a")}, ${v(s.bg_gradient_end, "#141a3a")})`
			: bgColor;

		/* General */
		const W  = v(s.sidebar_width, 220);
		const FF = s.sidebar_font_family ? `font-family: ${s.sidebar_font_family} !important;` : "";
		const FS = v(s.sidebar_font_size, 13);
		const FW = v(s.sidebar_font_weight, "400");

		/* Logo */
		const ltc  = v(s.logo_text_color, "#fff");
		const lsc  = v(s.logo_subtitle_color, "#8a8fad");
		const lts  = v(s.logo_text_size, 18);
		const lss  = v(s.logo_subtitle_size, 11);
		const lbg  = s.logo_bg_color || "transparent";
		const lpad = v(s.logo_section_padding, "16px");
		const libg = v(s.logo_icon_bg_color, "#4c6ef5");
		const litc = v(s.logo_icon_text_color, "#fff");
		const lir  = v(s.logo_icon_border_radius, 8);
		const chev = v(s.dropdown_chevron_color, "#6c7293");
		const showChev = s.show_dropdown_chevron;

		/* Search */
		const sBg           = v(s.search_bg_color, "#141a3a");
		const sTxt          = v(s.search_text_color, "#6c7293");
		const sBdr          = v(s.search_border_color, "#1a2048");
		const sRad          = v(s.search_border_radius, 8);
		const sIcon         = v(s.search_icon_color, "#6c7293");
		const sPad          = v(s.search_padding, "8px 12px");
		const sFocus        = v(s.search_focus_border_color, "#4c6ef5");
		const sBoxShadow    = v(s.search_box_shadow, "0 0 10px rgba(76,110,245,0.2)");
		const sHoverShadow  = v(s.search_hover_box_shadow, "0 4px 15px rgba(0,0,0,0.4)");
		const ssBg          = v(s.search_shortcut_bg, "#1a2048");
		const ssTxt         = v(s.search_shortcut_text_color, "#6c7293");

		/* Menu items */
		const iTxt  = v(s.item_text_color, "#c8ccd8");
		const iIcon = v(s.item_icon_color, "#6c7293");
		const iFS   = v(s.item_font_size, 13);
		const iPad  = v(s.item_padding, "8px 16px");
		const iMar  = v(s.item_margin, "2px 8px");
		const iRad  = v(s.item_border_radius, 6);
		const iChev = v(s.item_chevron_color, "#6c7293");
		const iLS   = v(s.item_letter_spacing, 0);

		/* Active */
		const aBg   = v(s.active_bg_color, "#1e2a5a");
		const aTxt  = v(s.active_text_color, "#fff");
		const aIcon = v(s.active_icon_color, "#fff");
		const aFW   = v(s.active_font_weight, "600");
		const aRad  = v(s.active_border_radius, 6);
		const aLCol = s.active_left_border_color || "#4c6ef5";
		const aLW   = v(s.active_left_border_width, 0);

		/* Hover */
		const hBg   = v(s.hover_bg_color, "#141a3a");
		const hTxt  = v(s.hover_text_color, "#fff");
		const hIcon = v(s.hover_icon_color, "#fff");
		const hTr   = v(s.hover_transition, "0.2s");

		/* Notifications */
		const nTxt  = v(s.notification_text_color, "#c8ccd8");
		const nIcon = v(s.notification_icon_color, "#6c7293");
		const nBBg  = v(s.notification_badge_bg, "#e74c3c");
		const nBTxt = v(s.notification_badge_text, "#fff");

		/* Borders */
		const bRC  = v(s.sidebar_border_right_color, "#1a2048");
		const bRW  = v(s.sidebar_border_right_width, 1);
		const dCol = v(s.divider_color, "#1a2048");
		const dW   = v(s.divider_width, 1);
		const showD = s.show_dividers;

		/* Scrollbar */
		const scCol = v(s.scrollbar_color, "#2a3065");
		const scHov = v(s.scrollbar_hover_color, "#3a4080");
		const scW   = v(s.scrollbar_width, 4);
		const scRad = v(s.scrollbar_border_radius, 4);

		/* Icon visibility */
		const iconDisplay = s.show_item_icons ? "inline-flex" : "none";

		return `
/* ========================================================= */
/* Portal Sidebar Theme — Auto-Generated                      */
/* Scope: ALL Frappe v16 screens (desk/form/list/report/ws)  */
/* ========================================================= */


/* ── 1. SIDEBAR CONTAINER (all screen wrappers) ─────────── */
/*
   Frappe v16 uses .body-sidebar as the primary wrapper.
   Some embedded views (report, print) clone the sidebar into
   .layout-side-section or .sidebar-column — we target both.
*/
.body-sidebar,
.layout-side-section .body-sidebar,
.sidebar-column {
    background: ${bgValue} !important;
    width: ${W}px !important;
    min-width: ${W}px !important;
    max-width: ${W}px !important;
    ${FF}
    font-size: ${FS}px !important;
    font-weight: ${FW} !important;
    border-right: ${bRW}px solid ${bRC} !important;
    transition: background 0.3s ease !important;
    box-sizing: border-box !important;
}

/* Desk page — main layout column that houses the sidebar */
.page-container .layout-main-section-wrapper {
    /* prevent content overlap when sidebar width changes */
    transition: margin-left 0.3s ease !important;
}


/* ── 2. INNER SCROLL AREAS ───────────────────────────────── */
.body-sidebar-top,
.body-sidebar .sidebar-top-section {
    background: transparent !important;
    flex: 1 1 auto !important;
    overflow-y: auto !important;
}

.body-sidebar-bottom,
.body-sidebar .sidebar-bottom-section {
    background: transparent !important;
    flex: 0 0 auto !important;
}


/* ── 3. LOGO / HEADER AREA ───────────────────────────────── */
.sidebar-header,
.body-sidebar .sidebar-header {
    background-color: ${lbg} !important;
    padding: ${lpad} !important;
}

.sidebar-header .icon-container,
.body-sidebar .icon-container {
    background-color: ${libg} !important;
    color: ${litc} !important;
    border-radius: ${lir}px !important;
    flex-shrink: 0 !important;
}

.sidebar-header .sidebar-item-label.header-title {
    color: ${ltc} !important;
    font-size: ${lts}px !important;
    font-weight: 700 !important;
}

.sidebar-header .sidebar-item-label.header-subtitle {
    color: ${lsc} !important;
    font-size: ${lss}px !important;
    font-weight: 400 !important;
}

/* Chevron / dropdown arrow in header */
.sidebar-header .icon.icon-sm,
.sidebar-header .icon.icon-sm svg {
    color: ${chev} !important;
    stroke: ${chev} !important;
    display: ${showChev ? "inline-flex" : "none"} !important;
}


/* ── 4. ALL MENU ITEMS — DEFAULT STATE ──────────────────── */
/* Covers desk modules, workspace pages, list/form shortcuts */
.body-sidebar .sidebar-item-container .item-anchor,
.body-sidebar .standard-sidebar-item > .item-anchor {
    padding: ${iPad} !important;
    margin: ${iMar} !important;
    border-radius: ${iRad}px !important;
    letter-spacing: ${iLS}px !important;
    transition: background ${hTr} ease, color ${hTr} ease !important;
    text-decoration: none !important;
    border: none !important;
    box-shadow: none !important;
    display: flex !important;
    align-items: center !important;
    gap: 8px !important;
}

.body-sidebar .sidebar-item-label {
    color: ${iTxt} !important;
    font-size: ${iFS}px !important;
}

/* Icons — all variants Frappe v16 uses */
.body-sidebar .sidebar-item-icon,
.body-sidebar .sidebar-item-icon svg,
.body-sidebar .sidebar-item-icon.text-ink-gray-7,
.body-sidebar .sidebar-item-icon.text-ink-gray-7 svg,
.body-sidebar .item-icon,
.body-sidebar .item-icon svg {
    color: ${iIcon} !important;
    stroke: ${iIcon} !important;
    display: ${iconDisplay} !important;
    flex-shrink: 0 !important;
}

/* Submenu chevrons */
.body-sidebar .sidebar-item-container .drop-icon,
.body-sidebar .sidebar-item-container .collapse-indicator,
.body-sidebar .sidebar-item-container .drop-icon svg {
    color: ${iChev} !important;
    stroke: ${iChev} !important;
}


/* ── 5. ACTIVE ITEM ──────────────────────────────────────── */
/* Priority: these must beat default and hover rules */
.body-sidebar .standard-sidebar-item.active-sidebar,
.body-sidebar .standard-sidebar-item.active-sidebar > .item-anchor,
.body-sidebar .standard-sidebar-item.active-sidebar-item > .item-anchor,
.body-sidebar .standard-sidebar-item > .item-anchor.active,
.body-sidebar .sidebar-item-container.active > .item-anchor {
    background-color: ${aBg} !important;
    color: ${aTxt} !important;
    font-weight: ${aFW} !important;
    border-radius: ${aRad}px !important;
    ${aLW > 0 ? `border-left: ${aLW}px solid ${aLCol} !important; padding-left: calc(${iPad.split(" ")[1] || "16px"} - ${aLW}px) !important;` : "border-left: none !important;"}
}

.body-sidebar .standard-sidebar-item.active-sidebar .sidebar-item-label,
.body-sidebar .standard-sidebar-item.active-sidebar-item > .item-anchor .sidebar-item-label,
.body-sidebar .standard-sidebar-item > .item-anchor.active .sidebar-item-label {
    color: ${aTxt} !important;
}

.body-sidebar .standard-sidebar-item.active-sidebar svg,
.body-sidebar .standard-sidebar-item.active-sidebar-item > .item-anchor svg,
.body-sidebar .standard-sidebar-item > .item-anchor.active svg {
    fill: ${aIcon} !important;
    stroke: ${aIcon} !important;
}


/* ── 6. HOVER STATE ──────────────────────────────────────── */
.body-sidebar .standard-sidebar-item:not(.active-sidebar):hover > .item-anchor,
.body-sidebar .standard-sidebar-item > .item-anchor:not(.active):hover,
.body-sidebar .sidebar-item-container:not(.active):hover > .item-anchor {
    background-color: ${hBg} !important;
    color: ${hTxt} !important;
    transition: background ${hTr} ease-in-out, color ${hTr} ease-in-out !important;
}

.body-sidebar .standard-sidebar-item:not(.active-sidebar):hover svg,
.body-sidebar .standard-sidebar-item > .item-anchor:not(.active):hover svg {
    fill: ${hIcon} !important;
    stroke: ${hIcon} !important;
}

.body-sidebar .standard-sidebar-item:not(.active-sidebar):hover .sidebar-item-label {
    color: ${hTxt} !important;
}


/* ── 7. SEARCH ITEM ──────────────────────────────────────── */
/* Frappe renders search as a special sidebar item */
.body-sidebar .sidebar-item-container[item-icon="search"] .item-anchor,
.body-sidebar .standard-sidebar-item[data-item-name="Search"] > .item-anchor,
.body-sidebar .standard-sidebar-item[data-label="Search"] > .item-anchor,
.body-sidebar .sidebar-item-container[item-name="Search"] .item-anchor {
    background-color: ${sBg} !important;
    border: 1px solid ${sBdr} !important;
    border-radius: ${sRad}px !important;
    padding: ${sPad} !important;
    box-shadow: ${sBoxShadow} !important;
    transition: border-color 0.2s ease, box-shadow 0.2s ease !important;
}

.body-sidebar .sidebar-item-container[item-icon="search"] .sidebar-item-label,
.body-sidebar .standard-sidebar-item[data-item-name="Search"] .sidebar-item-label {
    color: ${sTxt} !important;
}

.body-sidebar .sidebar-item-container[item-icon="search"] .sidebar-item-icon,
.body-sidebar .sidebar-item-container[item-icon="search"] .sidebar-item-icon svg {
    color: ${sIcon} !important;
    stroke: ${sIcon} !important;
    display: inline-flex !important;
}

/* Search hover & focus */
.body-sidebar .sidebar-item-container[item-icon="search"] .item-anchor:hover,
.body-sidebar .sidebar-item-container[item-icon="search"] .item-anchor:focus-within,
.body-sidebar .standard-sidebar-item[data-item-name="Search"] > .item-anchor:hover {
    border-color: ${sFocus} !important;
    box-shadow: ${sHoverShadow} !important;
    background-color: ${sBg} !important;
}

/* Keyboard shortcut badge */
.body-sidebar .sidebar-item-suffix.keyboard-shortcut,
.body-sidebar .sidebar-item-container[item-icon="search"] .sidebar-item-suffix {
    background-color: ${ssBg} !important;
    color: ${ssTxt} !important;
    border: 1px solid ${sBdr} !important;
    border-radius: 4px !important;
    font-size: 10px !important;
    padding: 2px 6px !important;
    margin-left: auto !important;
}


/* ── 8. NOTIFICATION ITEM ────────────────────────────────── */
.body-sidebar .sidebar-item-container[item-icon="notification"] .sidebar-item-label,
.body-sidebar .sidebar-item-container[item-icon="bell"] .sidebar-item-label {
    color: ${nTxt} !important;
}

.body-sidebar .sidebar-item-container[item-icon="notification"] .sidebar-item-icon,
.body-sidebar .sidebar-item-container[item-icon="notification"] .sidebar-item-icon svg,
.body-sidebar .sidebar-item-container[item-icon="bell"] .sidebar-item-icon svg {
    color: ${nIcon} !important;
    stroke: ${nIcon} !important;
}

.body-sidebar .notifications-badge,
.body-sidebar .indicator-pill,
.body-sidebar .badge {
    background-color: ${nBBg} !important;
    color: ${nBTxt} !important;
}


/* ── 9. USER / ACCOUNT SECTION (bottom) ──────────────────── */
.body-sidebar-bottom,
.body-sidebar .sidebar-user-section {
    border-top: ${bRW}px solid ${bRC} !important;
}

.body-sidebar .sidebar-user-button,
.body-sidebar .sidebar-user-button span,
.body-sidebar .sidebar-user-button .avatar-name,
.body-sidebar .sidebar-user-button .sidebar-item-label,
.body-sidebar .sidebar-user-section .sidebar-item-label {
    color: ${iTxt} !important;
}

.body-sidebar .sidebar-user-button .avatar-frame,
.body-sidebar .sidebar-user-button .standard-image {
    background-color: ${libg} !important;
    color: ${litc} !important;
}

.body-sidebar .sidebar-user-button:hover,
.body-sidebar .sidebar-user-section .item-anchor:hover {
    background-color: ${hBg} !important;
}


/* ── 10. SECTION DIVIDERS ────────────────────────────────── */
.body-sidebar hr,
.body-sidebar .divider,
.body-sidebar .sidebar-section-divider {
    border-color: ${dCol} !important;
    border-width: ${dW}px !important;
    border-style: solid !important;
    display: ${showD ? "block" : "none"} !important;
}


/* ── 11. SCROLLBAR ───────────────────────────────────────── */
.body-sidebar::-webkit-scrollbar,
.body-sidebar-top::-webkit-scrollbar,
.body-sidebar .body-sidebar-top::-webkit-scrollbar {
    width: ${scW}px !important;
}

.body-sidebar::-webkit-scrollbar-track,
.body-sidebar-top::-webkit-scrollbar-track {
    background: transparent !important;
}

.body-sidebar::-webkit-scrollbar-thumb,
.body-sidebar-top::-webkit-scrollbar-thumb {
    background-color: ${scCol} !important;
    border-radius: ${scRad}px !important;
}

.body-sidebar::-webkit-scrollbar-thumb:hover,
.body-sidebar-top::-webkit-scrollbar-thumb:hover {
    background-color: ${scHov} !important;
}

.body-sidebar,
.body-sidebar-top {
    scrollbar-width: thin !important;
    scrollbar-color: ${scCol} transparent !important;
}


/* ── 12. FORM / LIST / REPORT — SIDEBAR COLUMN ───────────── */
/*
   On form, list, and report views Frappe renders a right or left
   sidebar via .layout-side-section. We reuse the same tokens.
*/
.layout-side-section {
    ${FF}
    font-size: ${FS}px !important;
}

.layout-side-section .sidebar-label,
.layout-side-section .form-sidebar .sidebar-label,
.layout-side-section h5 {
    color: ${iTxt} !important;
    font-size: ${FS}px !important;
    font-weight: ${aFW} !important;
    letter-spacing: ${iLS}px !important;
}

.layout-side-section .form-sidebar-items .btn,
.layout-side-section .form-sidebar-items a {
    color: ${iTxt} !important;
    font-size: ${iFS}px !important;
}

.layout-side-section .form-sidebar-items .btn:hover,
.layout-side-section .form-sidebar-items a:hover {
    color: ${hTxt} !important;
    background-color: ${hBg} !important;
}


/* ── 13. WORKSPACE PAGE SIDEBAR ──────────────────────────── */
/* Workspace uses .sidebar-item-container inside a page sidebar */
.page-sidebar .body-sidebar,
.page-sidebar {
    background: ${bgValue} !important;
    ${FF}
}


/* ── 14. PRINT PREVIEW — hide sidebar ────────────────────── */
@media print {
    .body-sidebar {
        display: none !important;
    }
}


/* ── 15. RESPONSIVE — collapse sidebar on small screens ─── */
@media (max-width: 768px) {
    .body-sidebar {
        width: 0 !important;
        min-width: 0 !important;
        overflow: hidden !important;
        border-right: none !important;
    }

    .body-sidebar.show-sidebar-mobile {
        width: ${W}px !important;
        min-width: ${W}px !important;
    }
}
`;
	}
})();