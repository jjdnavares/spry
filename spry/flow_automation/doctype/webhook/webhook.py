# Copyright (c) 2025, Spry and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
import uuid


class Webhook(Document):
	"""Webhook registration for workflow triggers"""
	
	def before_insert(self):
		"""Generate webhook ID and calculate path length"""
		if not self.webhook_id:
			self.webhook_id = str(uuid.uuid4())
		
		if self.webhook_path:
			self.path_length = len(self.webhook_path.split('/'))
	
	def validate(self):
		"""Validate webhook configuration"""
		# Ensure webhook_path doesn't start with /
		if self.webhook_path and self.webhook_path.startswith('/'):
			self.webhook_path = self.webhook_path[1:]
		
		# Check for duplicate webhook path + method combination
		existing = frappe.db.exists({
			"doctype": "Webhook",
			"webhook_path": self.webhook_path,
			"method": self.method,
			"name": ["!=", self.name]
		})
		
		if existing:
			frappe.throw(f"Webhook with path '{self.webhook_path}' and method '{self.method}' already exists")
	
	def get_full_url(self):
		"""Get the full webhook URL"""
		site_url = frappe.utils.get_url()
		webhook_type = "test-webhook" if self.is_test_webhook else "webhook"
		return f"{site_url}/{webhook_type}/{self.webhook_path}"
	
	def is_dynamic(self):
		"""Check if webhook has dynamic path segments (e.g., :id)"""
		return ':' in self.webhook_path
	
	def get_cache_key(self):
		"""Get cache key for webhook lookup"""
		return f"webhook:{self.method}-{self.webhook_path}"
