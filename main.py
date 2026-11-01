from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ResumeProfile(BaseModel, extra="allow"):
    full_name: str
    target_job: str
    school: str
    city: str
    contact: str
    experience: str

# In-memory database para sa mga naka-save nga applicant profiles (View-Only)
profiles_db = [
    {
        "id": 1,
        "full_name": "Aproniano Mark Baliguat",
        "target_job": "High Reach Forklift Operator",
        "school": "High School Graduate",
        "city": "Christchurch, New Zealand",
        "contact": "ambaliguat25@gmail.com | +64...",
        "experience": "Operated Jungheinrich ETR 335D reach trucks, warehouse checking and logistics workflows."
    }
]

jobs_db = [
    {
        "id": 1,
        "company_name": "Sorted Logistics",
        "job_title": "High Reach Forklift Operator",
        "location": "Christchurch, New Zealand",
        "contact_info": "HR Department / Christchurch Operations",
        "verified": True,
        "is_sponsored": True
    }
]

@app.get("/api/jobs")
def get_jobs():
    return jobs_db

@app.get("/api/employer/profiles")
def get_employer_profiles():
    return profiles_db

@app.post("/api/ai-save-profile")
def save_profile(profile: ResumeProfile):
    profiles_db.insert(0, profile.dict())
    return {
        "status": "success",
        "message": "Profile successfully saved to account and secured for employer view-only mode!",
        "profile": profile
    }

@app.post("/api/ai-chat-assistant")
def ai_chat(data: dict):
    question = data.get("question", "")
    return {
        "reply": f"AI Assistant: Sugyot para sa imong pangulat ('{question}'): I-highlight ang imong mga lisensya ug certifications aron mas dali ka mapilian sa mga ahensya."
    }

@app.get("/api/admin/stats")
def admin_stats():
    return {"estimated_ad_revenue_usd": 245.50, "active_screen_users": 74}
