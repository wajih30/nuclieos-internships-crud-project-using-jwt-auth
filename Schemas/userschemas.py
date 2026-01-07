from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime



class UserBase(BaseModel):
    name: str
    email:str
    role: str




class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    role: Optional[str] = None




class UserResponse(BaseModel):
    id:int
    name: Optional[str] = None
    email: Optional[str] = None
    created_at: datetime 

    class Config:
        orm_mode= True







class UserCreate(UserBase):
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str


class RefreshTokenRequest(BaseModel):
    refresh_token: str


class RefreshTokenResponse(BaseModel):
    access_token: str
    token_type: str    

class TokenData(BaseModel):
    email: Optional[str] = None
