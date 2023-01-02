from fastapi import Body, FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import schemas, models, database, oauth2, utils

router = APIRouter(prefix="/vote", tags=["User Voting"])


@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(
    vote: schemas.Vote,
    db: Session = Depends(database.get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post number {vote.post_id} does not exist.",
        )
    vote_query = db.query(models.Vote).filter(
        models.Vote.post_id == vote.post_id,
        models.Vote.user_name == current_user.username,
    )
    found_vote = vote_query.first()
    if vote.dir == 1:
        if found_vote:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"user {current_user.username} has already voted for the post {vote.post_id}",
            )
        new_vote = models.Vote(post_id=vote.post_id, user_name=current_user.username)
        db.add(new_vote)
        db.commit()
        return {"message": "successfully upvoted"}
    else:
        if not found_vote:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=f"vote does not exist"
            )
        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"message": "successfully downvoted"}
