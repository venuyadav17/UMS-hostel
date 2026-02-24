from sqlalchemy.orm import Session
import models, schemas
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

from sqlalchemy import func, or_
import json
import time
import urllib.request
import urllib.error

def get_user(db: Session, username: str):
    return db.query(models.User).filter(
        or_(
            func.lower(models.User.username) == username.lower(),
            func.lower(models.User.email) == username.lower()
        )
    ).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = pwd_context.hash(user.password)
    db_user = models.User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password,
        role=user.role
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_hostels(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Hostel).offset(skip).limit(limit).all()

def create_hostel(db: Session, hostel: schemas.HostelCreate):
    db_hostel = models.Hostel(**hostel.dict())
    db.add(db_hostel)
    db.commit()
    db.refresh(db_hostel)
    return db_hostel

def get_rooms(db: Session, hostel_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.Room).filter(models.Room.hostel_id == hostel_id).offset(skip).limit(limit).all()

def create_room(db: Session, room: schemas.RoomCreate, hostel_id: int):
    # Initialize available_seats to capacity
    # #region agent log
    try:
        payload = json.dumps({
            "sessionId": "fc7b05",
            "runId": "initial",
            "hypothesisId": "H1",
            "location": "backend/crud.py:create_room:before",
            "message": "Creating room with capacity enum",
            "data": {
                "hostel_id": hostel_id,
                "capacity_raw": str(room.capacity)
            },
            "timestamp": int(time.time() * 1000)
        }).encode("utf-8")
        req = urllib.request.Request(
            "http://127.0.0.1:7278/ingest/6e3db191-d12b-4af7-a4d2-76ae65c9a96e",
            data=payload,
            headers={
                "Content-Type": "application/json",
                "X-Debug-Session-Id": "fc7b05",
            },
            method="POST",
        )
        urllib.request.urlopen(req, timeout=0.5)
    except Exception:
        pass
    # #endregion

    # Derive numeric capacity from enum or raw value
    capacity_value = room.capacity.value if hasattr(room.capacity, "value") else room.capacity
    capacity_int = int(capacity_value)

    # Use provided available_seats or default to capacity
    available_seats = room.available_seats if room.available_seats is not None else capacity_int
    is_available = room.is_available if room.is_available is not None else True

    db_room = models.Room(
        hostel_id=hostel_id,
        room_number=room.room_number,
        type=room.type,
        capacity=room.capacity,
        price=room.price,
        available_seats=available_seats,
        is_available=is_available
    )
    db.add(db_room)
    db.commit()
    db.refresh(db_room)
    return db_room

def create_booking(db: Session, booking: schemas.BookingCreate, user_id: int):
    # Check if room is available
    room = db.query(models.Room).filter(models.Room.id == booking.room_id).first()

    total_group_size = 1 + len(booking.additional_student_ids)

    # #region agent log
    try:
        payload = json.dumps({
            "sessionId": "fc7b05",
            "runId": "initial",
            "hypothesisId": "H2",
            "location": "backend/crud.py:create_booking:before",
            "message": "Before booking seat check",
            "data": {
                "room_id": booking.room_id,
                "user_id": user_id,
                "additional_student_ids": booking.additional_student_ids,
                "room_exists": room is not None,
                "room_available_flag": getattr(room, "is_available", None) if room else None,
                "available_seats_before": getattr(room, "available_seats", None) if room else None,
                "total_group_size": total_group_size
            },
            "timestamp": int(time.time() * 1000)
        }).encode("utf-8")
        req = urllib.request.Request(
            "http://127.0.0.1:7278/ingest/6e3db191-d12b-4af7-a4d2-76ae65c9a96e",
            data=payload,
            headers={
                "Content-Type": "application/json",
                "X-Debug-Session-Id": "fc7b05",
            },
            method="POST",
        )
        urllib.request.urlopen(req, timeout=0.5)
    except Exception:
        pass
    # #endregion

    if not room or not room.is_available or room.available_seats < total_group_size:
        return None

    bookings_to_add = []

    # Create booking for primary user
    db_booking = models.Booking(room_id=booking.room_id, booking_date=booking.booking_date, user_id=user_id)
    bookings_to_add.append(db_booking)

    # Create bookings for group members
    for student_id in booking.additional_student_ids:
        peer_booking = models.Booking(room_id=booking.room_id, booking_date=booking.booking_date, user_id=student_id)
        bookings_to_add.append(peer_booking)

    db.add_all(bookings_to_add)

    # Decrease available seats
    room.available_seats -= total_group_size
    if room.available_seats == 0:
        room.is_available = False

    db.commit()
    db.refresh(db_booking)

    # #region agent log
    try:
        payload = json.dumps({
            "sessionId": "fc7b05",
            "runId": "initial",
            "hypothesisId": "H3",
            "location": "backend/crud.py:create_booking:after",
            "message": "After booking seat update",
            "data": {
                "room_id": booking.room_id,
                "user_id": user_id,
                "available_seats_after": room.available_seats,
                "room_available_flag_after": room.is_available,
                "total_group_size": total_group_size
            },
            "timestamp": int(time.time() * 1000)
        }).encode("utf-8")
        req = urllib.request.Request(
            "http://127.0.0.1:7278/ingest/6e3db191-d12b-4af7-a4d2-76ae65c9a96e",
            data=payload,
            headers={
                "Content-Type": "application/json",
                "X-Debug-Session-Id": "fc7b05",
            },
            method="POST",
        )
        urllib.request.urlopen(req, timeout=0.5)
    except Exception:
        pass
    # #endregion

    return db_booking

def get_user_bookings(db: Session, user_id: int):
    return db.query(models.Booking).filter(models.Booking.user_id == user_id).all()
