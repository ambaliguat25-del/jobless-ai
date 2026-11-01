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

class ResumeProfile(BaseModel):
    full_name: str
    target_job: str
    school: str
    city: str
    state: str
    email: str
    phone: str
    education: str
    achievements: str
    skills: str
    experience: str

class JobRequest(BaseModel):
    company_name: str
    job_title: str
    location: str
    contact_info: str
    is_sponsored: bool = False

jobs_db = [
    {
        "id": 1,
        "company_name": "Sorted Logistics",
        "job_title": "High Reach Forklift Operator",
        "location": "Christchurch, New Zealand",
        "contact_info": "HR Department / Christchurch Operations",
        "verified": True,
        "is_sponsored": True
    },
    {
        "id": 2,
        "company_name": "International Pharmaceuticals, Inc. (IPI)",
        "job_title": "Warehouse Checker & Reach Truck Operator",
        "location": "Mandaue City, Cebu, Philippines",
        "contact_info": "careers@ipi.ph",
        "verified": True,
        "is_sponsored": False
    }
]

@app.get("/api/jobs")
def get_jobs():
    return jobs_db

@app.post("/api/ai-save-profile")
def save_profile(profile: ResumeProfile):
    return {
        "status": "success",
        "message": "Digital Resume Profile successfully saved and optimized for employers to view securely online!",
        "profile": profile
    }

@app.post("/api/ai-chat-assistant")
def ai_chat(data: dict):
    question = data.get("question", "")
    return {
        "reply": f"AI Assistant: Sugyot para sa imong pangutana ('{question}'): Ibutang ang imong konkretong kasinatian ug pamatud-i sa soft skills aron mas dali ka mapilian sa mga employer!"
    }

@app.post("/api/ai-auto-apply")
def ai_auto_apply(data: dict):
    return {"status": "success", "message": f"AI Bridge successfully submitted online resume profile using {data.get('applicant_email')}"}

@app.get("/api/admin/stats")
def admin_stats():
    return {"estimated_ad_revenue_usd": 210.40, "active_screen_users": 68}
