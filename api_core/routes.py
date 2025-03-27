# from .security import Depends, get_login_jwt_token, verify_credentials
from . import app
from . import JWT
from pydantic import BaseModel
from fastapi import HTTPException, Depends
from postgreSQL import DB_function
from typing import List, Optional, Annotated
from fastapi import Query
from datetime import datetime, timedelta
from postgreSQL import DB_function
# from .. import models


@app.get("/", tags=["根目錄"], summary="根目錄")
def callback():
    return {"status": "根目錄success幹機掰"}


# POST方法定義請求體結構
class register_member(BaseModel):
    name: str
    email: str
    password: str
@app.post("/add_user", tags=["前端登入功能"], summary="新增會員帳號")
def callback(register_information: register_member):
    sql_str = """
        INSERT INTO public.user_information(
        user_name, password, email)
        VALUES (%s, %s, %s);
        """
    
    params = (
        register_information.name,
        register_information.password,
        register_information.email,
        )
    
    output = DB_function.DB_modify(sql_str, params)
    print(output)
    return {register_information}


# POST方法定義請求體結構
class LoginRequest(BaseModel):
    name: str
    password: str
@app.post("/login_post", tags=["前端登入功能"], summary="查資料庫會員資料_post")
def callback(login_information: LoginRequest):
    #請注意login_information的變數名稱需跟前端設定一樣
    input_password = login_information.password
    input_user_name = login_information.name

    sql_str = """
        SELECT id, user_name, password, email
	    FROM public.user_information
        WHERE user_name = %s;
        """
    
    params = (input_user_name)
    search_result = DB_function.DB_fetch(sql_str, params)
    if len(search_result) == 0:
        print("未註冊使用者")
    elif search_result[0]["password"] == input_password:
        print(f"密碼正確，歡迎使用者{search_result[0]["user_name"]}")
        # 創建 JWT
        access_token = JWT.create_JWT_token(user_name=login_information.name)
        return {
            "status": "success",
            "access_token": access_token,   # 把JWT的資料傳給前端
            "token_type": "bearer",
            }
    else:
        print(f"密碼錯誤，請重新輸入密碼")
        raise HTTPException(status_code=401, detail="Invalid username or password")
        # return {"status": "error"}


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
    sql_str = """SELECT * FROM public.test_data_table"""

    search_result = DB_function.DB_fetch(sql_str)
    print(search_result)

    if sensor_ID == "CCT&T_CONS_1":
        return search_result
      
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
    if params:
        now_time = datetime.now()
        params.insert(0, now_time)
    print(sql_str)
    print(params)
    result = DB_function.DB_modify(sql_str, params)
    print(result)
    return result


# ESP32的GET方式好像只能傳單一參數，只好在感測器端以STR回傳，進行後續字串處理
@app.get("/get_sensor_data")
def get_sensor_data(data: str):
    # ESP32上傳資料長這樣: "+RCV=200,27,BT_V:567,moisture:40,temperature:25.30,-25,11"
    print(data)
    temp_dict = {}
    now_time = datetime.now()
    data_list = data.split(",")
    temp_dict["end_node_id"] = data_list[0].split("=")[1] # 這是感測器編號的部分
    temp_dict["data_length"] = data_list[1] # 這是Lora資料長度的部分
    temp_dict["RSSI"] = data_list[-1] # 這是Lora訊號強度的部分
    temp_dict["SNR"] = data_list[-2] # 這是Lora訊號信噪比的部分
    # 依據收到的資料建立字典
    for one_data in data_list[2:-2]:
            print(one_data)
            temp_dict[one_data.split(":")[0]] = one_data.split(":")[1]
    print(temp_dict)
    
    sql_str = """INSERT INTO public.test_table(
                time, temperature, moisture)
                VALUES (%s, %s, %s);"""
    
    params = [now_time, temp_dict["temperature"], temp_dict["moisture"]]
    result = DB_function.DB_modify(sql_str, params)
    print(result)
    return data


@app.get("/test_output", tags=["系統測試"], summary="JWT測試")
def callback(station_MTID: str = Depends(JWT.verify_JWT_token)):
    return {"status": "success"}


@app.get("/protected")
def protected_route(current_user: str = Depends(JWT.verify_jwt)):
    print("protected")
    return {"message": f"Hello, {current_user}. You have accessed a protected route."}

