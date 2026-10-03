from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from backend.config import COOKIE_NAME, COOKIE_SAMESITE, COOKIE_SECURE, ACCESS_TOKEN_EXPIRE_MINUTES
from backend.database import get_db
from backend.models.user import User
from backend.schemas.auth import UserRegister, UserLogin, UserOut, TokenResponse
from backend.services.auth_service import (
    get_user_by_email,
    get_user_by_username,
    create_user,
    authenticate_user,
    create_access_token,
)
from backend.middleware.auth import get_current_user

router = APIRouter(prefix="/api/auth", tags=["auth"])

def set_auth_cookie(response: Response, token: str):
    max_age_seconds = ACCESS_TOKEN_EXPIRE_MINUTES * 60
    response.set_cookie(
        key=COOKIE_NAME,
        value=token,
        httponly=True,
        samesite=COOKIE_SAMESITE,
        secure=COOKIE_SECURE,
        max_age=max_age_seconds,
        path="/"
    )

@router.post("/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
def register(data: UserRegister, response: Response, db: Session = Depends(get_db)):
    if get_user_by_email(db, data.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email is already registered"
        )
    if get_user_by_username(db, data.username):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username is already taken"
        )
    if len(data.password) < 6:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password must be at least 6 characters"
        )

    user = create_user(
        db,
        email=data.email,
        username=data.username,
        password=data.password,
        display_name=data.display_name
    )

    token = create_access_token(data={"sub": str(user.id), "username": user.username})
    set_auth_cookie(response, token)

    return TokenResponse(
        access_token=token,
        token_type="bearer",
        user=UserOut.model_validate(user)
    )

@router.post("/login", response_model=TokenResponse)
def login(data: UserLogin, response: Response, db: Session = Depends(get_db)):
    user = authenticate_user(db, data.username_or_email, data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username/email or password"
        )

    token = create_access_token(data={"sub": str(user.id), "username": user.username})
    set_auth_cookie(response, token)

    return TokenResponse(
        access_token=token,
        token_type="bearer",
        user=UserOut.model_validate(user)
    )

@router.post("/logout")
def logout(response: Response):
    response.delete_cookie(key=COOKIE_NAME, path="/")
    return {"message": "Successfully logged out"}

@router.get("/me", response_model=UserOut)
def me(current_user: User = Depends(get_current_user)):
    return UserOut.model_validate(current_user)
