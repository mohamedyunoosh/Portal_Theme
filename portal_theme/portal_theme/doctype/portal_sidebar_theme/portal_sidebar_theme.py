# Copyright (c) 2024, Sudhanshu Badole and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class PortalSidebarTheme(Document):
	def on_update(self):
		frappe.clear_cache()
