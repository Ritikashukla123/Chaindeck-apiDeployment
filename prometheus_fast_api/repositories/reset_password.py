from prometheus_fast_api.models import ResetPassword
from prometheus_fast_api.schemas import reset_password
from sqlalchemy.orm import Session
import uuid
import base64
# from passlib.hash import cisco_type7
import json



def create_token_user(db: Session, email:str ):
    
    uuid_key = uuid.uuid4()
    # token = str(uuid_key)
    db_user_token = ResetPassword.ResetPassword(email=email )
    db.add(db_user_token)
    db.commit()
    db.refresh(db_user_token)
    return db_user_token

def get_token_user_by_email(db: Session, email: str):
    return db.query(ResetPassword.ResetPassword).filter(ResetPassword.ResetPassword.email == email).first()

def create_token(db: Session, email:str):
     token_to_update = db.query(ResetPassword.ResetPassword).filter(ResetPassword.ResetPassword.email== email).first()
     uuid_key = uuid.uuid4()
     token = str(uuid_key)
     token_to_update.token=token
     db.commit()
     return token

def get_token_user_by_token(db: Session, token: str):
    return db.query(ResetPassword.ResetPassword).filter(ResetPassword.ResetPassword.token == token).first()

def delete_token(db: Session, email:str):
     token_to_delete = db.query(ResetPassword.ResetPassword).filter(ResetPassword.ResetPassword.email== email).first()
     token = None
     token_to_delete.token=token
     db.commit()
     return token_to_delete.token