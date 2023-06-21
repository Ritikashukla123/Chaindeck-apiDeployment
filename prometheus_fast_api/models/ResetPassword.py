from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import relationship
from prometheus_fast_api.models.common import Base

class ResetPassword(Base):
    __tablename__ = "reset_password"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True)
    token = Column(String)