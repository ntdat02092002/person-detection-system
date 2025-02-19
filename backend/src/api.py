import os
import cv2
import numpy as np
import base64
import imghdr
import uuid

from fastapi import FastAPI, File, UploadFile, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, validator
from sqlalchemy.orm import Session

from .database import SessionLocal, get_db
from .models import ImageResult
from .database import engine, Base

from ultralytics import YOLO

app = FastAPI()

model = YOLO("yolo11n.pt")

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ImageRequest(BaseModel):
    file: UploadFile

    @validator("file")
    async def validate_image_file(cls, value):
        # Kiểm tra định dạng file ảnh
        contents = await value.read(100)  # Đọc một phần nhỏ để xác định loại ảnh
        file_extension = imghdr.what(None, h=contents)
        
        if file_extension not in ["jpeg", "png"]:
            raise HTTPException(status_code=400, detail="File must be an image of type JPEG or PNG")
        
        # Reset lại vị trí file về đầu để có thể đọc lại
        await value.seek(0)
        return value

Base.metadata.create_all(bind=engine)

BASE_IMAGE_PATH = os.getenv("BASE_IMAGE_PATH", "./asset")

@app.post("/process-image/")
# async def process_image(file: UploadFile = File(...)):
async def process_image(file: UploadFile = File(...), db: Session = Depends(get_db)):
    # Đọc file ảnh từ request
    contents = await file.read()
    nparr = np.frombuffer(contents, np.uint8)
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    results = model(image)
    result = results[0]
    count = 0
    for box in result.boxes:
        if int(box.cls) == 0:  # Lớp 0 là "person"
            print(box.xyxy)
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)  # Vẽ bbox
            count += 1

    _, img_encoded = cv2.imencode(".jpg", image)
    img_base64 = base64.b64encode(img_encoded).decode("utf-8")

    image_filename = f"{uuid.uuid4()}.jpg"
    image_path = os.path.join(BASE_IMAGE_PATH, image_filename)
    os.makedirs(os.path.dirname(image_path), exist_ok=True)
    cv2.imwrite(image_path, image)


    db_result = ImageResult(count=count, image_path=image_path)
    db.add(db_result)
    db.commit()
    db.refresh(db_result)


    return JSONResponse(content={"processedImage": img_base64, "count": count})