from sqlalchemy import Column, Float, ForeignKey, Integer, String, Boolean, DateTime
from app.database import Base, engine
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

class User(Base):
    """SQLAlchemy model for a User."""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    role = Column(String, default="user")  
    hashed_password = Column(String)
    jobs = relationship("Job", back_populates="owner")
    jobApplications = relationship("Application", back_populates="applicant")

    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}', email='{self.email}')>"



class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    location = Column(String)
    salary = Column(Float)
    company = Column(String)
    job_type = Column(String)
    posted_by = Column(Integer, ForeignKey("users.id"))
    date_posted = Column(DateTime, default=func.now())     

    owner = relationship("User", back_populates="jobs")
    applicantions = relationship("Application", back_populates="job", cascade="all, delete-orphan")
    
class Application(Base):
    __tablename__ = 'applications'
    id =  Column(Integer, primary_key=True)
    applicantId = Column(Integer,ForeignKey("users.id"))
    jobId = Column(Integer,ForeignKey("jobs.id"))
    resumePath = Column(String)
    coverLetterPath = Column(String)
    submittedAt = Column(DateTime, default=func.now())  

    applicant = relationship("User", back_populates="jobApplications")
    job = relationship("Job", back_populates="applicantions")

# You can add a function to create tables if they don't exist
def create_db_tables():
    """Creates all defined database tables."""
    Base.metadata.create_all(bind=engine) # Use the engine from database.py if not already bound