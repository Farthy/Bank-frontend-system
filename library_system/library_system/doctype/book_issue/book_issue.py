# Copyright (c) 2024, Farthy and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

from frappe.model.document import Document
from frappe.utils import add_days, today, getdate
from datetime import datetime, timedelta
from frappe.utils.background_jobs import enqueue
import datetime as dt

class BookIssue(Document):
   def before_save(self):
    # book_issue = frappe.get_doc("Book Issue", self.name)
    book = frappe.get_doc("Book", {"title": self.book})
    
    if not book:
        frappe.throw("Book not found")
    
    book.status = "Issued"
    book.save(ignore_permissions=True)
    frappe.db.commit()
    
    library_member = frappe.get_doc("LIbrary Member", self.library_member)
    library_member.append("member_books", {
        "book_title": self.book,
        "status": self.status,
    })
    library_member.save(ignore_permissions=True)
    frappe.db.commit()
    
    settings = frappe.db.get_list("Library settings", fields=["return_date"])
    print(f"\n\n\n\n{"RETURN DATE FROM THE SETTINGS",settings}\n\n\n")
    if not settings or 'return_date' not in settings[0]:
        frappe.throw("Return date setting not found")
    
    given_days = int(settings[0]['return_date'])
    issue_date = getdate(self.issue_date)
    return_date = add_days(issue_date, given_days)
    self.return_date = return_date
    # return 


