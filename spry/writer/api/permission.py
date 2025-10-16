"""Permission utilities for Writer module"""

import frappe


@frappe.whitelist()
def has_writer_permission():
	"""
	Check if the current user has permission to access the Writer module.
	
	Returns:
		bool: True if user has permission, False otherwise
	"""
	# Allow System Manager role
	if "System Manager" in frappe.get_roles():
		return True
	
	# Check if user has any role that grants access to Generated Content doctype
	if frappe.has_permission("Generated Content", "read"):
		return True
	
	return False


@frappe.whitelist()
def can_create_content():
	"""
	Check if the current user can create content.
	
	Returns:
		bool: True if user can create content, False otherwise
	"""
	return frappe.has_permission("Generated Content", "create")


@frappe.whitelist()
def can_edit_content(doc_name):
	"""
	Check if the current user can edit a specific content document.
	
	Args:
		doc_name: Name of the Generated Content document
		
	Returns:
		bool: True if user can edit the document, False otherwise
	"""
	return frappe.has_permission("Generated Content", "write", doc_name)


@frappe.whitelist()
def can_delete_content(doc_name):
	"""
	Check if the current user can delete a specific content document.
	
	Args:
		doc_name: Name of the Generated Content document
		
	Returns:
		bool: True if user can delete the document, False otherwise
	"""
	return frappe.has_permission("Generated Content", "delete", doc_name)
