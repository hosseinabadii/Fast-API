import models
import schemas
from database import create_db, get_db
from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session

create_db()

app = FastAPI()


@app.get("/")
def index():
    index_content = """
    <html>
    <head>
        <title>Home</title>
    </head>
    <body>
        <h1>Welcome to My Hotel API</h1>
        <p>See the Swagger UI to test it.</p>
        <a href="http://127.0.0.1:8000/docs">click here</a>
    </body>
    </html>
    """
    return HTMLResponse(index_content)


# Customer routers


@app.get("/customers/")
def read_all_customers(db: Session = Depends(get_db)):
    return db.query(models.DBCustomer).all()


@app.get("/customer/{customer_id}")
def read_customer(customer_id: int, db: Session = Depends(get_db)):
    db_customer = (
        db.query(models.DBCustomer).filter(models.DBCustomer.id == customer_id).first()
    )
    if db_customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    return db_customer


@app.post("/customer/")
def create_customer(data: schemas.CustomerCreateData, db: Session = Depends(get_db)):
    db_customer = models.DBCustomer(**data.model_dump())
    db.add(db_customer)
    db.commit()
    db.refresh(db_customer)
    return db_customer


@app.put("/customer/{customer_id}")
def update_customer(
    customer_id: int,
    data: schemas.CustomerUpdateData,
    db: Session = Depends(get_db),
):
    db_customer = (
        db.query(models.DBCustomer).filter(models.DBCustomer.id == customer_id).first()
    )
    if db_customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_customer, key, value)
    db.commit()
    db.refresh(db_customer)
    return db_customer


@app.delete("/customer/{customer_id}")
def delete_customer(customer_id: int, db: Session = Depends(get_db)):
    db_customer = (
        db.query(models.DBCustomer).filter(models.DBCustomer.id == customer_id).first()
    )
    if db_customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    db.delete(db_customer)
    db.commit()
    return db_customer


# Rooms routers


@app.get("/rooms/")
def read_all_rooms(db: Session = Depends(get_db)):
    return db.query(models.DBRoom).all()


@app.get("/room/{room_id}")
def read_room(room_id: int, db: Session = Depends(get_db)):
    db_room = db.query(models.DBRoom).filter(models.DBRoom.id == room_id).first()
    if db_room is None:
        raise HTTPException(status_code=404, detail="Room not found")
    return db_room


@app.post("/room/")
def create_room(data: schemas.RoomCreateData, db: Session = Depends(get_db)):
    db_room = models.DBRoom(**data.model_dump())
    db.add(db_room)
    db.commit()
    db.refresh(db_room)
    return db_room


@app.put("/room/{room_id}")
def update_room(
    room_id: int, data: schemas.RoomUpdateData, db: Session = Depends(get_db)
):
    db_room = db.query(models.DBRoom).filter(models.DBRoom.id == room_id).first()
    if db_room is None:
        raise HTTPException(status_code=404, detail="Room not found")
    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_room, key, value)
    db.commit()
    db.refresh(db_room)
    return db_room


@app.delete("/room/{room_id}")
def delete_room(room_id: int, db: Session = Depends(get_db)):
    db_room = db.query(models.DBRoom).filter(models.DBRoom.id == room_id).first()
    if db_room is None:
        raise HTTPException(status_code=404, detail="Room not found")
    db.delete(db_room)
    db.commit()
    return db_room


# Booking routers


@app.get("/bookings/")
def read_all_bookings(db: Session = Depends(get_db)):
    return db.query(models.DBBooking).all()


@app.get("/booking/{booking_id}")
def read_booking(booking_id: int, db: Session = Depends(get_db)):
    db_booking = (
        db.query(models.DBBooking).filter(models.DBBooking.id == booking_id).first()
    )
    if db_booking is None:
        raise HTTPException(status_code=404, detail="Booking not found")
    return db_booking


@app.post("/booking/")
def create_booking(data: schemas.BookingCreateData, db: Session = Depends(get_db)):
    db_room = db.query(models.DBRoom).filter(models.DBRoom.id == data.room_id).first()
    if db_room is None:
        raise HTTPException(status_code=404, detail="Room not found")

    db_customer = (
        db.query(models.DBCustomer)
        .filter(models.DBCustomer.id == data.customer_id)
        .first()
    )
    if db_customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")

    days = (data.to_date - data.from_date).days
    if days <= 0:
        raise HTTPException(status_code=422, detail="Invalid dates")

    price = db_room.price * days
    db_booking = models.DBBooking(**data.dict(), price=price)
    db.add(db_booking)
    db.commit()
    db.refresh(db_booking)
    return db_booking


@app.put("/booking/{booking_id}")
def update_booking(
    booking_id: int, data: schemas.BookingUpdateData, db: Session = Depends(get_db)
):
    db_booking = (
        db.query(models.DBBooking).filter(models.DBBooking.id == booking_id).first()
    )
    if db_booking is None:
        raise HTTPException(status_code=404, detail="Booking not found")

    room_id = data.room_id
    if room_id is None:
        room_id = db_booking.room_id
    db_room = db.query(models.DBRoom).filter(models.DBRoom.id == room_id).first()
    if db_room is None:
        raise HTTPException(status_code=404, detail="Room not found")

    if data.customer_id is not None:
        db_customer = (
            db.query(models.DBCustomer)
            .filter(models.DBCustomer.id == data.customer_id)
            .first()
        )
        if db_customer is None:
            raise HTTPException(status_code=404, detail="Customer not found")

    from_date = data.from_date
    if from_date is None:
        from_date = db_booking.from_date

    to_date = data.to_date
    if to_date is None:
        to_date = db_booking.to_date

    days = (to_date - from_date).days
    if days <= 0:
        raise HTTPException(status_code=422, detail="Invalid dates")

    price = db_room.price * days
    update_data = data.model_dump(exclude_unset=True)
    update_data.update(price=price)
    for key, value in update_data.items():
        setattr(db_booking, key, value)
    db.commit()
    db.refresh(db_booking)
    return db_booking


@app.delete("/booking/{booking_id}")
def delete_booking(booking_id: int, db: Session = Depends(get_db)):
    db_booking = (
        db.query(models.DBBooking).filter(models.DBBooking.id == booking_id).first()
    )
    if db_booking is None:
        raise HTTPException(status_code=404, detail="Booking not found")
    db.delete(db_booking)
    db.commit()
    return db_booking
