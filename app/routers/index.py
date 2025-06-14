from fastapi import APIRouter


router = APIRouter()

@router.get("/")
def indext():
    """Root endpoint."""
    return "Hello, World!"