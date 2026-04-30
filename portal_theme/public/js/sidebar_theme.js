/**
 * Sidebar Theme — Dynamic CSS Injector
 * Uses exact Frappe sidebar class names for precise styling.
 */
(function () {
	"use strict";

	if (document.readyState === "loading") {
		document.addEventListener("DOMContentLoaded", loadSidebarTheme);
	} else {
		loadSidebarTheme();
	}

	function loadSidebarTheme() {
		frappe.call({
			method: "portal_theme.api.get_sidebar_theme",
			async: true,
			callback: function (r) {
				if (!r || !r.message) return;
				const s = r.message;
				if (!s.enable_sidebar_theme) return;
				injectCSS(buildSidebarCSS(s));
			},
		});
	}

	function injectCSS(css) {
		let tag = document.getElementById("sidebar-theme-css");
		if (!tag) {
			tag = document.createElement("style");
			tag.id = "sidebar-theme-css";
			document.head.appendChild(tag);
		}
		tag.textContent = css;
	}

	function v(val, fb) { return val || fb; }

	function buildSidebarCSS(s) {
		// === Background ===
		const bgColor = v(s.bg_color, "#0a0e2a");
		const bgValue = s.use_gradient
			? "linear-gradient(" + v(s.bg_gradient_direction, "to bottom") + ", " + v(s.bg_gradient_start, "#0a0e2a") + ", " + v(s.bg_gradient_end, "#141a3a") + ")"
			: bgColor;

		// === General ===
		const W = v(s.sidebar_width, 220);
		const FF = v(s.sidebar_font_family, "Inter, -apple-system, BlinkMacSystemFont, sans-serif");
		const FS = v(s.sidebar_font_size, 13);
		const FW = v(s.sidebar_font_weight, "400");

		// === Logo ===
		const ltc = v(s.logo_text_color, "#fff");
		const lsc = v(s.logo_subtitle_color, "#8a8fad");
		const lts = v(s.logo_text_size, 18);
		const lss = v(s.logo_subtitle_size, 11);
		const lbg = s.logo_bg_color || "transparent";
		const lpad = v(s.logo_section_padding, "16px");
		const libg = v(s.logo_icon_bg_color, "#4c6ef5");
		const litc = v(s.logo_icon_text_color, "#fff");
		const lir = v(s.logo_icon_border_radius, 8);
		const chev = v(s.dropdown_chevron_color, "#6c7293");
		const showChev = s.show_dropdown_chevron;

		// === Search ===
		const sBg = v(s.search_bg_color, "#141a3a");
		const sTxt = v(s.search_text_color, "#6c7293");
		const sBdr = v(s.search_border_color, "#1a2048");
		const sRad = v(s.search_border_radius, 8);
		const sIcon = v(s.search_icon_color, "#6c7293");
		const sPad = v(s.search_padding, "8px 12px");
		const sFocus = v(s.search_focus_border_color, "#4c6ef5");
		const sBoxShadow = v(s.search_box_shadow, "0 0 10px rgba(76, 110, 245, 0.2)");
		const sHoverBoxShadow = v(s.search_hover_box_shadow, "0 0 15px rgba(76, 110, 245, 0.5)");
		const ssBg = v(s.search_shortcut_bg, "#1a2048");
		const ssTxt = v(s.search_shortcut_text_color, "#6c7293");

		// === Menu Items ===
		const iTxt = v(s.item_text_color, "#c8ccd8");
		const iIcon = v(s.item_icon_color, "#6c7293");
		const iFS = v(s.item_font_size, 13);
		const iPad = v(s.item_padding, "8px 16px");
		const iMar = v(s.item_margin, "2px 8px");
		const iRad = v(s.item_border_radius, 6);
		const iChev = v(s.item_chevron_color, "#6c7293");
		const iLS = v(s.item_letter_spacing, 0);

		// === Active ===
		const aBg = v(s.active_bg_color, "#1e2a5a");
		const aTxt = v(s.active_text_color, "#fff");
		const aIcon = v(s.active_icon_color, "#fff");
		const aFW = v(s.active_font_weight, "600");
		const aRad = v(s.active_border_radius, 6);
		const aLCol = s.active_left_border_color || "transparent";
		const aLW = v(s.active_left_border_width, 0);

		// === Hover ===
		const hBg = v(s.hover_bg_color, "#141a3a");
		const hTxt = v(s.hover_text_color, "#fff");
		const hIcon = v(s.hover_icon_color, "#fff");
		const hTr = v(s.hover_transition, "0.2s");

		// === Notifications ===
		const nTxt = v(s.notification_text_color, "#c8ccd8");
		const nIcon = v(s.notification_icon_color, "#6c7293");
		const nBBg = v(s.notification_badge_bg, "#e74c3c");
		const nBTxt = v(s.notification_badge_text, "#fff");

		// === Borders ===
		const bRC = v(s.sidebar_border_right_color, "#1a2048");
		const bRW = v(s.sidebar_border_right_width, 1);
		const dCol = v(s.divider_color, "#1a2048");
		const dW = v(s.divider_width, 1);
		const showD = s.show_dividers;

		// === Scrollbar ===
		const scCol = v(s.scrollbar_color, "#2a3065");
		const scHov = v(s.scrollbar_hover_color, "#3a4080");
		const scW = v(s.scrollbar_width, 4);
		const scRad = v(s.scrollbar_border_radius, 4);

		return `
/* ================================================ */
/* Sidebar Theme — Auto-Generated CSS               */
/* ================================================ */


/* ── 1. OUTERMOST CONTAINER ──────────────────── */
.body-sidebar {
        background: ${bgValue} !important;
        width: ${W}px !important;
        min-width: ${W}px !important;
        max-width: ${W}px !important;
        font-family: ${FF} !important;
        font-size: ${FS}px !important;
        font-weight: ${FW} !important;
        border-right: ${bRW}px solid ${bRC} !important;
        transition: background 0.3s ease !important;
}


/* ── 2. SCROLLABLE TOP AREA ──────────────────── */
.body-sidebar-top {
        background: transparent !important;
}


/* ── 3. HEADER ───────────────────────────────── */
.sidebar-header {
        background-color: ${lbg} !important;
        padding: ${lpad} !important;
}

.sidebar-header .icon-container {
        background-color: ${libg} !important;
        color: ${litc} !important;
        border-radius: ${lir}px !important;
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

.sidebar-header .icon.icon-sm {
        color: ${chev} !important;
        display: ${showChev ? "inline-flex" : "none"} !important;
}
.sidebar-header .icon.icon-sm svg {
        color: ${chev} !important;
        stroke: ${chev} !important;
}


/* ── 4. ALL MENU ITEMS — DEFAULT (lowest priority) ── */
.body-sidebar .sidebar-item-container .item-anchor {
        padding: ${iPad} !important;
        margin: ${iMar} !important;
        border-radius: ${iRad}px !important;
        letter-spacing: ${iLS}px !important;
        transition: all ${hTr} ease !important;
        text-decoration: none !important;
        border: none !important;
        box-shadow: none !important;
}

.body-sidebar .sidebar-item-label {
        color: ${iTxt} !important;
        font-size: ${iFS}px !important;
}

.body-sidebar .sidebar-item-icon,
.body-sidebar .sidebar-item-icon svg,
.body-sidebar .sidebar-item-icon.text-ink-gray-7,
.body-sidebar .sidebar-item-icon.text-ink-gray-7 svg {
        color: ${iIcon} !important;
        stroke: ${iIcon} !important;
        display: ${s.show_item_icons ? "inline-flex" : "none"} !important;
}

.body-sidebar .sidebar-item-container .drop-icon,
.body-sidebar .sidebar-item-container .collapse-indicator {
        color: ${iChev} !important;
}


/* ── 5. SEARCH ITEM (HIGH specificity) ───────── */
.body-sidebar .sidebar-item-container[item-icon="search"] .item-anchor {
        border: 1px solid ${sBdr} !important;
        border-radius: ${sRad}px !important;
        padding: ${sPad} !important;
}

.body-sidebar .sidebar-item-container[item-icon="search"] .sidebar-item-label {
        color: ${sTxt} !important;
}

.body-sidebar .sidebar-item-container[item-icon="search"] .sidebar-item-icon,
.body-sidebar .sidebar-item-container[item-icon="search"] .sidebar-item-icon svg {
        color: ${sIcon} !important;
        stroke: ${sIcon} !important;
}

.body-sidebar .sidebar-item-container[item-icon="search"] .item-anchor:hover,
.body-sidebar .sidebar-item-container[item-icon="search"] .item-anchor:focus-within {
        border-color: ${sFocus} !important;
}

.body-sidebar .sidebar-item-suffix.keyboard-shortcut {
        background-color: ${ssBg} !important;
        color: ${ssTxt} !important;
        border: 1px solid ${sBdr} !important;
        border-radius: 4px !important;
        font-size: 10px !important;
        padding: 2px 6px !important;
}


/* ── 6. NOTIFICATION ITEM ────────────────────── */
.body-sidebar .sidebar-item-container[item-icon="notification"] .item-anchor {
        color: ${nTxt} !important;
}

.body-sidebar .sidebar-item-container[item-icon="notification"] .sidebar-item-label {
        color: ${nTxt} !important;
}

.body-sidebar .sidebar-item-container[item-icon="notification"] .sidebar-item-icon,
.body-sidebar .sidebar-item-container[item-icon="notification"] .sidebar-item-icon svg {
        color: ${nIcon} !important;
        stroke: ${nIcon} !important;
}

.body-sidebar .notifications-badge,
.body-sidebar .badge {
        background-color: ${nBBg} !important;
        color: ${nBTxt} !important;
}


/* ── 7. ACTIVE ITEM (HIGHEST specificity) ────── */
/* Handled by Sidebar Item Theme */


/* ── 8. HOVER STATE with GLOW ────────────────── */
/* Handled by Sidebar Item Theme */


/* ── 9. USER SECTION ─────────────────────────── */
.body-sidebar-bottom {
        background: transparent !important;
        border-top: ${bRW}px solid ${bRC} !important;
}

.body-sidebar .sidebar-user-button,
.body-sidebar .sidebar-user-button span,
.body-sidebar .sidebar-user-button .avatar-name,
.body-sidebar .sidebar-user-button .sidebar-item-label {
        color: ${iTxt} !important;
}

.body-sidebar .sidebar-user-button .avatar-frame,
.body-sidebar .sidebar-user-button .standard-image {
        background-color: ${libg} !important;
        color: ${litc} !important;
}

.body-sidebar .sidebar-user-button:hover {
        background-color: ${hBg} !important;
        box-shadow: 0 0 8px ${hBg}aa !important;
}


/* ── 10. DIVIDERS ────────────────────────────── */
.body-sidebar hr,
.body-sidebar .divider {
        border-color: ${dCol} !important;
        border-width: ${dW}px !important;
        display: ${showD ? "block" : "none"} !important;
}


/* ── 11. SCROLLBAR ───────────────────────────── */
.body-sidebar::-webkit-scrollbar,
.body-sidebar-top::-webkit-scrollbar {
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
`;
	}
})();