# Copyright (c) 2025, jumes.dev and Contributors
# See license.txt

import frappe
from frappe.tests.utils import FrappeTestCase


class TestGeneratedContent(FrappeTestCase):
	"""Test cases for Generated Content DocType"""
	
	def test_generated_content_creation(self):
		"""Test creating a Generated Content document"""
		doc = frappe.get_doc({
			"doctype": "Generated Content",
			"title": "Test Content",
			"prompt": "Generate a test article",
			"generated_text": "This is test generated content",
			"keyword": "test",
			"tone": "professional",
			"provider": "OpenAI",
			"model": "gpt-4",
			"content_type": "Article"
		})
		doc.insert()
		
		self.assertEqual(doc.title, "Test Content")
		self.assertEqual(doc.user, frappe.session.user)
		
		# Clean up
		doc.delete()
	
	def test_validation(self):
		"""Test validation rules"""
		doc = frappe.get_doc({
			"doctype": "Generated Content",
			"title": "",
			"prompt": "Test prompt",
			"generated_text": "Test text",
			"keyword": "test",
			"tone": "professional",
			"provider": "OpenAI"
		})
		
		with self.assertRaises(frappe.ValidationError):
			doc.insert()
