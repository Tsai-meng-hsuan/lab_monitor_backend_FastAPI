from jose import jwt, JWTError
from typing import Union
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
# from src.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES

# 在對JWT進行編碼簽章時所使用的 KEY 值，可使用任何方式生成，官方文件教學中使用亂數產生長度32字元字串。
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
# JWT 簽章時所用的演算法
ALGORITHM = "HS256"
# JWT 在多久後過期，這裡設定為 30 分鐘。
ACCESS_TOKEN_EXPIRE_MINUTES = 1

# 建立物件實例
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login_post")


# 系統生成JWT token
def create_JWT_token(
    user_name: str, expires_delta: Union[timedelta, None] = None
):
    payload = {"sub" : user_name }
    to_encode = payload.copy() #為了避免直接修改傳入的 payload 字典，創建了一個副本。
    if expires_delta is None:
        expires_delta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES) #若沒有特殊設定，則是用預設值
    elif isinstance(expires_delta, int):  # 如果传入的是整数分钟
        expires_delta = timedelta(minutes=expires_delta)
    expire = datetime.utcnow() + expires_delta #獲取當前時間，並加上 expires_delta 計算出 Token 的過期時間
    to_encode.update({"exp": expire}) #在要編碼的資料中新增 exp（過期時間）欄位，JWT必要欄位
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM) # 編碼，生成 JWT
    return encoded_jwt
    

def verify_jwt(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
        return username
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")


# 系統依據原先讀JWT token驗證
def verify_JWT_token(token: str)->bool:
    """驗證用戶token"""
    # payload = {'user_name': user_name}
    try:
        # 這裡的token為前端發給後端驗證，_payload為解碼後的內容
        _payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM]) #解碼
    except jwt.PyJWTError:
        print('token解析失敗')
        return False
    else:
        # print(_payload)
        exp = _payload.pop('exp') #反傳該欄位的值，並刪除字典中欄位
        # 轉換為 UNIX 時間戳（秒）
        now_time = datetime.utcnow()
        # 轉換為 UNIX 時間戳（秒）
        now_timestamp = int(now_time.timestamp())
        if now_timestamp > exp:
            print('已失效')
            return False
        return token




# @app.post("/get_token")
# def get_token(username: str, password: str):
#     # 模擬登錄驗證
#     if username == "testuser" and password == "testpassword":
#         token = jwt.encode({"sub": username}, SECRET_KEY, algorithm=ALGORITHM)
#         return {"access_token": token, "token_type": "bearer"}
#     raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

# @app.get("/protected")
# def protected_route(current_user: str = Depends(verify_jwt)):
#     return {"message": f"Hello, {current_user}. You have accessed a protected route."}


# user_name = "user123"
# # payload = {"sub" : user_name }
# token = create_JWT_token(user_name)
# print(30*"=")
# print(token)
# print(30*"=")
# print(datetime.utcnow())
# verify_JWT_token(user_name, token)
