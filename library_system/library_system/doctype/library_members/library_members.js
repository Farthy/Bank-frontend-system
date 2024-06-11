// Copyright (c) 2024, Farthy and contributors
// For license information, please see license.txt

frappe.ui.form.on("Library Members", {
	refresh(frm) {
        frm.add_custom_button(__('Order a Book'), function() {
            if (frm.doc.email) {
                frappe.call({
                    method: 'library_system.library_system.doctype.library_members.library_members.get_book',
                    args: {
                        email: frm.doc.email
                    },
                    callback: function(r) {
                        if (r.message) {
                            frappe.msgprint(r.message);
                        }
                    }
                });
            } else {
                frappe.msgprint(__('Please provide an email address.'));
            }
        }, __("Utilities"));

	},
    validate: function(frm) {
        if (frm.doc.first_name && frm.doc.last_name) {
            frm.set_value('full_name', frm.doc.first_name + ' ' + frm.doc.last_name);
        }
    }
});
