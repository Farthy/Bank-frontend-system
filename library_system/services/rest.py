import frappe
@frappe.whitelist()
def get_available_book():
    available_issues = frappe.get_all('Book Issue', filters={'status': 'available'}, fields=['book_name','member','status'])
    return available_issues
