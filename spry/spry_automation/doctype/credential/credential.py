import frappe
import json
from frappe.model.document import Document
from frappe.utils import now
from frappe.utils.password import encrypt, decrypt

class Credential(Document):
    def before_save(self):
        """Set audit fields before saving and encrypt credential data"""
        if not self.creation:
            self.created_by = frappe.session.user
            self.creation = now()
        
        self.modified_by = frappe.session.user
        
        # Encrypt credential data if it's not already encrypted
        if isinstance(self.credential_data, dict) or (
            isinstance(self.credential_data, str) and not self.credential_data.startswith("__enc__")
        ):
            if isinstance(self.credential_data, str):
                data = json.loads(self.credential_data)
            else:
                data = self.credential_data
            self.credential_data = encrypt(json.dumps(data))

    def get_decrypted_data(self):
        """Get the decrypted credential data"""
        if not self.credential_data:
            return {}
            
        if isinstance(self.credential_data, str) and self.credential_data.startswith("__enc__"):
            decrypted = decrypt(self.credential_data)
            return json.loads(decrypted)
        elif isinstance(self.credential_data, str):
            return json.loads(self.credential_data)
        else:
            return self.credential_data
