from api_core import app #api_core __init__.py 內的app物件
import uvicorn
if __name__ == "__main__":
    uvicorn.run("api_core:app", host="0.0.0.0", port=8000, reload=True)


# Swagger 是 FastAPI 的一個強大功能 http://127.0.0.1:8000/docs 