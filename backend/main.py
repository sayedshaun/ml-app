from api.auth import router as auth_router
from api.user import router as user_router
from api.inference import router as inference_router
from api.health import router as health_router
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os
import json


load_dotenv()
FRONTEND_URL = os.getenv("FRONTEND_URL")

app = FastAPI()

#=========FRONTEND==================
# from fastapi.responses import HTMLResponse
# from fastapi.templating import Jinja2Templates
# from fastapi import FastAPI, Request, Depends
# from fastapi.responses import RedirectResponse

# def templating():
#     templates = Jinja2Templates(directory="templates")
#     return templates

# @app.get("/", response_class=HTMLResponse)
# def index_page(request: Request, templates: Jinja2Templates = Depends(templating)):
#     return templates.TemplateResponse("index.html", {"request": request})

# @app.get("/login", response_class=HTMLResponse)
# def login_page(request: Request, templates: Jinja2Templates = Depends(templating)):
#     with open("token.json", "w") as f:
#         json.dump(f)
#     return templates.TemplateResponse("home.html", {"request": request})

# from fastapi import Response

# @app.post("/login-form")
# def login_form(response: Response, username: str = Form(...), password: str = Form(...)):
#     user = authenticate_user(username, password)
#     if not user:
#         # Return login page with error (template rendering)
#         return templates.TemplateResponse("login.html", {"request": request, "error": "Invalid credentials"})

#     token = create_access_token({"sub": user.email})

#     # Set token as HttpOnly cookie (expires in e.g. 1 hour)
#     response.set_cookie(key="access_token", value=f"Bearer {token}", httponly=True, max_age=3600, secure=True)

#     # Redirect to home page
#     return RedirectResponse(url="/", status_code=303)


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
