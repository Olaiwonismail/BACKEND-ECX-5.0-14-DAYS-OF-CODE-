from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.models import create_db_tables
from app.config import settings  


app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.PROJECT_VERSION,
    description="A basic FastAPI project setup"
)

# Add CORS middleware to allow requests from any origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)

# Create database tables if they don't exist
create_db_tables()
# Include the router from app.routers.index
from app.routers.index import router as index
from app.routers.users import router as users
app.include_router(index, prefix="", tags=["index"])
app.include_router(users,prefix="/auth",tags=["auth"])