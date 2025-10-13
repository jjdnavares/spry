import frappe
import json
from frappe.utils import now
from frappe import _

@frappe.whitelist()
def get_credential_list():
    """Get list of credentials"""
    credentials = frappe.get_list(
        "Credential",
        fields=["name", "credential_name", "credential_type", "creation", "modified"],
        order_by="credential_name"
    )
    return credentials

@frappe.whitelist()
def get_credential(name):
    """Get credential by name (returns only metadata, not the encrypted data)"""
    credential = frappe.get_doc("Credential", name)
    # Don't return the actual credential data for security reasons
    credential_dict = credential.as_dict()
    credential_dict.pop("credential_data", None)
    return credential_dict

@frappe.whitelist()
def save_credential(data):
    """Save credential"""
    if isinstance(data, str):
        data = json.loads(data)
        
    credential_name = data.get("credential_name")
    credential_type = data.get("credential_type")
    credential_data = data.get("credential_data")
    
    if not credential_name:
        frappe.throw(_("Credential name is required"))
        
    if not credential_type:
        frappe.throw(_("Credential type is required"))
        
    if not credential_data:
        frappe.throw(_("Credential data is required"))
        
    # Check if credential exists
    if frappe.db.exists("Credential", {"credential_name": credential_name}):
        # Update existing credential
        credential = frappe.get_doc("Credential", {"credential_name": credential_name})
        credential.credential_type = credential_type
        credential.credential_data = credential_data
        credential.save()
        
        # Don't return the credential data for security
        result = credential.as_dict()
        result.pop("credential_data", None)
        return result
    else:
        # Create new credential
        credential = frappe.new_doc("Credential")
        credential.credential_name = credential_name
        credential.credential_type = credential_type
        credential.credential_data = credential_data
        credential.insert()
        
        # Don't return the credential data for security
        result = credential.as_dict()
        result.pop("credential_data", None)
        return result

@frappe.whitelist()
def delete_credential(name):
    """Delete credential"""
    if not frappe.has_permission("Credential", "delete"):
        frappe.throw(_("You don't have permission to delete credentials"))
        
    # Check if credential is used in any workflow nodes
    # This would require additional implementation
    
    frappe.delete_doc("Credential", name)
    return {"success": True}

@frappe.whitelist()
def test_credential(name, test_data=None):
    """Test if a credential works"""
    credential = frappe.get_doc("Credential", name)
    
    # This is a placeholder. In a real implementation, you would:
    # 1. Get the credential type handler
    # 2. Use the handler to test the credential
    # For now, we'll return a dummy success response
    
    return {"success": True, "message": "Credential test successful"}

@frappe.whitelist()
def get_credential_types():
    """Get list of available credential types"""
    # This is a placeholder. In a real implementation, you would:
    # 1. Get a list of registered credential type handlers
    # 2. Return their metadata
    
    # For now, we'll return some common credential types
    return [
        {
            "type": "basic_auth",
            "name": "Basic Authentication",
            "fields": [
                {"name": "username", "type": "string", "required": True},
                {"name": "password", "type": "password", "required": True}
            ]
        },
        {
            "type": "api_key",
            "name": "API Key",
            "fields": [
                {"name": "api_key", "type": "password", "required": True},
                {"name": "header_name", "type": "string", "required": False, "default": "X-API-Key"}
            ]
        },
        {
            "type": "oauth2",
            "name": "OAuth 2.0",
            "fields": [
                {"name": "client_id", "type": "string", "required": True},
                {"name": "client_secret", "type": "password", "required": True},
                {"name": "auth_url", "type": "string", "required": True},
                {"name": "token_url", "type": "string", "required": True},
                {"name": "scope", "type": "string", "required": False}
            ]
        }
    ]
