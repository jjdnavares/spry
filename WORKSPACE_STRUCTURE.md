# Spry Workspace Structure

## Overview
Spry is now properly structured as a **single app** with **modules** (Automation, Writer, CMS) that appear in the Desk sidebar, not as separate apps.

## Architecture

### Before (Incorrect)
- ❌ Multiple apps shown on app selection screen
- ❌ "Spry Automation" as separate app
- ❌ "Writer" as separate app
- ❌ Each redirecting to custom pages

### After (Correct)
- ✅ **Spry** is the only app shown
- ✅ Clicking Spry opens the **Desk**
- ✅ **Automation** and **Writer** appear as workspaces in the sidebar
- ✅ Each workspace has links to their respective pages and doctypes

## Workspace Structure

### Automation Workspace
**Location**: `spry/spry_automation/workspace/automation/automation.json`

**Features**:
- Shortcuts to Workflow and Credentials
- Card sections:
  - **Workflows**: Workflow, Workflow Execution doctypes
  - **Credentials**: Credential doctype
  - **Flow Automation**: Link to `/flow-automation` page

**Sidebar Access**: Desk → Automation

### Writer Workspace
**Location**: `spry/writer/workspace/writer/writer.json`

**Features**:
- Shortcuts to Generated Content and LLM Settings
- Card sections:
  - **Content**: Generated Content doctype
  - **Settings**: LLM Settings doctype
  - **Writer App**: Link to `/writer` page

**Sidebar Access**: Desk → Writer

## User Flow

1. **Login** → User logs in
2. **App Selection** → Only "Spry" appears (along with Frappe if visible)
3. **Click Spry** → Opens Frappe Desk
4. **Sidebar** → Shows workspaces:
   - Home
   - Automation
   - Writer
   - (CMS - future)
   - Build (Frappe)
   - Users (Frappe)
   - etc.
5. **Click Automation** → Opens Automation workspace with:
   - Quick shortcuts
   - Links to Workflow, Credentials
   - Link to Flow Automation page
6. **Click Writer** → Opens Writer workspace with:
   - Quick shortcuts
   - Links to Generated Content, LLM Settings
   - Link to Writer page

## Module Pages

### Flow Automation Page
- **URL**: `/flow-automation`
- **Entry Point**: `frontend/main.js`
- **Vue App**: Full workflow builder interface
- **Access**: Via Automation workspace or direct URL

### Writer Page
- **URL**: `/writer`
- **Entry Point**: `frontend/writer.js`
- **Vue App**: AI content generation interface
- **Access**: Via Writer workspace or direct URL

## Configuration

### hooks.py
```python
# No add_to_apps_screen - Spry shows by default as the app
# Modules are accessed via workspaces in the Desk sidebar
```

### Workspace Files
- `spry/spry_automation/workspace/automation/automation.json`
- `spry/writer/workspace/writer/writer.json`

### Route Rules
```python
website_route_rules = [
    {'from_route': '/flow-automation/<path:app_path>', 'to_route': 'flow-automation/index'},
]
```

## Benefits

✅ **Cleaner UX**: Single app entry point
✅ **Standard Frappe Pattern**: Uses workspaces like ERPNext
✅ **Organized**: Modules grouped logically in sidebar
✅ **Scalable**: Easy to add more modules (CMS, etc.)
✅ **Discoverable**: Users can explore all modules from Desk
✅ **Flexible**: Can access pages directly or via workspace

## Adding New Modules

To add a new module (e.g., CMS):

1. **Create workspace JSON**:
   ```
   spry/cms/workspace/cms/cms.json
   ```

2. **Define workspace structure**:
   - Set module name
   - Add shortcuts
   - Add card sections with links
   - Add link to custom page if needed

3. **Create custom page** (if needed):
   - Add to `www/` directory
   - Create Vue entry point
   - Update vite.config.js
   - Build frontend

4. **Run migrations**:
   ```bash
   bench --site spry.localhost migrate
   bench --site spry.localhost clear-cache
   ```

5. **Result**: New module appears in Desk sidebar

## Files Structure

```
spry/
├── spry_automation/
│   └── workspace/
│       └── automation/
│           └── automation.json
├── writer/
│   └── workspace/
│       └── writer/
│           └── writer.json
├── www/
│   ├── flow-automation/
│   │   ├── index.html
│   │   └── index.py
│   ├── writer.html
│   └── writer.py
└── hooks.py
```

## Testing

1. ✅ Login to Spry
2. ✅ See only "Spry" on app selection
3. ✅ Click Spry → Opens Desk
4. ✅ See "Automation" in sidebar
5. ✅ See "Writer" in sidebar
6. ✅ Click Automation → Opens workspace
7. ✅ Click "Flow Automation" link → Opens `/flow-automation`
8. ✅ Click Writer → Opens workspace
9. ✅ Click "Writer" link → Opens `/writer`

## Summary

Spry is now properly structured as a **unified platform** with modular workspaces, following Frappe best practices and providing a clean, professional user experience.
