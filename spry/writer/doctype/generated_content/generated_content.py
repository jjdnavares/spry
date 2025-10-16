# Copyright (c) 2025, jumes.dev and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class GeneratedContent(Document):
	"""Document controller for Generated Content"""
	
	def before_insert(self):
		"""Set user before inserting"""
		if not self.user:
			self.user = frappe.session.user
	
	def validate(self):
		"""Validate the document before saving"""
		# Ensure title is not empty
		if not self.title:
			frappe.throw("Title is required")
		
		# Ensure prompt is not empty
		if not self.prompt:
			frappe.throw("Prompt is required")
		
		# Ensure generated text is not empty
		if not self.generated_text:
			frappe.throw("Generated text is required")
	
	def on_update(self):
		"""Called after the document is updated"""
		pass
	
	def on_trash(self):
		"""Called before the document is deleted"""
		pass
