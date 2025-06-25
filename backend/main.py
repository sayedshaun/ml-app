from api.auth import router as auth_router
from api.user import router as user_router
from api.inference import router as inference_router
from api.health import router as health_router
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

load_dotenv()
FRONTEND_URL = os.getenv("FRONTEND_URL")

app = FastAPI()
app.include_router(health_router)
app.include_router(auth_router)
app.include_router(user_router)
app.include_router(inference_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[FRONTEND_URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__=="__main__":
    import subprocess
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=8000)
    args = parser.parse_args()
    subprocess.run(f"uvicorn main:app --reload --port {args.port}", shell=True)
