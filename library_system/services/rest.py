import frappe
from frappe.model.document import Document
from frappe.utils import add_days, today
from datetime import datetime, timedelta
from frappe.utils.background_jobs import enqueue
import datetime as dt

@frappe.whitelist(allow_guest=True)
def enabled():
    today = datetime.today().strftime('%Y-%m-%d')
    
    doc = frappe.get_list("Book Issue", filters={
        'return_date': ('<', today)
    }, fields=['name','return_date']) 
    for entry in doc:
        if entry.get('return_date'):
            frappe.db.set_value("Book Issue", entry['name'], "extended", 1)
        else:
            frappe.db.set_value("Book Issue", entry['name'], "extended", 0)

    frappe.db.commit()

    return "Enabled field updated successfully"
enabled()

def schedule_update():
    enqueue(method=enabled, queue='short', interval=1, now=True)

schedule_update()

@frappe.whitelist(allow_guest=True)
def is_book_available(docname):
    given_book = frappe.get_doc("Book", docname)
    return given_book.status

@frappe.whitelist(allow_guest=True)
def apply_penalty_and_blacklist(docname):
    book_issue = frappe.get_doc("Book Issue", docname)
    penalty_amount_list = frappe.db.get_list("Library settings", fields=["penalty_amount"])
    penalty_amount = penalty_amount_list[0].get("penalty_amount")

    return_date = book_issue.return_date + timedelta(days=1)
    today_date = dt.datetime.strptime(frappe.utils.today(), "%Y-%m-%d").date()
    days_overdue = (today_date - return_date).days if today_date > return_date else 0
    
    penalty = 0
    
    if days_overdue > 0:
     penalty = days_overdue * penalty_amount
    
    member = frappe.get_doc("LIbrary Member", book_issue.library_member)
    frappe.db.set_value("LIbrary Member", member.name, "penalty", penalty)
   
    if penalty > 100:
        frappe.db.set_value("LIbrary Member", member.name, "blacklisted", 1)

    frappe.db.commit()
    
    member.reload()   

    return member.blacklisted
@frappe.whitelist(allow_guest=True)
def unblacklist(docname):
    book_issue = frappe.get_doc("Book Issue", docname)
    today_date_str = frappe.utils.today()
    today_date = datetime.strptime(today_date_str, "%Y-%m-%d").date()
    
    member = frappe.get_doc("LIbrary Member", book_issue.library_member)
    
    frappe.db.set_value("LIbrary Member", member.name, "penalty", 0)
    frappe.db.set_value("LIbrary Member", member.name, "blacklisted", 0)
    
    frappe.db.set_value("Book Issue", book_issue.name, "return_date", today_date)
    frappe.db.set_value("Book Issue", book_issue.name, "extended", 0)
    
    frappe.db.commit()
    member.reload()


    