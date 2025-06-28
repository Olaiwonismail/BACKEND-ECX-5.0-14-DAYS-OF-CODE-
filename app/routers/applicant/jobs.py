from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi_pagination import Page,Params
from fastapi_pagination.ext.sqlalchemy import paginate

from app.auth import require_role
from app.database import get_db
from app.models import Job, Application
from app.schemas import JobResponse, JobSearch, JobSortBy, SortOrder, ApplicationResponse

router = APIRouter()

@router.get("/", response_model=Page[JobResponse])
def list_all_jobs(
    db: Session = Depends(get_db),
    params: Params = Depends()
):
    return paginate(db.query(Job).order_by(Job.date_posted.desc()), params)

@router.post("/search", response_model=Page[JobResponse])
def search_jobs(
    filters: JobSearch,
    db: Session = Depends(get_db),
    params: Params = Depends()
):
    query = db.query(Job)
    
    # Apply filters
    if filters.job_type:
        query = query.filter(Job.job_type == filters.job_type)
    if filters.location:
        query = query.filter(Job.location.ilike(f"%{filters.location}%"))
    if filters.min_salary:
        query = query.filter(Job.salary >= filters.min_salary)
    if filters.max_salary:
        query = query.filter(Job.salary <= filters.max_salary)
    
    # Apply sorting
    if filters.sortBy:
        sort_column = None
        if filters.sortBy == JobSortBy.date_posted:
            sort_column = Job.date_posted
        elif filters.sortBy == JobSortBy.salary:
            sort_column = Job.salary
        
        if sort_column:
            sort_method = sort_column.desc() if filters.sortOrder == SortOrder.desc else sort_column.asc()
            query = query.order_by(sort_method)
    else:
        query = query.order_by(Job.date_posted.desc())
    
    return paginate(query, params)

@router.get("/{job_id}", response_model=JobResponse)
def get_job_details(job_id: int, db: Session = Depends(get_db)):
    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job

@router.get("/me/applications", response_model=List[ApplicationResponse])
def get_user_applications(
    db: Session = Depends(get_db),
    user = Depends(require_role("applicant"))
):
    return user.applications