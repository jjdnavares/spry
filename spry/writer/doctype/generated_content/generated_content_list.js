// Copyright (c) 2025, jumes.dev and contributors
// For license information, please see license.txt

frappe.listview_settings['Generated Content'] = {
	add_fields: ['title', 'keyword', 'tone', 'provider', 'content_type', 'user'],
	
	get_indicator: function(doc) {
		// Add color indicators based on provider
		const provider_colors = {
			'OpenAI': 'green',
			'Anthropic': 'blue',
			'Google': 'orange',
			'Local': 'gray'
		};
		
		return [__(doc.provider || 'Unknown'), provider_colors[doc.provider] || 'gray', 'provider,=,' + doc.provider];
	},
	
	onload: function(listview) {
		// Add custom buttons to the list view
		listview.page.add_inner_button(__('Generate New Content'), function() {
			frappe.new_doc('Generated Content');
		});
	},
	
	formatters: {
		title: function(value) {
			// Truncate long titles
			if (value && value.length > 50) {
				return value.substring(0, 50) + '...';
			}
			return value;
		}
	}
};
