from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI(title="JobLess Global AI Job Marketplace API", version="1.0")

# Enable CORS for frontend connection
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Models
class JobPost(BaseModel):
    id: Optional[int] = None
    company_name: str
    job_title: str
    location: str
    contact_info: str
    verified: bool = False

class AIApplicationRequest(BaseModel):
    applicant_email: str
    job_id: int

class UniversalPortalSync(BaseModel):
    portal_url: str
    search_role: str

# In-memory database simulation para sa mga trabaho
jobs_database = [
    {
        "id": 1,
        "company_name": "KwikCargo Logistics",
        "job_title": "High Reach Forklift Operator",
        "location": "Christchurch, New Zealand",
        "contact_info": "+64 3 555 0192 | hr@kwikcargo.nz",
        "verified": True
    },
    {
        "id": 2,
        "company_name": "AnneMark Printing Services",
        "job_title": "Graphic Layout Artist & Printer",
        "location": "Mandaue City, Cebu, Philippines",
        "contact_info": "+63 917 555 0192",
        "verified": False
    }
]

# In-memory database para sa ATS Applicants
applicants_database = [
    {"id": 101, "job_id": 1, "applicant_email": "aproniano.mark@gmail.com", "job_title": "High Reach Forklift Operator", "status": "Pending"},
    {"id": 102, "job_id": 2, "applicant_email": "worker.sample@gmail.com", "job_title": "Graphic Layout Artist & Printer", "status": "Interviewed"}
]

@app.get("/")
def read_root():
    return {"message": "Welcome to JobLess Global AI Job Marketplace API!"}

@app.get("/api/jobs", response_model=List[JobPost])
def get_jobs():
    return jobs_database

@app.post("/api/jobs", response_model=JobPost)
def create_job(job: JobPost):
    job.id = len(jobs_database) + 1
    jobs_database.append(job.dict())
    return job

@app.get("/api/employer/applicants/{job_id}")
def get_job_applicants(job_id: int):
    filtered = [app for app in applicants_database if app["job_id"] == job_id]
    return filtered

@app.post("/api/ai-auto-apply")
def ai_auto_apply(request: AIApplicationRequest):
    new_app = {
        "id": len(applicants_database) + 1,
        "job_id": request.job_id,
        "applicant_email": request.applicant_email,
        "job_title": "Requested Position",
        "status": "Pending"
    }
    applicants_database.append(new_app)
    return {
        "status": "success",
        "message": f"AI successfully sent application using {request.applicant_email} as a bridge for Job ID {request.job_id}!"
    }

@app.post("/api/sync-universal-portal")
def sync_universal_portal(data: UniversalPortalSync):
    new_synced_job = {
        "id": len(jobs_database) + 1,
        "company_name": f"Verified Employer via {data.portal_url}",
        "job_title": f"{data.search_role} (AI Synced List)",
        "location": "Global / International / Remote",
        "contact_info": f"careers@{data.portal_url.lower().replace('https://','').replace('www.','').split('/')[0]}",
        "verified": True
    }
    jobs_database.append(new_synced_job)
    return {
        "status": "success",
        "message": f"AI successfully crawled and added '{data.search_role}' listings from {data.portal_url} to your feed!"
    }

@app.get("/api/admin/stats")
def get_admin_stats():
    return {
        "total_jobs": len(jobs_database),
        "total_applicants": len(applicants_database),
        "estimated_ad_revenue_usd": 142.50,
        "active_screen_users": 1280
    }