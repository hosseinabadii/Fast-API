from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from hotel.db.database import get_db
from hotel.operations.customers import (
    create_customer,
    delete_customer,
    read_all_customers,
    read_customer,
    update_customer,
)
from hotel.operations.schemas import (
    CustomerCreateData,
    CustomerResult,
    CustomerUpdateData,
)

router = APIRouter(tags=["Customers"])


@router.get("/customers/", response_model=list[CustomerResult])
def api_read_all_customers(db: Session = Depends(get_db)):
    return read_all_customers(db)


@router.get("/customer/{customer_id}", response_model=CustomerResult)
def api_read_customer(customer_id: int, db: Session = Depends(get_db)):
    return read_customer(db, customer_id)


@router.post(
    "/customer/", response_model=CustomerResult, status_code=status.HTTP_201_CREATED
)
def api_create_customer(customer: CustomerCreateData, db: Session = Depends(get_db)):
    return create_customer(db, customer)


@router.put(
    "/customer/{customer_id}",
    response_model=CustomerResult,
    status_code=status.HTTP_202_ACCEPTED,
)
def api_update_customer(
    customer_id: int, customer: CustomerUpdateData, db: Session = Depends(get_db)
):
    return update_customer(db, customer_id, customer)


@router.delete("/customer/{customer_id}", status_code=status.HTTP_204_NO_CONTENT)
def api_delete_customer(customer_id: int, db: Session = Depends(get_db)):
    return delete_customer(db, customer_id)
