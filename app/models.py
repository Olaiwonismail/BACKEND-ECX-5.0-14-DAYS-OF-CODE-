from sqlalchemy import Column, Float, ForeignKey, Integer, String, DateTime, CheckConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base, engine

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    role = Column(String(20), nullable=False)
    hashed_password = Column(String(128), nullable=False)
    
    jobs = relationship("Job", back_populates="owner")
    applications = relationship("Application", back_populates="applicant")
    
    __table_args__ = (
        CheckConstraint(role.in_(["employer", "applicant"]), name="valid_role"),
    )

class Job(Base):
    __tablename__ = "jobs"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False)
    description = Column(String(2000), nullable=False)
    location = Column(String(100), nullable=False)
    salary = Column(Float, nullable=False)
    company = Column(String(100), nullable=False)
    job_type = Column(String(20), nullable=False)
    posted_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    date_posted = Column(DateTime, default=func.now())
    
    owner = relationship("User", back_populates="jobs")
    applications = relationship("Application", back_populates="job")

class Application(Base):
    __tablename__ = "applications"
    
    id = Column(Integer, primary_key=True)
    applicant_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    job_id = Column(Integer, ForeignKey("jobs.id"), nullable=False)
    resume_path = Column(String(200), nullable=False)
    cover_letter_path = Column(String(200), nullable=False)
    submitted_at = Column(DateTime, default=func.now())
    status = Column(String(20), default="pending")
    
    applicant = relationship("User", back_populates="applications")
    job = relationship("Job", back_populates="applications")
    
    __table_args__ = (
        CheckConstraint(status.in_(["pending", "reviewed", "rejected", "hired"]), 
                       name="valid_status"),
    )

def create_db_tables():
    """Creates all defined database tables."""
    Base.metadata.create_all(bind=engine)     