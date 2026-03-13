import os
import requests

def create_invoice(customer_id: str, project_name: str, amount: float) -> dict:
    token = os.getenv("ZOHO_ACCESS_TOKEN")
    org_id = os.getenv("ZOHO_ORG_ID")
    
    url = f"https://www.zohoapis.com/books/v3/invoices?organization_id={org_id}"
    
    headers = {
        "Authorization": f"Zoho-oauthtoken {token}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "customer_id": customer_id,
        "line_items": [
            {
                "name": f"Services rendered for {project_name}",
                "rate": amount,
                "quantity": 1
            }
        ]
    }
    
    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()
    
    json_response = response.json()

    if json_response.get("code") != 0:
        raise Exception(f"Zoho API Error: {json_response.get('message')}")
        
    invoice_data = json_response.get("invoice", {})
    
    return {
        "status": "success", 
        "invoice_id": invoice_data.get("invoice_id"),
        "invoice_number": invoice_data.get("invoice_number"),
        "customer_id": invoice_data.get("customer_id"),
        "amount": amount
    }