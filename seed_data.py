import sys
sys.path.insert(0, 'c:\\Users\\atike\\OneDrive\\Desktop\\PEP\\UMS-hostel\\backend')

from database import SessionLocal, engine, Base
from models import Hostel, Room, Booking, RoomType, SeaterType

# Recreate all tables with the current schema
Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

db = SessionLocal()

# Create sample hostels
hostels_data = [
    {
        "name": "Green Haven Hostel",
        "location": "Near Campus Gate 1",
        "description": "Modern hostel with excellent facilities and friendly environment"
    },
    {
        "name": "Sunrise Residency",
        "location": "University Avenue",
        "description": "Budget-friendly accommodation with good food services"
    },
    {
        "name": "Elite Dormitory",
        "location": "Premium Zone",
        "description": "Advanced amenities including gym, study area, and recreation"
    }
]

hostels = []
for hostel_data in hostels_data:
    hostel = Hostel(**hostel_data)
    db.add(hostel)
    hostels.append(hostel)

db.commit()

# Create sample rooms for each hostel
rooms_config = [
    {"room_number": "101", "type": RoomType.AC, "capacity": SeaterType.THREE, "available_seats": 2, "price": 15000},
    {"room_number": "102", "type": RoomType.AC, "capacity": SeaterType.FOUR, "available_seats": 3, "price": 18000},
    {"room_number": "103", "type": RoomType.NON_AC, "capacity": SeaterType.THREE, "available_seats": 1, "price": 10000},
    {"room_number": "104", "type": RoomType.NON_AC, "capacity": SeaterType.FOUR, "available_seats": 0, "price": 12000},
    {"room_number": "201", "type": RoomType.AC, "capacity": SeaterType.THREE, "available_seats": 3, "price": 15000},
    {"room_number": "202", "type": RoomType.AC, "capacity": SeaterType.FOUR, "available_seats": 2, "price": 18000},
]

for hostel in hostels:
    for config in rooms_config:
        room = Room(
            hostel_id=hostel.id,
            room_number=config["room_number"],
            type=config["type"],
            capacity=config["capacity"],
            available_seats=config["available_seats"],
            price=config["price"],
            is_available=config["available_seats"] > 0
        )
        db.add(room)

db.commit()
print("✅ Sample data added successfully!")
print(f"   - {len(hostels)} hostels created")
print(f"   - {len(hostels) * len(rooms_config)} rooms created")
db.close()
