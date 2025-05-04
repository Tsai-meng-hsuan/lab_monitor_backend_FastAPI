# from .security import Depends, get_login_jwt_token, verify_credentials
from . import app
from . import JWT
from pydantic import BaseModel
from fastapi import HTTPException, Depends
from typing import List, Optional, Annotated
from fastapi import Query
from fastapi import File, UploadFile, Form
from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse, StreamingResponse
from datetime import datetime, timedelta
from postgreSQL import DB_function
# from .. import models

import pandas as pd
import io
import json


def topological_sort(nodes, edges):
    #     nodes = [
    #     {"id": "A"},
    #     {"id": "B"},
    #     {"id": "C"},
    #     {"id": "D"}
    # ]

    # edges = [
    #     {"source": "A", "target": "B"},
    #     {"source": "A", "target": "C"},
    #     {"source": "B", "target": "D"},
    #     {"source": "C", "target": "D"}
    # ]

    # 建立節點入度與鄰接圖
    in_degree = {}
    graph = {}

    # 初始化，在in_degree、graph字典中加入所有節點
    for node in nodes:
        node_id = node["id"]
        in_degree[node_id] = 0
        graph[node_id] = [] # graph為list，儲存每個node的下一個節點ID

    # 填入邊的資訊，注意這邊的source、target其實就是node的id
    for edge in edges:
        source = edge["source"]
        target = edge["target"]
        graph[source].append(target)    # 以<邊>為單位，建立每一個node的對應關係list(graph[source]),EX: graph[0] = [1,2,5]
        in_degree[target] += 1  # 計算入度累加，EX: in_degree[1] = 1, in_degree[2] = 1, in_degree[5] = 1

    # 找出入度為 0 的節點
    queue = [node_id for node_id in in_degree if in_degree[node_id] == 0]
    sorted_nodes = []

    # 拓撲排序主迴圈，持續執行直到queue中沒有資料
    while queue:
        node = queue.pop(0)  # 取出第一個元素（index 0），並從列表中移除它，模擬 queue（效率不如 deque，但可用）
        sorted_nodes.append(node) # 將當前節點加入排序結果

        for neighbor in graph[node]:    # EX: graph[0] = [1,2,5]
            in_degree[neighbor] -= 1    # 對下一個節點的degree進行遞減
            if in_degree[neighbor] == 0:    # 若下一個節點的degree為0，則由後方加入queue list中，保證先入先出的順序
                queue.append(neighbor)

    # 檢查是否有循環（即無法排序完整，最終只輸出一個序列的list，且必須包含所有的node
    if len(sorted_nodes) != len(nodes):
        raise ValueError("圖中有循環，無法進行拓撲排序")

    return sorted_nodes


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


@app.post("/data_analyze/init_data_upload")
async def upload_file(file: UploadFile = File(...), pipeline_id: int = Form(...)):
    try:
        content = await file.read() # 這是前端二進制資料
        df = pd.read_csv(io.StringIO(content.decode("utf-8")))
        # ✅ 清理數據 (例如去除空白、處理 NaN)
        df = df.dropna().reset_index(drop=True)  # 移除空值並重置索引
        df.columns = df.columns.str.strip()  # 清除欄位名稱的空白
        header_list = df.columns.tolist()   # 取得標頭
        header_list = [header.lower() for header in header_list]    # PostgreSQL 欄位名稱是小寫敏感，除非加上雙引號（"）
        column_settings = {}
        # 建立資料標頭與資料型態對照字典
        for one_header in header_list:
            column_settings[one_header.lower()] = "character varying"

        table_name = f'public."pipeline_{pipeline_id}_process_0"'
        DB_function.creat_table(table_name, **column_settings)  # 先建立table
        
        # 將 DataFrame 轉換成 tuples 並使用 execute_values 批次插入
        init_data_list = list(df.itertuples(index=False, name=None))
        DB_function.DB_batch_insert(table_name, header_list, init_data_list)    # 在插入數據
        
        # ✅ 轉換為 JSON 格式
        # json_data = df.to_dict(orient="records")
        # 這邊設定回傳給前端的資料
        content = {
            "message": f"檔案 {file.filename} 上傳成功",
            # "data": json_data  # 傳回清理後的資料
        }

        return JSONResponse(content=content, status_code=200)
    except Exception as e:
        print(e)
        return JSONResponse(content={"message": str(e)}, status_code=500)
    

@app.post("/data_analyze/json_process")
async def json_process(request: Request):
    try:
        # 讀取前端傳來的 JSON 資料
        json_process_data = await request.json()
        pipeline_id = json_process_data["pipeline_id"]
        process_step = json_process_data["step"]
        process_type = json_process_data["process_type"]
        process_parameter = json_process_data["process_parameter"]
        

        # 先取得上一步驟的資料
        table_name = f"public.pipeline_{pipeline_id}_process_{process_step-1}"  
        sql_str = f"SELECT * FROM {table_name}"  # 要加上 FROM 關鍵字
        result = DB_function.DB_fetch(sql_str)
        df = pd.DataFrame(result)

        # 再建立新的table
        header_list = df.columns.tolist()   # 取得標頭
        header_list = [header.lower() for header in header_list]    # PostgreSQL 欄位名稱是小寫敏感，除非加上雙引號（"）
        column_settings = {}
        # 建立資料標頭與資料型態對照字典
        for one_header in header_list:
            column_settings[one_header.lower()] = "character varying"

        table_name = f'public."pipeline_{pipeline_id}_process_{process_step}"'
        DB_function.creat_table(table_name, **column_settings)  

        # 最後將 DataFrame 轉換成 tuples 並使用 execute_values 批次插入
        init_data_list = list(df.itertuples(index=False, name=None))
        DB_function.DB_batch_insert(table_name, header_list, init_data_list)    # 在插入數據

        # 將 JSON 資料轉為 DataFrame
        # df = pd.DataFrame(json_data)

        # # ✅ 數據清理
        # df = df.dropna().reset_index(drop=True)  # 移除空值
        # df.columns = df.columns.str.strip()      # 去除欄位名稱空白
        # print("清理後的 DataFrame：", df)

        # # ✅ 再轉回 JSON
        # cleaned_json = df.to_dict(orient="records")

        # return JSONResponse(content={
        #     "message": "JSON 資料處理成功",
        #     "data": cleaned_json
        # }, status_code=200)

    except Exception as e:
        print("錯誤：", e)
        return JSONResponse(content={"message": str(e)}, status_code=500)
    

@app.post("/data_analyze/run_process")
async def upload_data(
    nodes: str = Form(...),
    edges: str = Form(...),
    file_node_id: str = Form(...),
    csv_files: List[UploadFile] = File(...)
    ):

    # 將 JSON 字串解析成 Python 物件
    node_data = json.loads(nodes)
    edge_data = json.loads(edges)
    file_node_id = json.loads(file_node_id)

    print("file node ID: ", file_node_id)

    node_topo = []
    edge_topo = []
    for one_node in node_data:
        print(one_node["data"]["label"])
        print(one_node["type"])
        print(30*"=")
        temp_dict = {}
        temp_dict["id"] = one_node["id"]
        node_topo.append(temp_dict)
    
    for one_edge in edge_data:
        print(one_edge["id"])
        print(one_edge["source"])
        print(one_edge["target"])
        print(30*"=")
        temp_dict = {}
        temp_dict["source"] = one_edge["source"]
        temp_dict["target"] = one_edge["target"]
        edge_topo.append(temp_dict)
    
    # 處理 CSV 檔案
    csv_contents = []
    for file in csv_files:
        content = await file.read()
        # content = file.read()
        csv_contents.append({
            "filename": file.filename,
            "content": content.decode("utf-8")
        })

    # 建立資料對照字典
    data_file_dict = {}
    for one_csv in csv_contents:
        filename = one_csv["filename"]
        content = one_csv["content"]
        # 使用 StringIO 將字串當成檔案處理
        df = pd.read_csv(io.StringIO(content), header=None)
        # 選擇加上欄位名稱
        df.columns = ["time", "value"]
        for one_dict in file_node_id:
            if filename == one_dict["filename"]:
                data_file_dict[one_dict["node_id"]] = df

    result = topological_sort(node_topo, edge_topo)
    print("這是排序後的node ID: ", result)
    
    # ✅ 這裡定義 generator，用來一筆筆傳資料
    def event_stream():
        # analyze_node_id 是目前分析的一個節點位置
        for analyze_node_id in result:
            # 找到node_info了解節點的工作項目
            node_info = [one_node for one_node in node_data if one_node['id'] == analyze_node_id]
            # 找到edge_info了解資料輸入來源
            edge_info = [one_edge for one_edge in edge_data if one_edge["target"] == analyze_node_id]
            # print("這是node的內部資訊: ", node_info)
            # print("這是edge的內部資訊: ", edge_info)
            # print(30*"=")
            
            if node_info[0]["type"] == "input":
                print("input data")
                # 先前已經先建置好資料了，所以這裡不做更新
                message = {
                    "message": "接收到輸入資料",
                    "node_id": analyze_node_id,
                    "node_name": node_info[0]["data"]["label"],
                    "output_data": None
                }
                yield f"data: {json.dumps(message)}\n\n"
                
            elif node_info[0]["type"] == "process":
                print("do the analyze")

            elif node_info[0]["type"] == "output":
                print("output data")
                # 依據edge資訊，抓取上一個節點的資料，把資料加入data_file_dict中
                source_node_id = edge_info[0]["source"]
                output_data = data_file_dict[source_node_id]
                output_data = output_data.to_dict(orient="records")  # 傳成 list of dicts
                
                print(analyze_node_id)
                print(node_info)
                # print(node_info[0]["data"]["label"])
                print(output_data)
                message = {
                    "message": "輸出資料準備完成",
                    "node_id": analyze_node_id,
                    "node_name": node_info[0]["data"]["label"],
                    "output_data": output_data
                }
                yield f"data: {json.dumps(message)}\n\n"

    return StreamingResponse(event_stream(), media_type="text/event-stream")


@app.post("/data_analyze/vueflow_data_upload")
async def upload_file(file: UploadFile = File(...)):
    try:
        content = await file.read() # 這是前端二進制資料
        df = pd.read_csv(io.StringIO(content.decode("utf-8")))
        # ✅ 清理數據 (例如去除空白、處理 NaN)
        df = df.dropna().reset_index(drop=True)  # 移除空值並重置索引
        df.columns = df.columns.str.strip()  # 清除欄位名稱的空白
        header_list = df.columns.tolist()   # 取得標頭
        header_list = [header.lower() for header in header_list]    # PostgreSQL 欄位名稱是小寫敏感，除非加上雙引號（"）
        print(df)
        column_settings = {}
        # 建立資料標頭與資料型態對照字典
        for one_header in header_list:
            column_settings[one_header.lower()] = "character varying"

        # table_name = f'public."pipeline_{pipeline_id}_process_0"'
        # DB_function.creat_table(table_name, **column_settings)  # 先建立table
        
        # # 將 DataFrame 轉換成 tuples 並使用 execute_values 批次插入
        # init_data_list = list(df.itertuples(index=False, name=None))
        # DB_function.DB_batch_insert(table_name, header_list, init_data_list)    # 在插入數據
        
        # ✅ 轉換為 JSON 格式
        json_data = df.to_dict(orient="records")
        # 這邊設定回傳給前端的資料
        content = {
            "message": f"檔案 {file.filename} 上傳成功",
            "data": json_data  # 傳回清理後的資料
        }

        return JSONResponse(content=content, status_code=200)
    except Exception as e:
        print(e)
        return JSONResponse(content={"message": str(e)}, status_code=500)