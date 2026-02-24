from backend.database import SessionLocal
from backend.models import User, UserRole

db = SessionLocal()
user = db.query(User).filter(User.username == "testuser").first()
if user:
    user.role = UserRole.ADMIN
    db.commit()
    print(f"User {user.username} promoted to {user.role}")
else:
    print("User testuser not found")
db.close()
