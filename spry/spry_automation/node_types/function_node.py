import frappe
import json
from typing import Dict, Any

from . import NodeHandler, register_node_type

class FunctionNodeHandler(NodeHandler):
    """Handler for function execution nodes"""
    
    node_type = "function"
    
    def execute(self, parameters: Dict[str, Any], input_data: Any) -> Any:
        """Execute a function based on the node parameters"""
        function_code = parameters.get("functionCode", "")
        function_language = parameters.get("language", "python")
        
        if not function_code:
            return {"error": True, "message": "No function code provided"}
        
        if function_language.lower() == "python":
            return self._execute_python_function(function_code, input_data)
        elif function_language.lower() == "javascript":
            return self._execute_javascript_function(function_code, input_data)
        else:
            return {"error": True, "message": f"Unsupported language: {function_language}"}
    
    def _execute_python_function(self, function_code, input_data):
        """Execute Python function code"""
        # Create a safe execution environment
        global_vars = {"frappe": frappe, "input": input_data, "result": None}
        local_vars = {}
        
        try:
            # Add the function_code to a proper function definition
            full_code = f"""
def execute_function(input):
{self._indent_code(function_code, 4)}

result = execute_function(input)
"""
            # Execute the code
            exec(full_code, global_vars, local_vars)
            
            return global_vars.get("result")
        except Exception as e:
            frappe.log_error(f"Function execution failed: {str(e)}", "Function Node Error")
            return {"error": True, "message": str(e)}
    
    def _execute_javascript_function(self, function_code, input_data):
        """Execute JavaScript function code (requires a JS execution environment)"""
        # This is a placeholder - we'd need to implement a proper JS execution engine
        # or use a service like PyExecJS to run JavaScript code
        return {"error": True, "message": "JavaScript execution not implemented yet"}
    
    def _indent_code(self, code, spaces):
        """Indent code by the specified number of spaces"""
        indent = " " * spaces
        return indent + code.replace("\n", f"\n{indent}")

# Register the node type
register_node_type("function", FunctionNodeHandler)
