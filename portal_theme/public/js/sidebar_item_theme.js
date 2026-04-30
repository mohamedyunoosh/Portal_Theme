frappe.after_ajax(function() {
    frappe.call({
        method: 'portal_theme.api.get_sidebar_item_theme',
        callback: function(r) {
            $("#custom-sidebar-item-theme").remove();

            if (r.message && r.message.enable_item_theme) {
                let theme = r.message;
                let css = `
                    .standard-sidebar-item.active-sidebar,
                    .standard-sidebar-item.active-sidebar-item > .item-anchor,
                    .standard-sidebar-item > .item-anchor.active {
                        background-color: ${theme.active_bg_color || '#080e24'} !important;
                        color: ${theme.active_text_color || '#ffffff'} !important;
                        font-weight: ${theme.active_font_weight || '600'} !important;
                        border-radius: ${theme.active_border_radius || 8}px !important;
                        border-left: ${theme.active_left_border_width !== undefined ? theme.active_left_border_width : 2}px solid ${theme.active_left_border_color || '#4463F0'} !important;
                    }
                    .standard-sidebar-item.active-sidebar svg,
                    .standard-sidebar-item.active-sidebar-item > .item-anchor svg,
                    .standard-sidebar-item > .item-anchor.active svg {
                        fill: ${theme.active_icon_color || '#ffffff'} !important;
                        stroke: ${theme.active_icon_color || '#ffffff'} !important;
                    }
                    .standard-sidebar-item.active-sidebar .icon use,
                    .standard-sidebar-item.active-sidebar-item > .item-anchor .icon use,
                    .standard-sidebar-item > .item-anchor.active .icon use {
                        stroke: ${theme.active_icon_color || '#ffffff'} !important;
                    }

                    .standard-sidebar-item:hover,
                    .standard-sidebar-item > .item-anchor:hover {
                        background-color: ${theme.hover_bg_color || '#101e4b'} !important;
                        color: ${theme.hover_text_color || '#9ba1b9'} !important;
                        transition: all ${theme.hover_transition || '0.2s'} ease-in-out !important;
                    }
                    .standard-sidebar-item:hover svg,
                    .standard-sidebar-item > .item-anchor:hover svg {
                        fill: ${theme.hover_icon_color || '#9ba1b9'} !important;
                        stroke: ${theme.hover_icon_color || '#9ba1b9'} !important;
                        transition: all ${theme.hover_transition || '0.2s'} ease-in-out !important;
                    }
                    .standard-sidebar-item:hover .icon use,
                    .standard-sidebar-item > .item-anchor:hover .icon use {
                        stroke: ${theme.hover_icon_color || '#9ba1b9'} !important;
                        transition: all ${theme.hover_transition || '0.2s'} ease-in-out !important;
                    }

                    /* SEARCH BAR STYLING */
                    .body-sidebar .standard-sidebar-item[data-item-name="Search"] > .item-anchor,
                    .body-sidebar .standard-sidebar-item[data-label="Search"] > .item-anchor,
                    .body-sidebar .standard-sidebar-item[item-name="Search"] > .item-anchor,
                    .body-sidebar .sidebar-item-container[data-label="Search"] .item-anchor,
                    .body-sidebar .sidebar-item-container[item-name="Search"] .item-anchor,
                    .body-sidebar .sidebar-item-container[item-icon="search"] .item-anchor,
                    .body-sidebar .sidebar-search,
                    .body-sidebar .search-bar,
                    .body-sidebar [class*="search"] input {
                        background-color: ${theme.search_bg_color || '#191f35'} !important;
                        box-shadow: ${theme.search_box_shadow || '0 0 10px rgba(76, 110, 245, 0.2)'} !important;
                        transition: all 0.3s ease !important;
                    }

                    .body-sidebar .standard-sidebar-item[data-item-name="Search"] > .item-anchor:hover,
                    .body-sidebar .standard-sidebar-item[data-label="Search"] > .item-anchor:hover,
                    .body-sidebar .standard-sidebar-item[item-name="Search"] > .item-anchor:hover,
                    .body-sidebar .sidebar-item-container[data-label="Search"] .item-anchor:hover,
                    .body-sidebar .sidebar-item-container[item-name="Search"] .item-anchor:hover,
                    .body-sidebar .sidebar-item-container[item-icon="search"] .item-anchor:hover,
                    .body-sidebar .sidebar-search:hover,
                    .body-sidebar .sidebar-search:focus-within,
                    .body-sidebar [class*="search"] input:focus,
                    .body-sidebar [class*="search"] input:hover {
                        box-shadow: ${theme.search_hover_box_shadow || '0 4px 15px rgba(0, 0, 0, 0.4)'} !important;
                    }
                `;
                
                $('<style id="custom-sidebar-item-theme">').text(css).appendTo("head");
            }
        }
    });
});
