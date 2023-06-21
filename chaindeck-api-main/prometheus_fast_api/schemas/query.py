from typing import List, Union
from uuid import UUID
from pydantic import BaseModel, Field, EmailStr,Json


class QueryBase(BaseModel):
    query: str = Field(allow_mutation=True)