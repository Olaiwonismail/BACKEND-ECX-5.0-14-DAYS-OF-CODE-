import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Settings:
    """Application settings loaded from environment variables."""
    PROJECT_NAME: str = os.getenv("APP_NAME")
    PROJECT_VERSION: str = os.getenv("APP_VERSION")
    DATABASE_URL: str = os.getenv("DATABASE_URI")

settings = Settings()
