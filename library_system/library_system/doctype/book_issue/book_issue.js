frappe.ui.form.on('Book Issue', {
    refresh: function(frm) {

        frm.clear_custom_buttons();
    
        if (frm.doc.extended) {
            frm.add_custom_button('Penalize and Blacklist', () => {
                frappe.call({
                    method: "library_system.services.rest.apply_penalty_and_blacklist",
                    args: {
                        docname: frm.doc.name
                    },
                    callback: function(response) {
                        if (response.message === 1) {
                            frm.clear_custom_buttons();
                            frm.add_custom_button('Return Book', () => {
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
        } else {
            frm.add_custom_button('Return Book', () => {
                frappe.call({
                    method: "library_system.services.rest.return_book",
                    args: {
                        docname: frm.doc.name

                    },
                    callback: function(response) {
                        if (response.message === "Complete") {
                            frappe.msgprint('Book returned successfully');
                            frm.clear_custom_buttons();
                            
                        }
                    }
                })
            })

        }

        
    
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
            method: "library_system.services.rest.validatingB4",
            args: {
                docname: frm.doc.name
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
