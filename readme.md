# 開發環境建置
1.python執行環境
```
pip install pipenv // 在root環境下安裝 pipenv為pyhton虛擬環境套件
cd ${程式碼專案位置}
pipenv --python 3.12 //在虛擬環境中安裝python(須注意全域環境中也需要有python特定版本程式)
pipenv shell //啟動虛擬環境env
pip install -r requirements.txt //安裝需要的先關套件
```

2.程式碼環境變數使用dotenv套件，故需在app路徑下建立.env，.env檔可參照app\template.env內容進行創建。

<br>

# minIO 開啟方式
1.下載minIO.exe檔(有分企業版跟一般版，請選一般版)
Invoke-WebRequest -Uri "https://dl.min.io/server/minio/release/windows-amd64/minio.exe" -OutFile "C:\minio.exe" 

2.設定環境變數使用者名稱及密碼
setx MINIO_ROOT_USER admin
setx MINIO_ROOT_PASSWORD password

3.以PowerShell開啟minIO.exe，並指定資料儲存位置(請先確認資料夾已建立)、開設port位置
C:\minio.exe server C:\minIO --console-address ":9001"