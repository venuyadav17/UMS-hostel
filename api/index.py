import sys
import os
from pathlib import Path

# Add backend to path
backend_path = Path(__file__).parent.parent / "backend"
sys.path.insert(0, str(backend_path))

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

# Initialize FastAPI app first
app = FastAPI()

# Try to import and initialize database
try:
    from database import engine, Base
    from routers import users, hostels
    
    # Create all tables
    Base.metadata.create_all(bind=engine)
    
    # Include routers
    app.include_router(users.router)
    app.include_router(hostels.router)
except Exception as e:
    print(f"Error initializing database or routers: {e}")
    import traceback
    traceback.print_exc()

app = FastAPI()

# Frontend directories
frontend_dir = Path(__file__).parent.parent / "frontend"
static_dir = frontend_dir / "static"

# Mount static files
try:
    app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")
except Exception as e:
    print(f"Warning: Could not mount static files: {e}")

# CORS (Cross-Origin Resource Sharing)
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

# Catch-all for 404
@app.get("/{full_path:path}", response_class=FileResponse)
def serve_fallback(full_path: str):
    """Fallback to index for single-page app routing."""
    file_path = frontend_dir / full_path
    if file_path.exists() and file_path.is_file():
        return FileResponse(file_path)
    # Return index for client-side routing
    return FileResponse(frontend_dir / "index.html")
