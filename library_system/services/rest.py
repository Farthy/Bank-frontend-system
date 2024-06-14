import frappe
from frappe.model.document import Document
from frappe.utils import add_days, today, getdate
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
def issue_book(docname):
    book_issue = frappe.get_doc("Book Issue", docname)
    book = frappe.get_doc("Book", {"title": book_issue.book})
    
    if book:
        frappe.db.set_value("Book", book.name, "status", "Issued")
    
    frappe.db.commit()
    book.reload()
    return book


@frappe.whitelist(allow_guest=True)
def available_books():
   filters = {
        "status": "available"
    }
   fields = ["name", "title", "status"] 
   books = frappe.get_all("Book", filters=filters, fields=fields)
   return books

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
   
    if penalty >= 100:
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
    
    book = frappe.get_doc("Book", {"title": book_issue.book})
    
    if book:
        frappe.db.set_value("Book", book.name, "status", "available")
    
    frappe.db.commit()
    member.reload()
    
    return book


@frappe.whitelist(allow_guest=True)
def concatenate_fullname(member):
    new_member = frappe.get_doc("LIbrary Member", member)
    first_name = new_member.first_name 
    last_name = new_member.last_name 
    new_member.full_name = f"{first_name} {last_name}".strip()
    new_member.save()

@frappe.whitelist(allow_guest=True)
def return_date(issue_date):
    settings = frappe.db.get_list("Library settings", fields=["return_date"])
    
    if not settings or 'return_date' not in settings[0]:
        frappe.throw("Return date setting not found")
    
    given_days = int(settings[0]['return_date'])
    issue_date = getdate(issue_date)
    return_date = add_days(issue_date, given_days)
    
    return return_date

@frappe.whitelist(allow_guest=True)
def if_extended(docname):
    book_issue = frappe.get_doc("Book Issue", docname)
    return book_issue
