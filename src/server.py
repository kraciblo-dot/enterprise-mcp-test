import sys
from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv
from connectors.asana import create_task
from connectors.zohobooks import create_invoice
from connectors.workday import log_effort

load_dotenv()

# Initialize the MCP Server
mcp = FastMCP("EnterpriseWorkflowServer")

@mcp.tool()
def asana_create_task_tool(project_id: str, task_name: str, notes: str) -> str:
    try:
        result = create_task(project_id, task_name, notes)
        return f"Successfully created Asana task '{result['name']}' with ID: {result['task_id']}"
    except Exception as e:
        return f"Failed to create Asana task: {str(e)}"

@mcp.tool()
def zoho_create_invoice_tool(customer_id: str, project_name: str, amount: float) -> str:
    try:
        result = create_invoice(customer_id, project_name, amount)
        return f"Successfully generated Zoho Invoice '{result['invoice_id']}' for ${result['amount']}"
    except Exception as e:
        return f"Failed to create Zoho invoice: {str(e)}"

@mcp.tool()
def hr_log_effort_tool(employee_id: str, task_id: str, hours: float) -> str:
    try:
        result = log_effort(employee_id, task_id, hours)
        return f"Successfully logged {result['hours_logged']} hours for employee {result['employee_id']} on task {task_id}."
    except Exception as e:
        return f"Failed to log effort: {str(e)}"

if __name__ == "__main__":
    print("Starting Enterprise Workflow MCP Server...", file=sys.stderr)
    mcp.run()