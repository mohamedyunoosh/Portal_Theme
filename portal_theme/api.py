import frappe


# ══════════════════════════════════════════════════════════
# INTERNAL HELPERS
# ══════════════════════════════════════════════════════════

def _v(val, fallback="inherit"):
    """Return val if truthy, else fallback."""
    return val if val else fallback


def _resolve_font(font_name):
    if not font_name:
        return "inherit", None
    try:
        font = frappe.get_doc("Font", font_name)
    except Exception:
        return "inherit", None

    stack = (font.css_stack or "inherit").rstrip(";").strip()

    import_url = None

    if font.font_type == "Google Font" and font.google_font_name:
        encoded = font.google_font_name.strip().replace(" ", "+")
        import_url = (
            f"https://fonts.googleapis.com/css2?family={encoded}"
            f":ital,wght@0,100;0,200;0,300;0,400;0,500;0,600;0,700;0,800;0,900&display=swap"
        )
    elif font.font_type == "Google Font" and not font.google_font_name:
        import re
        match = re.search(r'["\']([^"\']+)["\']', stack)
        if match:
            encoded = match.group(1).replace(" ", "+")
            import_url = (
                f"https://fonts.googleapis.com/css2?family={encoded}"
                f":ital,wght@0,100;0,200;0,300;0,400;0,500;0,600;0,700;0,800;0,900&display=swap"
            )

    return stack, import_url


def _build_portal_theme_css(s):
    def v(val, fallback="inherit"):
        return val if val else fallback

    font_stack, font_import_url = _resolve_font(s.body_font)
    google_import = f'@import url("{font_import_url}");' if font_import_url else ""

    parts = [google_import] if google_import else []
    parts.append(":root {")
    parts.append(f"  --navbar-bg: {v(s.navbar_color)};")
    parts.append(f"  --navbar-text: {v(s.navbar_text_color)};")
    parts.append(f"  --btn-primary-bg: {v(s.primary_button_background)};")
    parts.append(f"  --btn-primary-text: {v(s.primary_button_text)};")
    parts.append(f"  --btn-primary-hover-bg: {v(s.primary_button_hover_background)};")
    parts.append(f"  --btn-secondary-bg: {v(s.secondary_button_background)};")
    parts.append(f"  --btn-secondary-text: {v(s.secondary_button_text)};")
    parts.append(f"  --card-bg: {v(s.card_background_color)};")
    parts.append(f"  --card-header-bg: {v(s.card_header_color)};")
    parts.append(f"  --card-text: {v(s.card_text_color)};")
    parts.append(f"  --form-bg: {v(s.form_background_color)};")
    parts.append(f"  --form-text: {v(s.form_text_color)};")
    parts.append(f"  --portal-bg: {v(s.portal_background_color)};")
    parts.append(f"  --section-heading: {v(s.section_heading_color)};")
    parts.append(f"  --body-font: {font_stack};")
    parts.append("}")

    parts.append(f"""
/* Global Font */
html, body, input, button, select, textarea,
.form-control, .btn, .navbar, .card,
.frappe-list, .page-container {{
    font-family: {font_stack} !important;
}}

/* Portal Background */
html, body, .page-container {{
    background-color: var(--portal-bg) !important;
}}

/* Navbar */
.navbar {{
    background-color: var(--navbar-bg) !important;
    color: var(--navbar-text) !important;
}}
.navbar a, .navbar .nav-link {{
    color: var(--navbar-text) !important;
}}

/* Primary Button */
.btn.btn-primary {{
    background-color: var(--btn-primary-bg) !important;
    color: var(--btn-primary-text) !important;
}}
.btn.btn-primary:hover {{
    background-color: var(--btn-primary-hover-bg) !important;
}}

/* Secondary Button */
.btn.btn-secondary {{
    background-color: var(--btn-secondary-bg) !important;
    color: var(--btn-secondary-text) !important;
}}

/* Cards */
.card, .card .card-body {{
    background-color: var(--card-bg) !important;
    color: var(--card-text) !important;
}}
.card-header {{
    background-color: var(--card-header-bg) !important;
}}

/* Forms */
.form-control {{
    background-color: var(--form-bg) !important;
    color: var(--form-text) !important;
}}

/* Headings */
h1, h2, h3, h4, h5, h6, .section-head {{
    color: var(--section-heading) !important;
}}
""")

    return "\n".join(parts)


def _build_sidebar_css(s):
    """
    Build CSS from Sidebar Theme doc.
    Uses local helper c() with explicit hex fallbacks — never 'inherit' —
    so colors always render correctly even when DocType fields are blank.
    """
    def c(val, fallback):
        """Color helper: always returns a real value, never empty."""
        return val if val else fallback

    stack, import_url = _resolve_font(s.sidebar_font_family)
    google_import = f'@import url("{import_url}");' if import_url else ""
    font_rule = f"font-family: {stack} !important;" if stack and stack != "inherit" else ""

    # Background
    if s.use_gradient:
        bg = (
            f"linear-gradient({c(s.bg_gradient_direction, 'to bottom')}, "
            f"{c(s.bg_gradient_start, '#0a0e2a')}, "
            f"{c(s.bg_gradient_end, '#141a3a')})"
        )
    else:
        bg = c(s.bg_color, "#0a0e2a")

    # Active left border
    active_border = (
        f"border-left: {s.active_left_border_width}px solid "
        f"{c(s.active_left_border_color, '#4c6ef5')} !important;"
        if s.active_left_border_width
        else "border-left: none !important;"
    )

    # Toggles
    show_icons    = "inline-flex" if s.show_item_icons       else "none"
    show_chevron  = "inline-flex" if s.show_dropdown_chevron else "none"
    show_dividers = "block"       if s.show_dividers         else "none"

    # Values — all with explicit hex fallbacks
    W     = s.sidebar_width or 220
    FS    = s.item_font_size or 13
    FW    = c(s.sidebar_font_weight, "400")
    bRW   = s.sidebar_border_right_width or 1
    bRC   = c(s.sidebar_border_right_color, "#1a2048")
    lbg   = c(s.logo_bg_color, bg)
    lpad  = c(s.logo_section_padding, "16px")
    libg  = c(s.logo_icon_bg_color, "#4c6ef5")
    litc  = c(s.logo_icon_text_color, "#ffffff")
    lir   = s.logo_icon_border_radius or 8
    ltc   = c(s.logo_text_color, "#ffffff")
    lts   = s.logo_text_size or 18
    lsc   = c(s.logo_subtitle_color, "#8a8fad")
    lss   = s.logo_subtitle_size or 11
    chev  = c(s.dropdown_chevron_color, "#6c7293")
    sBg   = c(s.search_bg_color, "#141a3a")
    sTxt  = c(s.search_text_color, "#6c7293")
    sBdr  = c(s.search_border_color, "#1a2048")
    sRad  = s.search_border_radius or 8
    sIcon = c(s.search_icon_color, "#6c7293")
    sPad  = c(s.search_padding, "8px 12px")
    sFoc  = c(s.search_focus_border_color, "#4c6ef5")
    sShadow      = c(s.search_box_shadow, "0 0 10px rgba(76,110,245,0.2)")
    sHoverShadow = c(s.search_hover_box_shadow, "0 4px 15px rgba(0,0,0,0.4)")
    ssBg  = c(s.search_shortcut_bg, "#1a2048")
    ssTxt = c(s.search_shortcut_text_color, "#6c7293")
    iTxt  = c(s.item_text_color, "#c8ccd8")
    iIcon = c(s.item_icon_color, "#6c7293")
    iFS   = s.item_font_size or 13
    iPad  = c(s.item_padding, "8px 16px")
    iMar  = c(s.item_margin, "2px 8px")
    iRad  = s.item_border_radius or 6
    iChev = c(s.item_chevron_color, "#6c7293")
    iLS   = s.item_letter_spacing or 0
    hTr   = c(s.hover_transition, "0.2s")
    hBg   = c(s.hover_bg_color, "#141a3a")
    hTxt  = c(s.hover_text_color, "#ffffff")
    hIcon = c(s.hover_icon_color, "#ffffff")
    aBg   = c(s.active_bg_color, "#1e2a5a")
    aTxt  = c(s.active_text_color, "#ffffff")
    aIcon = c(s.active_icon_color, "#ffffff")
    aFW   = c(s.active_font_weight, "600")
    aRad  = s.active_border_radius or 6
    nTxt  = c(s.notification_text_color, "#c8ccd8")
    nIcon = c(s.notification_icon_color, "#6c7293")
    nBBg  = c(s.notification_badge_bg, "#e74c3c")
    nBTxt = c(s.notification_badge_text, "#ffffff")
    dCol  = c(s.divider_color, "#1a2048")
    dW    = s.divider_width or 1
    scCol = c(s.scrollbar_color, "#2a3065")
    scHov = c(s.scrollbar_hover_color, "#3a4080")
    scW   = s.scrollbar_width or 4
    scRad = s.scrollbar_border_radius or 4

    return f"""
{google_import}

/* ══════════════════════════════════════════════════════════
   Sidebar Theme — generated from Sidebar Theme DocType
   Applied globally: desk / form / list / report / workspace
   ══════════════════════════════════════════════════════════ */


/* ── 1. SIDEBAR CONTAINER ───────────────────────────────── */
.body-sidebar {{
    background: {bg} !important;
    {font_rule}
    font-size: {FS}px !important;
    font-weight: {FW} !important;
    border-right: {bRW}px solid {bRC} !important;
    transition: background 0.3s ease !important;
    box-sizing: border-box !important;
}}

.body-sidebar-top {{
    background: transparent !important;
    flex: 1 1 auto !important;
    overflow-y: auto !important;
    overflow-x: hidden !important;
}}

.body-sidebar-bottom {{
    background: transparent !important;
    flex: 0 0 auto !important;
}}

/* Remove Frappe default gap that causes large spacing between items */
.body-sidebar .sidebar-items,
.body-sidebar .standard-items-sections,
.body-sidebar .sidebar-item-container {{
    gap: 0 !important;
    padding: 0 !important;
}}


/* ── 2. LOGO / HEADER ────────────────────────────────────── */
.sidebar-header,
a.sidebar-header-hover {{
    background: {lbg} !important;
    padding: {lpad} !important;
}}

/* Icon badge — the coloured square with initials */
.sidebar-header .sidebar-item-icon,
.body-sidebar .sidebar-item-icon[style*="background-color"] {{
    background-color: {libg} !important;
    color: {litc} !important;
    border-radius: {lir}px !important;
}}

/* Also override the CSS var Frappe uses for icon bg */
.body-sidebar {{
    --sidebar-item-icon-bg: {libg} !important;
}}

/* Logo text (workspace name — Frappe controlled, we style only) */
.sidebar-header .header-title,
.sidebar-header .sidebar-item-label.header-title {{
    color: {ltc} !important;
    font-size: {lts}px !important;
    font-weight: 700 !important;
    overflow: hidden !important;
    text-overflow: ellipsis !important;
    white-space: nowrap !important;
}}

/* Logo subtitle (username — Frappe controlled, we style only) */
.sidebar-header .header-subtitle,
.sidebar-header .sidebar-item-label.header-subtitle {{
    color: {lsc} !important;
    font-size: {lss}px !important;
    font-weight: 400 !important;
}}

/* Dropdown chevron */
.sidebar-header .drop-icon,
.sidebar-header .drop-icon svg {{
    color: {chev} !important;
    stroke: {chev} !important;
    display: {show_chevron} !important;
}}

.sidebar-header .icon.icon-sm,
.sidebar-header .icon.icon-sm svg {{
    color: {chev} !important;
    stroke: {chev} !important;
    display: {show_chevron} !important;
}}


/* ── 3. SEARCH BAR ───────────────────────────────────────── */
.body-sidebar .sidebar-item-container[item-icon="search"] .item-anchor,
.body-sidebar .standard-sidebar-item[data-item-name="Search"] > .item-anchor,
.body-sidebar .sidebar-item-container[item-name="Search"] .item-anchor {{
    background: {sBg} !important;
    border: 1px solid {sBdr} !important;
    border-radius: {sRad}px !important;
    padding: {sPad} !important;
    box-shadow: {sShadow} !important;
    transition: border-color 0.2s ease, box-shadow 0.2s ease !important;
}}

.body-sidebar .sidebar-item-container[item-icon="search"] .sidebar-item-label {{
    color: {sTxt} !important;
}}

.body-sidebar .sidebar-item-container[item-icon="search"] .sidebar-item-icon,
.body-sidebar .sidebar-item-container[item-icon="search"] .sidebar-item-icon svg {{
    color: {sIcon} !important;
    stroke: {sIcon} !important;
    display: inline-flex !important;
}}

.body-sidebar .sidebar-item-container[item-icon="search"] .item-anchor:hover,
.body-sidebar .sidebar-item-container[item-icon="search"] .item-anchor:focus-within {{
    border-color: {sFoc} !important;
    box-shadow: {sHoverShadow} !important;
}}

.body-sidebar .sidebar-item-suffix.keyboard-shortcut {{
    background: {ssBg} !important;
    color: {ssTxt} !important;
    border: 1px solid {sBdr} !important;
    border-radius: 4px !important;
    font-size: 10px !important;
    padding: 2px 6px !important;
}}


/* ── 4. MENU ITEMS — DEFAULT ─────────────────────────────── */
.standard-sidebar-item > .item-anchor {{
    color: {iTxt} !important;
    padding: {iPad} !important;
    margin: {iMar} !important;
    border-radius: {iRad}px !important;
    {font_rule}
    font-size: {iFS}px !important;
    font-weight: {FW} !important;
    letter-spacing: {iLS}px !important;
    transition: background {hTr} ease, color {hTr} ease !important;
    display: flex !important;
    align-items: center !important;
    gap: 8px !important;
    text-decoration: none !important;
    border: none !important;
    box-shadow: none !important;
}}

.body-sidebar .sidebar-item-label {{
    color: {iTxt} !important;
    font-size: {iFS}px !important;
}}

.body-sidebar .sidebar-item-icon,
.body-sidebar .sidebar-item-icon svg,
.body-sidebar .sidebar-item-icon.text-ink-gray-7,
.body-sidebar .sidebar-item-icon.text-ink-gray-7 svg {{
    color: {iIcon} !important;
    stroke: {iIcon} !important;
    display: {show_icons} !important;
    flex-shrink: 0 !important;
}}

.body-sidebar .sidebar-item-icon.text-ink-gray-7 {{
    --icon-stroke: {iIcon} !important;
}}

.body-sidebar .sidebar-item-container .drop-icon,
.body-sidebar .sidebar-item-container .collapse-indicator {{
    color: {iChev} !important;
    stroke: {iChev} !important;
}}


/* ── 5. MENU ITEMS — HOVER ───────────────────────────────── */
/* Frappe collapses the sidebar to width:50px with no extra class.
   We override --sidebar-hover-color on the expanded parent container
   and reset it to transparent when collapsed (data-sidebar=0 on body). */
body[data-sidebar="1"] .body-sidebar {{
    --sidebar-hover-color: {hBg} !important;
}}

body[data-sidebar="0"] .body-sidebar {{
    --sidebar-hover-color: transparent !important;
}}

.body-sidebar .standard-sidebar-item:not(.active-sidebar-item):has(a:not(.section-break)):hover .sidebar-item-label {{
    color: {hTxt} !important;
}}

.body-sidebar .standard-sidebar-item:not(.active-sidebar-item):has(a:not(.section-break)):hover .sidebar-item-icon,
.body-sidebar .standard-sidebar-item:not(.active-sidebar-item):has(a:not(.section-break)):hover .sidebar-item-icon svg {{
    color: {hIcon} !important;
    stroke: {hIcon} !important;
}}

.body-sidebar .standard-sidebar-item:not(.active-sidebar-item):has(a:not(.section-break)):hover .sidebar-item-icon.text-ink-gray-7 {{
    --icon-stroke: {hIcon} !important;
}}


/* ── 6. MENU ITEMS — ACTIVE ──────────────────────────────── */
/* Frappe v16 adds .active-sidebar to .standard-sidebar-item
   when the item is the current page */
.body-sidebar .standard-sidebar-item.active-sidebar > .item-anchor {{
    background: {aBg} !important;
    color: {aTxt} !important;
    font-weight: {aFW} !important;
    border-radius: {aRad}px !important;
    {active_border}
}}

.body-sidebar .standard-sidebar-item.active-sidebar .sidebar-item-label {{
    color: {aTxt} !important;
}}

.body-sidebar .standard-sidebar-item.active-sidebar .sidebar-item-icon,
.body-sidebar .standard-sidebar-item.active-sidebar .sidebar-item-icon svg {{
    color: {aIcon} !important;
    stroke: {aIcon} !important;
    display: {show_icons} !important;
}}

.body-sidebar .standard-sidebar-item.active-sidebar .sidebar-item-icon.text-ink-gray-7 {{
    --icon-stroke: {aIcon} !important;
}}


/* ── 7. NOTIFICATIONS ────────────────────────────────────── */
.body-sidebar .sidebar-item-container[item-icon="notification"] .sidebar-item-label,
.body-sidebar .sidebar-item-container[item-icon="bell"] .sidebar-item-label {{
    color: {nTxt} !important;
}}

.body-sidebar .sidebar-item-container[item-icon="notification"] .sidebar-item-icon svg,
.body-sidebar .sidebar-item-container[item-icon="bell"] .sidebar-item-icon svg {{
    color: {nIcon} !important;
    stroke: {nIcon} !important;
}}

.body-sidebar .notifications-badge,
.body-sidebar .indicator-pill,
.body-sidebar .badge,
.body-sidebar .notification-count {{
    background: {nBBg} !important;
    color: {nBTxt} !important;
}}


/* ── 8. USER SECTION (bottom) ────────────────────────────── */
.body-sidebar-bottom {{
    border-top: {bRW}px solid {bRC} !important;
}}

.body-sidebar .sidebar-user-button,
.body-sidebar .sidebar-user-button .avatar-name,
.body-sidebar .sidebar-user-button .sidebar-item-label,
.body-sidebar-bottom .nav-link {{
    color: {iTxt} !important;
}}

.body-sidebar .sidebar-user-button .avatar-frame,
.body-sidebar .sidebar-user-button .standard-image {{
    background: {libg} !important;
    color: {litc} !important;
}}

.body-sidebar .sidebar-user-button:hover {{
    background: {hBg} !important;
}}


/* ── 9. DIVIDERS ─────────────────────────────────────────── */
.body-sidebar hr,
.body-sidebar .divider {{
    border-color: {dCol} !important;
    border-width: {dW}px !important;
    display: {show_dividers} !important;
}}


/* ── 10. SCROLLBAR ───────────────────────────────────────── */
.body-sidebar::-webkit-scrollbar,
.body-sidebar-top::-webkit-scrollbar {{
    width: {scW}px !important;
}}

.body-sidebar::-webkit-scrollbar-track,
.body-sidebar-top::-webkit-scrollbar-track {{
    background: transparent !important;
}}

.body-sidebar::-webkit-scrollbar-thumb,
.body-sidebar-top::-webkit-scrollbar-thumb {{
    background: {scCol} !important;
    border-radius: {scRad}px !important;
}}

.body-sidebar::-webkit-scrollbar-thumb:hover,
.body-sidebar-top::-webkit-scrollbar-thumb:hover {{
    background: {scHov} !important;
}}

.body-sidebar,
.body-sidebar-top {{
    scrollbar-width: thin !important;
    scrollbar-color: {scCol} transparent !important;
}}


/* ── 11. PRINT ───────────────────────────────────────────── */
@media print {{
    .body-sidebar {{ display: none !important; }}
}}
"""


# ══════════════════════════════════════════════════════════
# PUBLIC WHITELISTED ENDPOINTS
# ══════════════════════════════════════════════════════════

@frappe.whitelist()
def get_active_theme_css():
    try:
        cached = frappe.cache().get_value("active_theme_css")
        if cached:
            return {"css": cached}

        css_parts = []

        pts = frappe.get_single("Portal Theme Setting")
        if pts.enable:
            css_parts.append(_build_portal_theme_css(pts))

        st = frappe.get_single("Sidebar Theme")
        if st.enable_sidebar_theme:
            css_parts.append(_build_sidebar_css(st))

        final_css = "\n".join(css_parts)
        frappe.cache().set_value("active_theme_css", final_css)

        return {"css": final_css}

    except Exception:
        frappe.log_error(frappe.get_traceback(), "Theme CSS Error")
        return {"css": ""}


def clear_theme_cache(doc=None, method=None):
    frappe.cache().delete_value("active_theme_css")


@frappe.whitelist()
def get_sidebar_theme():
    """Returns Sidebar Theme settings as dict."""
    try:
        return frappe.get_single("Sidebar Theme").as_dict()
    except Exception:
        return {}


@frappe.whitelist()
def get_sidebar_item_theme():
    """Returns Sidebar Item Theme settings as dict."""
    try:
        return frappe.get_single("Sidebar Item Theme").as_dict()
    except Exception:
        return {}


@frappe.whitelist()
def get_portal_sidebar_theme():
    """Returns Portal Sidebar Theme settings as dict."""
    try:
        return frappe.get_single("Portal Sidebar Theme").as_dict()
    except Exception:
        return {}