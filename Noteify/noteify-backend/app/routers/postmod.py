from fastapi import Body, FastAPI, Response, status, HTTPException, Depends, APIRouter
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import func
from sqlalchemy import and_
from sqlalchemy.orm.attributes import flag_modified
from .. import models, schemas, oauth2, utils
from ..database import get_db
from ..config import settings

router = APIRouter(prefix="/mhposts", tags=["Moderator Posts Roles"])


@router.get(
    "/",
    response_model=List[schemas.PostModOut],
)
async def get_posts(
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_moderator),
    limit: int = 10,
    skip: int = 0,
    user: Optional[str] = "",
    search: Optional[str] = "",
):
    posts = (
        db.query(models.Post, func.count(models.Vote.post_id).label("votes"))
        .join(models.Vote, models.Post.id == models.Vote.post_id, isouter=True)
        .group_by(models.Post.id)
        .filter(
            models.Post.username.contains(user)
            if user
            else models.Post.subject_code.contains(search)
        )
        .limit(limit)
        .offset(skip)
        .all()
    )
    return posts


@router.get("/{id}", response_model=schemas.PostModOut)
async def get_post(
    id: int,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_moderator),
):
    post = (
        db.query(models.Post, func.count(models.Vote.post_id).label("votes"))
        .join(models.Vote, models.Post.id == models.Vote.post_id, isouter=True)
        .group_by(models.Post.id)
        .filter(models.Post.id == id)
        .first()
    )
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} was not found",
        )
    return post


@router.put("/{id}", response_model=schemas.PostMod)
def update_post(
    id: int,
    updated_post: schemas.PostModUpdate,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_moderator),
):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} does not exist.",
        )
    updated_post_dict = updated_post.dict()
    new_rev = updated_post.revision
    if len(new_rev) == 0:
        updated_post_dict["curr_version"] = ""
    else:
        updated_post_dict["curr_version"] = new_rev[-1]
    post_query.update(updated_post_dict, synchronize_session=False)
    db.commit()
    return post_query.first()


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(
    id: int,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_moderator),
):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} does not exist.",
        )
    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
