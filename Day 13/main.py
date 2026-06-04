
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from ultralytics import YOLO
import shutil
import os
import uuid
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# Serve uploaded images
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# Allow frontend connection
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load model
model = YOLO("model/best.pt")

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    file_id = str(uuid.uuid4())
    file_path = f"{UPLOAD_DIR}/{file_id}_{file.filename}"

    # Save uploaded file
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Run YOLO
    results = model(file_path, conf=0.1)

    # 🔥 IMPORTANT: Fix label names for output image
    results[0].names = {
        0: "crack",
        1: "pothole"
    }

    # Collect detections for frontend
    detections = []
    boxes = results[0].boxes

    for box in boxes:
        cls_id = int(box.cls[0])
        label = results[0].names[cls_id]
        detections.append(label)

    # Save output image
    output_path = f"{UPLOAD_DIR}/{file_id}_output.jpg"
    results[0].save(output_path)

    return {
        "status": "success",
        "output": output_path,
        "detections": detections
    }


@app.get("/")
def home():
    return {"message": "Backend running"}