import os
import requests

def create_task(project_id: str, task_name: str, notes: str) -> dict:
    token = os.getenv("ASANA_ACCESS_TOKEN")
    url = "https://app.asana.com/api/1.0/tasks"
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    
    payload = {
        "data": {
            "name": task_name,
            "notes": notes,
            "projects": [project_id]
        }
    }
    
    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status() # Raises an error if the call fails (e.g., 400 or 401)
    response_data = response.json().get("data", {})
    
    return {
        "status": "success", 
        "task_id": response_data.get("gid"),
        "name": response_data.get("name")
    }