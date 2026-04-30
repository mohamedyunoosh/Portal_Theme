import frappe

@frappe.whitelist()
def get_active_theme_css():
    """
    Returns CSS of the currently active Portal Theme
    """
    theme = frappe.get_value(
        "Portal Theme",
        filters={"is_active": 1},
        fieldname="css_content"
    )

    return {
        "css": theme or ""
    }


@frappe.whitelist()
def get_sidebar_theme():
    """
    Returns all Sidebar Theme settings as a dict.
    Used by sidebar_theme.js to dynamically apply CSS.
    """
    try:
        doc = frappe.get_single("Sidebar Theme")
        return doc.as_dict()
    except Exception:
        return {}


@frappe.whitelist()
def get_sidebar_item_theme():
    """
    Returns all Sidebar Item Theme settings as a dict.
    Used by sidebar_item_theme.js to dynamically apply CSS.
    """
    try:
        doc = frappe.get_single("Sidebar Item Theme")
        return doc.as_dict()
    except Exception:
        return {}
