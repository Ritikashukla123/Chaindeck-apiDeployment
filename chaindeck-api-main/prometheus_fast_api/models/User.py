from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy_utils import EmailType
from prometheus_fast_api.models.common import Base
from uuid import UUID
from sqlalchemy import ARRAY
# from prometheus_fast_api.models import Event

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    # api_key = Column(String)
    # is_active = Column(Boolean, default=True)
    name = Column(String)
    age = Column(Integer)
    gender = Column(String)
    country = Column(String)
    # plain_password = Column(String)
    # username = Column(String)
    user_role = Column(String)

    # events = relationship("Event", back_populates="owner")
    # cart = relationship("Cart", back_populates="User")
    #order_user = relationship("Order", back_populates="order_user")