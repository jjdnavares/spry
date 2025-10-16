# Copyright (c) 2025, Spry and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class WorkflowTagMapping(Document):
	"""Junction table for many-to-many relationship between Workflows and Tags"""
	
	def validate(self):
		"""Prevent duplicate mappings"""
		existing = frappe.db.exists({
			"doctype": "Workflow Tag Mapping",
			"workflow": self.workflow,
			"tag": self.tag,
			"name": ["!=", self.name]
		})
		
		if existing:
			frappe.throw(f"Tag '{self.tag}' is already assigned to workflow '{self.workflow}'")
