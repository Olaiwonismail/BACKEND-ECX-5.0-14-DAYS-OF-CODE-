from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
   

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

class JobResponse(JobCreate):
    id: int
    posted_by: int

    class Config:
        orm_mode = True    