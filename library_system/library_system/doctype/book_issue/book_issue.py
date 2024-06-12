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
    def apply_penalty_and_blacklist(self):
        library_settings = frappe.get_single("Library settings")
        penalty_per_day = library_settings.penalty_amount
        return_date = add_days(self.return_date, 1)
        days_overdue = (today() - return_date).days

        if days_overdue > 0:
            penalty = days_overdue * penalty_per_day
            member = frappe.get_doc("LIbrary Member", self.first_name)
            member.blacklisted = True
            member.penalty = penalty
            member.save()

        self.extended = False  # Reset the extension status after applying penalty


    @frappe.whitelist()
    def fetch_book_issue_data(docname):
        doc = frappe.get_doc("Book Issue", docname)
        return {"return_date": doc.return_date}
