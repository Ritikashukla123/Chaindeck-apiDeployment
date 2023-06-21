from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import relationship
from prometheus_fast_api.models.common import Base
# from prometheus_fast_api.models import Event

class Node(Base):
    __tablename__ = "nodes"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, index=True)
    # node_id = Column(String)
    node_name = Column(String)
   
   
   
    # is_active = Column(Boolean, default=True)
    # prometheus_url = Column(String)
    
    # events = relationship("Event", back_populates="owner")