from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Enum
from sqlalchemy.orm import relationship
from database import Base
import enum

class UserRole(str, enum.Enum):
    ADMIN = "admin"
    STUDENT = "student"

class RoomType(str, enum.Enum):
    AC = "ac"
    NON_AC = "non_ac"

class SeaterType(str, enum.Enum):
    THREE = "3"
    FOUR = "4"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    role = Column(Enum(UserRole), default=UserRole.STUDENT)
    is_active = Column(Boolean, default=True)
    
    bookings = relationship("Booking", back_populates="user")

class Hostel(Base):
    __tablename__ = "hostels"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    location = Column(String, nullable=True)
    description = Column(String)

    rooms = relationship("Room", back_populates="hostel")

class Room(Base):
    __tablename__ = "rooms"

    id = Column(Integer, primary_key=True, index=True)
    hostel_id = Column(Integer, ForeignKey("hostels.id"))
    room_number = Column(String)
    type = Column(Enum(RoomType))
    capacity = Column(Enum(SeaterType))
    available_seats = Column(Integer, default=0)
    price = Column(Integer)
    is_available = Column(Boolean, default=True)

    hostel = relationship("Hostel", back_populates="rooms")
    bookings = relationship("Booking", back_populates="room")

class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    room_id = Column(Integer, ForeignKey("rooms.id"))
    booking_date = Column(String) # Storing as string for simplicity, can be DateTime

    user = relationship("User", back_populates="bookings")
    room = relationship("Room", back_populates="bookings")
