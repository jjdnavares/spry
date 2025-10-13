# Flow Automation - Design Document

## Overview Page Design

The Flow Automation overview page follows modern UI/UX principles with a clean, organized layout inspired by n8n but with our own modern aesthetic.

### Key Design Features

#### 1. **Statistics Dashboard**
- 5 key metrics displayed at the top
- Clean card-based layout with borders
- Metrics include:
  - Production executions (last 7 days)
  - Failed production executions (last 7 days)
  - Failure rate percentage
  - Time saved
  - Average run time

#### 2. **Tab Navigation**
- Three main tabs: Workflows, Credentials, Executions
- Clean underline indicator for active tab
- Smooth hover states

#### 3. **Workflows List**
Modern card-based layout with:
- **Search functionality** - Real-time filtering
- **Sort options** - By last updated, name, or created date
- **Filter button** - For advanced filtering (to be implemented)
- **Card design**:
  - Workflow name prominently displayed
  - Active/Inactive status badge
  - Personal/Shared indicator
  - Last updated and created timestamps
  - Hover actions (Run, View Executions, More menu)
  - Smooth hover effects with border color change

#### 4. **Empty States**
- Friendly empty state when no workflows exist
- Clear call-to-action to create first workflow
- Icon-based visual feedback

#### 5. **Loading States**
- Spinner animation during data fetch
- Helpful loading message

### Design Principles Applied

1. **Visual Hierarchy**
   - Clear heading structure (h1 for page title, smaller for sections)
   - Proper spacing between elements
   - Strategic use of color for emphasis

2. **Consistency**
   - Rounded corners (lg = 8px) throughout
   - Consistent spacing (Tailwind's spacing scale)
   - Uniform button styles

3. **Feedback**
   - Hover states on all interactive elements
   - Smooth transitions (transition-all, transition-opacity)
   - Clear active states

4. **Accessibility**
   - Proper semantic HTML
   - ARIA labels where needed
   - Keyboard navigation support
   - Color contrast compliance

5. **Responsiveness**
   - Grid layout adapts to screen size (md:grid-cols-5)
   - Flexible containers
   - Mobile-friendly spacing

### Color Palette

- **Primary**: Blue-600 (#2563eb) for CTAs and active states
- **Success**: Green-600 for active workflows and run actions
- **Neutral**: Gray scale for text and borders
- **Background**: Gray-50 for page background, White for cards

### Typography

- **Headings**: Bold, clear hierarchy
- **Body**: Regular weight, comfortable reading size
- **Small text**: Used for metadata and timestamps

### Interactive Elements

1. **Primary Button** (Create Workflow)
   - Blue background
   - White text
   - Rounded corners
   - Shadow on hover

2. **Icon Buttons**
   - Appear on hover
   - Circular or rounded square
   - Clear tooltips
   - Appropriate colors (green for run, gray for others)

3. **Search Input**
   - Left-aligned icon
   - Clear placeholder text
   - Focus ring in primary color

4. **Dropdown/Select**
   - Consistent with input styling
   - Clear options

### Workflow Card Anatomy

```
┌─────────────────────────────────────────────────────────────┐
│ [Workflow Name]  [Active Badge]  [Personal Icon]            │
│ Last updated X ago • Created Y ago                    [···] │
│                                              [▶] [🕐] [···]  │
└─────────────────────────────────────────────────────────────┘
```

### Future Enhancements

1. **Context Menu** - Right-click or three-dot menu for more actions
2. **Bulk Actions** - Select multiple workflows
3. **Advanced Filters** - Filter by status, tags, owner
4. **Drag and Drop** - Reorder workflows
5. **Quick Preview** - Hover to see workflow details
6. **Keyboard Shortcuts** - Power user features

## Page Structure

```
/flow-automation/
├── Overview (WorkflowList)
│   ├── Statistics Dashboard
│   ├── Tabs (Workflows, Credentials, Executions)
│   └── Workflow Cards
├── /workflow/:id (WorkflowEditor) - Canvas page
├── /workflow/:id/executions
├── /execution/:executionId
├── /credentials
└── /credential/:id
```

## Workflow Canvas/Editor Design

The workflow canvas is a full-screen editor with a modern, light-themed interface for building workflows visually.

### Layout Structure

```
┌─────────────────────────────────────────────────────────────┐
│ [←] Personal | My workflow [+tag]  [Editor|Exec|Settings]   │
│                                     [Active ⚫] [Share] [Save]│
├─────────────────────────────────────────────────────────────┤
│                                                         │ Add │
│                                                         │Node │
│                    Canvas Area                          │     │
│              (Dotted Grid Background)                   │ [□] │
│                                                         │ [□] │
│                                                         │ [□] │
│  [⊡ ⊖ 100% ⊕ ⊞]                                        │     │
└─────────────────────────────────────────────────────────────┘
```

### Key Components

#### 1. **Top Navigation Bar**
- **Left Section**:
  - Back button (← arrow)
  - Personal/Shared indicator
  - Editable workflow name (inline input)
  - Add tag button
  
- **Center Section**:
  - Tab navigation (Editor, Executions, Settings)
  - Pill-style active indicator
  
- **Right Section**:
  - Active/Inactive toggle switch (green when active)
  - Share button
  - Save button (blue, primary action)
  - More menu (three dots)

#### 2. **Canvas Area**
- **Background**: Light gray (#F9FAFB) with dotted grid pattern
- **Grid**: Radial gradient dots, 20px spacing
- **Empty State**: 
  - Centered dashed box with plus icon
  - "Add first step..." text
  - Hover effect (blue border and background)

- **Nodes**:
  - White background with shadow
  - Rounded corners (8px)
  - Border on hover
  - Draggable
  - Close button (X) on hover
  - Node name and type displayed

#### 3. **Bottom Toolbar**
- **Position**: Bottom-left corner
- **Background**: White card with shadow
- **Controls**:
  - Reset zoom (expand icon)
  - Zoom out (minus magnifier)
  - Zoom level display (e.g., "100%")
  - Zoom in (plus magnifier)
  - Fit to screen (fit icon)

#### 4. **Right Sidebar**
- **Width**: 320px (w-80)
- **Header**: "Add Node" title
- **Node Palette**:
  - Scrollable list of available nodes
  - Each node card shows:
    - Icon (left, in colored circle)
    - Node name (bold)
    - Description (gray text)
  - Hover effect: Blue border and background
  - Click to add node to canvas

### Tab Content

#### Editor Tab
- Full canvas with grid background
- Node placement and editing
- Connection drawing (to be implemented)

#### Executions Tab
- White background
- List of workflow executions
- Empty state message

#### Settings Tab
- White background
- Form layout with:
  - Description textarea
  - Execution settings checkboxes
  - Other workflow configuration options

### Design Principles

1. **Light Theme Consistency**
   - White backgrounds for cards and panels
   - Gray-50 for canvas background
   - Blue-600 for primary actions
   - Green-500 for active states

2. **Modern UI Elements**
   - Rounded corners throughout
   - Subtle shadows for depth
   - Smooth transitions
   - Clear visual hierarchy

3. **Professional Aesthetics**
   - Clean, uncluttered interface
   - Ample whitespace
   - Consistent spacing (Tailwind scale)
   - Professional typography

4. **Interactive Feedback**
   - Hover states on all interactive elements
   - Toggle switches for boolean settings
   - Disabled states for buttons
   - Loading indicators

### Color Palette

- **Canvas Background**: Gray-50 (#F9FAFB)
- **Grid Dots**: Gray-300 (#D1D5DB)
- **Cards/Panels**: White (#FFFFFF)
- **Primary Action**: Blue-600 (#2563EB)
- **Active State**: Green-500 (#10B981)
- **Borders**: Gray-200 (#E5E7EB)
- **Text Primary**: Gray-900 (#111827)
- **Text Secondary**: Gray-600 (#4B5563)
- **Text Tertiary**: Gray-500 (#6B7280)

### Interactive Elements

1. **Toggle Switch**
   - Green background when active
   - Gray when inactive
   - Smooth slide animation
   - White circle indicator

2. **Node Cards (Sidebar)**
   - Border: Gray-200 default
   - Border: Blue-500 on hover
   - Background: Blue-50 on hover
   - Icon background changes color

3. **Canvas Nodes**
   - Shadow increases on hover
   - Cursor changes to move
   - Close button appears on hover

4. **Zoom Controls**
   - Icon buttons with hover background
   - Current zoom level displayed
   - Disabled state when at limits

### Future Enhancements

1. **Node Connections**
   - Bezier curves between nodes
   - Connection points on nodes
   - Drag to create connections
   - Connection validation

2. **Node Configuration**
   - Side panel for node settings
   - Parameter inputs
   - Credential selection
   - Test node functionality

3. **Canvas Features**
   - Pan and zoom with mouse/trackpad
   - Multi-select nodes
   - Copy/paste nodes
   - Undo/redo
   - Minimap for navigation

4. **Collaboration**
   - Real-time collaboration indicators
   - User cursors
   - Change history
   - Comments on nodes

## Next Steps

1. ✅ Complete overview page design
2. ✅ Design workflow canvas/editor page
3. ⏳ Implement node connections
4. ⏳ Design credential management pages
5. ⏳ Design execution detail pages
6. ⏳ Implement statistics API
7. ⏳ Add context menus and bulk actions
