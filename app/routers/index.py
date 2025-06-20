from fastapi import HTTPException
from fastapi import APIRouter, Depends

from app.auth import get_current_user, require_role


router = APIRouter()

@router.get("/user")
def user(user = Depends(get_current_user)):
    
    """Endpoint for regular users."""
    return f"Hello, User {user.username} !"

@router.get("/admin")
def admin(user = Depends(get_current_user),admin = Depends(require_role("employer"))):
    """Admin endpoint."""
    
    return f"Hello, Admin {user.username} !"
