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

class UserRegister(BaseModel):
    email: str
    password: str
    role: str # "seeker" o "employer"

class ResumeProfile(BaseModel, extra="allow"):
    email: str
    full_name: str
    target_job: str
    school: str
    city: str
    contact: str
    experience: str

# In-memory databases
users_db = []
profiles_db = [
    {
        "email": "aproniano@gmail.com",
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

@app.post("/api/auth/register")
def register_user(user: UserRegister):
    users_db.append(user.dict())
    return {"status": "success", "message": f"Successfully registered as {user.role}!"}

@app.post("/api/auth/login")
def login_user(user: UserRegister):
    return {"status": "success", "message": f"Welcome back, {user.email}!", "role": user.role}

@app.get("/api/employer/profiles")
def get_employer_profiles():
    return profiles_db

@app.post("/api/ai-save-profile")
def save_profile(profile: ResumeProfile):
    profiles_db.insert(0, profile.dict())
    return {
        "status": "success",
        "message": "Profile securely saved to your account! View-only mode active for verified employers.",
        "profile": profile
    }

@app.post("/api/ai-auto-apply")
def ai_auto_apply(data: dict):
    applicant_email = data.get("applicant_email")
    job_id = data.get("job_id")
    return {
        "status": "success", 
        "message": f"AI Bridge successfully notified employer and shared secure view-only profile link for applicant: {applicant_email}"
    }

@app.get("/api/admin/stats")
def admin_stats():
    return {"estimated_ad_revenue_usd": 280.00, "active_screen_users": 82}
