import os
from dotenv import load_dotenv
import psycopg2
from datetime import datetime, timedelta

# load_dotenv()
# 連接到 PostgreSQL 資料庫
# conn = psycopg2.connect(
#     dbname=os.getenv("DB_name"),
#     user=os.getenv("DB_user"),
#     password=os.getenv("DB_passward"),
#     host=os.getenv("DB_host"),  # 或其他主機
#     port=os.getenv("DB_port")        # 預設 PostgreSQL 端口
# )


def get_DB_config():
    load_dotenv()
    DB_config_dict =  {
        "dbname":os.getenv("DB_name"),
        "user":os.getenv("DB_user"),
        "password":os.getenv("DB_passward"),
        "host":os.getenv("DB_host"),  # 或其他主機
        "port":os.getenv("DB_port"),}
    return DB_config_dict


def DB_fetch(sql_str, *params: tuple):
    # 取得資料庫配置
    DB_config_dict = get_DB_config()
    conn = psycopg2.connect(**DB_config_dict)
    # 創建游標對象
    cur = conn.cursor()
    # 執行查詢，將 sql_str 和 params 分開傳入
    cur.execute(sql_str, params)
    # 獲取查詢結果
    rows = cur.fetchall()
    # 關閉游標和連接
    cur.close()
    conn.close()
    return rows


def DB_modify(sql_str, *params: tuple):
    # 取得資料庫配置
    DB_config_dict = get_DB_config()
    conn = psycopg2.connect(**DB_config_dict)
    # 創建游標對象
    cur = conn.cursor()
    # 執行查詢，將 sql_str 和 params 分開傳入
    cur.execute(sql_str, params[0])
    # 提交變更到資料庫
    conn.commit()
    # 關閉游標和連接
    cur.close()
    conn.close()
    return "successful"


# sql_str = """SELECT * FROM public.temperature_moisture_monitor
# ORDER BY serial_id ASC LIMIT 100"""


# sql_str = """INSERT INTO public.temperature_moisture_monitor(
# 	"time", temperature, moisture)
# 	VALUES (%s, %s, %s);"""

# # print(DB_fetch(sql_str))
# now_time = datetime.now()
# print(DB_modify(sql_str, [now_time, 99, 0]))
