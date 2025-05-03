import os
from dotenv import load_dotenv
import psycopg2
from psycopg2.extras import RealDictCursor
from psycopg2.extras import execute_values  # 這是批次加入數據用的
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


def  DB_fetch(sql_str, *params: tuple):
    # 取得資料庫配置
    DB_config_dict = get_DB_config()
    conn = psycopg2.connect(**DB_config_dict)
    # 使用字典游標執行查詢(DB以字典回傳，方便後續程式編輯)
    cur = conn.cursor(cursor_factory=RealDictCursor)
    # 執行查詢，將 sql_str 和 params 分開傳入
    cur.execute(sql_str, params)
    # 獲取查詢結果
    rows = cur.fetchall()
    # 關閉游標和連接
    cur.close()
    conn.close()
    return rows

# 批次加入大量數據
def DB_batch_insert(table_name, header_list, init_data_list):
    # 假設我們有大量的資料需要插入
    # data_to_insert = [
    #     ('Alice', 25),
    #     ('Bob', 30),
    #     ('Charlie', 35),
    #     # 更多資料...
    # ]

    # 取得資料庫配置
    DB_config_dict = get_DB_config()
    conn = psycopg2.connect(**DB_config_dict)
    # 使用字典游標執行查詢(DB以字典回傳，方便後續程式編輯)
    cur = conn.cursor(cursor_factory=RealDictCursor)
    header_str = ', '.join(header_list)
    
    # print(table_name, header_list, init_data_list)
    # 插入資料的 SQL 語句
    insert_query = f"""
    INSERT INTO {table_name} ({header_str})
    VALUES %s
    """
    
    execute_values(cur, insert_query, init_data_list)
    # 提交事務
    conn.commit()
    # 關閉游標與連線
    cur.close()
    conn.close()
    print("資料插入成功")


def DB_modify(sql_str, *params):
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

def creat_table(table_name, **column_setting):
    # 取得資料庫配置
    DB_config_dict = get_DB_config()
    conn = psycopg2.connect(**DB_config_dict)
    # 創建游標對象
    cur = conn.cursor()
    # 動態生成欄位設定
    column_definitions = []
    for column_name, column_type in column_setting.items():
        column_definitions.append(f'"{column_name}" {column_type}')

    # 動態生成 SQL 指令
    sql_str = f"""
        DROP TABLE IF EXISTS {table_name};
        CREATE TABLE IF NOT EXISTS {table_name}
        (
            {', '.join(column_definitions)}
        )
        TABLESPACE pg_default;

        ALTER TABLE IF EXISTS {table_name}
            OWNER TO postgres;
    """

    cur.execute(sql_str)
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


# column_settings = {
#     "time": "character varying",
#     "name": "character varying",
#     "age": "integer"
# }
# creat_table("test_table", **column_settings)

# DB_batch_insert()