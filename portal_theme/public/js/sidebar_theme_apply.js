// sidebar_theme_apply.js
// Place in: your_app/public/js/sidebar_theme_apply.js
// Register in hooks.py: app_include_js = ["assets/your_app/js/sidebar_theme_apply.js"]

frappe.after_ajax(function () {
    frappe.call({
        method: "frappe.client.get",
        args: {
            doctype: "Sidebar Theme",
            name: "Sidebar Theme",
        },
        callback: function (r) {
            if (r.exc || !r.message) return;
            if (!r.message.enable_sidebar_theme) {
                // Remove theme if disabled
                $("#custom-sidebar-theme").remove();
                return;
            }
            apply_sidebar_theme(r.message);
        },
    });
});

function apply_sidebar_theme(s) {
    $("#custom-sidebar-theme").remove();

    const bg = s.use_gradient
        ? `linear-gradient(${s.bg_gradient_direction}, ${s.bg_gradient_start}, ${s.bg_gradient_end})`
        : s.bg_color;

    const css = `

    /* ══════════════════════════════════
       SIDEBAR CONTAINER
    ══════════════════════════════════ */
    .body-sidebar {
      background: ${bg} !important;
      width: ${s.sidebar_width}px !important;
      min-width: auto !important;
      font-family: ${s.sidebar_font_family} !important;
      font-size: ${s.sidebar_font_size}px !important;
      font-weight: ${s.sidebar_font_weight} !important;
      border-right: ${s.sidebar_border_right_width}px solid ${s.sidebar_border_right_color} !important;
      overflow: hidden !important;
    }

    /* ══════════════════════════════════
       HEADER / LOGO AREA
    ══════════════════════════════════ */
    .sidebar-header {
      background: ${s.logo_bg_color || bg} !important;
      padding: ${s.logo_section_padding} !important;
      border-bottom: none !important;
    }

    /* Logo icon badge (the "C" square) */
    .icon-container {
      background: ${s.logo_icon_bg_color} !important;
      color: ${s.logo_icon_text_color} !important;
      border-radius: ${s.logo_icon_border_radius}px !important;
      min-width: 32px !important;
      min-height: 32px !important;
      display: flex !important;
      align-items: center !important;
      justify-content: center !important;
    }
    .icon-container svg,
    .icon-container .icon {
      color: ${s.logo_icon_text_color} !important;
      fill: ${s.logo_icon_text_color} !important;
    }

    /* App name (e.g. "CRM") */
    .header-title {
      color: ${s.logo_text_color} !important;
      font-size: ${s.logo_text_size}px !important;
      font-weight: 600 !important;
    }

    /* Subtitle (e.g. "SBOSS") */
    .header-subtitle {
      color: ${s.logo_subtitle_color} !important;
      font-size: ${s.logo_subtitle_size}px !important;
    }

    /* Dropdown chevron in header */
    .sidebar-header .icon.icon-sm {
      color: ${s.dropdown_chevron_color} !important;
      fill: ${s.dropdown_chevron_color} !important;
      display: ${s.show_dropdown_chevron ? "inline-flex" : "none"} !important;
    }

    /* ══════════════════════════════════
       SEARCH BAR
    ══════════════════════════════════ */
    .body-sidebar .sidebar-search,
    .body-sidebar .search-bar,
    .body-sidebar [class*="search"] input,
    .body-sidebar .awesomplete input {
      color: ${s.search_text_color} !important;
      border: 1px solid ${s.search_border_color} !important;
      border-radius: ${s.search_border_radius}px !important;
      padding: ${s.search_padding} !important;
      font-family: ${s.sidebar_font_family} !important;
    }
    .body-sidebar .sidebar-search::placeholder,
    .body-sidebar input::placeholder {
      color: ${s.search_text_color} !important;
      opacity: 1 !important;
    }
    .body-sidebar .sidebar-search:focus,
    .body-sidebar .sidebar-search:focus-within,
    .body-sidebar .sidebar-search:hover,
    .body-sidebar [class*="search"] input:hover,
    .body-sidebar [class*="search"] input:focus {
      border-color: ${s.search_focus_border_color} !important;
      outline: none !important;
    }
    /* Search icon */
    .body-sidebar .sidebar-search .icon,
    .body-sidebar .sidebar-search svg {
      color: ${s.search_icon_color} !important;
      fill: ${s.search_icon_color} !important;
    }
    /* Ctrl+K shortcut badge */
    .keyboard-shortcut {
      background: ${s.search_shortcut_bg} !important;
      color: ${s.search_shortcut_text_color} !important;
      border: 1px solid ${s.search_border_color} !important;
      border-radius: 4px !important;
      font-size: 11px !important;
    }

    /* ══════════════════════════════════
       NOTIFICATION ITEM
    ══════════════════════════════════ */
    .body-sidebar .sidebar-item-label {
      color: ${s.item_text_color} !important;
    }
    .body-sidebar .sidebar-item-icon.text-ink-gray-7,
    .body-sidebar .sidebar-item-icon svg {
      color: ${s.notification_icon_color} !important;
      fill: ${s.notification_icon_color} !important;
    }
    .body-sidebar .badge,
    .body-sidebar .notification-count {
      background: ${s.notification_badge_bg} !important;
      color: ${s.notification_badge_text} !important;
    }

    /* ══════════════════════════════════
       MENU ITEMS — DEFAULT STATE
    ══════════════════════════════════ */
    .standard-sidebar-item > .item-anchor {
      color: ${s.item_text_color} !important;
      padding: ${s.item_padding} !important;
      margin: ${s.item_margin} !important;
      border-radius: ${s.item_border_radius}px !important;
      font-size: ${s.item_font_size}px !important;
      letter-spacing: ${s.item_letter_spacing}px !important;
      transition: background ${s.hover_transition}, color ${s.hover_transition} !important;
      display: flex !important;
      align-items: center !important;
      gap: 8px !important;
      text-decoration: none !important;
      background: transparent !important;
      border: none !important;
    }

    /* Menu item icons (default) */
    .standard-sidebar-item > .item-anchor .sidebar-item-icon,
    .standard-sidebar-item > .item-anchor .sidebar-item-icon.text-ink-gray-7 {
      color: ${s.item_icon_color} !important;
      fill: ${s.item_icon_color} !important;
      display: ${s.show_item_icons ? "inline-flex" : "none"} !important;
    }
    .standard-sidebar-item > .item-anchor .sidebar-item-icon svg {
      color: ${s.item_icon_color} !important;
      fill: ${s.item_icon_color} !important;
    }

    /* Menu item label text */
    .standard-sidebar-item > .item-anchor .sidebar-item-label {
      color: ${s.item_text_color} !important;
      font-size: ${s.item_font_size}px !important;
    }

    /* Submenu chevron */
    .standard-sidebar-item > .item-anchor .sidebar-item-suffix .icon,
    .standard-sidebar-item > .item-anchor .sidebar-item-suffix svg {
      color: ${s.item_chevron_color} !important;
      fill: ${s.item_chevron_color} !important;
    }

    /* ══════════════════════════════════
       MENU ITEMS — HOVER STATE
    ══════════════════════════════════ */
    /* Handled by Sidebar Item Theme */

    /* ══════════════════════════════════
       MENU ITEMS — ACTIVE STATE
    ══════════════════════════════════ */
    /* Handled by Sidebar Item Theme */

    /* ══════════════════════════════════
       SECTION DIVIDERS
    ══════════════════════════════════ */
    .body-sidebar hr,
    .body-sidebar .divider {
      border-color: ${s.divider_color} !important;
      border-width: ${s.divider_width}px !important;
      display: ${s.show_dividers ? "block" : "none"} !important;
    }

    /* ══════════════════════════════════
       BOTTOM USER BUTTON
    ══════════════════════════════════ */
    .body-sidebar-bottom .sidebar-user-button,
    .body-sidebar-bottom .nav-link {
      color: ${s.item_text_color} !important;
      border-top: 1px solid ${s.sidebar_border_right_color} !important;
      background: transparent !important;
    }
    .body-sidebar-bottom .sidebar-user-button:hover {
      background: ${s.hover_bg_color} !important;
    }

    /* ══════════════════════════════════
       SCROLLBAR
    ══════════════════════════════════ */
    .body-sidebar::-webkit-scrollbar {
      width: ${s.scrollbar_width}px !important;
    }
    .body-sidebar::-webkit-scrollbar-track {
      background: transparent !important;
    }
    .body-sidebar::-webkit-scrollbar-thumb {
      background: ${s.scrollbar_color} !important;
      border-radius: ${s.scrollbar_border_radius}px !important;
    }
    .body-sidebar::-webkit-scrollbar-thumb:hover {
      background: ${s.scrollbar_hover_color} !important;
    }

    /* ══════════════════════════════════
       KILL DEFAULT FRAPPE OVERRIDES
    ══════════════════════════════════ */
    .body-sidebar .sidebar-item-icon.text-ink-gray-7 {
      --icon-stroke: ${s.item_icon_color} !important;
    }
    .standard-sidebar-item.active-sidebar-item .sidebar-item-icon.text-ink-gray-7 {
      --icon-stroke: ${s.active_icon_color} !important;
    }
    .standard-sidebar-item > .item-anchor:hover .sidebar-item-icon.text-ink-gray-7 {
      --icon-stroke: ${s.hover_icon_color} !important;
    }
  `;

    $('<style id="custom-sidebar-theme">').text(css).appendTo("head");
}