from typing import Annotated

from db.db_setup import get_db
from fastapi import Depends
from sqlalchemy.orm import Session

SessionDep = Annotated[Session, Depends(get_db)]
