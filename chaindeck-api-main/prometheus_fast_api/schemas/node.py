from pydantic import BaseModel

class Node(BaseModel):
    query: str
    start_time: str
    end_time: str
    step: str



class TokenSchema(BaseModel):
    access_token: str
    refresh_token: str
    
    
class TokenPayload(BaseModel):
    sub: str = None
    exp: int = None

