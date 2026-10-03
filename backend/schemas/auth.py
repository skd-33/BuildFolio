from typing import Optional
from datetime import datetime
from pydantic import BaseModel, ConfigDict

class UserRegister(BaseModel):
    email: str
    username: str
    password: str
    display_name: Optional[str] = None

class UserLogin(BaseModel):
    username_or_email: str
    password: str

class UserOut(BaseModel):
    id: int
    email: str
    username: str
    display_name: Optional[str] = None
    created_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserOut
