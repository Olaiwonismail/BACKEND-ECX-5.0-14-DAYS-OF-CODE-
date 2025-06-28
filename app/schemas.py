from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, EmailStr, Field, constr
from enum import Enum

# User Schemas
class UserCreate(BaseModel):
    username: constr(min_length=3, max_length=50)
    email: EmailStr
    password: str
    role: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    role: str

    class Config:
        orm_mode = True

# Job Schemas
class JobCreate(BaseModel):
    title: constr(min_length=3, max_length=100)
    description: constr(min_length=10)
    location: constr(min_length=2, max_length=100)
    salary: float
    company: constr(min_length=2, max_length=100)
    job_type: str

class JobResponse(JobCreate):
    id: int
    posted_by: int
    date_posted: datetime

    class Config:
        orm_mode = True

# Enums
class JobType(str, Enum):
    full_time = "full-time"
    part_time = "part-time"
    contract = "contract"

class JobSortBy(str, Enum):
    date_posted = "date_posted"
    salary = "salary"

class SortOrder(str, Enum):
    asc = "asc"
    desc = "desc"

# Search/Filters
class JobSearch(BaseModel):
    location: Optional[str] = None
    min_salary: Optional[float] = None
    max_salary: Optional[float] = None
    job_type: Optional[JobType] = None
    date_posted: Optional[datetime] = None
    sortBy: Optional[JobSortBy] = None
    sortOrder: Optional[SortOrder] = SortOrder.desc

# Application Schemas
class ApplicationBase(BaseModel):
    job_id: int

class ApplicationCreate(ApplicationBase):
    pass

class ApplicationResponse(BaseModel):
    id: int
    applicant_id: int
    job_id: int
    resume_path: str
    cover_letter_path: str
    submitted_at: datetime
    status: str

    class Config:
        orm_mode = True