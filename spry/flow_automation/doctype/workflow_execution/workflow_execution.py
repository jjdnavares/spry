import frappe
import json
import uuid
from frappe.model.document import Document
from frappe.utils import now

class WorkflowExecution(Document):
    def before_save(self):
        """Set audit fields before saving"""
        if not self.creation:
            self.created_by = frappe.session.user
            self.creation = now()
        
        self.modified_by = frappe.session.user
        
        # Generate a unique execution ID if not already set
        if not self.execution_id:
            self.execution_id = str(uuid.uuid4())
        
    def start_execution(self):
        """Mark the execution as started"""
        self.status = "running"
        self.start_time = now()
        self.save()
        
    def complete_execution(self, output_data=None):
        """Mark the execution as completed successfully"""
        self.status = "success"
        self.end_time = now()
        if output_data:
            self.output_data = json.dumps(output_data) if isinstance(output_data, dict) else output_data
        self.save()
        
    def fail_execution(self, error_message):
        """Mark the execution as failed with an error message"""
        self.status = "error"
        self.end_time = now()
        self.error_message = error_message
        self.save()
        
    def terminate_execution(self):
        """Mark the execution as terminated"""
        self.status = "terminated"
        self.end_time = now()
        self.save()
