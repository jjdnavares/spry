# Flow Automation API endpoints
import frappe

def has_workflow_permission():
    """
    Check if the current user has permission to access flow automation.
    By default, only System Managers can access flow automation.
    """
    return frappe.session.user == "Administrator" or "System Manager" in frappe.get_roles()