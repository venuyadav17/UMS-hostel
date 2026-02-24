import sys
sys.path.insert(0, 'c:\\Users\\atike\\OneDrive\\Desktop\\PEP\\UMS-hostel\\backend')

from database import SessionLocal
from models import Hostel, Room, Booking

db = SessionLocal()

# Clear all bookings first (due to foreign key constraints)
db.query(Booking).delete()
db.commit()

# Clear all rooms
db.query(Room).delete()
db.commit()

# Clear all hostels
db.query(Hostel).delete()
db.commit()

print("✅ All hostels and rooms cleared!")
print("   You can now add hostels from the admin panel")

db.close()
