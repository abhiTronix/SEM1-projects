from fastapi import Body, FastAPI, Response, status, HTTPException, Depends, APIRouter
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import func
from sqlalchemy import and_
from sqlalchemy.orm.attributes import flag_modified
from .. import models, schemas, oauth2, utils
import io
from pathlib import Path
from typing import List, Optional
from ..database import get_db
from ..config import settings
import json
import errno
import os
import sys

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
    username: Optional[str] = "",
    search: Optional[str] = "",
):
    posts = (
        db.query(models.Post, func.count(models.Vote.post_id).label("votes"))
        .join(models.Vote, models.Post.id == models.Vote.post_id, isouter=True)
        .group_by(models.Post.id)
        .filter(
            models.Post.username.contains(username)
            if username
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


@router.put("/tpublish/{id}", response_model=schemas.PostMod)
def update_post_publish_status(
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
    post_query.update(updated_post_dict, synchronize_session=False)
    db.commit()
    return post_query.first()


@router.delete(
    "/deletefile/{username}/{sub}/{filename}", status_code=status.HTTP_204_NO_CONTENT
)
async def delete_post(
    username: str,
    sub: str,
    filename: str,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    filename = filename.strip()
    subsplit = sub.strip().split("_")
    if len(subsplit) > 1:
        sub, _ = subsplit
    else:
        sub = subsplit[0]
    print(sub)
    post_query = db.query(models.Post).filter(
        and_(
            models.Post.owner_username == username,
            models.Post.subject_code == sub,
        )
    )
    post = post_query.first()
    if post is None or not (filename in post.revision):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Files with filename: {filename} does not exist.",
        )
    files = db.query(models.Files).filter(
        and_(
            models.Files.owner_username == username,
            models.Files.filename == filename,
        )
    )
    post_dict = dict()
    pos_del_file = files.first().filepath
    curr_rev = post.revision
    if filename in curr_rev:
        curr_rev.remove(filename)
    post_dict["revision"] = curr_rev
    if len(curr_rev) > 0:
        post_dict["curr_version"] = curr_rev[-1]
        post_query.update(post_dict, synchronize_session=False)
        db.commit()
    else:
        post_query.delete(synchronize_session=False)
        db.commit()
    if files:
        files.delete(synchronize_session=False)
        db.commit()
    if os.path.isfile(pos_del_file):
        delete_file_safe(pos_del_file)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.delete("/deletesub/{username}/{sub}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_all_posts(
    username: str,
    sub: str,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    subsplit = sub.strip().split("_")
    if len(subsplit) > 1:
        sub, _ = subsplit
    else:
        sub = subsplit
    print(sub)
    post_query = db.query(models.Post).filter(
        and_(
            models.Post.owner_username == username,
            models.Post.subject_code == sub,
        )
    )
    post = post_query.first()
    files = db.query(models.Files).filter(
        and_(
            models.Files.owner_username == username,
            models.Files.subject_code == sub,
        )
    )
    files_d = files.all()
    files_del = [f.filepath for f in files_d]
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with subject code: {sub} does not exist.",
        )
    post_query.delete(synchronize_session=False)
    db.commit()
    if files:
        files.delete(synchronize_session=False)
        db.commit()
    for f in files_del:
        delete_file_safe(f)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.delete("/deleteuser/{username}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    username: str,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    subsplit = sub.strip().split("_")
    if len(subsplit) > 1:
        sub, _ = subsplit
    else:
        sub = subsplit
    print(sub)
    post_query = db.query(models.Post).filter(models.Post.owner_username == username)
    post = post_query.first()
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with username: {username} does not exist.",
        )
    post_query.delete(synchronize_session=False)
    db.commit()
    votes = db.query(models.Vote).filter(models.Files.owner_username == username)
    votes.delete(synchronize_session=False)
    db.commit()
    files = db.query(models.Files).filter(models.Files.owner_username == username)
    files.delete(synchronize_session=False)
    db.commit()
    user = db.query(models.User).filter(models.Files.owner_username == username)
    user.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
