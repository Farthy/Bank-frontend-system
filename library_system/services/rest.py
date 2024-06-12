# import frappe
# @frappe.whitelist()
# def get_available_book():
#     available_issues = frappe.get_all('Book Issue', filters={'status': 'available'}, fields=['book_name','member','status'])
#     return available_issues
# @frappe.whitelist()
# def blacklist_user_method(member, book_issue_name):
#     book_issue = frappe.get_doc("Book Issue", book_issue_name)
#     current_date = frappe.utils.nowdate()
#     if book_issue.return_date < current_date:
#         blacklist_user(member)
#         return "User blacklisted successfully"
#     else:
#         return "Return date not exceeded"
    
# @f@frappe.whitelist() rappe.whitelist()  
# def blacklist_user(member):
#     frappe.db.set_value("Book_Issue", member, "Blacklisted", 1)

# @frappe.whitelist()
# def fine_calculation():
#     book_issue = frappe.get_doc("Book Issue")
#     current_date = frappe.utils.nowdate()
#     fine_days = current_date - book_issue.return_date
#     return fine_days * 15
# library_management/library_management/doctype/book_issue/book_issue.py
# library_management/library_management/doctype/book_issue/book_issue.py
