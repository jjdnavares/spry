import frappe
import json
from frappe.model.document import Document
from frappe.utils import now

class Workflow(Document):
    def before_save(self):
        """Set audit fields before saving"""
        if not self.creation:
            self.created_by = frappe.session.user
            self.creation = now()
        
        self.modified_by = frappe.session.user

    def validate(self):
        """Validate workflow definition"""
        # Ensure nodes is valid JSON
        try:
            if isinstance(self.nodes, str):
                json.loads(self.nodes)
            # Ensure connections is valid JSON
            if isinstance(self.connections, str):
                json.loads(self.connections)
            # Ensure settings is valid JSON
            if self.settings and isinstance(self.settings, str):
                json.loads(self.settings)
            # Ensure pinned_data is valid JSON
            if self.pinned_data and isinstance(self.pinned_data, str):
                json.loads(self.pinned_data)
        except ValueError:
            frappe.throw("Invalid JSON data in workflow definition")

    def execute(self, input_data=None, run_id=None):
        """Execute the workflow with the given input data"""
        # This is a placeholder for the workflow execution logic
        # We'll implement this when we add the execution engine adapter
        from spry.flow_automation.workflow_engine import execute_workflow
        return execute_workflow(self, input_data, run_id)
