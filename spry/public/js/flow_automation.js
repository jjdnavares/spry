frappe.provide('spry');

// Override the Website sidebar item to redirect to Flow Automation
function redirectWebsiteToFlowAutomation() {
    // Use MutationObserver to watch for sidebar changes
    const observer = new MutationObserver(function(mutations) {
        updateWebsiteLinks();
    });

    // Start observing the document for changes
    if (document.body) {
        observer.observe(document.body, {
            childList: true,
            subtree: true
        });
    }

    // Initial update
    updateWebsiteLinks();
}

function updateWebsiteLinks() {
    // Find all links in the sidebar
    const allLinks = document.querySelectorAll('a');
    
    allLinks.forEach(function(link) {
        const href = link.getAttribute('href');
        const linkText = link.textContent.trim();
        
        // Check if this is a Website link
        if (linkText === 'Website' && href && href.includes('/app/website')) {
            // Check if we haven't already modified this link
            if (!link.hasAttribute('data-flow-automation-redirect')) {
                link.setAttribute('data-flow-automation-redirect', 'true');
                
                // Update href
                link.setAttribute('href', '/app/flow-automation');
                
                // Remove any existing click handlers and add new one
                const newLink = link.cloneNode(true);
                newLink.addEventListener('click', function(e) {
                    e.preventDefault();
                    e.stopPropagation();
                    frappe.set_route('flow-automation');
                    return false;
                });
                
                if (link.parentNode) {
                    link.parentNode.replaceChild(newLink, link);
                }
            }
        }
    });
}

// Initialize when Frappe is ready
$(document).ready(function() {
    redirectWebsiteToFlowAutomation();
});

// Also initialize on app_ready event
frappe.ready(function() {
    redirectWebsiteToFlowAutomation();
});
