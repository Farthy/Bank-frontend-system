// Copyright (c) 2024, Farthy and contributors
// For license information, please see license.txt

frappe.ui.form.on("LIbrary Member", {

    before_save: function(frm){
        frappe.call({
            method: "library_system.services.rest.concatenate_fullname",
            args: {
                member: frm.doc.name
            },
            callback: function(response) {
                frm.reload_doc();
            }
        })

    },
    refresh: function(frm) {
        toggle_fields(frm);
    },
    penalty: function(frm) {
        toggle_fields(frm);
    },
    blacklisted: function(frm) {
        toggle_fields(frm);
    }
	
});

function toggle_fields(frm) {
    if (frm.doc.blacklisted) {
        frm.set_df_property('penalty', 'hidden', 0);
        frm.set_df_property('blacklisted', 'hidden', 0);
    } else if (frm.doc.penalty) {
        frm.set_df_property('penalty', 'hidden', 0);
        frm.set_df_property('blacklisted', 'hidden', 1);
    } else {
        frm.set_df_property('penalty', 'hidden', 1);
        frm.set_df_property('blacklisted', 'hidden', 1); 
    }
}
