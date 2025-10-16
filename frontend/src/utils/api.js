import { call } from 'frappe-ui'

/**
 * Wrapper for making API calls that works in both dev and production
 */
export async function apiCall(method, args = {}) {
  // In production (when running through Frappe), use window.frappe
  if (window.frappe && window.frappe.call) {
    return window.frappe.call({ method, args })
  }
  
  // In development (standalone Vue dev server), use frappe-ui's call
  return call(method, args)
}

export default {
  call: apiCall
}
