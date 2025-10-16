# Copyright (c) 2025, Spry and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from datetime import datetime, timedelta


class WorkflowStatistics(Document):
	"""Tracks workflow execution statistics"""
	
	def validate(self):
		"""Validate workflow exists"""
		if not frappe.db.exists("Workflow", self.workflow):
			frappe.throw(f"Workflow '{self.workflow}' does not exist")
		
		# Calculate failure rate
		if self.total_executions > 0:
			self.failure_rate = (self.error_count / self.total_executions) * 100
		else:
			self.failure_rate = 0
	
	def update_statistics(self, execution_doc):
		"""Update statistics based on execution"""
		self.total_executions = (self.total_executions or 0) + 1
		
		if execution_doc.status == "success":
			self.success_count = (self.success_count or 0) + 1
		elif execution_doc.status == "error":
			self.error_count = (self.error_count or 0) + 1
		
		self.last_execution = execution_doc.start_time
		
		# Calculate runtime
		if execution_doc.end_time and execution_doc.start_time:
			runtime = (execution_doc.end_time - execution_doc.start_time).total_seconds()
			self.total_runtime = (self.total_runtime or 0) + runtime
			self.average_runtime = self.total_runtime / self.total_executions
		
		# Update 7-day statistics
		self.update_7day_stats()
		
		self.save()
	
	def update_7day_stats(self):
		"""Update 7-day statistics"""
		seven_days_ago = datetime.now() - timedelta(days=7)
		
		# Count production executions in last 7 days
		self.production_executions_7d = frappe.db.count("Workflow Execution", {
			"workflow": self.workflow,
			"start_time": [">=", seven_days_ago],
			"execution_mode": ["!=", "manual"]
		})
		
		# Count failed executions in last 7 days
		self.failed_executions_7d = frappe.db.count("Workflow Execution", {
			"workflow": self.workflow,
			"start_time": [">=", seven_days_ago],
			"status": "error"
		})
	
	def format_time_saved(self):
		"""Format time saved in human-readable format"""
		if not self.total_runtime:
			return "0m"
		
		hours = int(self.total_runtime // 3600)
		minutes = int((self.total_runtime % 3600) // 60)
		
		if hours > 0:
			return f"{hours}h {minutes}m"
		else:
			return f"{minutes}m"
