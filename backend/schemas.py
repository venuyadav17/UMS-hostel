from pydantic import BaseModel, EmailStr
from typing import List, Optional
from models import UserRole, RoomType, SeaterType

class UserBase(BaseModel):
    username: str
    email: EmailStr
    role: UserRole

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    is_active: bool = True

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

class RoomBase(BaseModel):
    room_number: str
    type: RoomType
    capacity: SeaterType
    price: int

class RoomCreate(RoomBase):
    available_seats: Optional[int] = None
    is_available: Optional[bool] = None

class Room(RoomBase):
    id: int
    hostel_id: int
    available_seats: int
    is_available: bool

    class Config:
        orm_mode = True

class HostelBase(BaseModel):
    name: str
    location: Optional[str] = None
    description: Optional[str] = None

class HostelCreate(HostelBase):
    pass

class Hostel(HostelBase):
    id: int
    rooms: List[Room] = []

    class Config:
        orm_mode = True

class BookingBase(BaseModel):
    room_id: int
    booking_date: str

class BookingCreate(BookingBase):
    additional_student_ids: List[int] = []

class Booking(BookingBase):
    id: int
    user_id: int
    room: Optional[Room] = None

    class Config:
        orm_mode = True
