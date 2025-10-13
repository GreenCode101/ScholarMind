from fastapi import FastAPI
from routers import auth
from core.firebase_init import init_firebase

app = FastAPI(
    title="ScholarMind", 
    version="1.0.0",
    description="An AI-powered platform to assist students with their academic needs.",
    docs_url="/"
)

init_firebase()
app.include_router(auth.router)

if(__name__ == "__main__"):
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)