from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Job

router= APIRouter()

@router.get("/")
def list_jobs(db: Session = Depends(get_db)):
    jobs = db.query(Job).all()
    return jobs




