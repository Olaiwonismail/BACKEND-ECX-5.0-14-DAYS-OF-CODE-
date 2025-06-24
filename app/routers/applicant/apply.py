import uuid
from fastapi import APIRouter,Depends, File, HTTPException, UploadFile
from app.auth import require_role
from app.database import get_db
from app.models import Application
from app.schemas import  ApplicationModel
import os,dotenv 
dotenv.load_dotenv()


router = APIRouter()


UPLOAD_DIR_RESUME = os.getenv("UPLOAD_DIR_RESUME")
UPLOAD_DIR_COVER_LETTER = os.getenv("UPLOAD_DIR_COVER_LETTER")
ALLOWED_EXTENSIONS = os.getenv('ALLOWED_EXTENSIONS')
MAX_FILE_SIZE = 10 * 1024 * 1024
# create folder if it doesn't exist

os.makedirs(UPLOAD_DIR_COVER_LETTER, exist_ok=True)
os.makedirs(UPLOAD_DIR_RESUME, exist_ok=True)




async def validate_upload(file: UploadFile):
    # ✅ Check extension
 

    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail="Only PDF, DOC, and DOCX files are allowed.")

    # ✅ Check size
    contents = await file.read()
    print('wwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww')
    print(type(MAX_FILE_SIZE))
    if len(contents) > MAX_FILE_SIZE:
        raise HTTPException(status_code=400, detail="File too large. Max size is 5 MB.")

    






@router.post("/apply")
async def apply(application : int,db = Depends(get_db),user= Depends(require_role("applicant")),resume: UploadFile=File(...), coverLetter: UploadFile=File(...)):
    """
    Apply for a job
    ---
    responses:
      200:
        description: Application successful
      400:
        description: Bad request
    """
    if db.query(Application).filter(
        Application.applicantId == user.id ,
        Application.jobId==application
        ).all():
        raise HTTPException(status_code=400, detail="You have already applied for this job")
    
    await validate_upload(resume)
    await validate_upload(coverLetter)

    unique_filename_resume = f"{uuid.uuid4()}"
    unique_filename_cover_letter = f"{uuid.uuid4()}"
    resume_location = os.path.join(UPLOAD_DIR_RESUME, unique_filename_resume)
    cover_letter_location = os.path.join(UPLOAD_DIR_COVER_LETTER, unique_filename_cover_letter)
    
    

    with open(resume_location, "wb") as buffer:
        contents = await resume.read()
        buffer.write(contents)

    with open(cover_letter_location, "wb") as buffer:
        contents = await coverLetter.read()
        buffer.write(contents)
    
     # to prevent duplicate application 
   
    application = Application(
        applicantId=user.id,
        jobId=application,
        resumePath=resume_location,
        coverLetterPath=cover_letter_location   
    )
    try:
        db.add(application)
        db.commit()
        db.refresh(application)
    except Exception as e:
        return {"error": str(e), "message": "Failed to submit application"}
    return {"message": "Application submitted successfully"}


