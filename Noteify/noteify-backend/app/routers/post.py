from fastapi import (
    Body,
    FastAPI,
    Response,
    status,
    HTTPException,
    Depends,
    APIRouter,
    BackgroundTasks,
)
from fastapi.responses import FileResponse
import io
from pathlib import Path
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import func
from sqlalchemy import and_
from sqlalchemy.orm.attributes import flag_modified
from fastapi import FastAPI, File, UploadFile
from .. import models, schemas, oauth2, utils
from ..database import get_db
from ..config import settings
import json
import errno
import os
import sys

router = APIRouter(prefix="/posts", tags=["User Posts Roles"])


def mkdir_safe(dir_path):
    """
    ## mkdir_safe
    Safely creates directory at given path.
    Parameters:
        dir_path (string): path to the directory
        logging (bool): enables logging for its operations
    """
    try:
        os.makedirs(dir_path)
    except (OSError, IOError) as e:
        if e.errno != errno.EACCES and e.errno != errno.EEXIST:
            raise


def delete_file_safe(file_path):
    """
    ## delete_ext_safe
    Safely deletes files at given path.
    Parameters:
        file_path (string): path to the file
    """
    try:
        dfile = Path(file_path)
        if sys.version_info >= (3, 8, 0):
            dfile.unlink(missing_ok=True)
        else:
            dfile.exists() and dfile.unlink()
    except Exception as e:
        print(str(e))


@router.get("/subcodes")
async def get_supported_subject_codes(
    current_user: int = Depends(oauth2.get_current_user),
):
    formatted_list = [
        "{}_{}".format(x, y) for x, y in settings.supported_subcodes.items()
    ]
    return Response(content=json.dumps(formatted_list), media_type="application/json")


# @router.get("/{sub}")
# async def get_versions(
#     db: Session = Depends(get_db),
#     current_user: int = Depends(oauth2.get_current_user),
# ):
#     post_query = db.query(models.Post).filter(
#         and_(
#             models.Post.owner_username == current_user.username,
#             models.Post.curr_version == sub,
#         )
#     )
#     post_q = post_query.first()
#     if post_q:
#         return Response(
#             content=json.dumps(formatted_list), media_type="application/json"
#         )
#     else:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail=f"data with subid: {sub} was not found",
#         )


# @router.get("/subcodes")
# async def get_supported_subject_codes(
#     current_user: int = Depends(oauth2.get_current_user),
#     response_model=List[schemas.SubjectCodes],
# ):
#     return {k: v for k, v in enumerate(settings.supported_subcodes)}


@router.get(
    "/",
    response_model=List[schemas.PostOut],
)
async def get_all_posts(
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
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


# @router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
# async def create_posts(
#     post: schemas.PostCreate,
#     db: Session = Depends(get_db),
#     current_user: int = Depends(oauth2.get_current_user),
# ):
#     if not post.subject_code.strip().upper() in settings.supported_subcodes:
#         raise HTTPException(
#             status_code=status.HTTP_406_NOT_ACCEPTABLE,
#             detail=f"Posts on subject: {post.subject_code.strip()} is not accepted yet.",
#         )
#     post_query = db.query(models.Post).filter(
#         and_(
#             models.Post.owner_username == current_user.username,
#             models.Post.subject_code == post.subject_code,
#         )
#     )
#     post_q = post_query.first()
#     if post_q:
#         raise HTTPException(
#             status_code=status.HTTP_409_CONFLICT,
#             detail=f"post already exists. Try updating it instead",
#         )
#     else:
#         new_rev = [post.curr_version]
#         new_post = models.Post(
#             owner_username=current_user.username, revision=new_rev, **post.dict()
#         )
#         db.add(new_post)
#         db.commit()
#         db.refresh(new_post)
#         return new_post


@router.get(
    "/{id}",
    response_model=schemas.PostOut,
)
async def get_post(
    id: int,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
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


# @router.put(
#     "/{id}",
#     response_model=schemas.Post,
# )
# def update_post(
#     id: int,
#     updated_post: schemas.PostUpdate,
#     db: Session = Depends(get_db),
#     current_user: int = Depends(oauth2.get_current_user),
# ):
#     post_query = db.query(models.Post).filter(models.Post.id == id)
#     post = post_query.first()
#     if post == None:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail=f"post with id: {id} does not exist.",
#         )
#     if post.owner_username != current_user.username:
#         raise HTTPException(
#             status_code=status.HTTP_403_FORBIDDEN,
#             detail="Not authorized to perform requested action",
#         )
#     updated_post_dict = updated_post.dict()
#     prev_rev = post.revision
#     if not updated_post.curr_version and post.curr_version in prev_rev:
#         prev_rev.remove(updated_post.curr_version)
#         if len(prev_rev) >= 1:
#             updated_post_dict["curr_version"] = prev_rev[-1]
#     elif updated_post.curr_version in prev_rev:
#         updated_post_dict.pop("curr_version", "")
#         print("Cannot update same version again.")
#     else:
#         prev_rev.append(updated_post.curr_version)
#     updated_post_dict["revision"] = prev_rev
#     post_query.update(updated_post_dict, synchronize_session=False)
#     db.commit()
#     return post_query.first()


@router.get(
    "/revision/{sub}",
)
async def get_all_revisions(
    sub: str,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    subsplit = sub.strip().split("_")
    if len(subsplit) > 1:
        sub, _ = subsplit
    else:
        sub = subsplit[0]
    print(sub)
    post_query = db.query(models.Post).filter(
        and_(
            models.Post.owner_username == current_user.username,
            models.Post.subject_code == sub,
        )
    )
    post = post_query.first()
    if post == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post for subject: {sub} does not exist.",
        )
    return Response(content=json.dumps(post.revision), media_type="application/json")


@router.get(
    "/find/{sub}",
    response_model=schemas.PostOut,
)
async def get_post(
    sub: str,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    subsplit = sub.strip().split("_")
    if len(subsplit) > 1:
        sub, _ = subsplit
    else:
        sub = subsplit[0]
    print(sub)
    post = (
        db.query(models.Post, func.count(models.Vote.post_id).label("votes"))
        .join(models.Vote, models.Post.id == models.Vote.post_id, isouter=True)
        .group_by(models.Post.id)
        .filter(models.Post.subject_code == sub)
        .first()
    )
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} was not found",
        )
    return post


@router.post("/{sub}")
async def create_and_update_post(
    sub: str,
    file: UploadFile | None,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    sub = sub.strip().encode("ascii", "replace").decode()
    print(sub)
    subsplit = sub.split("_")
    if len(subsplit) > 1:
        sub, _ = subsplit
    else:
        sub = subsplit[0]
    print(sub)
    if not sub.strip().upper() in settings.supported_subcodes:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail=f"Posts on subject: {sub.strip()} is not accepted yet.",
        )
    post_query = db.query(models.Post).filter(
        and_(
            models.Post.owner_username == current_user.username,
            models.Post.subject_code == sub,
        )
    )
    post_q = post_query.first()
    files = db.query(models.Files)
    if post_q:
        if post_q.owner_username != current_user.username:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to perform requested action",
            )
        prev_rev = post_q.revision
        if file.filename == post_q.curr_version or file.filename in prev_rev:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Cannot update same version again. Try different filename.",
            )
        dfolder = "@{}".format(current_user.username)
        fpath = os.path.abspath(os.path.join(*["data", sub, dfolder, file.filename]))
        ffolder = os.path.dirname(fpath)
        prev_rev.append(file.filename)
        post_dict = dict(
            curr_version=file.filename,
            revision=prev_rev,
            subject_code=post_q.subject_code,
            owner_username=current_user.username,
        )
        post_query.update(post_dict, synchronize_session=False)
        db.commit()
        new_files = models.Files(
            owner_username=current_user.username,
            subject_code=post_q.subject_code,
            filename=file.filename,
            filepath=fpath,
        )
        db.add(new_files)
        db.commit()
        db.refresh(new_files)
        try:
            mkdir_safe(ffolder)
            contents = file.file.read()
            with open(fpath, "wb") as f:
                f.write(contents)
        except Exception:
            return {"message": "There was an error updating the file"}
        finally:
            file.file.close()
        return {"message": f"Successfully updated {file.filename}"}
    else:
        dfolder = "@{}".format(current_user.username)
        fpath = os.path.abspath(os.path.join(*["data", sub, dfolder, file.filename]))
        ffolder = os.path.dirname(fpath)
        new_rev = [file.filename]
        new_post = models.Post(
            owner_username=current_user.username,
            revision=new_rev,
            subject_code=sub,
            curr_version=file.filename,
        )
        new_files = models.Files(
            owner_username=current_user.username,
            subject_code=sub,
            filename=file.filename,
            filepath=fpath,
        )
        db.add(new_post)
        db.commit()
        db.refresh(new_post)
        db.add(new_files)
        db.commit()
        db.refresh(new_files)
        try:
            mkdir_safe(ffolder)
            contents = file.file.read()
            with open(fpath, "wb") as f:
                f.write(contents)
        except Exception:
            return {"message": "There was an error uploading the file"}
        finally:
            file.file.close()
        return {"message": f"Successfully uploaded {file.filename}"}


# @router.post("/create/{sub}")
# async def create_post(
#     sub: str,
#     file: UploadFile | None,
#     db: Session = Depends(get_db),
#     current_user: int = Depends(oauth2.get_current_user),
# ):
#     sub = sub.strip()
#     if not sub.strip().upper() in settings.supported_subcodes:
#         raise HTTPException(
#             status_code=status.HTTP_406_NOT_ACCEPTABLE,
#             detail=f"Posts on subject: {sub.strip()} is not accepted yet.",
#         )
#     post_query = db.query(models.Post).filter(
#         and_(
#             models.Post.owner_username == current_user.username,
#             models.Post.subject_code == sub,
#         )
#     )
#     post_q = post_query.first()
#     files = db.query(models.Files)
#     if post_q:
#         raise HTTPException(
#             status_code=status.HTTP_409_CONFLICT,
#             detail=f"Post already created. Try update",
#         )
#     else:
#         dfolder = "@{}".format(current_user.username)
#         fpath = os.path.abspath(os.path.join(*["data", sub, dfolder, file.filename]))
#         ffolder = os.path.dirname(fpath)
#         try:
#             mkdir_safe(ffolder)
#             contents = file.file.read()
#             with open(fpath, "wb") as f:
#                 f.write(contents)
#         except Exception:
#             return {"message": "There was an error uploading the file"}
#         finally:
#             file.file.close()
#         new_rev = [file.filename]
#         new_post = models.Post(
#             owner_username=current_user.username,
#             revision=new_rev,
#             subject_code=sub,
#             curr_version=file.filename,
#         )
#         new_files = models.Files(
#             owner_username=current_user.username,
#             subject_code=sub,
#             filename=file.filename,
#             filepath=fpath,
#         )
#         db.add(new_post)
#         db.commit()
#         db.refresh(new_post)
#         db.add(new_files)
#         db.commit()
#         db.refresh(new_files)
#         return {"message": f"Successfully uploaded {file.filename}"}


# @router.put("/update/{sub}")
# def add_post(
#     sub: str,
#     file: UploadFile | None,
#     db: Session = Depends(get_db),
#     current_user: int = Depends(oauth2.get_current_user),
# ):
#     sub = sub.strip()
#     post_query = db.query(models.Post).filter(
#         and_(
#             models.Post.owner_username == current_user.username,
#             models.Post.subject_code == sub,
#         )
#     )

#     print(current_user.username, sub)
#     post_q = post_query.first()
#     print(post_q)
#     files = db.query(models.Files)
#     if post_q == None:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail=f"post for subject: {sub} does not exist.",
#         )
#     if post_q.owner_username != current_user.username:
#         raise HTTPException(
#             status_code=status.HTTP_403_FORBIDDEN,
#             detail="Not authorized to perform requested action",
#         )
#     prev_rev = post_q.revision
#     curr_filename = file.filename
#     post_dict = schemas.PostUpdate.dict()
#     if curr_filename == post_q.curr_version or curr_filename in prev_rev:
#         raise HTTPException(
#             status_code=status.HTTP_409_CONFLICT,
#             detail=f"Cannot update same version again. Try different filename.",
#         )
#     else:
#         dfolder = "@{}".format(current_user.username)
#         fpath = os.path.abspath(os.path.join(*["data", sub, dfolder, curr_filename]))
#         ffolder = os.path.dirname(fpath)
#         try:
#             mkdir_safe(ffolder)
#             contents = file.file.read()
#             with open(fpath, "wb") as f:
#                 f.write(contents)
#         except Exception:
#             return {"message": "There was an error uploading the file"}
#         finally:
#             file.file.close()
#         post_dict.curr_version = curr_filename
#         prev_rev.append(curr_filename)
#     post_dict.revision = prev_rev
#     post_dict.subject_code = post_q.subject_code
#     post_dict.owner_username = current_user.username
#     post_dict.update(post_dict, synchronize_session=False)
#     db.commit()
#     db.refresh(post_dict)
#     new_files = models.Files(
#         owner_username=current_user.username,
#         subject_code=sub,
#         filename=curr_filename,
#         filepath=fpath,
#     )
#     db.add(new_files)
#     db.commit()
#     db.refresh(new_files)
#     return post_query.first()


@router.delete("/deletefile/{sub}/{filename}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(
    sub: str,
    filename: str,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    subsplit = sub.strip().split("_")
    if len(subsplit) > 1:
        sub, _ = subsplit
    else:
        sub = subsplit[0]
    filename = filename.strip()
    print(sub, filename)
    post_query = db.query(models.Post).filter(
        and_(
            models.Post.owner_username == current_user.username,
            models.Post.subject_code == sub,
        )
    )
    post = post_query.first()
    print(post)
    if post is None or not (filename in post.revision):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Files with filename: {filename} does not exist.",
        )
    files = db.query(models.Files).filter(
        and_(
            models.Files.owner_username == current_user.username,
            models.Post.subject_code == sub,
        )
    )
    if post.owner_username != current_user.username:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to perform requested action",
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


@router.delete("/deletesub/{sub}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_all_posts(
    sub: str,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    subsplit = sub.strip().split("_")
    if len(subsplit) > 1:
        sub, _ = subsplit
    else:
        sub = subsplit[0]
    print(sub)
    post_query = db.query(models.Post).filter(
        and_(
            models.Post.owner_username == current_user.username,
            models.Post.subject_code == sub,
        )
    )
    post = post_query.first()
    files = db.query(models.Files).filter(
        and_(
            models.Files.owner_username == current_user.username,
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
    if post.owner_username != current_user.username:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to perform requested action",
        )
    post_query.delete(synchronize_session=False)
    db.commit()
    if files:
        files.delete(synchronize_session=False)
        db.commit()
    for f in files_del:
        delete_file_safe(f)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# def download_image_file(
#     db: Session = Depends(get_db),
#     current_user: int = Depends(oauth2.get_current_user),
# ):
#     filepath = Path("../image.png")
#     return filepath.resolve()


# @router.get("/file/{image_id}", response_class=FileResponse)
# def get_image_file(
#     image_id: int,
#     db: Session = Depends(get_db),
# ) -> Any:
#     image: Optional[Image] = db.get(Image, image_id)
#     if not image:
#         raise HTTPException(404)

#     file_path = f"{settings.images_upload_path}{image.filename}{image.extension}"

#     logger.info(f"Getting image {file_path} (ID {image.id})")
#     return file_path
