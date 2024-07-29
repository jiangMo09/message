import io
import boto3
from botocore.exceptions import ClientError
import uuid
from fastapi import FastAPI, Request, Form, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os

from utils.mysql import get_db_connection, execute_query
from utils.load_env import S3_BUCKET, CLOUDFRONT_URL

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

MAX_FILE_SIZE = 5 * 1024 * 1024
ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif"}


@app.get("/")
async def index(request: Request):
    connection = get_db_connection()
    try:
        query = "SELECT * FROM MESSAGE ORDER BY time DESC"
        posts = execute_query(connection, query, fetch_method="fetchall")
        return templates.TemplateResponse(
            "index.html",
            {"request": request, "header_text": "歡迎來到留言板", "posts": posts},
        )
    finally:
        connection.close()


@app.post("/post")
async def create_post(message: str = Form(...), image: UploadFile = File(...)):
    if not message.strip():
        raise HTTPException(status_code=400, detail="留言內容不能為空")

    if not image.filename:
        raise HTTPException(status_code=400, detail="必須上傳圖片")

    contents = await image.read()
    if len(contents) > MAX_FILE_SIZE:
        raise HTTPException(status_code=400, detail="圖片大小不能超過 5MB")

    file_ext = os.path.splitext(image.filename)[1].lower()
    if file_ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400, detail="只允許上傳 JPG、JPEG、PNG 或 GIF 格式的圖片"
        )

    folderName = "message"
    unique_filename = f"{uuid.uuid4()}{file_ext}"
    s3_path = f"{folderName}/{unique_filename}"

    try:
        s3_client = boto3.client("s3")
        s3_client.upload_fileobj(
            io.BytesIO(contents),
            S3_BUCKET,
            s3_path,
            ExtraArgs={"ContentType": image.content_type},
        )
        image_url = f"{CLOUDFRONT_URL}/{s3_path}"
    except ClientError as e:
        raise HTTPException(status_code=500, detail=f"上傳到 S3 失敗: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"創建 S3 客戶端失敗: {str(e)}")

    connection = get_db_connection()
    try:
        query = "INSERT INTO MESSAGE (message, image_path) VALUES (%s, %s)"
        execute_query(connection, query, (message, image_url))
        return JSONResponse(content={"success": True})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"數據庫錯誤: {str(e)}")
    finally:
        connection.close()


@app.get("/loaderio-dd2c4743eaa719c6810019d76f9a84fb")
def verify():
    return "loaderio-dd2c4743eaa719c6810019d76f9a84fb"
