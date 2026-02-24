import json
from backend.database import SessionLocal
from backend.models import User

db = SessionLocal()
users = db.query(User).all()

user_list = []
for user in users:
    user_list.append({
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "role": user.role
    })

print(json.dumps(user_list, indent=2))
db.close()
