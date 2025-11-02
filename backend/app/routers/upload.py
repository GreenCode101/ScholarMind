from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
from werkzeug.utils import secure_filename

app = FastAPI()

# CORS middleware setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  #we can limit it
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create uploads directory
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)


@app.post("/upload_pdf")
async def upload_pdf(file: UploadFile = File(...)):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed.")

    safe_filename = secure_filename(file.filename)
    file_path = UPLOAD_DIR / safe_filename

    content = await file.read()


    with open(file_path, "wb") as f:
        f.write(content)

    return {
        "filename": safe_filename,
        "message": "PDF uploaded successfully!",
        "file_path": file_path.as_posix()
    }
