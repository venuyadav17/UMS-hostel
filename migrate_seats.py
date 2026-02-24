from sqlalchemy import text
from backend.database import engine

def migrate_seats():
    try:
        with engine.connect() as connection:
            print("Checking if 'available_seats' column exists in 'rooms' table...")
            result = connection.execute(text("SELECT column_name FROM information_schema.columns WHERE table_name='rooms' AND column_name='available_seats';"))
            if not result.fetchone():
                print("Adding 'available_seats' column to 'rooms' table...")
                connection.execute(text("ALTER TABLE rooms ADD COLUMN available_seats INTEGER DEFAULT 0;"))
                
                # Initialize available seats based on capacity enum
                # Assuming Enum values correspond to integer capacities (3, 4) or we map them.
                # Since capacity in DB holds integer strings '3', '4' due to SeaterType enum setup.
                print("Initializing available seats...")
                connection.execute(text("UPDATE rooms SET available_seats = CAST(capacity AS INTEGER);"))
                
                connection.commit()
                print("✅ Migration successful: 'available_seats' column added and initialized.")
            else:
                print("ℹ️ 'available_seats' column already exists.")
    except Exception as e:
        print(f"❌ Migration failed: {e}")

if __name__ == "__main__":
    migrate_seats()
