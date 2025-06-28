import uuid
import os
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from app.auth import require_role
from app.database import get_db
from app.models import Application, Job
from sqlalchemy.orm import Session
from app.schemas import ApplicationCreate

router = APIRouter()

# Configurations
UPLOAD_DIR_RESUME = os.getenv("UPLOAD_DIR_RESUME", "uploads/resumes")
UPLOAD_DIR_COVER_LETTER = os.getenv("UPLOAD_DIR_COVER_LETTER", "uploads/cover_letters")
ALLOWED_EXTENSIONS = {".pdf", ".doc", ".docx"}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB

# Create upload directories
os.makedirs(UPLOAD_DIR_RESUME, exist_ok=True)
os.makedirs(UPLOAD_DIR_COVER_LETTER, exist_ok=True)

def sanitize_filename(filename: str) -> str:
    return os.path.basename(filename)

async def validate_and_save_upload(file: UploadFile, directory: str) -> str:
    # Validate file extension
    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only PDF, DOC, and DOCX files are allowed"
        )
    
    # Read file content
    contents = await file.read()
    
    # Validate file size
    if len(contents) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File too large. Max size is {MAX_FILE_SIZE // (1024 * 1024)}MB"
        )
    
    # Generate unique filename
    unique_filename = f"{uuid.uuid4()}{ext}"
    file_path = os.path.join(directory, unique_filename)
    
    # Save file
    with open(file_path, "wb") as buffer:
        buffer.write(contents)
    
    return file_path

@router.post("/", status_code=status.HTTP_201_CREATED)
async def apply_for_job(
    application: int,
    db: Session = Depends(get_db),
    user = Depends(require_role("applicant")),
    resume: UploadFile = File(...),
    cover_letter: UploadFile = File(...)
):
    # Check job exists
    job = db.query(Job).filter(Job.id == application).first()
    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job not found"
        )
    
    # Prevent duplicate applications
    existing_application = db.query(Application).filter(
        Application.applicant_id == user.id,
        Application.job_id == application
    ).first()
    
    if existing_application:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You have already applied for this job"
        )
    
    # Process files
    resume_path = await validate_and_save_upload(resume, UPLOAD_DIR_RESUME)
    cover_path = await validate_and_save_upload(cover_letter, UPLOAD_DIR_COVER_LETTER)
    
    # Create application
    new_application = Application(
        applicant_id=user.id,
        job_id=application,
        resume_path=resume_path,
        cover_letter_path=cover_path
    )
    
    try:
        db.add(new_application)
        db.commit()
        db.refresh(new_application)
    except Exception as e:
        # Clean up files if DB operation fails
        for path in [resume_path, cover_path]:
            if os.path.exists(path):
                os.remove(path)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to submit application"
        )
    
    return {
        "message": "Application submitted successfully",
        "application_id": new_application.id
    }