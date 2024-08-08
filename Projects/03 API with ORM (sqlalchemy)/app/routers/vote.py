from db.db_setup import get_session
from db.models import Vote as DBVote
from fastapi import APIRouter, Depends, HTTPException, status
from oauth2 import get_current_user
from operations.item import get_item_by_id
from schemas.token import Vote
from schemas.user import User
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/vote",
    tags=["Vote"],
)


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_vote(
    vote: Vote,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    item = get_item_by_id(session, vote.item_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item with id={vote.item_id} does not exists.",
        )

    vote_query = session.query(DBVote).filter(
        DBVote.item_id == vote.item_id, DBVote.user_id == current_user.id
    )
    found_vote = vote_query.first()

    if vote.vote_dir:
        if found_vote:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"User {current_user.id} has already voted on item {vote.item_id}.",
            )
        new_vote = DBVote(user_id=current_user.id, item_id=vote.item_id)
        session.add(new_vote)
        session.commit()
        return {"message": "successfully added vote."}

    if not found_vote:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Vote does not exists."
        )
    vote_query.delete(synchronize_session=False)
    session.commit()
    return {"message": "successfully deleted vote."}
