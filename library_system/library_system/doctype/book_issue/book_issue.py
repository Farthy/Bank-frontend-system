# Copyright (c) 2024, Farthy and contributors
# For license information, please see license.
import frappe
from frappe.model.document import Document
from frappe.utils import add_days, today

class BookIssue(Document):
    @frappe.whitelist()
    def before_save(self):
        if self.extended:
            self.apply_penalty_and_blacklist()
    

    @frappe.whitelist()
    def fetch_book_issue_data(docname):
        doc = frappe.get_doc("Book Issue", docname)
        return {"return_date": doc.return_date}
@frappe.whitelist(allow_guest=True)
def issue():
    frappe.msgprint("thank you")
