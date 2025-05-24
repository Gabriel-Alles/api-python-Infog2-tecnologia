from pydantic import BaseModel, EmailStr
from app.models.user import UserRole


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    role: UserRole = UserRole.USER


class UserLogin(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"



class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    is_admin: bool

    class Config:
        from_attributes = True