// Copyright (c) 2024, Farthy and contributors
// For license information, please see license.txt
frappe.ui.form.on('Book Issue', {
    refresh: function(frm) {
        frm.add_custom_button(__('Show Available Book Issues'), function() {
            frappe.call({
                method: 'library_system.services.rest.get_available_book',
                callback: function(r) {
                    if (r.message) {
                        let issues = r.message;
                        let issue_list = issues.map(issue => `${issue.book_name}: ${issue.member}`).join('<br>');
                        frappe.msgprint({
                            title: __('Available Book Issues'),
                            message: issue_list,
                            indicator: 'green'
                        });
                    } else {
                        frappe.msgprint(__('No available book issues found.'));
                    }
                }
            });
        }, __("Actions"));

        frappe.call({
            method: 'library_system.services.rest.blacklist_user_method',
            args:{
                member: frm.doc.member,
                book_issue_name: frm.doc.book_name
            },
            callback: function(r){
                if(r.message){
                    frappe.msgprint(r.message);
                }
            }
        })
    }
});

