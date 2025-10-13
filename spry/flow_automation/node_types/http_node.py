import frappe
import requests
import json
from typing import Dict, Any

from . import NodeHandler, register_node_type

class HttpNodeHandler(NodeHandler):
    """Handler for HTTP request nodes"""
    
    node_type = "http"
    
    def execute(self, parameters: Dict[str, Any], input_data: Any) -> Any:
        """Execute an HTTP request based on the node parameters"""
        method = parameters.get("method", "GET").upper()
        url = parameters.get("url", "")
        headers = parameters.get("headers", {})
        query_params = parameters.get("queryParameters", {})
        body = parameters.get("body", None)
        response_type = parameters.get("responseType", "json")
        
        # Replace placeholders in the URL, headers, and body with input data
        if input_data:
            url = self._replace_placeholders(url, input_data)
            headers = self._replace_placeholders_in_dict(headers, input_data)
            if isinstance(body, str):
                body = self._replace_placeholders(body, input_data)
            elif isinstance(body, dict):
                body = self._replace_placeholders_in_dict(body, input_data)
        
        # Make the HTTP request
        try:
            if method == "GET":
                response = requests.get(url, headers=headers, params=query_params)
            elif method == "POST":
                response = requests.post(url, headers=headers, params=query_params, json=body if isinstance(body, dict) else body)
            elif method == "PUT":
                response = requests.put(url, headers=headers, params=query_params, json=body if isinstance(body, dict) else body)
            elif method == "PATCH":
                response = requests.patch(url, headers=headers, params=query_params, json=body if isinstance(body, dict) else body)
            elif method == "DELETE":
                response = requests.delete(url, headers=headers, params=query_params)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")
            
            # Process the response
            response.raise_for_status()  # Raise an exception for HTTP errors
            
            if response_type == "json":
                try:
                    return {
                        "statusCode": response.status_code,
                        "headers": dict(response.headers),
                        "body": response.json()
                    }
                except ValueError:
                    # If the response is not valid JSON, return it as text
                    return {
                        "statusCode": response.status_code,
                        "headers": dict(response.headers),
                        "body": response.text
                    }
            elif response_type == "text":
                return {
                    "statusCode": response.status_code,
                    "headers": dict(response.headers),
                    "body": response.text
                }
            elif response_type == "binary":
                return {
                    "statusCode": response.status_code,
                    "headers": dict(response.headers),
                    "body": response.content
                }
            else:
                return {
                    "statusCode": response.status_code,
                    "headers": dict(response.headers),
                    "body": response.text
                }
                
        except requests.exceptions.RequestException as e:
            frappe.log_error(f"HTTP request failed: {str(e)}", "HTTP Node Error")
            return {
                "error": True,
                "message": str(e)
            }
    
    def _replace_placeholders(self, text, data):
        """Replace placeholders in a string with values from data"""
        if not text or not isinstance(text, str):
            return text
            
        # Simple placeholder replacement, could be more sophisticated
        for key, value in self._flatten_dict(data).items():
            placeholder = f"{{{{{key}}}}}"
            if isinstance(value, (str, int, float, bool)):
                text = text.replace(placeholder, str(value))
                
        return text
    
    def _replace_placeholders_in_dict(self, dictionary, data):
        """Replace placeholders in dictionary values with values from data"""
        if not dictionary or not isinstance(dictionary, dict):
            return dictionary
            
        result = {}
        for key, value in dictionary.items():
            if isinstance(value, str):
                result[key] = self._replace_placeholders(value, data)
            elif isinstance(value, dict):
                result[key] = self._replace_placeholders_in_dict(value, data)
            else:
                result[key] = value
                
        return result
    
    def _flatten_dict(self, dictionary, parent_key=""):
        """Flatten a nested dictionary to a single level with dotted keys"""
        items = []
        for key, value in dictionary.items():
            new_key = f"{parent_key}.{key}" if parent_key else key
            
            if isinstance(value, dict):
                items.extend(self._flatten_dict(value, new_key).items())
            else:
                items.append((new_key, value))
                
        return dict(items)

# Register the node type
register_node_type("http", HttpNodeHandler)
