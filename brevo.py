import os
import requests

def send_personalized_email(lead: dict) -> bool:
    """
    Stage 4: Automated outreach engine[cite: 2].
    """
    api_key = os.getenv("BREVO_API_KEY")
    if not api_key:
        print("  ⚠️ Brevo configuration key missing. Skipping execution context.")
        return False
        
    url = "https://api.brevo.com/v3/smtp/email"
    headers = {
        "accept": "application/json",
        "api-key": api_key,
        "content-type": "application/json"
    }
    
    subject = f"Scalability strategy review for {lead['company']}"
    html_content = f"""
    <html>
        <body>
            <p>Hi {lead['name']},</p>
            <p>I hope this message finds you well. I was reviewing operational models at <strong>{lead['company']}</strong> 
            in your capacity as <strong>{lead['title']}</strong> and wanted to connect regarding automated performance architectures.</p>
            <p>Do you have 5 minutes for a brief call next Tuesday?</p>
            <p>Best regards,<br>Engineering Automation Team</p>
        </body>
    </html>
    """
    
    payload = {
        "sender": {"name": "Outreach Engine", "email": "srilakshmiramesh1707@gmail.com"}, # Adjust placeholder as needed
        "to": [{"email": lead["email"], "name": lead["name"]}],
        "subject": subject,
        "htmlContent": html_content
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=8)
        return response.status_code in [200, 201, 202]
    except Exception:
        return False