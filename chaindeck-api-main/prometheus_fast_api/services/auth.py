from passlib.context import CryptContext
import os
from datetime import datetime, timedelta
from typing import Union, Any
from jose import jwt
from typing import Union, Any
from datetime import datetime
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from prometheus_fast_api.models import get_db
from jose import jwt
from pydantic import ValidationError
from prometheus_fast_api.schemas.auth import TokenPayload
# schemas , SystemUser,User
from sqlalchemy.orm import Session
from .logging import logger
from prometheus_fast_api.models.User import User
from prometheus_fast_api.services.config import JWT_SECRET_KEY,JWT_REFRESH_SECRET_KEY
from fastapi.security import OAuth2PasswordBearer

ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # 30 minutes
REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7 # 7 days
ALGORITHM = "HS256"


password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_hashed_password(password: str) -> str:
    return password_context.hash(password)


def verify_password(password: str, hashed_pass: str) -> bool:
    return password_context.verify(password, hashed_pass)


def create_access_token(subject: Union[str, Any], expires_delta: int = None) -> str:
    if expires_delta is not None:
        expires_delta = datetime.utcnow() + expires_delta
    else:
        expires_delta = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode = {"exp": expires_delta, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, ALGORITHM)
    return encoded_jwt

def create_refresh_token(subject: Union[str, Any], expires_delta: int = None) -> str:
    if expires_delta is not None:
        expires_delta = datetime.utcnow() + expires_delta
    else:
        expires_delta = datetime.utcnow() + timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)
    
    to_encode = {"exp": expires_delta, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, JWT_REFRESH_SECRET_KEY, ALGORITHM)
    return encoded_jwt



reuseable_oauth = OAuth2PasswordBearer(
    tokenUrl="/login",
   # scheme_name="JWT"
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")  # use token authentication





async def get_current_user(db: Session=Depends(get_db),token: str = Depends(reuseable_oauth)) -> User:
   
    try:
        logger.info("{}".format(token))

        payload = jwt.decode(
            token, JWT_SECRET_KEY, algorithms=[ALGORITHM]
        )
        token_data = TokenPayload(**payload)
        logger.info(token_data)
        logger.info(payload)
        if datetime.fromtimestamp(token_data.exp) < datetime.now():
            raise HTTPException(
                status_code = status.HTTP_401_UNAUTHORIZED,
                detail="Token expired",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except(jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
   # user= db.select(token_data.sub, None)
    user = db.query(User).filter(User.email == token_data.sub).first()
    
    
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Could not find user",
        )
    logger.info(user)
    return (user)