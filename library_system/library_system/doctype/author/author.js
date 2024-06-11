// Copyright (c) 2024, Farthy and contributors
// For license information, please see license.txt

frappe.ui.form.on("Author", {

    validate: function(frm) {
        if (frm.doc.first_name && frm.doc.last_name) {
            frm.set_value('full_name', frm.doc.first_name + ' ' + frm.doc.last_name);
        }
    }
});
