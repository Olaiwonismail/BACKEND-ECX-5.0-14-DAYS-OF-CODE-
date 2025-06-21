from typing import Optional
from pydantic import BaseModel, EmailStr
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

class JobSearch(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    location: Optional[str] = None
    min_salary: Optional[float] = None
    max_salary: Optional[float] = None
    company:Optional[str] = None
    job_type: Optional[JobType] = None


    class Config:
        orm_mode = True 
