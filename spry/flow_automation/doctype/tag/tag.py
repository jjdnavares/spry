# Copyright (c) 2025, Spry and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class Tag(Document):
	"""Tag for organizing workflows"""
	
	def validate(self):
		"""Validate tag name length"""
		if len(self.tag_name) > 24:
			frappe.throw("Tag name must be 24 characters or less")
	
	def before_save(self):
		"""Set default color if not provided"""
		if not self.color:
			self.color = "#3B82F6"
