"""API endpoints for content generation operations"""

import frappe
from frappe import _
from spry.writer.api.llm import call_llm


@frappe.whitelist()
def generate_content(prompt, keyword, tone, provider="OpenAI", model="gpt-4o", content_type="Article"):
	"""
	Generate content using AI.
	
	Args:
		prompt: The prompt to generate content from
		keyword: Main keyword for the content
		tone: Tone of the content (e.g., professional, casual, friendly)
		provider: LLM provider to use (default: OpenAI)
		model: Model name to use (default: gpt-4o)
		content_type: Type of content to generate (default: Article)
		
	Returns:
		dict: Generated content document details
	"""
	# Check permission
	if not frappe.has_permission("Generated Content", "create"):
		frappe.throw(_("You don't have permission to create content"), frappe.PermissionError)
	
	# Build the full prompt with context
	full_prompt = f"""Create {content_type} content about: {keyword}

Tone: {tone}

Instructions: {prompt}

Please generate high-quality, engaging content that matches the specified tone and addresses the topic comprehensively."""
	
	# Call LLM to generate content
	try:
		generated_text = call_llm(full_prompt, provider, model)
	except Exception as e:
		frappe.log_error(frappe.get_traceback(), "Content Generation Failed")
		frappe.throw(_("Failed to generate content: {0}").format(str(e)))
	
	# Create the document
	doc = frappe.get_doc({
		"doctype": "Generated Content",
		"title": f"{content_type} for {keyword}",
		"prompt": prompt,
		"generated_text": generated_text,
		"keyword": keyword,
		"tone": tone,
		"provider": provider,
		"model": model,
		"content_type": content_type,
		"user": frappe.session.user
	})
	
	doc.insert()
	frappe.db.commit()
	
	return doc.as_dict()


@frappe.whitelist()
def get_content_list(filters=None, limit=20, offset=0):
	"""
	Get list of generated content.
	
	Args:
		filters: Optional filters dict
		limit: Number of records to return (default: 20)
		offset: Offset for pagination (default: 0)
		
	Returns:
		list: List of generated content documents
	"""
	# Check permission
	if not frappe.has_permission("Generated Content", "read"):
		frappe.throw(_("You don't have permission to view content"), frappe.PermissionError)
	
	filters = filters or {}
	
	# Get the list
	content_list = frappe.get_all(
		"Generated Content",
		filters=filters,
		fields=["name", "title", "keyword", "tone", "provider", "model", "content_type", "creation", "user"],
		order_by="creation desc",
		limit=limit,
		start=offset
	)
	
	return content_list


@frappe.whitelist()
def get_content_detail(name):
	"""
	Get detailed information about a specific content document.
	
	Args:
		name: Name of the Generated Content document
		
	Returns:
		dict: Content document details
	"""
	# Check permission
	if not frappe.has_permission("Generated Content", "read", name):
		frappe.throw(_("You don't have permission to view this content"), frappe.PermissionError)
	
	doc = frappe.get_doc("Generated Content", name)
	
	return doc.as_dict()


@frappe.whitelist()
def update_content(name, **kwargs):
	"""
	Update a content document.
	
	Args:
		name: Name of the Generated Content document
		**kwargs: Fields to update
		
	Returns:
		dict: Updated document details
	"""
	# Check permission
	if not frappe.has_permission("Generated Content", "write", name):
		frappe.throw(_("You don't have permission to edit this content"), frappe.PermissionError)
	
	doc = frappe.get_doc("Generated Content", name)
	
	# Update fields
	for key, value in kwargs.items():
		if hasattr(doc, key):
			setattr(doc, key, value)
	
	doc.save()
	frappe.db.commit()
	
	return {
		"success": True,
		"message": _("Content updated successfully"),
		"name": doc.name
	}


@frappe.whitelist()
def delete_content(name):
	"""
	Delete a content document.
	
	Args:
		name: Name of the Generated Content document
		
	Returns:
		dict: Success message
	"""
	# Check permission
	if not frappe.has_permission("Generated Content", "delete", name):
		frappe.throw(_("You don't have permission to delete this content"), frappe.PermissionError)
	
	frappe.delete_doc("Generated Content", name)
	frappe.db.commit()
	
	return {
		"success": True,
		"message": _("Content deleted successfully")
	}
