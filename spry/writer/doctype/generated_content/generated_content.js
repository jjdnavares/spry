// Copyright (c) 2025, jumes.dev and contributors
// For license information, please see license.txt

frappe.ui.form.on('Generated Content', {
	refresh: function(frm) {
		// Add custom buttons or actions here
		if (!frm.is_new()) {
			// Add a button to regenerate content
			frm.add_custom_button(__('Regenerate'), function() {
				frappe.msgprint(__('Regenerate functionality to be implemented'));
			});
			
			// Add a button to copy content
			frm.add_custom_button(__('Copy to Clipboard'), function() {
				if (frm.doc.generated_text) {
					navigator.clipboard.writeText(frm.doc.generated_text).then(function() {
						frappe.show_alert({
							message: __('Content copied to clipboard'),
							indicator: 'green'
						});
					}).catch(function(err) {
						frappe.msgprint(__('Failed to copy content: ') + err);
					});
				}
			});
		}
	},
	
	onload: function(frm) {
		// Set default values
		if (frm.is_new()) {
			frm.set_value('user', frappe.session.user);
		}
	},
	
	prompt: function(frm) {
		// Auto-generate title from prompt if title is empty
		if (frm.doc.prompt && !frm.doc.title) {
			const words = frm.doc.prompt.split(' ').slice(0, 5).join(' ');
			frm.set_value('title', words + '...');
		}
	}
});
