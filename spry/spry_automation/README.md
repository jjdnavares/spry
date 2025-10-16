# Spry Automation Module

The Spry Automation module provides comprehensive workflow automation capabilities within Spry, enabling users to create, manage, and execute automated workflows with AI-powered nodes.

## Features

- **Visual Workflow Editor**: Create and manage workflows with a user-friendly interface
- **Node-based Architecture**: Build workflows using different node types (HTTP, Function, Data Transform)
- **Credential Management**: Securely store and manage API credentials
- **Execution History**: Track and monitor workflow executions
- **Scheduled Workflows**: Run workflows on a schedule
- **Frappe Integration**: Leverages Frappe's DocType system for data storage

## Architecture

### Backend Components

- **DocTypes**:
  - `Workflow`: Stores workflow definitions with nodes and connections as JSON (n8n-style)
  - `Credential`: Encrypted credential storage
  - `Workflow Execution`: Execution history and results
  - `Tag`: Workflow organization tags
  - `Workflow Tag Mapping`: Many-to-many relationship between workflows and tags
  - `Webhook`: Webhook endpoint registration for triggers
  - `Execution Data`: Detailed execution data (separate from metadata)
  - `Shared Workflow`: Workflow sharing and permissions
  - `Workflow Statistics`: Execution statistics and metrics

- **API Endpoints** (`api/`):
  - `workflow.py`: Workflow CRUD and execution
  - `credential.py`: Credential management
  - `node_types.py`: Available node types
  - `permission.py`: Access control

- **Workflow Engine** (`workflow_engine.py`):
  - Executes workflows based on node definitions
  - Handles node connections and data flow
  - Manages execution state

- **Node Types** (`node_types/`):
  - HTTP Request nodes
  - Function execution nodes
  - Data transformation nodes

### Frontend Components

Built with Vue 3 and Tailwind CSS:

- **Workflow List**: View and manage all workflows
- **Workflow Editor**: Create and edit workflow definitions
- **Workflow Executions**: View execution history
- **Execution Detail**: Detailed execution information
- **Credential List**: Manage credentials
- **Credential Editor**: Create and edit credentials

## Installation

1. Install the Spry app in your Frappe bench
2. Build the frontend assets:
   ```bash
   cd /home/jumes/bench/apps/spry
   ./build.sh
   ```

3. Clear cache and restart:
   ```bash
   cd /home/jumes/bench
   bench clear-cache
   bench restart
   ```

## Usage

Access Flow Automation at: `http://spry.localhost:8002/flow-automation`

### Creating a Workflow

1. Navigate to Flow Automation
2. Click "Create Workflow"
3. Add nodes from the available node types
4. Connect nodes to define the workflow
5. Save and activate the workflow

### Running a Workflow

- **Manual**: Click "Run" on any workflow
- **Scheduled**: Configure schedule in workflow settings
- **API**: Call the execution API endpoint

## API Reference

### Execute Workflow

```python
frappe.call({
    method: 'spry.flow_automation.api.workflow.execute_workflow',
    args: { 
        name: 'workflow_name',
        input_data: { /* optional input */ }
    }
})
```

### Get Workflow List

```python
frappe.call({
    method: 'spry.flow_automation.api.workflow.get_workflow_list'
})
```

## Development

### Adding New Node Types

1. Create a new handler in `node_types/`
2. Extend the `NodeHandler` base class
3. Register the node type in `node_types/__init__.py`
4. Add node type metadata in `api/node_types.py`

### Example Node Handler

```python
from . import NodeHandler, register_node_type

class CustomNodeHandler(NodeHandler):
    node_type = "custom"
    
    def execute(self, parameters, input_data):
        # Your node logic here
        return result

register_node_type("custom", CustomNodeHandler)
```

## Security

- Credentials are encrypted using Frappe's encryption utilities
- Access control via `has_workflow_permission()` function
- CSRF protection on all API endpoints
- User authentication required for all operations

## Scheduled Tasks

Configured in `hooks.py`:

- **All**: Check for scheduled workflows
- **Daily**: Cleanup old execution records

## License

MIT
