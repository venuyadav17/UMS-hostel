import sys
sys.path.insert(0, 'c:\\Users\\atike\\OneDrive\\Desktop\\PEP\\UMS-hostel\\backend')

from database import SessionLocal
from models import User, UserRole
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

db = SessionLocal()

# Check if test user exists
test_user = db.query(User).filter(User.username == "testuser").first()

if not test_user:
    # Create a new test user
    hashed_password = pwd_context.hash("password123")
    new_user = User(
        username="testuser",
        email="test@example.com",
        hashed_password=hashed_password,
        role=UserRole.STUDENT,
        is_active=True
    )
    db.add(new_user)
    db.commit()
    print("✅ Test user 'testuser' created successfully!")
    print("   Username: testuser")
    print("   Password: password123")
    print("   Role: student")
else:
    print(f"ℹ️ Test user already exists: {test_user.username}")

# Also create an admin user
admin_user = db.query(User).filter(User.username == "admin").first()

if not admin_user:
    hashed_password = pwd_context.hash("admin123")
    new_admin = User(
        username="admin",
        email="admin@example.com",
        hashed_password=hashed_password,
        role=UserRole.ADMIN,
        is_active=True
    )
    db.add(new_admin)
    db.commit()
    print("✅ Admin user 'admin' created successfully!")
    print("   Username: admin")
    print("   Password: admin123")
    print("   Role: admin")
else:
    print(f"ℹ️ Admin user already exists: {admin_user.username}")

# List all users
all_users = db.query(User).all()
print(f"\n📋 Total users in database: {len(all_users)}")
for user in all_users:
    print(f"   - {user.username} ({user.role})")

db.close()
