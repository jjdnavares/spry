# Copyright (c) 2025, Spry and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
import json


class ExecutionData(Document):
	"""Stores detailed execution data separately from execution metadata"""
	
	def validate(self):
		"""Validate execution exists"""
		if not frappe.db.exists("Workflow Execution", self.execution):
			frappe.throw(f"Workflow Execution '{self.execution}' does not exist")
	
	def set_data(self, data_dict):
		"""Set execution data from dictionary"""
		if isinstance(data_dict, dict):
			self.data = json.dumps(data_dict, indent=2)
		else:
			self.data = str(data_dict)
	
	def get_data(self):
		"""Get execution data as dictionary"""
		if self.data:
			try:
				return json.loads(self.data)
			except json.JSONDecodeError:
				return {"raw": self.data}
		return {}
