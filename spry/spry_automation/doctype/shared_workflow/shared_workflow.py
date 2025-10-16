# Copyright (c) 2025, Spry and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class SharedWorkflow(Document):
	"""Manages workflow sharing and permissions"""
	
	def validate(self):
		"""Validate sharing configuration"""
		# Check if workflow exists
		if not frappe.db.exists("Workflow", self.workflow):
			frappe.throw(f"Workflow '{self.workflow}' does not exist")
		
		# Check if user exists
		if not frappe.db.exists("User", self.user):
			frappe.throw(f"User '{self.user}' does not exist")
		
		# Prevent duplicate sharing
		existing = frappe.db.exists({
			"doctype": "Shared Workflow",
			"workflow": self.workflow,
			"user": self.user,
			"name": ["!=", self.name]
		})
		
		if existing:
			frappe.throw(f"Workflow '{self.workflow}' is already shared with user '{self.user}'")
	
	def has_permission(self, permission_type="read"):
		"""Check if user has permission"""
		if permission_type == "read":
			return True
		elif permission_type == "write":
			return self.role in ["Owner", "Editor"]
		elif permission_type == "delete":
			return self.role == "Owner"
		return False
