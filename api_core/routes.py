# from .security import Depends, get_login_jwt_token, verify_credentials
from . import app
from . import JWT
from pydantic import BaseModel
from fastapi import HTTPException, Depends
from postgreSQL import DB_function
from typing import List, Optional, Annotated
from fastapi import Query
from datetime import datetime, timedelta
# from .. import models



@app.get("/login_get", tags=["會員登入查詢"], summary="查資料庫會員資料_get")
def callback(station_MTID: str):
    return {"status": "success"}


# POST方法定義請求體結構
class LoginRequest(BaseModel):
    name: str
    password: str
@app.post("/login_post", tags=["會員登入查詢"], summary="查資料庫會員資料_post")
def callback(login_information: LoginRequest):
    name = login_information.name
    password = login_information.password
    if name == "mhtsai" and password == "mengal25141425":
        # 創建 JWT
        access_token = JWT.create_JWT_token(user_name=name)
        print("ok~")
        return {
            "status": "success",
            "access_token": access_token, 
            "token_type": "bearer",
            }
    else:
        print("error !")
        raise HTTPException(status_code=401, detail="Invalid username or password")
        # return {"status": "error"}


@app.get("/test_output_data", tags=["資料傳輸測試"], summary="data_output")
def callback(sensor_ID):
    # print(type(sensor_ID))
    print(sensor_ID)
    if sensor_ID == "CCT&T_CONS_1":
        return [
            { "time": '00:00', "value": 100 },
            { "time": '01:15', "value": 200 },
            { "time": '02:30', "value": 150 },
            { "time": '03:45', "value": 300 },
            { "time": '05:00', "value": 88 },
            { "time": '06:15', "value": 98 },
            { "time": '07:30', "value": 123 },
            { "time": '08:45', "value": 219 },
        ]
    elif sensor_ID == "CCT&T_CONS_2":
        return [
            { "time": '00:00', "value": 1100 },
            { "time": '01:15', "value": 1200 },
            { "time": '02:30', "value": 1150 },
            { "time": '03:45', "value": 1300 },
            { "time": '05:00', "value": 188 },
            { "time": '06:15', "value": 198 },
            { "time": '07:30', "value": 1123 },
            { "time": '08:45', "value": 1219 },
        ]
    elif sensor_ID == "CCT&T_CONS_3":
        return [
            { "time": '00:00', "value": 1 },
            { "time": '01:15', "value": 30 },
            { "time": '02:30', "value": 40 },
            { "time": '03:45', "value": 66 },
            { "time": '05:00', "value": 388 },
            { "time": '06:15', "value": 88 },
            { "time": '07:30', "value": 123 },
            { "time": '08:45', "value": 762 },
        ]


@app.get("/test_output_sensorsIDs", tags=["系統測試"], summary="傳出所有感測器ID")
def callback():
    return [
        { "name": '第一組', "sensor_ID": "CCT&T_CONS_1" },
        { "name": '第二組', "sensor_ID": "CCT&T_CONS_2" },
        { "name": '第三組', "sensor_ID": "CCT&T_CONS_3" },
    ]


@app.get("/DB_fetch")
def DB_fetch(sql_str: str, params: Annotated[list[str], Query()] = None ):
    rows = DB_function.DB_fetch(sql_str, params)
    print(rows)


@app.get("/DB_modify")
def DB_modify(sql_str: str, params: Annotated[list[str], Query()] = None ):
    print(type(sql_str), type(params))
    now_time = datetime.now()
    params.insert(0, now_time)
    print(sql_str)
    print(params)
    result = DB_function.DB_modify(sql_str, params)
    print(result)
    return result


@app.get("/test_output", tags=["系統測試"], summary="JWT測試")
def callback(station_MTID: str = Depends(JWT.verify_JWT_token)):
    return {"status": "success"}


@app.get("/protected")
def protected_route(current_user: str = Depends(JWT.verify_jwt)):
    print("protected")
    return {"message": f"Hello, {current_user}. You have accessed a protected route."}

