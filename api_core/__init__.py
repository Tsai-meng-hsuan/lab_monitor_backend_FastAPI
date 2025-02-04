import os
import dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer



def get_config_setting():
    # os_name = platform.system()
    # if os_name == 'Windows':
    dotenv.load_dotenv()

    #抓到.env內的環境變數
    db_host = os.getenv("DB_HOST")
    db_port = os.getenv("DB_PORT")
    db_database = os.getenv("DB_DATABASE")
    db_user = os.getenv("DB_USER")
    db_password = os.getenv("DB_PASSWORD")

    #建立物件實例
    setting = Setting()
    #設定物件屬性
    setting.config_db = {
        "host": db_host,
        "port": int(db_port),
        "database": db_database,
        "user": db_user,
        "password": db_password
    }
    setting.api_description = {
        "title": os.getenv("API_TITLE"),
        "description": os.getenv("API_DESCRIPTION"),
        "root_path": os.getenv("API_ROOT_PATH"),
    }

    setting.jwt_secret = os.getenv("JWT_SECRET_KEY")

    setting.aws_access_key_id = os.environ.get('AWS_ACCESS_KEY_ID')
    setting.aws_secret_access_key = os.environ.get('AWS_SECRET_ACCESS_KEY')

    return setting



# 創建 FastAPI 應用實例
app = FastAPI()

origins = ["*"] #這裡允許所有來源的請求。
app.add_middleware(
    CORSMiddleware, #將 CORS 中介軟體添加到應用中，允許跨域請求。
    # allow_origins=origins,
    allow_origins=["*"], #這裡允許所有來源的請求。
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"], 
)


from api_core import routes #加入相關路由設定
# handler = Mangum(app)