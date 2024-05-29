from fastapi import HTTPException
from sqlalchemy.orm import Session

from ..db.models import DBCustomer
from ..operations.schemas import CustomerCreateData, CustomerUpdateData


def read_all_customers(session: Session):
    return session.query(DBCustomer).all()


def read_customer(session: Session, customer_id: int):
    db_customer = session.get(DBCustomer, customer_id)
    if db_customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    return db_customer


def create_customer(session: Session, data: CustomerCreateData):
    db_customer = DBCustomer(**data.model_dump())
    session.add(db_customer)
    session.commit()
    session.refresh(db_customer)
    return db_customer


def update_customer(
    session: Session,
    customer_id: int,
    data: CustomerUpdateData,
):
    db_customer = session.get(DBCustomer, customer_id)
    if db_customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_customer, key, value)
    session.commit()
    session.refresh(db_customer)
    return db_customer


def delete_customer(session: Session, customer_id: int):
    db_customer = session.get(DBCustomer, customer_id)
    if db_customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    session.delete(db_customer)
    session.commit()
