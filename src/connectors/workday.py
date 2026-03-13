import os
import requests
from datetime import datetime

def log_effort(worker_id: str, task_id: str, hours: float) -> dict:
    token = os.getenv("WORKDAY_ACCESS_TOKEN")
    tenant = os.getenv("WORKDAY_TENANT_NAME")
    host = os.getenv("WORKDAY_HOST")
    
    url = f"https://{host}/ccx/api/timeTracking/v1/{tenant}/workers/{worker_id}/timeEntries"
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "date": datetime.now().strftime("%Y-%m-%d"),
        "quantity": hours,
        "timeEntryCode": {
            "id": "Regular_Time" 
        },
        "comment": f"Effort logged for task: {task_id}"
    }
    
    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()
    response_data = response.json()
    
    return {
        "status": "success", 
        "log_id": response_data.get("id"), 
        "employee_id": worker_id,
        "hours_logged": response_data.get("quantity")
    }