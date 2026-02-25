import sys
import os
from pathlib import Path

# Add backend to path
backend_path = Path(__file__).parent / "backend"
sys.path.insert(0, str(backend_path))

from database import SessionLocal
from crud import create_user
from schemas import UserCreate

# Create a session
db = SessionLocal()

try:
    # Create the first admin
    admin_data = UserCreate(
        username="admin10",
        password="admin10",
        email="admin10@gmail.com",
        role="admin"
    )
    
    # Check if admin already exists
    from crud import get_user
    existing_admin = get_user(db, "admin10")
    if existing_admin:
        print("Admin user 'admin10' already exists!")
    else:
        admin = create_user(db, admin_data)
        print(f"✓ Admin created successfully!")
        print(f"  Username: {admin.username}")
        print(f"  Email: {admin.email}")
        print(f"  Role: {admin.role}")
finally:
    db.close()
