from typing import Optional
from fastapi import Request, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.config import COOKIE_NAME
from backend.database import get_db
from backend.models.user import User
from backend.services.auth_service import decode_access_token, get_user_by_id

def get_token_from_request(request: Request) -> Optional[str]:
    # 1. First priority: httpOnly cookie as requested
    cookie_token = request.cookies.get(COOKIE_NAME)
    if cookie_token:
        return cookie_token

    # 2. Fallback: Authorization header (Bearer <token>)
    auth_header = request.headers.get("Authorization")
    if auth_header and auth_header.startswith("Bearer "):
        return auth_header.split(" ", 1)[1].strip()

    return None

def get_current_user(
    request: Request,
    db: Session = Depends(get_db)
) -> User:
    token = get_token_from_request(request)
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required"
        )

    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )

    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token missing user identity"
        )

    try:
        user_id_int = int(user_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid user identity format"
        )

    user = get_user_by_id(db, user_id_int)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )

    return user

def get_optional_current_user(
    request: Request,
    db: Session = Depends(get_db)
) -> Optional[User]:
    try:
        return get_current_user(request, db)
    except HTTPException:
        return None
