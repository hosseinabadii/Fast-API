from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from ..db.database import get_session
from ..operations.customers import (
    create_customer,
    delete_customer,
    read_all_customers,
    read_customer,
    update_customer,
)
from ..operations.schemas import CustomerCreateData, CustomerResult, CustomerUpdateData

router = APIRouter(tags=["Customers"])


@router.get("/customers/", response_model=list[CustomerResult])
def api_read_all_customers(session: Session = Depends(get_session)):
    return read_all_customers(session)


@router.get("/customer/{customer_id}", response_model=CustomerResult)
def api_read_customer(customer_id: int, session: Session = Depends(get_session)):
    return read_customer(session, customer_id)


@router.post(
    "/customer/", response_model=CustomerResult, status_code=status.HTTP_201_CREATED
)
def api_create_customer(
    customer: CustomerCreateData,
    session: Session = Depends(get_session),
):
    return create_customer(session, customer)


@router.put(
    "/customer/{customer_id}",
    response_model=CustomerResult,
    status_code=status.HTTP_202_ACCEPTED,
)
def api_update_customer(
    customer_id: int,
    customer: CustomerUpdateData,
    session: Session = Depends(get_session),
):
    return update_customer(session, customer_id, customer)


@router.delete("/customer/{customer_id}", status_code=status.HTTP_204_NO_CONTENT)
def api_delete_customer(customer_id: int, session: Session = Depends(get_session)):
    return delete_customer(session, customer_id)
