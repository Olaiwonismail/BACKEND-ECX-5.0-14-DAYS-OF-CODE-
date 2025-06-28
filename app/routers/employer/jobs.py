from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.auth import get_current_user, require_role
from app.database import get_db
from app.models import Job, Application
from app.schemas import ApplicationResponse, JobCreate, JobResponse

router = APIRouter()

@router.get("/", response_model=list[JobResponse])
def list_employer_jobs(
    db: Session = Depends(get_db),
    employer = Depends(require_role("employer"))
):
    jobs = db.query(Job).filter(Job.posted_by == employer.id).all()
    return jobs

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=JobResponse)
def create_job(
    job: JobCreate,
    employer = Depends(require_role("employer")),
    db: Session = Depends(get_db)
):
    new_job = Job(**job.dict(), posted_by=employer.id)
    
    try:
        db.add(new_job)
        db.commit()
        db.refresh(new_job)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create job"
        )
    
    return new_job

@router.put("/{job_id}", response_model=JobResponse)
def update_job(
    job_id: int,
    job_update: JobCreate,
    db: Session = Depends(get_db),
    employer = Depends(require_role("employer"))
):
    job = db.query(Job).filter(Job.id == job_id).first()
    
    # Validate job existence
    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job not found"
        )
    
    # Validate ownership
    if job.posted_by != employer.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this job"
        )
    
    # Update job fields
    for key, value in job_update.dict().items():
        setattr(job, key, value)
    
    try:
        db.commit()
        db.refresh(job)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update job"
        )
    
    return job

@router.delete("/{job_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_job(
    job_id: int,
    db: Session = Depends(get_db),
    employer = Depends(require_role("employer"))
):
    job = db.query(Job).filter(Job.id == job_id).first()
    
    # Validate job existence
    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job not found"
        )
    
    # Validate ownership
    if job.posted_by != employer.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this job"
        )
    
    try:
        db.delete(job)
        db.commit()
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete job"
        )

@router.get("/{job_id}/applications", response_model=list[ApplicationResponse])
def get_job_applications(
    job_id: int,
    db: Session = Depends(get_db),
    employer = Depends(require_role("employer"))
):
    job = db.query(Job).filter(Job.id == job_id).first()
    
    # Validate job existence
    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job not found"
        )
    
    # Validate ownership
    if job.posted_by != employer.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to view these applications"
        )
    
    return job.applications