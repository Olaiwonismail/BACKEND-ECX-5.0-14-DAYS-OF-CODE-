from fastapi import APIRouter, Depends
from app.auth import get_current_user, require_role

router = APIRouter()

@router.get("/user")
def user_route(user = Depends(require_role("applicant"))):
    return {"message": f"Hello, Applicant {user.username}!"}

@router.get("/admin")
def admin_route(user = Depends(require_role("employer"))):
    return {"message": f"Hello, Employer {user.username}!"}