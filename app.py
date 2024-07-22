from fastapi import FastAPI, Request, Form, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from typing import List
import os
from pydantic import BaseModel
import uuid

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# 確保上傳目錄存在
UPLOAD_DIRECTORY = "static/uploads"
os.makedirs(UPLOAD_DIRECTORY, exist_ok=True)

MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB
ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif"}


class Post(BaseModel):
    message: str
    image_path: str


posts: List[Post] = []


@app.get("/")
async def index(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "header_text": "歡迎來到留言板", "posts": posts},
    )


@app.post("/post")
async def create_post(message: str = Form(...), image: UploadFile = File(...)):
    if not message.strip():
        raise HTTPException(status_code=400, detail="留言內容不能為空")

    if not image.filename:
        raise HTTPException(status_code=400, detail="必須上傳圖片")

    # 檢查文件大小
    contents = await image.read()
    if len(contents) > MAX_FILE_SIZE:
        raise HTTPException(status_code=400, detail="圖片大小不能超過 5MB")

    # 檢查文件類型
    file_ext = os.path.splitext(image.filename)[1].lower()
    if file_ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400, detail="只允許上傳 JPG、JPEG、PNG 或 GIF 格式的圖片"
        )

    # 生成唯一文件名
    unique_filename = f"{uuid.uuid4()}{file_ext}"
    file_location = f"{UPLOAD_DIRECTORY}/{unique_filename}"

    with open(file_location, "wb+") as file_object:
        file_object.write(contents)

    image_path = f"/static/uploads/{unique_filename}"

    new_post = Post(message=message, image_path=image_path)
    posts.append(new_post)

    return JSONResponse(content={"success": True})
