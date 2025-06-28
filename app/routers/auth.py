from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.models import User
from app.auth import ACCESS_EXPIRE_MINUTES, create_token, create_tokens, decode_token, hash_password, verify_password
from app.database import get_db
from app.schemas import UserCreate, UserLogin, UserResponse

router = APIRouter()

@router.post("/signup", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def signup(user: UserCreate, db: Session = Depends(get_db)):
    # Check for existing username
    if db.query(User).filter(User.username == user.username).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already taken"
        )
    
    # Check for existing email
    if db.query(User).filter(User.email == user.email).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create new user
    hashed = hash_password(user.password)
    new_user = User(
        email=user.email,
        username=user.username,
        role=user.role,
        hashed_password=hashed
    )
    
    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create user"
        )
    
    return new_user

@router.post("/login")
async def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    
    # Validate credentials
    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return create_tokens(db_user.email)


@router.post("/refresh")
def refresh_token(refresh_token: str):
    payload = decode_token(refresh_token)
    
    if payload.get("type") != "refresh":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token type"
        )
    
    email = payload.get("sub")
    access_token = create_token(
        {"sub": email, "type": "access"},
        timedelta(minutes=ACCESS_EXPIRE_MINUTES)
    )
    return {"access_token": access_token}