from fastapi import FastAPI, HTTPException, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.models import create_db_tables
from app.config import settings
from fastapi_pagination import add_pagination
import os

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.PROJECT_VERSION,
    description="Job Application Platform API"
)

# CORS Configuration
origins = os.getenv("ALLOWED_ORIGINS", "*").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create database tables
create_db_tables()

# Global exception handler
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Internal server error"},
    )

# Include routers
from app.routers.index import router as health_router
from app.routers.auth import router as auth_router
from app.routers.employer.jobs import router as employer_jobs_router
from app.routers.applicant.jobs import router as job_search_router
from app.routers.applicant.apply import router as application_router

app.include_router(health_router, prefix="", tags=["System Health"])
app.include_router(auth_router, prefix="/auth", tags=["Authentication"])
app.include_router(employer_jobs_router, prefix="/employer/jobs", tags=["Employer - Job Management"])
app.include_router(job_search_router, prefix="/jobs", tags=["Job Search"])
app.include_router(application_router, prefix="/applicant", tags=["Applicant - Applications"])


add_pagination(app)