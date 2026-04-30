// Copyright (c) 2026, Sudhanshu Badole and contributors
// For license information, please see license.txt

frappe.ui.form.on("Sidebar Theme", {
	after_save: function (frm) {
		frappe.show_alert({
			message: __("Sidebar theme saved. Reloading..."),
			indicator: "green",
		});
		setTimeout(() => {
			window.location.reload();
		}, 500);
	},

	enable_sidebar_theme: function (frm) {
		if (!frm.doc.enable_sidebar_theme) {
			frappe.show_alert({
				message: __("Sidebar theme will be disabled on save."),
				indicator: "orange",
			});
		}
	},
});
