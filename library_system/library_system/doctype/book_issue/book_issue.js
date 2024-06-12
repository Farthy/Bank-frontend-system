frappe.ui.form.on('Book Issue', {
    refresh: function(frm) {
        if (frm.doc.extended) {
            frm.add_custom_button('Apply Penalty and Blacklist', () => {
                frappe.call({
                    method: "library_system.library_system.doctype.book_issue.book_issue.apply_penalty_and_blacklist",
                    callback: function() {
                        frm.reload_doc();
                    }
                });
            });
        }
    },
    onload: function(frm) {
        frappe.call({
            method: "library_system.library_system.doctype.book_issue.book_issue.fetch_book_issue_data",
            args: { docname: frm.doc.name },
            callback: function(response) {
                var data = response.message;
                if (data && data.return_date) {
                    if (frappe.datetime.str_to_obj(data.return_date) < frappe.datetime.now_datetime()) {
                        frm.toggle_enable('extended', true);
                    } else {
                        frm.toggle_enable('extended', false);
                    }
                }
            }
        }); 
    }
});
