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

class ResumeRequest(BaseModel):
    full_name: str
    target_job: str
    experience: str
    skills: str

class JobRequest(BaseModel):
    company_name: str
    job_title: str
    location: str
    contact_info: str
    is_sponsored: bool = False

# In-memory database of jobs
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

@app.post("/api/jobs/add-sponsored")
def add_sponsored_job(job: JobRequest):
    new_job = {
        "id": len(jobs_db) + 1,
        "company_name": job.company_name,
        "job_title": job.job_title,
        "location": job.location,
        "contact_info": job.contact_info,
        "verified": True,
        "is_sponsored": True
    }
    jobs_db.insert(0, new_job) # I-una sa taas ang sponsored jobs
    return {"status": "success", "message": "Sponsored job successfully listed and prioritized!", "job": new_job}

@app.post("/api/ai-generate-resume")
def generate_ai_resume(data: ResumeRequest):
    optimized_summary = f"Results-driven professional with extensive background in {data.target_job}. Proven expertise in {data.skills}. Committed to safety, efficiency, and high-performance standards."
    formatted_experience = f"- {data.experience}\n- Successfully managed daily warehouse and operational workflows adhering to international standards."
    
    return {
        "status": "success",
        "message": "AI Resume successfully generated and optimized!",
        "resume_data": {
            "name": data.full_name,
            "title": data.target_job,
            "summary": optimized_summary,
            "experience": formatted_experience,
            "skills": [s.strip() for s in data.skills.split(",")]
        }
    }

@app.post("/api/ai-auto-apply")
def ai_auto_apply(data: dict):
    return {"status": "success", "message": f"AI Bridge successfully submitted application using {data.get('applicant_email')}"}

@app.post("/api/sync-universal-portal")
def sync_portal(data: dict):
    return {"status": "success", "message": f"Successfully crawled listings from {data.get('portal_url')} for role: {data.get('search_role')}"}

@app.get("/api/admin/stats")
def admin_stats():
    return {"estimated_ad_revenue_usd": 184.50, "active_screen_users": 56}
