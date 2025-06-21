from fastapi import APIRouter, HTTPException, status
from fastapi.params import Depends

from app.auth import get_current_user, require_role
from app.database import get_db
from app.models import Job
from app.schemas import JobCreate, JobResponse


router = APIRouter()

@router.get("/", response_model=list[JobResponse])
def list_jobs(db = Depends(get_db), employer = Depends(require_role("employer"))):
    """
    List all job postings for the employer.
    """
    jobs = db.query(Job).filter(Job.posted_by == employer.id).all()
    if not jobs:
        raise HTTPException(status_code=404, detail="No jobs found for this employer")
    return jobs
    

@router.post("/create_jobs",status_code=status.HTTP_201_CREATED, response_model=JobResponse)
def create_jobs(job: JobCreate,
                
                # employer = Depends(require_role("employer")),
                db=Depends(get_db),
                
                ):
    """
    Create a new job posting.
    """
    new_job = Job(**job.dict(), posted_by=1)
    db.add(new_job)
    db.commit()
    db.refresh(new_job)
    return new_job


@router.put("/{job_id}", response_model=JobResponse)
def update_job(
    job_id: int,
    job_update: JobCreate,
    db = Depends(get_db),
    employer = Depends(require_role("employer"))
):
    """
    Update Job Postings
    """
    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:  
        raise HTTPException(404, "Job not found")
    if job.posted_by != employer.id:
        raise HTTPException(403, "Not authorized to update this job")
    
    for key, value in job_update.dict().items():
        setattr(job, key, value)

    db.commit()
    db.refresh(job)
    return job

@router.delete("/{job_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_job(
    job_id: int,
    db = Depends(get_db),
    employer = Depends(require_role("employer"))
):
    
    """
    delete a job posting
    """
    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        raise HTTPException(404, "Job not found")
    if job.posted_by != employer.id:
        raise HTTPException(403, "Not authorized to delete this job")
    
    db.delete(job)
    db.commit()
    return "job posting deleted"
