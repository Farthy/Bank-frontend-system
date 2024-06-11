# Copyright (c) 2024, Farthy and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


# class LibraryMembers(Document):
@frappe.whitelist()
def order_a_book(email):
    if email:
        
        return "Book ordered successfully for email: {}".format(email)
    else:
        return "Email is required to order a book"
