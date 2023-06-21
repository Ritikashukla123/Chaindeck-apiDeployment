from prometheus_fast_api.models import Node
from prometheus_fast_api.schemas import node
from sqlalchemy.orm import Session,load_only
from sqlalchemy import and_, or_, not_
import json

def get_node(db: Session, user_id: str, node_name: str):
    
    node_name = ''  
    node_data = db.query(Node.Node).filter(and_(Node.Node.user_id == user_id),(Node.Node.node_name == node_name)).first()
    # print(node_data.node_name)
    if node_data is not None:
        node_name = node_data.node_name
        print(node_name)     
    return node_name

def node_name(db: Session, user_id: str):

    node_list= db.query(Node.Node).options(load_only(Node.Node.node_name)).filter(Node.Node.user_id == user_id).all()
    # node_list=(node_list)
    print(node_list)

    return node_list