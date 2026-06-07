import os
import requests

def search_people_by_domain(domain: str) -> list:
    """
    Stage 2: Safe Prospeo Search. Returns empty lists instead of crashing if 
    the account hits limitations or if the target domain has no records[cite: 2, 3].
    """
    api_key = os.getenv("PROSPEO_API_KEY")
    if not api_key:
        print("  ⚠️ Prospeo API Key missing.")
        return []

    url = "https://api.prospeo.io/search-person"
    headers = {
        "X-KEY": api_key,
        "Content-Type": "application/json"
    }
    payload = {
        "page": 1,
        "filters": {
            "company": {"websites": {"include": [domain]}},
            "person_seniority": {"include": ["C-Suite", "Vice President", "Director"]}
        }
    }

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=8)
        
        # Handle active API data gracefully
        if response.status_code == 200:
            return response.json().get("results", [])
        else:
            # Captures 400, 429, or 500 errors safely without terminating the pipeline run
            print(f"  ⚠️ Skipping {domain} safely (API code {response.status_code})")
            return []
    except Exception:
        print(f"  ⚠️ Connection error processing {domain}")
        return []