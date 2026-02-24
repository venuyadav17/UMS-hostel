from sqlalchemy import text
from backend.database import engine

def apply_migration():
    try:
        with engine.connect() as connection:
            print("Checking if 'is_active' column exists in 'users' table...")
            # Check if column exists
            result = connection.execute(text("SELECT column_name FROM information_schema.columns WHERE table_name='users' AND column_name='is_active';"))
            if not result.fetchone():
                print("Adding 'is_active' column to 'users' table...")
                connection.execute(text("ALTER TABLE users ADD COLUMN is_active BOOLEAN DEFAULT TRUE;"))
                connection.commit()
                print("✅ Migration successful: 'is_active' column added.")
            else:
                print("ℹ️ 'is_active' column already exists.")
    except Exception as e:
        print(f"❌ Migration failed: {e}")

if __name__ == "__main__":
    apply_migration()
