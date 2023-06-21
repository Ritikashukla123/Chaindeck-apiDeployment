from typing import List, Union
from datetime import datetime, timedelta
from urllib import response
from fastapi import Depends, FastAPI, HTTPException, Header, status 
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel
from fastapi.responses import RedirectResponse
from uuid import uuid4
import sqlalchemy as db
from fastapi.middleware.cors import CORSMiddleware
import logging
from fastapi import FastAPI, Response
import random
import time
from prometheus_client.core import GaugeMetricFamily, REGISTRY, CounterMetricFamily
from prometheus_api_client.utils import parse_datetime
from datetime import timedelta
import requests
import urllib.request
import os
# from supertokens_python import get_all_cors_headers
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
# from supertokens_python.framework.fastapi import get_middleware
# from prometheus_fast_api.supertokens.jwt_creation import create_jwt
import asyncio
import clickhouse_connect
from prometheus_fast_api.models import User as mduser
from prometheus_fast_api.models import Node as mdnode
from prometheus_fast_api.repositories import user as repo_user
from prometheus_fast_api.repositories import node as repo_node
from prometheus_fast_api.schemas import user
from prometheus_fast_api.schemas import node
from prometheus_fast_api.services import auth as ath
from prometheus_fast_api.models import get_db
from prometheus_fast_api.services.auth import get_current_user
from clickhouse_driver import Client
from prometheus_fast_api.schemas import query as click_house_query
from prometheus_api_client import PrometheusConnect
from fastapi.exceptions import RequestValidationError
from typing import Annotated
import json
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from uuid import UUID
import base64
from prometheus_fast_api.models import ResetPassword as mdresetpassword
from prometheus_fast_api.schemas import reset_password as reset_password_schema
from prometheus_fast_api.repositories import reset_password as repo_reset_password
# from passlib.hash import cisco_type7
from prometheus_fast_api.services.config import PROMETHEUS_URL,CLICKHOUSE_PASSWORD,CLICKHOUSE_URL,CLICKHOUSE_USER,API_URL

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "*",
        "http://localhost:3000",
        "https://localhost:3000"
    ],
    allow_credentials=True,
    allow_methods=["GET", "PUT", "POST", "DELETE", "OPTIONS", "PATCH"],
    allow_headers=["Content-Type","Access-Control-Allow-Origin", "application/json", "node-id","*"],
)

PROMETHEUS_URL = os.environ['PROMETHEUS_URL'] 
CLICKHOUSE_URL = os.environ['CLICKHOUSE_URL']
prom = PrometheusConnect(url = PROMETHEUS_URL, disable_ssl=True)




@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/users/me")
async def read_users_me( current_user: user.User = Depends(get_current_user)
):
    return current_user.email

@app.post("/signup", response_model=user.User)
def create_user(user: user.UserCreate, db: Session = Depends(get_db)):
    db_user = repo_user.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    else:
        client = Client(host=CLICKHOUSE_URL,user=CLICKHOUSE_USER,password=CLICKHOUSE_PASSWORD)    
        query = "CREATE USER IF NOT EXISTS'" + user.email + "' IDENTIFIED  WITH sha256_password BY '"+user.password+"'"
        result = client.execute(query)
        # clickhouse_read_only = "GRANT SHOW TABLES, SELECT ON default.*, SHOW QUOTAS ON *.*,SELECT ON ethereum.* TO '"+user.email+"'"
        # client.execute(clickhouse_read_only)

        print(result)
        user_role = user.user_role
        # for role in user_role:
        user_role_list = user_role.split(",")
        for role in user_role_list:
            print(role)    
            if role == "hobbyist":
                clickhouse_role = "GRANT hobbyist TO '"+user.email+"'"
                client.execute(clickhouse_role)
                print(clickhouse_role)
            if role == "developer":
                clickhouse_role = "GRANT developer,hobbyist TO '"+user.email+"'"
                client.execute(clickhouse_role)
                print(clickhouse_role)
            if role == "startup":
                clickhouse_role = "GRANT startup,hobbyist,developer TO '"+user.email+"'"
                client.execute(clickhouse_role)
                print(clickhouse_role)    
        
        user.password = ath.get_hashed_password(user.password)
        print(user.password)
        # print(plain_password)
        return repo_user.create_user(db=db, user=user, hashed_password=user.password, user_role=user_role_list)
    


@app.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends(),db: Session = Depends(get_db)):  
    user_dict = db.query(mduser.User).filter(mduser.User.email ==form_data.username).first()
    if not user_dict:
        raise HTTPException(status_code=400, detail="Incorrect username")
    if not ath.verify_password(form_data.password ,user_dict.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    return {
        "access_token": ath.create_access_token(user_dict.email),
        "refresh_token":ath.create_refresh_token(user_dict.email),
    }

@app.post("/jwt_login")
async def login(user: user.UserAuth,db: Session = Depends(get_db)):  
    user_dict = db.query(mduser.User).filter(mduser.User.email == user.email).first()
    if not user_dict:
        raise HTTPException(status_code=400, detail="Incorrect username")
    if not ath.verify_password(user.password ,user_dict.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    return {
        "access_token": ath.create_access_token(user_dict.email),
        "refresh_token":ath.create_refresh_token(user_dict.email),
        "user_id":user_dict.id,
    }


@app.get("/allmetrics")
async def allmetric():
    
    prom.all_metrics()
    print(prom.all_metrics())
    result = prom.all_metrics()
    print((prom.custom_query(query="prometheus_http_requests_total")))
    
    return {"message": result }

@app.get("/query_range_v1")
async def query(query:str,start_time:str, end_time:str,step:str,current_user: user.User = Depends(get_current_user), node_id: str = Header(title="checking node-id"), db: Session = Depends(get_db)):

    start_time = parse_datetime(start_time)
    end_time = parse_datetime(end_time)
    step=step
    print(node_id)
    node_name = ''
    # node_name_ = repo_node.get_node(db=db,user_id=current_user.id, node_name=node_id)
    # print(node_name)
    # query= query + '{'+"instance='"+node_ip+"'}"
    node_name = node_id + ".*"
    print(node_name)
    query = query.replace("$pod", node_name)
    print(query)
    result = prom.custom_query_range(query=query,start_time=start_time,end_time=end_time,step=step )
    print(node_name,result)

    return("result", result)

@app.get("/time_gap")
async def query(query:str,start_time:str,end_time:str,step:str,node_id: str = Header(title="checking node-id"),current_user: user.User = Depends(get_current_user),db: Session = Depends(get_db)):
    start_time = parse_datetime(start_time)
    end_time = parse_datetime(end_time)
    start_time = str(start_time)
    end_time = str(end_time)
    print(node_id)
    node_ip = repo_node.get_node(db=db,user_id=current_user.id, node_id=node_id)
    print(node_ip)
    query= query + '{'+"instance='"+node_ip+"'}"
    print(query)
    connect_string = PROMETHEUS_URL+"/api/v1/query?query="+query+"&start="+start_time+"&end_time="+end_time+"&step="+step+"s"
    response = requests.get(connect_string, params=query)
    print("printing response",response.json())

    return ("result", response.json())

# @app.post("/query")
# async def query(query:click_house_query.QueryBase ,current_user: user.User = Depends(get_current_user), db: Session = Depends(get_db)):
#     client = Client(host=CLICKHOUSE_URL,user=CLICKHOUSE_USER,password=CLICKHOUSE_PASSWORD)
#     query_res = query.query
#     print(query_res)
#     try:
#         result = client.execute(query_res)
#         print("Hello")
#     except Exception as e:
#        raise HTTPException(status_code=500, detail=e)  
    
#     print(result)

#     return("result", result)

@app.get("/nodes")
async def nodes(current_user:user.User = Depends(get_current_user), db: Session = Depends(get_db)):

    print(current_user.id)
    node_list = repo_node.node_name(db=db,user_id=current_user.id)
    print (node_list)

    return node_list



@app.get("/prom_query_range")
async def query(query:str,start_time:str, end_time:str,step:str,current_user: user.User = Depends(get_current_user), db: Session = Depends(get_db)):

    start_time = parse_datetime(start_time)
    end_time = parse_datetime(end_time)
    step=step
    print(query)
    result = prom.custom_query_range(query=query,start_time=start_time,end_time=end_time,step=step )
    print(result)

    return("result", result)


@app.post("/reset_password")
async def reset_passwor(new_password: user.UserResetPassword , db: Session = Depends(get_db)):

    token_dict=repo_reset_password.get_token_user_by_token(db=db,token=new_password.token)
 
    if not token_dict:
        raise HTTPException(status_code=400, detail="Link used already token has expired")
    
    user_dict = db.query(mduser.User).filter(mduser.User.email == token_dict.email).first()

    # if not user_dict:
    #     raise HTTPException(status_code=400, detail="Incorrect username")
    # # user = user_dict.email
    password_local = ath.get_hashed_password(new_password.password)
    update_local_password = repo_user.update_password(db=db, password=password_local, email=user_dict.email)
    client = Client(host=CLICKHOUSE_URL,user=CLICKHOUSE_USER, password=CLICKHOUSE_PASSWORD)
    alter_password_query = "ALTER USER '"+user_dict.email+"' IDENTIFIED WITH sha256_password  BY '"+new_password.password+"'"
    print(alter_password_query)
    try:
        result = client.execute(alter_password_query)
        print("Password Updated Successfully")
    except Exception as e:
       raise HTTPException(status_code=500, detail=e)  
    
    print(result)
    repo_reset_password.delete_token(db=db,email=user_dict.email)
    return ("Password Updated Successsfully, new password is :" ,new_password.password)


@app.post("/reset_password_token")
async def create_token(email:reset_password_schema.TokenBase, db: Session = Depends(get_db)):

    user_dict = db.query(mduser.User).filter(mduser.User.email == email.email).first()
        
    if not user_dict:
        raise HTTPException(status_code=400, detail="User does not exists")
    
    user_token_dict = repo_reset_password.get_token_user_by_email(db=db,email=email.email)
    
    if not user_token_dict:
        repo_reset_password.create_token_user(db=db,email=email.email)
    
    token = repo_reset_password.create_token(db=db, email=email.email)

    url = API_URL +"?token="+token
    
    
    # token = {"tokentoken": token}
    # url = API_URL+"/"+token
    # print(token)

    return url



# @app.post("/quota_test")
# async def query(query:click_house_query.QueryBase ,user:str, password:str):
#     client = Client(host=CLICKHOUSE_URL,user=user,password=password)
#     query_res = query.query
#     print(query_res)
#     try:
#         for i in range (250):
#             result = client.execute(query_res)
#         print("Hello")
#     except Exception as e:
#        raise HTTPException(status_code=500, detail=e)   
    
#     print(result)

#     return result

@app.post("/quota_query")
async def query(current_user: user.User = Depends(get_current_user), db: Session = Depends(get_db)):

    user_dict = db.query(mduser.User).filter(mduser.User.email == current_user.email).first()
    # user = user_dict.email
    # password = user_dict.plain_password
    # password = cisco_type7.decode(password)
    client = Client(host=CLICKHOUSE_URL,user=CLICKHOUSE_USER,password=CLICKHOUSE_PASSWORD)
    query_res = "Select * from system.quotas_usage where quota_key ='"+user_dict.email+"'"
    print(query_res)
    try:
        result = client.execute(query_res)
        # print(resu)
        print("Hello")
    except Exception as e:
       raise HTTPException(status_code=500, detail=e)  
    
    print(result)


    return (result)
# ("result", result)