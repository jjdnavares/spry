import frappe
import json
import uuid
from datetime import datetime

class WorkflowEngine:
    def __init__(self, workflow_doc):
        self.workflow = workflow_doc
        self.nodes = {}
        self.connections = {}
        self.execution_data = {}
        
        # Load nodes and connections from the workflow document
        if isinstance(self.workflow.nodes, str):
            self.nodes = json.loads(self.workflow.nodes)
        else:
            self.nodes = self.workflow.nodes
            
        if isinstance(self.workflow.connections, str):
            self.connections = json.loads(self.workflow.connections)
        else:
            self.connections = self.workflow.connections
    
    def create_execution_record(self, input_data=None, triggered_by=None, execution_mode="manual"):
        """Create a workflow execution record"""
        execution = frappe.new_doc("Workflow Execution")
        execution.workflow = self.workflow.name
        execution.status = "waiting"
        execution.start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        execution.triggered_by = triggered_by or frappe.session.user
        execution.execution_mode = execution_mode
        
        if input_data:
            execution.input_data = json.dumps(input_data) if isinstance(input_data, dict) else input_data
            
        execution.insert()
        return execution
    
    def get_node_type_handler(self, node_type):
        """Get the handler for a specific node type"""
        # This would be implemented to return the appropriate node handler
        # based on the node type. For now, we'll return a placeholder.
        
        # In a real implementation, we would have a registry of node handlers
        # for different types of nodes (HTTP, Function, Data Transformation, etc.)
        from spry.flow_automation.node_types import get_node_handler
        return get_node_handler(node_type)
    
    def execute_node(self, node_id, input_data=None):
        """Execute a single node in the workflow"""
        if node_id not in self.nodes:
            raise ValueError(f"Node {node_id} not found in workflow")
            
        node = self.nodes[node_id]
        node_type = node.get("type")
        node_params = node.get("parameters", {})
        
        # Get the handler for this node type
        handler = self.get_node_type_handler(node_type)
        if not handler:
            raise ValueError(f"No handler available for node type: {node_type}")
            
        # Execute the node
        result = handler.execute(node_params, input_data)
        return result
    
    def execute_workflow(self, input_data=None, execution_record=None):
        """Execute the entire workflow"""
        if not execution_record:
            execution_record = self.create_execution_record(input_data)
            
        execution_record.start_execution()
        
        try:
            # Find the starting node(s)
            start_nodes = self._find_start_nodes()
            if not start_nodes:
                raise ValueError("No start nodes found in the workflow")
                
            # Execute the workflow starting from the start nodes
            results = {}
            for node_id in start_nodes:
                node_result = self._execute_node_and_downstream(node_id, input_data, {}, results)
                results.update(node_result)
                
            # Mark the execution as complete
            execution_record.complete_execution(results)
            return results
            
        except Exception as e:
            # Mark the execution as failed
            execution_record.fail_execution(str(e))
            frappe.log_error(f"Workflow execution failed: {str(e)}", "Workflow Engine Error")
            raise
    
    def _find_start_nodes(self):
        """Find the starting nodes of the workflow (nodes with no incoming connections)"""
        all_nodes = set(self.nodes.keys())
        destination_nodes = set()
        
        for _, connections in self.connections.items():
            for connection in connections:
                destination_nodes.add(connection.get("node"))
                
        # Start nodes are nodes that have no incoming connections
        return list(all_nodes - destination_nodes)
    
    def _execute_node_and_downstream(self, node_id, input_data, visited, results):
        """Execute a node and all its downstream nodes recursively"""
        if node_id in visited:
            return results
            
        visited[node_id] = True
        node_result = self.execute_node(node_id, input_data)
        results[node_id] = node_result
        
        # Find downstream nodes
        downstream_connections = self.connections.get(node_id, [])
        for connection in downstream_connections:
            next_node_id = connection.get("node")
            if next_node_id and next_node_id not in visited:
                self._execute_node_and_downstream(next_node_id, node_result, visited, results)
                
        return results

def execute_workflow(workflow_doc, input_data=None, run_id=None):
    """Execute a workflow"""
    engine = WorkflowEngine(workflow_doc)
    
    execution_record = None
    if run_id:
        # Try to find an existing execution record
        execution_record = frappe.get_doc("Workflow Execution", {"execution_id": run_id})
    
    return engine.execute_workflow(input_data, execution_record)
