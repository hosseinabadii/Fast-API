from fastapi import HTTPException
from sqlalchemy.orm import Session

from hotel.db.models import DBCustomer
from hotel.operations.schemas import CustomerCreateData, CustomerUpdateData


def read_all_customers(db: Session):
    return db.query(DBCustomer).all()


def read_customer(db: Session, customer_id: int):
    db_customer = db.query(DBCustomer).filter(DBCustomer.id == customer_id).first()
    if db_customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    return db_customer


def create_customer(db: Session, data: CustomerCreateData):
    db_customer = DBCustomer(**data.dict())
    db.add(db_customer)
    db.commit()
    db.refresh(db_customer)
    return db_customer


def update_customer(
    db: Session,
    customer_id: int,
    data: CustomerUpdateData,
):
    db_customer = db.query(DBCustomer).filter(DBCustomer.id == customer_id).first()
    if db_customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    update_data = data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_customer, key, value)
    db.commit()
    db.refresh(db_customer)
    return db_customer


def delete_customer(db: Session, customer_id: int):
    db_customer = db.query(DBCustomer).filter(DBCustomer.id == customer_id).first()
    if db_customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    db.delete(db_customer)
    db.commit()
