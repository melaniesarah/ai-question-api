import os
import uuid
from typing import Optional
from fastapi import HTTPException, UploadFile, File
from pydantic import BaseModel


# Response model
class PDFUploadResponse(BaseModel):
    file_id: str
    filename: str
    message: str


# Create uploads directory if it doesn't exist
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


async def upload_pdf(file: UploadFile = File(...)) -> PDFUploadResponse:
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")

    max_size = 10 * 1024 * 1024  # 10MB
    if file.size and file.size > max_size:
        raise HTTPException(status_code=400, detail="File size exceeds 10MB limit")

    try:
        content = await file.read()

        if len(content) > max_size:
            raise HTTPException(status_code=400, detail="File size exceeds 10MB limit")

        file_id = str(uuid.uuid4())

        filename = f"{file_id}_{file.filename}"
        file_path = os.path.join(UPLOAD_DIR, filename)

        with open(file_path, "wb") as f:
            f.write(content)

        return PDFUploadResponse(
            file_id=file_id, filename=file.filename, message="PDF uploaded successfully"
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error uploading PDF: {str(e)}")
