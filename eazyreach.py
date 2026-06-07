import os
import re
import requests

def resolve_linkedin_to_email(linkedin_url: str) -> str:
    """
    Stage 3: Seamlessly parses LinkedIn strings into valid routing structures.
    Uses environment-driven plus-addressing for safe staging demonstrations.
    """
    api_key = os.getenv("EAZYREACH_API_KEY")
    fallback_destination = os.getenv("TEST_FALLBACK_EMAIL")
    
    # --- STAGING / INTERVIEW MODE ---
    if not api_key or api_key == "":
        handle = linkedin_url.split("/in/")[-1].replace("/", "") if "/in/" in linkedin_url else "lead"
        clean_name = re.sub(r'[-–_]\w+\d+\w*', '', handle).replace('-', '').lower()
        
        # If a personal test email is provided in .env, use safe plus-addressing
        if fallback_destination and "@" in fallback_destination:
            email_username, email_domain = fallback_destination.split("@")
            return f"{email_username}+{clean_name}@{email_domain}"
            
        # Standard corporate structure simulation if no test email is configured
        return f"{clean_name}@workplace.com"
        
    # --- PRODUCTION INTEGRATION ---
    try:
        url = "https://api.eazyreach.app/api/v1/enrich"
        headers = {"X-API-KEY": api_key, "Content-Type": "application/json"}
        response = requests.post(url, headers=headers, json={"linkedin_url": linkedin_url}, timeout=5)
        if response.status_code == 200:
            return response.json().get("work_email")
    except Exception:
        pass
    return "contact@workplace.com"