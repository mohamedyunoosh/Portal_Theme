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

    # ── CSS Variables (:root) ──────────────────────────────
    parts = [google_import] if google_import else []
    parts.append(":root {")
    parts.append(f"  --navbar-bg: {v(s.navbar_color)};")
    parts.append(f"  --navbar-text: {v(s.navbar_text_color)};")
    parts.append(f"  --btn-primary-bg: {v(s.primary_button_background)};")
    parts.append(f"  --btn-primary-text: {v(s.primary_button_text)};")
    parts.append(f"  --btn-primary-hover-bg: {v(s.primary_button_hover_background)};")
    parts.append(f"  --btn-default-hover-bg: {v(s.primary_button_hover_background)};")
    parts.append(f"  --btn-secondary-bg: {v(s.secondary_button_background)};")
    parts.append(f"  --btn-secondary-text: {v(s.secondary_button_text)};")
    parts.append(f"  --card-bg: {v(s.card_background_color)};")
    parts.append(f"  --card-text: {v(s.card_text_color)};")
    parts.append(f"  --form-bg: {v(s.form_background_color)};")
    parts.append(f"  --gray-50: {v(s.form_background_color)};")
    parts.append(f"  --form-text: {v(s.form_text_color)};")
    parts.append(f"  --text-light: {v(s.card_header_color)};")
    parts.append(f"  --text-neutral: {v(s.header_hover_color)};")
    parts.append(f"  --portal-bg: {v(s.portal_background_color)};")
    parts.append(f"  --form-bg: {v(s.portal_background_color)};")
    parts.append(f"  --section-heading: {v(s.section_heading_color)};")
    parts.append(f"  --body-font: {font_stack};")
    parts.append(f"  --home-icon-text: {v(s.home_page_icon_text)};")
    parts.append(f"  --bg-color: {v(s.card_background_color)};")

    # ── Form View Field variables ──────────────────────────
    parts.append(f"  --field-label-color: {v(s.field_label_color)};")
    parts.append(f"  --field-border-color: {v(s.field_border_color)};")
    parts.append(f"  --red-400: {v(s.required_asterisk_color)};")
    parts.append(f"  --field-border-radius: {s.field_border_radius or 4}px;")
    parts.append(f"  --field-label-size: {s.label_font_size or 13}px;")
    parts.append(f"  --border-color: {v(s.borders)};")
    parts.append(f"  --subtle-accent: {v(s.borders)};")
    parts.append(f"  --fg-color: {v(s.portal_background_color)};")

    # ── Form View Right Sidebar variables ─────────────────
    parts.append(f"  --form-sidebar-bg: {v(s.sidebar_background)};")
    parts.append(f"  --form-sidebar-heading: {v(s.sidebar_heading_color)};")
    parts.append(f"  --form-sidebar-label: {v(s.sidebar_label_color)};")
    parts.append(f"  --form-sidebar-icon: {v(s.sidebar_icon_color)};")
    parts.append(f"  --form-sidebar-border: {v(s.sidebar_border_color)};")

    # ── List View variables ────────────────────────────────
    parts.append(f"  --list-header-bg: {v(s.header_row_background)};")
    parts.append(f"  --list-header-text: {v(s.header_text_color)};")
    parts.append(f"  --icon-stroke: {v(s.header_text_color)};")
    parts.append(f"  --list-row-bg: {v(s.row_background)};")
    parts.append(f"  --highlight-color: {v(s.row_hover_color)};")
    parts.append(f"  --list-row-alt-bg: {v(s.alternate_row_background)};")
    parts.append(f"  --list-row-text: {v(s.row_text_color)};")
    parts.append(f"  --list-row-hover-bg: {v(s.row_hover_color)};")
    parts.append(f"  --list-row-border: {v(s.row_border_color)};")
    parts.append(f"  --list-filter-bg: {v(s.filter_color)};")
    parts.append(f"  --control-bg: {v(s.filter_color)};")
    parts.append(f"  --list-filter-text: {v(s.filter_text_color)};")
    parts.append(f"  --text-color: {v(s.filter_text_color)};")
    parts.append(f"  --list-filter-btn-bg: {v(s.filter_button_color)};")
    parts.append(f"  --list-filter-btn-text: {v(s.filter_button_text_color)};")
    parts.append(f"  --modal-bg: {v(s.dialogue_boxes)};")

    parts.append("}")

    # ── Background image / color / slider ─────────────────
    bg_css = ""
    if s.apply_on_login_page:
        mode = s.apply_image_or_color or "Color"
        opacity = s.background_opacity or 1.0

        if mode == "Image" and s.background_image:
            bg_css = f"""
/* Login Page — Single Background Image */
.login-content.page-card,
body.login-page {{
    background-image: url('{s.background_image}') !important;
    background-size: cover !important;
    background-position: center !important;
    background-repeat: no-repeat !important;
    opacity: {opacity} !important;
}}"""
        elif mode == "Color" and s.background_color:
            bg_css = f"""
/* Login Page — Background Color */
.login-content.page-card,
body.login-page {{
    background-color: {s.background_color} !important;
    opacity: {opacity} !important;
}}"""

    parts.append(bg_css)

    # ── Portal background ──────────────────────────────────
    has_global_image = bool(getattr(s, "global_background_image", None))
    if has_global_image:
        portal_bg_css = "/* portal-bg skipped: global background image is active */"
    else:
        portal_bg_css = "html, body, .page-container { background-color: var(--portal-bg) !important; }"

    # ── Global background image ────────────────────────────
    global_bg_css = ""
    if getattr(s, "global_background_image", None):
        opacity = getattr(s, "global_background_opacity", None) or 1.0
        global_bg_css = f"""
/* ── Global Background Image ─────────────────────────────── */
body::before {{
    content: '' !important;
    position: fixed !important;
    top: 0 !important;
    left: 0 !important;
    width: 100vw !important;
    height: 100vh !important;
    background-image: url('{s.global_background_image}') !important;
    background-size: cover !important;
    background-position: center center !important;
    background-repeat: no-repeat !important;
    background-attachment: fixed !important;
    opacity: {opacity} !important;
    z-index: -9999 !important;
    pointer-events: none !important;
}}

html, body,
.page-container {{
    background: transparent !important;
    background-color: transparent !important;
}}"""

    # ── Font ───────────────────────────────────────────────
    font_css = ""
    if s.body_font and font_stack and font_stack != "inherit":
        font_css = f"""
/* Global Font */
html, body, input, button, select, textarea,
.form-control, .btn, .navbar, .card,
.frappe-list, .page-container {{
    font-family: {font_stack} !important;
}}"""

    parts.append(font_css)

    parts.append(f"""
/* ── Portal Background ───────────────────────────────────── */
{portal_bg_css}

{global_bg_css}

/* ── Navbar ──────────────────────────────────────────────── */
.navbar  {{
    background-color: var(--navbar-bg) !important;
    color: var(--navbar-text) !important;
}}

.page-head .page-head-content {{
    background-color: var(--navbar-bg) !important;
}}
.navbar a, .navbar .nav-link {{
    color: var(--navbar-text) !important;
}}

/* ── Home Icon Text ───────────────────────────────────────── */
.desktop-icon .icon-caption .icon-title,
.icons-container .desktop-icon .icon-title {{
    color: var(--home-icon-text) !important;
}}

/* ── Primary Button ──────────────────────────────────────── */
.btn.btn-primary {{
    background-color: var(--btn-primary-bg) !important;
    color: var(--btn-primary-text) !important;
}}
.btn.btn-primary:hover {{
    background-color: var(--btn-primary-hover-bg) !important;
}}

/* ── Secondary Button ────────────────────────────────────── */
.btn.btn-secondary {{
    background-color: var(--btn-secondary-bg) !important;
    color: var(--btn-secondary-text) !important;
}}

/* ── Cards ───────────────────────────────────────────────── */
.card, .card .card-body {{
    background-color: var(--card-bg) !important;
    color: var(--card-text) !important;
}}
.card-header {{
    background-color: var(--card-header-bg) !important;
}}

/* ── Forms (legacy) ──────────────────────────────────────── */
.form-control {{
    background-color: var(--form-bg) !important;
    color: var(--form-text) !important;
}}

/* ── Headings ────────────────────────────────────────────── */
h1, h2, h3, h4, h5, h6, .section-head {{
    color: var(--section-heading) !important;
}}

/* ══════════════════════════════════════════════════════════
   FORM VIEW — FIELD LABELS & INPUTS
   ══════════════════════════════════════════════════════════ */

/* Field label */
.form-layout .frappe-control .control-label,
.form-layout .frappe-control label,
.form-section .frappe-control .control-label,
.form-section .frappe-control label {{
    color: var(--field-label-color) !important;
    font-size: var(--field-label-size) !important;
}}




/* Required asterisk */
.form-layout .frappe-control .reqd-star,
.form-layout .frappe-control .control-label .reqd,
.form-section .frappe-control .reqd-star {{
    color: var(--field-required-color) !important;
}}

/* Field input background, text, border */
.form-layout .frappe-control input:not([type="submit"]):not([type="button"]):not([type="checkbox"]):not([type="radio"]),
.form-layout .frappe-control textarea,
.form-layout .frappe-control select,
.form-layout .frappe-control .input-with-feedback,
.form-layout .frappe-control .form-control,
.form-section .frappe-control .form-control {{
    background-color: var(--form-bg) !important;
    color: var(--form-text) !important;
    border-color: var(--field-border-color) !important;
    border-radius: var(--field-border-radius) !important;
}}

/* Read-only / disabled fields */
.form-layout .frappe-control .form-control[disabled],
.form-layout .frappe-control .form-control[readonly] {{
    background-color: var(--form-bg) !important;
    opacity: 0.7;
}}

/* ══════════════════════════════════════════════════════════
   FORM VIEW — RIGHT SIDEBAR
   Selectors verified from DevTools inspection
   ══════════════════════════════════════════════════════════ */

/* ── Sidebar container background ───────────────────────── */
.layout-side-section,
.layout-side-section .form-sidebar {{
    background-color: var(--form-sidebar-bg) !important;
}}



/* Dropdown item — default state: NO background, just text color */
.sort-selector .dropdown-menu li > a,
.sort-selector .dropdown-menu li > span,
.sort-selector .dropdown-menu a {{
    color: var(--list-header-text) !important;
    display: block !important;
}}

.dropdown-menu {{
background-color: var(--list-header-bg) !important;
}}

.form-links .document-link {{
    background-color: var(--form-sidebar-bg) !important;
}}


/* Item hover — only highlight on mouse over */
.sort-selector .dropdown-menu li > a:hover,
.sort-selector .dropdown-menu a:hover {{
    background-color: var(--list-row-hover-bg) !important;
    color: var(--list-header-text) !important;
}}

/* Active selected item */
.sort-selector .dropdown-menu li.active > a,
.sort-selector .dropdown-menu li.active > span {{
    background-color: var(--list-row-hover-bg) !important;
    color: var(--list-header-text) !important;
    font-weight: 600 !important;
}}



/* ── "Test Task" title ───────────────────────────────────── */
/* DevTools: span.bold.ellipsis.form-title-text.mr-3.text-medium */
.layout-side-section .form-sidebar .form-title-text {{
    color: var(--form-sidebar-heading) !important;
}}

/* ── "TASK-2026-00009" doc ID ────────────────────────────── */
/* DevTools: span.ellipsis.mr-3 inside div.form-name-container */
.layout-side-section .form-sidebar .form-name-container .ellipsis {{
    color: var(--form-sidebar-label) !important;
}}

/* ── Assign / Attachments / Tags / Share labels ──────────── */
/* DevTools: span.add-assignment-label.form-sidebar-label
             span.ellipsis inside span.form-sidebar-items      */
.layout-side-section .form-sidebar .form-sidebar-label,
.layout-side-section .form-sidebar .add-assignment-label,
.layout-side-section .form-sidebar .form-sidebar-items .ellipsis {{
    color: var(--form-sidebar-heading) !important;
}}

/* ── "Last Edited by You" / "Created By You" text ───────── */
/* DevTools: li.modified-by and li.created-by — text is a
   direct text node inside the <li>, not a child element     */
.layout-side-section .form-sidebar .sidebar-section.text-muted li.modified-by,
.layout-side-section .form-sidebar .sidebar-section.text-muted li.created-by {{
    color: var(--form-sidebar-heading) !important;
}}

/* ── "1 month ago" timestamps ────────────────────────────── */
/* DevTools: span.frappe-timestamp inside li.modified-by / li.created-by */
.layout-side-section .form-sidebar .sidebar-section.text-muted .frappe-timestamp {{
    color: var(--form-sidebar-label) !important;
}}

/* ── Header icons: edit, print, heart (top-right of sidebar) */
/* DevTools: div.form-title-text, div.form-print,
             span.liked-by.like-action inside
             div.align-items-baseline.flex.form-stats-likes   */
.layout-side-section .form-sidebar .form-stats-likes svg,
.layout-side-section .form-sidebar .form-stats-likes .icon,
.layout-side-section .form-sidebar .form-title-text svg,
.layout-side-section .form-sidebar .form-title-text .icon,
.layout-side-section .form-sidebar .form-print svg,
.layout-side-section .form-sidebar .form-print .icon,
.layout-side-section .form-sidebar .liked-by svg,
.layout-side-section .form-sidebar .like-action svg {{
    stroke: var(--form-sidebar-icon) !important;
    color: var(--form-sidebar-icon) !important;
}}

/* ── Icons: svg inside sidebar-section rows ─────────────── */
/* DevTools: svg.icon.icon-sm inside span.form-sidebar-items */
.layout-side-section .form-sidebar .form-sidebar-items svg,
.layout-side-section .form-sidebar .form-sidebar-items .icon {{
    stroke: var(--form-sidebar-icon) !important;
    color: var(--form-sidebar-icon) !important;
}}

/* ── + add buttons ───────────────────────────────────────── */
/* DevTools: button.add-assignment-btn.btn.btn-link.icon-btn  */
.layout-side-section .form-sidebar .add-assignment-btn,
.layout-side-section .form-sidebar .icon-btn {{
    color: var(--form-sidebar-icon) !important;
}}
.layout-side-section .form-sidebar .add-assignment-btn svg,
.layout-side-section .form-sidebar .icon-btn svg {{
    stroke: var(--form-sidebar-icon) !important;
}}

/* ── Fix: last section has no bottom border (Frappe default) */
.layout-side-section .sidebar-section:last-child {{
    border-bottom: none !important;
}}

/* ── Fix: remove stray border/line before "Last Edited" ─── */
/* DevTools: div.sidebar-section.text-muted.pt-3             */
.layout-side-section .form-sidebar .sidebar-section.text-muted {{
    border-top: none !important;
    border-left: none !important;
}}

/* ══════════════════════════════════════════════════════════
   LIST VIEW
   ══════════════════════════════════════════════════════════ */

/* Header row */
.frappe-list .list-row-head,
.list-row-head,
.list-row-head .level-right,
.frappe-list .list-row-head .level-right,
.result-no-assign-to .list-row-head .level-right {{
    background-color: var(--list-header-bg) !important;
}}

.frappe-list .list-row-head .list-row-col,
.frappe-list .list-row-head .list-row-col span,
.list-row-head .list-header-subject,
.list-row-head .list-row-col {{
    color: var(--list-header-text) !important;
}}

/* Filter inputs: text, link/awesomplete, select */
.standard-filter-section .input-with-feedback,
.standard-filter-section .form-control,
.standard-filter-section input,
.standard-filter-section .ellipsis,
.standard-filter-section .awesomplete input,
.standard-filter-section .awesomplete .input-with-feedback {{
    background-color: var(--list-filter-bg) !important;
    color: var(--list-filter-text) !important;
    border-color: var(--list-filter-bg) !important;
    box-shadow: none !important;
}}

.standard-filter-section input::placeholder,
.standard-filter-section .awesomplete input::placeholder {{
    color: var(--list-filter-text) !important;
    opacity: 0.6 !important;
}}

.standard-filter-section select,
.standard-filter-section .frappe-control select {{
    background-color: var(--list-filter-bg) !important;
    color: var(--list-filter-text) !important;
    border-color: var(--list-filter-bg) !important;
}}

/* Filter buttons: div.filter-section.flex > div.filter-selector */
.page-form .filter-section .filter-button,
.page-form .filter-section .filter-x-button,
.page-form .filter-selector .filter-button,
.page-form .filter-selector .filter-x-button,
.filter-section .filter-button,
.filter-section .filter-x-button,
.filter-section .filter-selector .btn,
.filter-section .sort-selector .btn,
.page-form .filter-section .filter-selector .btn,
.page-form .filter-section .sort-selector .btn {{
    background-color: var(--list-filter-btn-bg) !important;
    color: var(--list-filter-btn-text) !important;
    border-color: var(--list-filter-btn-bg) !important;
}}



/* Alternating rows */
.frappe-list .list-row:nth-child(even),
.list-row:nth-child(even),
.frappe-list .list-row:nth-child(even) .level-right,
.list-row:nth-child(even) .level-right {{
    background-color: var(--list-row-alt-bg) !important;
}}

/* Row text */
.frappe-list .list-row .list-row-col,
.frappe-list .list-row .list-row-col a,
.frappe-list .list-row .list-row-col span,
.list-row .list-row-col {{
    color: var(--list-row-text) !important;
}}

/* Row hover */
.frappe-list .list-row:hover,
.list-row:hover {{
    background-color: var(--list-row-hover-bg) !important;
}}

/* Row border */
.frappe-list .list-row,
.list-row {{
    border-color: var(--list-row-border) !important;
}}
""")

    return "\n".join(parts)


# ══════════════════════════════════════════════════════════
# SIDEBAR CSS BUILDER (unchanged)
# ══════════════════════════════════════════════════════════

def _build_sidebar_css(s):
    def c(val, fallback):
        return val if val else fallback

    stack, import_url = _resolve_font(s.sidebar_font_family)
    google_import = f'@import url("{import_url}");' if import_url else ""
    font_rule = f"font-family: {stack} !important;" if s.sidebar_font_family and stack and stack != "inherit" else ""

    if s.use_gradient:
        bg = (
            f"linear-gradient({c(s.bg_gradient_direction, 'to bottom')}, "
            f"{c(s.bg_gradient_start, '#0a0e2a')}, "
            f"{c(s.bg_gradient_end, '#141a3a')})"
        )
    else:
        bg = c(s.bg_color, "#0a0e2a")

    active_border = (
        f"border-left: {s.active_left_border_width}px solid "
        f"{c(s.active_left_border_color, '#4c6ef5')} !important;"
        if s.active_left_border_width
        else "border-left: none !important;"
    )

    show_icons    = "inline-flex" if s.show_item_icons       else "none"
    show_chevron  = "inline-flex" if s.show_dropdown_chevron else "none"
    show_dividers = "block"       if s.show_dividers         else "none"

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
    sBadgeRad = s.search_border_radius or 4
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
   ══════════════════════════════════════════════════════════ */

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

.body-sidebar .sidebar-items,
.body-sidebar .standard-items-sections,
.body-sidebar .sidebar-item-container {{
    gap: 0 !important;
    padding: 0 !important;
}}

.sidebar-header,
a.sidebar-header-hover {{
    background: {lbg} !important;
    padding: {lpad} !important;
}}

.sidebar-header .sidebar-item-icon .icon-container,
.body-sidebar .sidebar-item-icon .icon-container,
.body-sidebar .header-logo .icon-container,
.sidebar-header .icon-container[style],
.body-sidebar .icon-container[style] {{
    background-color: {libg} !important;
    color: {litc} !important;
    border-radius: {lir}px !important;
}}

.sidebar-header .icon-container svg,
.sidebar-header .icon-container svg use,
.body-sidebar .icon-container svg,
.body-sidebar .icon-container svg use {{
    color: {litc} !important;
    fill: {litc} !important;
    stroke: {litc} !important;
}}

.body-sidebar {{
    --sidebar-item-icon-bg: {libg} !important;
}}
.body-sidebar .body-sidebar-bottom,
.text-secondary {{
    --text-color: {iTxt} !important;
}}

.sidebar-header .header-title,
.sidebar-header .sidebar-item-label.header-title {{
    color: {ltc} !important;
    font-size: {lts}px !important;
    font-weight: 700 !important;
    overflow: hidden !important;
    text-overflow: ellipsis !important;
    white-space: nowrap !important;
}}

.sidebar-header .header-subtitle,
.sidebar-header .sidebar-item-label.header-subtitle {{
    color: {lsc} !important;
    font-size: {lss}px !important;
    font-weight: 400 !important;
}}

.sidebar-header .drop-icon,
.sidebar-header .drop-icon svg,
.sidebar-header .btn-reset.drop-icon .icon.icon-sm,
.sidebar-header .btn-reset.drop-icon .icon.icon-sm svg {{
    color: {chev} !important;
    stroke: {chev} !important;
    display: {show_chevron} !important;
}}

.body-sidebar .sidebar-item-suffix.keyboard-shortcut {{
    background: {ssBg} !important;
    color: {ssTxt} !important;
    border-radius: {sBadgeRad}px !important;
    font-size: 10px !important;
    padding: 2px 6px !important;
}}

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

.body-sidebar .sidebar-item-container .standard-sidebar-item.active-sidebar > .item-anchor,
.body-sidebar .standard-sidebar-item.active-sidebar > .item-anchor,
.body-sidebar .standard-sidebar-item.active-sidebar > a.item-anchor,
.body-sidebar .sidebar-item-container .active-sidebar > .item-anchor {{
    background: {aBg} !important;
    color: {aTxt} !important;
    font-weight: {aFW} !important;
    border-radius: {aRad}px !important;
    {active_border}
    box-shadow: none !important;
}}

/* Force Frappe's --sidebar-hover-color to not override active bg */
.body-sidebar .standard-sidebar-item.active-sidebar > .item-anchor:hover {{
    background: {aBg} !important;
}}

.body-sidebar {{
    --sidebar-active-color: {aBg}!important;
}}

/* Remove Frappe default active item white border/shadow */
.body-sidebar .standard-sidebar-item.active-sidebar > .item-anchor,
.body-sidebar .active-sidebar > .item-anchor {{
    outline: none !important;
    box-shadow: none !important;
    border: none !important;
}}

.body-sidebar .sidebar-item-container .standard-sidebar-item.active-sidebar .sidebar-item-label,
.body-sidebar .standard-sidebar-item.active-sidebar .sidebar-item-label {{
    color: {aTxt} !important;
}}

.body-sidebar .sidebar-item-container .standard-sidebar-item.active-sidebar .sidebar-item-icon,
.body-sidebar .sidebar-item-container .standard-sidebar-item.active-sidebar .sidebar-item-icon svg,
.body-sidebar .standard-sidebar-item.active-sidebar .sidebar-item-icon,
.body-sidebar .standard-sidebar-item.active-sidebar .sidebar-item-icon svg {{
    color: {aIcon} !important;
    stroke: {aIcon} !important;
    display: {show_icons} !important;
}}

.body-sidebar .standard-sidebar-item.active-sidebar .sidebar-item-icon.text-ink-gray-7 {{
    --icon-stroke: {aIcon} !important;
}}

.body-sidebar hr,
.body-sidebar .divider {{
    border-color: {dCol} !important;
    border-width: {dW}px !important;
    display: {show_dividers} !important;
}}

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

        pts_name = frappe.db.get_value("Portal Theme Settings", {"enable": 1}, "name")
        if pts_name:
            pts = frappe.get_doc("Portal Theme Settings", pts_name)
            css_parts.append(_build_portal_theme_css(pts))

        st_name = frappe.db.get_value("Sidebar Settings", {"enable_sidebar_theme": 1}, "name")
        if st_name:
            st = frappe.get_doc("Sidebar Settings", st_name)
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
def get_login_background():
    """Returns login page background config for JS slider."""
    try:
        pts_name = frappe.db.get_value("Portal Theme Settings", {"enable": 1}, "name")
        if not pts_name:
            return {}
        pts = frappe.get_doc("Portal Theme Settings", pts_name)
        if not pts.apply_on_login_page:
            return {}

        mode = pts.apply_image_or_color or "Color"
        result = {
            "mode": mode,
            "opacity": pts.background_opacity or 1.0,
            "transition": pts.transition or 1.0,
            "interval": pts.interval or 5.0,
        }

        if mode == "Image":
            result["image"] = pts.background_image or ""
        elif mode == "Color":
            result["color"] = pts.background_color or ""
        elif mode == "Slider":
            result["images"] = [row.image for row in pts.background_images if row.image]

        return result
    except Exception:
        frappe.log_error(frappe.get_traceback(), "Login Background Error")
        return {}


@frappe.whitelist()
def get_sidebar_theme():
    """Returns Sidebar Settings settings as dict."""
    try:
        st_name = frappe.db.get_value("Sidebar Settings", {"enable_sidebar_theme": 1}, "name")
        if not st_name:
            return {}
        return frappe.get_doc("Sidebar Settings", st_name).as_dict()
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