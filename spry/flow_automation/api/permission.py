import frappe

def has_workflow_permission():
    """Check if user has permission to access the Flow Automation app"""
    # Check if user has System Manager role
    if frappe.session.user == "Administrator" or "System Manager" in frappe.get_roles():
        return True
        
    # Or allow custom role for workflow automation
    if "Workflow Manager" in frappe.get_roles():
        return True
        
    return False
