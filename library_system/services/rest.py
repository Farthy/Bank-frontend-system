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
def apply_penalty(docname):
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

    frappe.db.commit()
    
    member.reload()   

    return member
@frappe.whitelist(allow_guest=True)
def blacklist():
   members = frappe.get_all("LIbrary Member", fields=["name", "penalty", "blacklisted"])     
   members_to_blacklist = [member for member in members if member.penalty > 100 and not member.blacklisted]
            
   for member in members_to_blacklist:
            frappe.db.set_value("LIbrary Member", member.name, "blacklisted", 1)
           
   frappe.db.commit()   
   for member in members_to_blacklist:
            frappe.get_doc("LIbrary Member", member.name).reload()
        
   return members_to_blacklist

    