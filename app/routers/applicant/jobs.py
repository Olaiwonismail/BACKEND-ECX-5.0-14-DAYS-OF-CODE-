from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi_pagination import Page, Params,paginate

from app.database import get_db
from app.models import Job
from app.schemas import JobResponse, JobSearch, JobSortBy, SortOrder

router= APIRouter()

@router.get("/all")
def list_jobs(db: Session = Depends(get_db),params: Params = Depends()):
    jobs = db.query(Job).all()
    return paginate(jobs, params)



#
@router.post("/filtered", response_model=Page[JobResponse])
def filter_jobs(filter: JobSearch, db: Session = Depends(get_db)
                ,params: Params = Depends()
                ):
    query =db.query(Job)
    if filter.job_type:
        # print('jj')
        query = query.filter(Job.job_type == filter.job_type)
    if filter.location:
        # print('kk')
        query = query.filter(Job.location == filter.location)
    if filter.min_salary:    
        query = query.filter(Job.salary >= filter.min_salary)
    if filter.max_salary:
        query = query.filter(Job.salary <= filter.max_salary)   
    if filter.sortBy:
        sort_column = None
        if filter.sortBy == JobSortBy.date_posted:
            sort_column = Job.date_posted
        elif filter.sortBy == JobSortBy.salary:
            sort_column = Job.salary
        if sort_column:
            if filter.sortOrder == SortOrder.desc:
                query = query.order_by(sort_column.desc())
            else: # Defaults to asc if not 'desc'
                query = query.order_by(sort_column.asc())

     # Default sorting if no sortBy is provided (e.g., by most recent)
    else:
        # If no explicit sort, always sort by date_posted descending
        query = query.order_by(Job.date_posted.desc())          

    return paginate(query.all(), params)


    # if not jobs:
    #     raise HTTPException(status_code=404, detail="No jobs found for this type")
    # return jobs



