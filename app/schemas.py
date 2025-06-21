from typing import Optional
from pydantic import BaseModel, EmailStr, Field
from pyparsing import Enum


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    role: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    username: str
    email: EmailStr
    role: str

    class Config:
        orm_mode = True

class JobCreate(BaseModel):
    title: str
    description: str
    location: str
    salary: float
    company: str
    job_type: str
    

class JobResponse(JobCreate):
    id: int
    posted_by: int

    class Config:
        orm_mode = True    

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

class JobSearch(BaseModel):
   
    location: Optional[str] = None
    min_salary: Optional[float] = None
    max_salary: Optional[float] = None
    job_type: Optional[JobType] = None
    date_posted: Optional[str] = None  # ISO 8601 date string
    sortBy: Optional[JobSortBy] = Field(None, description="Field to sort by (e.g., date_posted, salary, title)")
    sortOrder: Optional[SortOrder] = Field(SortOrder.desc, description="Sort order (asc or desc). Defaults to 'desc'.")
    

    class Config:
        orm_mode = True 
