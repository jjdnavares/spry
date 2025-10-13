import frappe
from frappe import _
import json
from spry.flow_automation.node_types import NODE_TYPE_REGISTRY

@frappe.whitelist()
def get_node_types():
    """Get list of available node types"""
    # This is a simplified version. In a real implementation,
    # you would provide more metadata about each node type.
    node_types = []
    
    # Basic node types
    node_types.append({
        "type": "http",
        "name": "HTTP Request",
        "description": "Make HTTP requests to external services",
        "category": "Communication",
        "icon": "globe",
        "inputs": [
            {"name": "main", "label": "Input", "multiple": True}
        ],
        "outputs": [
            {"name": "main", "label": "Output", "multiple": True}
        ],
        "parameters": [
            {"name": "method", "type": "select", "options": ["GET", "POST", "PUT", "PATCH", "DELETE"], "default": "GET"},
            {"name": "url", "type": "string", "required": True},
            {"name": "headers", "type": "json"},
            {"name": "queryParameters", "type": "json"},
            {"name": "body", "type": "json"},
            {"name": "responseType", "type": "select", "options": ["json", "text", "binary"], "default": "json"}
        ]
    })
    
    node_types.append({
        "type": "function",
        "name": "Function",
        "description": "Execute custom code",
        "category": "Logic",
        "icon": "code",
        "inputs": [
            {"name": "main", "label": "Input", "multiple": True}
        ],
        "outputs": [
            {"name": "main", "label": "Output", "multiple": True}
        ],
        "parameters": [
            {"name": "functionCode", "type": "code", "language": "python", "required": True},
            {"name": "language", "type": "select", "options": ["python", "javascript"], "default": "python"}
        ]
    })
    
    node_types.append({
        "type": "transform",
        "name": "Transform Data",
        "description": "Transform input data structure",
        "category": "Data",
        "icon": "exchange",
        "inputs": [
            {"name": "main", "label": "Input", "multiple": True}
        ],
        "outputs": [
            {"name": "main", "label": "Output", "multiple": True}
        ],
        "parameters": [
            {"name": "transformations", "type": "json", "required": True}
        ]
    })
    
    # Add more node types here
    node_types.append({
        "type": "trigger",
        "name": "Trigger",
        "description": "Starting point of a workflow",
        "category": "Triggers",
        "icon": "play",
        "inputs": [],
        "outputs": [
            {"name": "main", "label": "Output", "multiple": True}
        ],
        "parameters": [
            {"name": "triggerType", "type": "select", "options": ["manual", "webhook", "schedule"], "default": "manual"},
            {"name": "schedule", "type": "string", "show": {"triggerType": "schedule"}},
            {"name": "webhookPath", "type": "string", "show": {"triggerType": "webhook"}}
        ]
    })
    
    return node_types

@frappe.whitelist()
def get_node_type(node_type):
    """Get details for a specific node type"""
    for nt in get_node_types():
        if nt["type"] == node_type:
            return nt
            
    frappe.throw(_("Node type not found"))

@frappe.whitelist()
def test_node(node_type, parameters, input_data=None):
    """Test a node with sample data"""
    if node_type not in NODE_TYPE_REGISTRY:
        frappe.throw(_("Node type not found"))
        
    if isinstance(parameters, str):
        parameters = json.loads(parameters)
        
    if isinstance(input_data, str):
        input_data = json.loads(input_data)
        
    handler = NODE_TYPE_REGISTRY[node_type]()
    
    try:
        result = handler.execute(parameters, input_data)
        return {
            "success": True,
            "result": result
        }
    except Exception as e:
        frappe.log_error(f"Node test failed: {str(e)}", "Node Type API Error")
        return {
            "success": False,
            "error": str(e)
        }
