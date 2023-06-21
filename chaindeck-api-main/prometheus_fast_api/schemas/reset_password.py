from typing import List, Union
from uuid import UUID
from pydantic import BaseModel, Field, EmailStr, Json


class TokenBase(BaseModel):
    email: str

class TokenCreate(TokenBase):
    email: str
    # token: str
