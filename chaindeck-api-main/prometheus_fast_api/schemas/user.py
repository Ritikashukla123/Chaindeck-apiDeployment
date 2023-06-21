from typing import List, Union
from uuid import UUID
from pydantic import BaseModel, Field, EmailStr, Json


class UserBase(BaseModel):
    email: str




class User(BaseModel):
    email: EmailStr
    password: str
    name: str
    age: int
    country: str


class UserCreate(UserBase):
    email: EmailStr
    password: str
    name: str
    age: int
    gender: str
    country: str
    user_role: str

class User(UserBase):
    id: int
    class Config:
        orm_mode = True



class UserAuth(BaseModel):
    # email: EmailStr = Field(..., description="user email")
    # password: str = Field(..., min_length=5, max_length=24, description="user password")
    email: EmailStr 
    password: str 
    

class UserOut(BaseModel):
    id: UUID
    email: str

class UserResetPassword(BaseModel):
    token: str
    password: str