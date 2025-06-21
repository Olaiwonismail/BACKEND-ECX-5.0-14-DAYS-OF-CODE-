from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Job
from app.schemas import JobResponse, JobSearch

router= APIRouter()

@router.get("/all")
def list_jobs(db: Session = Depends(get_db)):
    jobs = db.query(Job).all()
    return jobs



# response_model=list[JobResponse]
@router.post("/filtered",)
def filter_jobs(filter: JobSearch, db: Session = Depends(get_db)):
    query =db.query(Job)
    if filter.job_type:
        print('jj')
        query = query.filter(Job.job_type == filter.job_type)
    if filter.location:
        print('kk')
        query = query.filter(Job.location == filter.location)
    if filter.min_salary:    
        query = query.filter(Job.salary >= filter.min_salary)
    if filter.max_salary:
        query = query.filter(Job.salary <= filter.max_salary)   
    jobs = query.all()

    return jobs


    # if not jobs:
    #     raise HTTPException(status_code=404, detail="No jobs found for this type")
    # return jobs



