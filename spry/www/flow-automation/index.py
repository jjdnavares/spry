import frappe
from spry.flow_automation.api.permission import has_workflow_permission

def get_context(context):
    """Serve the Flow Automation application."""
    context.no_cache = 1
    context.show_sidebar = False
    context.no_breadcrumbs = True
    
    # Check if user is logged in
    if frappe.session.user == "Guest":
        frappe.local.flags.redirect_location = "/login"
        raise frappe.Redirect
    
    # Check if user has permission to access Flow Automation
    if not has_workflow_permission():
        frappe.throw("You don't have permission to access Flow Automation", frappe.PermissionError)
    
    return context
