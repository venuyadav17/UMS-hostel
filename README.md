# Hostel Booking System

A full-stack Hostel Booking System with Admin and Student roles.

## Features
- **Admin**: Add Hostels and Rooms (AC/Non-AC, 3/4 Seater).
- **Student**: Search hostels, filter by room type, and book rooms.
- **Authentication**: Secure Login and Registration using JWT.

## Quick Start

1.  **Backend Setup**:
    - Install requirements: `pip install -r backend/requirements.txt`
    - Update DB credentials in `backend/database.py`
    - Run server: `cd backend && uvicorn main:app --reload`

2.  **Frontend**:
    - Open `frontend/index.html` in your browser.

## Technologies
- Backend: FastAPI, SQLAlchemy, PostgreSQL
- Frontend: HTML, CSS, JavaScript
