# Flow Automation - DocType Reference

## Overview

The Flow Automation module uses 9 core doctypes to manage workflows, credentials, executions, and related data. This follows n8n's data model architecture while adhering to Frappe framework standards.

## Core DocTypes

### 1. Workflow
**Purpose**: Stores workflow definitions with nodes and connections

**Key Fields**:
- `workflow_name` (Data, unique): Workflow identifier
- `description` (Text): Workflow description
- `active` (Check): Whether workflow is active
- `nodes` (JSON): Node definitions (n8n-style)
- `connections` (JSON): Node connections
- `settings` (JSON): Workflow settings
- `version` (Int): Version number
- `version_id` (Data): Version identifier
- `pinned_data` (JSON): Pinned test data

**Naming**: By fieldname (workflow_name)

### 2. Credential
**Purpose**: Securely stores API credentials

**Key Fields**:
- `credential_name` (Data, unique): Credential identifier
- `credential_type` (Data): Type of credential (e.g., "http_auth", "oauth2")
- `credential_data` (JSON): Encrypted credential data

**Naming**: By fieldname (credential_name)

**Security**: Data is encrypted using Frappe's encryption utilities

### 3. Workflow Execution
**Purpose**: Tracks workflow execution history and results

**Key Fields**:
- `workflow` (Link): Reference to Workflow
- `status` (Select): waiting, running, success, error, terminated
- `start_time` (Datetime): Execution start time
- `end_time` (Datetime): Execution end time
- `input_data` (JSON): Input data for execution
- `output_data` (JSON): Output data from execution
- `error_message` (Text): Error details if failed
- `execution_mode` (Select): manual, trigger, scheduled
- `execution_id` (Data, unique): Unique execution identifier
- `triggered_by` (Link): User who triggered execution

**Naming**: Random hash

### 4. Tag
**Purpose**: Organize workflows with tags

**Key Fields**:
- `tag_name` (Data, unique, max 24 chars): Tag name
- `description` (Text): Tag description
- `color` (Color): Tag color for UI (default: #3B82F6)

**Naming**: By fieldname (tag_name)

**Usage**: Many-to-many relationship with workflows via Workflow Tag Mapping

### 5. Workflow Tag Mapping
**Purpose**: Junction table for many-to-many relationship between workflows and tags

**Key Fields**:
- `workflow` (Link): Reference to Workflow
- `tag` (Link): Reference to Tag

**Naming**: Random hash

**Validation**: Prevents duplicate mappings

### 6. Webhook
**Purpose**: Register and manage webhook endpoints for workflow triggers

**Key Fields**:
- `workflow` (Link): Reference to Workflow
- `node` (Data): Node name in workflow
- `webhook_path` (Data, unique): Webhook URL path
- `method` (Select): HTTP method (GET, POST, PUT, etc.)
- `webhook_id` (Data): Unique webhook identifier (auto-generated UUID)
- `path_length` (Int): Number of path segments
- `is_test_webhook` (Check): Whether this is a test webhook

**Naming**: Random hash

**Methods**:
- `get_full_url()`: Returns complete webhook URL
- `is_dynamic()`: Checks if path has dynamic segments (e.g., :id)
- `get_cache_key()`: Returns cache key for webhook lookup

**URL Format**: 
- Production: `{site_url}/webhook/{webhook_path}`
- Test: `{site_url}/test-webhook/{webhook_path}`

### 7. Execution Data
**Purpose**: Store detailed execution data separately from execution metadata

**Key Fields**:
- `execution` (Link, unique): Reference to Workflow Execution
- `data` (Long Text): Detailed execution data including node outputs
- `workflow_data` (JSON): Snapshot of workflow definition at execution time

**Naming**: By fieldname (execution)

**Why Separate**: Large execution data is stored separately to optimize queries on Workflow Execution doctype

**Methods**:
- `set_data(data_dict)`: Set execution data from dictionary
- `get_data()`: Get execution data as dictionary

### 8. Shared Workflow
**Purpose**: Manage workflow sharing and permissions

**Key Fields**:
- `workflow` (Link): Reference to Workflow
- `user` (Link): User with access
- `role` (Select): Owner, Editor, Viewer
- `project` (Data): Project or team workspace

**Naming**: Random hash

**Roles**:
- **Owner**: Full access (read, write, delete)
- **Editor**: Read and write access
- **Viewer**: Read-only access

**Methods**:
- `has_permission(permission_type)`: Check user permissions

### 9. Workflow Statistics
**Purpose**: Track workflow execution statistics and metrics

**Key Fields**:
- `workflow` (Link, unique): Reference to Workflow
- `total_executions` (Int): Total number of executions
- `success_count` (Int): Number of successful executions
- `error_count` (Int): Number of failed executions
- `last_execution` (Datetime): Last execution time
- `average_runtime` (Float): Average execution time in seconds
- `total_runtime` (Float): Total execution time in seconds
- `production_executions_7d` (Int): Production executions in last 7 days
- `failed_executions_7d` (Int): Failed executions in last 7 days
- `failure_rate` (Percent): Calculated failure rate
- `time_saved` (Data): Human-readable time saved (e.g., "2h 30m")

**Naming**: By fieldname (workflow)

**Methods**:
- `update_statistics(execution_doc)`: Update stats after execution
- `update_7day_stats()`: Refresh 7-day statistics
- `format_time_saved()`: Format time saved in human-readable format

**Auto-calculation**: Failure rate is automatically calculated on save

## DocType Relationships

```
Workflow (1) ←→ (N) Workflow Tag Mapping ←→ (1) Tag
Workflow (1) ←→ (N) Workflow Execution
Workflow (1) ←→ (N) Webhook
Workflow (1) ←→ (N) Shared Workflow
Workflow (1) ←→ (1) Workflow Statistics

Workflow Execution (1) ←→ (1) Execution Data

User (1) ←→ (N) Shared Workflow
```

## Data Storage Strategy

### JSON vs Separate DocTypes

Following n8n's approach:

**Stored as JSON** (in Workflow):
- Nodes: Complete node definitions with parameters
- Connections: Node connection graph
- Settings: Workflow configuration
- Pinned Data: Test data for nodes

**Stored as Separate DocTypes**:
- Tags: Reusable across workflows
- Executions: Historical records
- Webhooks: Active endpoint registry
- Statistics: Aggregated metrics
- Sharing: Permission management

### Why This Approach?

1. **Performance**: No joins needed to load workflow definition
2. **Atomicity**: Workflow updates are atomic
3. **Simplicity**: Matches n8n's proven architecture
4. **Flexibility**: Easy to version and export workflows

## Permissions

All doctypes use role-based permissions:
- **System Manager**: Full access (CRUD)
- Additional roles can be configured per doctype

Shared Workflow implements fine-grained permissions at the document level.

## Next Steps

1. Migrate existing workflows to use new doctypes
2. Implement API endpoints for tag management
3. Add webhook trigger handler
4. Integrate statistics dashboard with Workflow Statistics doctype
5. Implement workflow sharing UI

## Notes

- All doctypes follow Frappe naming conventions (PascalCase for doctype names, snake_case for fields)
- Standard audit fields (created_by, modified_by, creation, modified) are included
- Track changes is enabled for Workflow, Credential, and Tag doctypes
- All doctypes are in the "Flow Automation" module
