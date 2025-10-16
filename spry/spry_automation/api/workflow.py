import frappe
import json
from frappe.utils import now
from frappe.model.document import get_doc
from frappe import _

@frappe.whitelist()
def get_workflow_list():
    """Get list of workflows"""
    workflows = frappe.get_list(
        "Flow Workflow",
        fields=["name", "workflow_name", "description", "active", "creation", "modified"],
        order_by="modified desc"
    )
    return workflows

@frappe.whitelist()
def get_workflow(name):
    """Get workflow by name"""
    workflow = frappe.get_doc("Flow Workflow", name)
    return workflow.as_dict()

@frappe.whitelist()
def save_workflow(data):
    """Save workflow"""
    try:
        if isinstance(data, str):
            data = json.loads(data)
            
        workflow_name = data.get("workflow_name")
        
        if not workflow_name:
            frappe.throw(_("Workflow name is required"))
        
        # Ensure nodes and connections are properly formatted
        if "nodes" in data and isinstance(data["nodes"], str):
            # Already a JSON string, keep as is
            pass
        elif "nodes" in data:
            # Convert to JSON string if it's a dict/list
            data["nodes"] = json.dumps(data["nodes"])
        else:
            # Set default empty array as JSON string
            data["nodes"] = "[]"
        
        if "connections" in data and isinstance(data["connections"], str):
            # Already a JSON string, keep as is
            pass
        elif "connections" in data:
            # Convert to JSON string if it's a dict/list
            data["connections"] = json.dumps(data["connections"])
        else:
            # Set default empty array as JSON string
            data["connections"] = "[]"
            
        # Check if workflow exists
        if frappe.db.exists("Flow Workflow", {"workflow_name": workflow_name}):
            # Update existing workflow
            workflow = frappe.get_doc("Flow Workflow", {"workflow_name": workflow_name})
            
            # Check permission
            if not frappe.has_permission("Flow Workflow", "write", workflow):
                frappe.throw(_("You don't have permission to update this workflow"))
            
            workflow.update(data)
            workflow.save(ignore_permissions=False)
            frappe.db.commit()
            return workflow.as_dict()
        else:
            # Check permission for creating new workflow
            if not frappe.has_permission("Flow Workflow", "create"):
                frappe.throw(_("You don't have permission to create workflows"))
            
            # Create new workflow
            workflow = frappe.new_doc("Flow Workflow")
            workflow.update(data)
            workflow.insert(ignore_permissions=False)
            frappe.db.commit()
            return workflow.as_dict()
    except Exception as e:
        frappe.log_error(f"Failed to save workflow: {str(e)}\nData: {json.dumps(data, indent=2)}", "Workflow Save Error")
        frappe.throw(_("Failed to save workflow: {0}").format(str(e)))

@frappe.whitelist()
def delete_workflow(name):
    """Delete workflow"""
    if not frappe.has_permission("Flow Workflow", "delete"):
        frappe.throw(_("You don't have permission to delete workflows"))
        
    frappe.delete_doc("Flow Workflow", name)
    return {"success": True}

@frappe.whitelist()
def execute_workflow(name, input_data=None):
    """Execute workflow"""
    workflow = frappe.get_doc("Flow Workflow", name)
    
    if not workflow.active:
        frappe.throw(_("Cannot execute inactive workflow"))
        
    if input_data and isinstance(input_data, str):
        input_data = json.loads(input_data)
        
    # Create execution record
    execution = frappe.new_doc("Workflow Execution")
    execution.workflow = workflow.name
    execution.status = "waiting"
    execution.start_time = now()
    execution.triggered_by = frappe.session.user
    execution.execution_mode = "manual"
    
    if input_data:
        execution.input_data = json.dumps(input_data)
        
    execution.insert()
    
    # Execute the workflow
    try:
        execution.start_execution()
        result = workflow.execute(input_data, execution.execution_id)
        execution.complete_execution(result)
        
        return {
            "success": True,
            "execution_id": execution.execution_id,
            "result": result
        }
    except Exception as e:
        execution.fail_execution(str(e))
        frappe.log_error(f"Workflow execution failed: {str(e)}", "Workflow API Error")
        return {
            "success": False,
            "execution_id": execution.execution_id,
            "error": str(e)
        }

@frappe.whitelist()
def get_workflow_executions(workflow_name=None, limit=20, offset=0):
    """Get workflow executions"""
    filters = {}
    if workflow_name:
        filters["workflow"] = workflow_name
        
    executions = frappe.get_list(
        "Workflow Execution",
        filters=filters,
        fields=["name", "workflow", "status", "start_time", "end_time", "execution_id", "execution_mode", "triggered_by"],
        order_by="start_time desc",
        limit_start=offset,
        limit=limit
    )
    
    return executions

@frappe.whitelist()
def get_workflow_execution(execution_id):
    """Get workflow execution details"""
    execution = frappe.get_doc("Workflow Execution", {"execution_id": execution_id})
    return execution.as_dict()

@frappe.whitelist()
def stop_workflow_execution(execution_id):
    """Stop a running workflow execution"""
    execution = frappe.get_doc("Workflow Execution", {"execution_id": execution_id})
    
    if execution.status != "running":
        frappe.throw(_("Cannot stop execution that is not running"))
        
    execution.terminate_execution()
    return {"success": True}
