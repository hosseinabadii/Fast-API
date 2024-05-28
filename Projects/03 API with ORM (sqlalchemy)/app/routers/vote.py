from fastapi import Depends, APIRouter, HTTPException, status
from sqlalchemy.orm import Session
from .. import schemas, oauth2, models, crud
from ..database import get_db


router = APIRouter(
    prefix="/vote",
    tags=["Vote"],
)


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_vote(
    vote: schemas.Vote,
    current_user: schemas.User = Depends(oauth2.get_current_user),
    db: Session = Depends(get_db),
):
    item = crud.get_item(db, vote.item_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item with id={vote.item_id} does not exists.",
        )

    vote_query = db.query(models.Vote).filter(
        models.Vote.item_id == vote.item_id, models.Vote.user_id == current_user.id
    )
    found_vote = vote_query.first()

    if vote.vote_dir:
        if found_vote:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"User {current_user.id} has already voted on item {vote.item_id}.",
            )
        new_vote = models.Vote(user_id=current_user.id, item_id=vote.item_id)
        db.add(new_vote)
        db.commit()
        return {"message": "successfully added vote."}

    if not found_vote:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Vote does not exists."
        )
    vote_query.delete(synchronize_session=False)
    db.commit()
    return {"message": "successfully deleted vote."}
