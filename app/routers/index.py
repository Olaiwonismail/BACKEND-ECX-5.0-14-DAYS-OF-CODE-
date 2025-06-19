from http.client import HTTPException
from fastapi import APIRouter, Depends

from app.auth import get_current_user


router = APIRouter()

@router.get("/user")
def user(user = Depends(get_current_user)):
    
    """Endpoint for regular users."""
    return f"Hello, User {user.username} !"

@router.get("/admin")
def admin(user = Depends(get_current_user)):
    """Admin endpoint."""
    if user.role != "admin":
        return HTTPException(status_code=403, detail="Access denied")
    return f"Hello, Admin {user.username} !"
