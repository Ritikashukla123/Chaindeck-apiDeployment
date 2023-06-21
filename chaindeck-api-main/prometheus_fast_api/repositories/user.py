from prometheus_fast_api.models import User
from prometheus_fast_api.schemas import user
from sqlalchemy.orm import Session
import uuid
import base64
# from passlib.hash import cisco_type7
import json

def get_user(db: Session, user_id: int):
    return db.query(User.User).filter(User.User.id == user_id).first()
    


def get_user_by_email(db: Session, email: str):
    return db.query(User.User).filter(User.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(User.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: user.UserCreate, hashed_password: str, user_role: str):
    fake_hashed_password = hashed_password
    # uuid_key = uuid.uuid4()
    # api_key = str(uuid_key)
    # plain_password=cisco_type7.hash(plain_password)
    print(id)
    print(user_role)
    user_role=json.dumps(user_role)
    db_user = User.User(email=user.email, hashed_password=fake_hashed_password, name=user.name, age=user.age, country=user.country, gender=user.gender, user_role=user_role)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_password(db: Session, password:str, email:str):
     password_to_update = db.query(User.User).filter(User.User.email== email).first()
     password_to_update.hashed_password=password
     db.commit()
     return password_to_update
