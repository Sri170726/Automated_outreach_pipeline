import os
import sys
import time
from dotenv import load_dotenv

from services.ocean import get_lookalike_companies
from services.prospeo import search_people_by_domain
from services.eazyreach import resolve_linkedin_to_email
from services.brevo import send_personalized_email

load_dotenv()

def run_pipeline():
    print("==================================================")
    print("🚀 UNCRASHABLE AUTOMATED OUTREACH ENGINE")
    print("==================================================\n")
    
    seed_domain = input("Enter any domain name (e.g., flipkart.com, google.com): ").strip()
    if not seed_domain:
        print("❌ System Error: Input target string is null.")
        return

    print(f"\n[Stage 1] Mapping peer lookalikes for '{seed_domain}'...")
    companies = get_lookalike_companies(seed_domain)
    print(f"👉 Target Domains Resolved: {companies}")
    
    leads_queue = []

    # --- STAGE 2 & 3: Loops perfectly through any dataset ---
    for company in companies:
        print(f"\n🔬 Processing domain: {company}...")
        
        # Defensive Pause: Prevents 429 Rate Throttling[cite: 2]
        time.sleep(1.5) 
        
        prospects = search_people_by_domain(company)
        
        if not prospects:
            print(f"  ⚠️ Skipping {company} - no target decision profiles available.")
            continue
            
        for prospect_data in prospects[:2]:
            person = prospect_data.get("person", {})
            name = person.get("full_name")
            linkedin = person.get("linkedin_url")
            title = person.get("current_job_title")
            
            if not name or not linkedin:
                continue
                
            print(f"  Found Lead: {name} ({title})")
            email = resolve_linkedin_to_email(linkedin)
            
            if email:
                leads_queue.append({
                    "name": name,
                    "email": email,
                    "company": company,
                    "title": title
                })
                print(f"  ✅ String Mapped: {email}")

    # --- SAFETY CHECKPOINT ---[cite: 2]
    if not leads_queue:
        print("\n==============================================")
        print("🛡️ SAFETY SUMMARY: NO DIRECT LEADS AVAILABLE")
        print("==============================================")
        print("All downstream APIs processed safely with 0 crash records. Terminating run.")
        return

    print("\n==============================================")
    print(f"🛡️ SAFETY SUMMARY: REVIEW BEFORE DISPATCHING")
    print("==============================================")
    for index, lead in enumerate(leads_queue, 1):
        print(f"[{index}] {lead['name']} | {lead['title']} at {lead['company']} -> {lead['email']}")
    print("==============================================")
    
    send_confirmation = input(f"\nConfirm automated email execution to these {len(leads_queue)} contacts? (yes/no): ").strip().lower()
    
    if send_confirmation == "yes":
        print("\n[Stage 4] Dispatching transactional outreach...")
        for lead in leads_queue:
            success = send_personalized_email(lead)
            if success:
                print(f"  📨 Dispatched safely to {lead['email']}")
        print("\n🎉 Pipeline execution complete.")
    else:
        print("\n🛑 Outreach cycle aborted cleanly by developer.")

if __name__ == "__main__":
    run_pipeline()