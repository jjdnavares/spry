# Flow Automation - Testing Guide

## Testing the Overview Page

### Prerequisites
1. ✅ Frontend assets built (`yarn build` in `/frontend`)
2. ✅ Cache cleared (`bench --site spry.localhost clear-cache`)
3. ⏳ Bench server running (`bench start`)

### Access Points

**Main Entry Point:**
- URL: `http://spry.localhost:8002/flow-automation`
- Should redirect to Flow Automation overview page

### What to Test

#### 1. Overview Page Layout
- [ ] Page loads without errors
- [ ] Statistics dashboard displays (5 cards)
- [ ] Tab navigation visible (Workflows, Credentials, Executions)
- [ ] "Create Workflow" button visible in top right

#### 2. Statistics Cards
- [ ] All 5 cards display:
  - Prod. executions
  - Failed prod. executions
  - Failure rate
  - Time saved
  - Run time (avg.)
- [ ] Cards show "Last 7 days" subtitle
- [ ] Numbers display correctly (currently 0s as placeholder)

#### 3. Tab Navigation
- [ ] Clicking "Workflows" tab shows workflow list
- [ ] Clicking "Credentials" tab shows placeholder
- [ ] Clicking "Executions" tab shows placeholder
- [ ] Active tab has blue underline
- [ ] Hover states work on inactive tabs

#### 4. Workflows Tab (Empty State)
- [ ] If no workflows exist:
  - Shows document icon
  - Shows "No workflows" heading
  - Shows "Get started by creating a new workflow" text
  - Shows "Create Workflow" button

#### 5. Workflows Tab (With Data)
Once you create a workflow:
- [ ] Search bar works (filters workflows)
- [ ] Sort dropdown works (by last updated, name, created)
- [ ] Filter button visible
- [ ] Workflow cards display:
  - Workflow name
  - Active/Inactive badge
  - Personal indicator
  - Last updated timestamp
  - Created timestamp
- [ ] Hover on card shows:
  - Border color changes to blue
  - Run button (green play icon)
  - View executions button (clock icon)
  - More menu button (three dots)
- [ ] Clicking card opens workflow editor
- [ ] Pagination shows "Total X" and "50/page"

#### 6. Interactions
- [ ] "Create Workflow" button navigates to `/flow-automation/workflow/new`
- [ ] Clicking workflow card navigates to editor
- [ ] Run button executes workflow (shows alert)
- [ ] View executions button navigates to executions page

#### 7. Responsive Design
- [ ] Page looks good on desktop (1920px)
- [ ] Page looks good on laptop (1366px)
- [ ] Statistics cards stack properly on smaller screens
- [ ] Search and filters work on mobile

### Expected Behavior

1. **First Load (No Workflows)**
   - Statistics show all zeros
   - Empty state displayed
   - Clean, professional look

2. **After Creating Workflow**
   - Workflow appears in list
   - Card shows proper information
   - Hover effects work smoothly
   - Actions are accessible

3. **Search & Filter**
   - Real-time search filtering
   - Sort changes order immediately
   - Smooth transitions

### Common Issues & Solutions

**Issue: Page shows 404**
- Solution: Check that `/spry/www/flow-automation/` exists
- Solution: Verify `website_route_rules` in hooks.py

**Issue: Assets not loading**
- Solution: Check `/spry/public/frontend/assets/` has files
- Solution: Rebuild with `yarn build`
- Solution: Clear cache again

**Issue: Blank page**
- Solution: Check browser console for errors
- Solution: Verify `index.js` exists in assets
- Solution: Check if CSRF token is set

**Issue: Frappe API calls fail**
- Solution: Verify user is logged in
- Solution: Check API endpoints exist in `spry/flow_automation/api/`
- Solution: Check permissions

### Browser Console Checks

Open browser DevTools (F12) and check:

1. **Console Tab**
   - No red errors
   - Vue app should mount successfully
   - API calls should complete (check Network tab)

2. **Network Tab**
   - `index.js` loads (200 status)
   - `index.css` loads (200 status)
   - `vendor.js` loads (200 status)
   - API calls to `/api/method/spry.flow_automation.*` work

3. **Elements Tab**
   - `<div id="app">` should have content
   - Vue components should be rendered
   - Tailwind classes should be applied

### Next Steps After Testing

1. If overview page works → Design workflow canvas
2. If issues found → Debug and fix
3. Create sample workflows for testing
4. Implement statistics API endpoint
