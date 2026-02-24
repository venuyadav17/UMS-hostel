from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from database import engine, Base
from routers import users, hostels

Base.metadata.create_all(bind=engine)

app = FastAPI()

import os
from pathlib import Path

# Frontend directories
frontend_dir = Path(__file__).resolve().parent.parent / "frontend"
static_dir = frontend_dir / "static"

# Mount static files
app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")

# CORS (Cross-Origin Resource Sharing)
origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://127.0.0.1:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users.router)
app.include_router(hostels.router)

@app.get("/", response_class=FileResponse)
def serve_index():
    """Serve the main login page."""
    return FileResponse(frontend_dir / "index.html")


@app.get("/login", response_class=FileResponse)
def serve_login():
    """Serve the login page."""
    return FileResponse(frontend_dir / "index.html")


@app.get("/admin", response_class=FileResponse)
def serve_admin_dashboard():
    """Serve the admin dashboard page."""
    return FileResponse(frontend_dir / "admin_dashboard.html")


@app.get("/student", response_class=FileResponse)
def serve_student_dashboard():
    """Serve the student dashboard page."""
    return FileResponse(frontend_dir / "student_dashboard.html")


@app.get("/student_dashboard.html", response_class=FileResponse)
def serve_student_dashboard_html():
    """Serve the student dashboard page via direct HTML file request."""
    return FileResponse(frontend_dir / "student_dashboard.html")


@app.get("/admin_dashboard.html", response_class=FileResponse)
def serve_admin_dashboard_html():
    """Serve the admin dashboard page via direct HTML file request."""
    return FileResponse(frontend_dir / "admin_dashboard.html")


@app.get("/register.html", response_class=FileResponse)
def serve_register_html():
    """Serve the registration page."""
    return FileResponse(frontend_dir / "register.html")
