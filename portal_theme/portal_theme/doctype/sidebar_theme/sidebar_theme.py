# Copyright (c) 2026, Sudhanshu Badole and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class SidebarTheme(Document):

	def validate(self):
		"""Validate sidebar theme settings"""
		if self.sidebar_width and self.sidebar_width < 150:
			frappe.throw("Sidebar width cannot be less than 150px")
		if self.sidebar_width and self.sidebar_width > 400:
			frappe.throw("Sidebar width cannot be more than 400px")
		if self.sidebar_font_size and self.sidebar_font_size < 8:
			frappe.throw("Font size cannot be less than 8px")
		if self.sidebar_font_size and self.sidebar_font_size > 24:
			frappe.throw("Font size cannot be more than 24px")
