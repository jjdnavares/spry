import frappe
import json
from frappe.utils import now, add_days
from datetime import datetime, timedelta

def check_scheduled_workflows():
    """Check and run scheduled workflows"""
    # Get all active workflows
    active_workflows = frappe.get_all(
        "Workflow",
        filters={"active": 1},
        fields=["name", "settings"]
    )
    
    current_time = datetime.now()
    
    for workflow in active_workflows:
        try:
            # Check if workflow has schedule settings
            settings = workflow.get("settings")
            if not settings:
                continue
                
            if isinstance(settings, str):
                settings = json.loads(settings)
                
            schedule = settings.get("schedule")
            if not schedule:
                continue
                
            # Check if it's time to run the workflow
            if should_run_workflow(workflow.name, schedule, current_time):
                # Execute the workflow
                execute_scheduled_workflow(workflow.name)
        except Exception as e:
            frappe.log_error(f"Error checking scheduled workflow {workflow.name}: {str(e)}", "Workflow Scheduler Error")

def should_run_workflow(workflow_name, schedule, current_time):
    """Check if a workflow should be run based on its schedule"""
    # This is a simplified implementation
    schedule_type = schedule.get("type")
    
    if schedule_type == "interval":
        # Run workflow at regular intervals
        interval = schedule.get("interval", 1)
        interval_unit = schedule.get("intervalUnit", "hours")
        
        # Get last execution time
        last_execution = get_last_execution_time(workflow_name)
        if not last_execution:
            return True
            
        # Calculate next run time
        if interval_unit == "minutes":
            next_run = last_execution + timedelta(minutes=interval)
        elif interval_unit == "hours":
            next_run = last_execution + timedelta(hours=interval)
        elif interval_unit == "days":
            next_run = last_execution + timedelta(days=interval)
        else:
            return False
            
        return current_time >= next_run
        
    elif schedule_type == "cron":
        # Implement cron-like scheduling
        # This would require a more complex implementation using a library like croniter
        # For simplicity, we'll return False for now
        return False
        
    elif schedule_type == "specific":
        # Run at specific times of day
        run_time = schedule.get("runTime")
        run_days = schedule.get("runDays", [0, 1, 2, 3, 4, 5, 6])  # Default to every day
        
        if not run_time:
            return False
            
        # Check if today is a run day
        if current_time.weekday() not in run_days:
            return False
            
        # Parse run time (format: "HH:MM")
        hour, minute = map(int, run_time.split(":"))
        run_datetime = current_time.replace(hour=hour, minute=minute, second=0, microsecond=0)
        
        # Get last execution time
        last_execution = get_last_execution_time(workflow_name)
        if not last_execution:
            return current_time >= run_datetime
            
        # Check if it's been run today
        if last_execution.date() == current_time.date() and last_execution >= run_datetime:
            return False
            
        return current_time >= run_datetime
        
    return False

def get_last_execution_time(workflow_name):
    """Get the last execution time of a workflow"""
    last_execution = frappe.get_all(
        "Workflow Execution",
        filters={
            "workflow": workflow_name,
            "execution_mode": "scheduled",
            "status": ["in", ["success", "error"]]
        },
        fields=["start_time"],
        order_by="start_time desc",
        limit=1
    )
    
    if not last_execution:
        return None
        
    return datetime.fromisoformat(last_execution[0].start_time.replace(" ", "T"))

def execute_scheduled_workflow(workflow_name):
    """Execute a workflow on schedule"""
    try:
        workflow = frappe.get_doc("Workflow", workflow_name)
        
        # Create execution record
        execution = frappe.new_doc("Workflow Execution")
        execution.workflow = workflow.name
        execution.status = "waiting"
        execution.start_time = now()
        execution.triggered_by = "Administrator"  # System execution
        execution.execution_mode = "scheduled"
        execution.insert()
        
        # Execute the workflow
        execution.start_execution()
        result = workflow.execute(None, execution.execution_id)
        execution.complete_execution(result)
        
        return {
            "success": True,
            "execution_id": execution.execution_id,
            "result": result
        }
    except Exception as e:
        if execution:
            execution.fail_execution(str(e))
        frappe.log_error(f"Scheduled workflow execution failed: {str(e)}", "Workflow Scheduler Error")
        return {
            "success": False,
            "error": str(e)
        }

def cleanup_old_workflow_executions():
    """Delete old workflow execution records"""
    # Get retention days from settings
    retention_days = 30  # Default to 30 days
    
    try:
        # You could store this in a settings doctype
        system_settings = frappe.get_doc("System Settings")
        if hasattr(system_settings, "workflow_execution_retention_days"):
            retention_days = system_settings.workflow_execution_retention_days
    except:
        pass
    
    # Calculate cutoff date
    cutoff_date = add_days(now(), -retention_days)
    
    # Delete old records
    frappe.db.delete(
        "Workflow Execution",
        {
            "start_time": ["<", cutoff_date]
        }
    )
    
    frappe.db.commit()
