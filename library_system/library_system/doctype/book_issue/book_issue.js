frappe.ui.form.on('Book Issue', {
    refresh: function(frm) {
        frm.clear_custom_buttons();
    
        if (frm.doc.extended) {
            frm.add_custom_button('Apply Penalty and Blacklist', () => {
                frappe.call({
                    method: "library_system.services.rest.apply_penalty_and_blacklist",
                    args: {
                        docname: frm.doc.name
                    },
                    callback: function(response) {
                        if (response.message === 1) {
                            frm.clear_custom_buttons();
                            frm.add_custom_button('Unblacklist Member', () => {
                                frappe.call({
                                    method: "library_system.services.rest.unblacklist",
                                    args: {
                                        docname: frm.doc.name
                                    }
                                });
                            });
                        }
                    }
                });
            });
        }
    
        // Call to load available books
        frappe.call({
            method: "library_system.services.rest.available_books",
            callback: function(response) {
                var available_books = response.message;
                console.log("Available books", available_books);
                if (available_books && available_books.length > 0) {
                    var options = available_books.map(book => book.name);
                    frm.set_query("book", function() {
                        return {
                            filters: {
                                name: ["in", options]
                            }
                        };
                    });
                } else {
                    frm.set_query("book", function() {
                        return {
                            filters: {
                                name: ["in", []]
                            }
                        };
                    });
                }
            }
        });
    },
    
    before_save: function(frm){
        frappe.call({
            method: "library_system.services.rest.return_date",
            args: {
                issue_date: frm.doc.issue_date
            },
            callback: function(r) {
                if(r.message) {
                    frm.set_value('return_date', r.message);
                }
            }
        })

    },
    onload: function(frm) {
        frappe.call({
            method: 'library_system.services.rest.enabled',
        });
    }
});
