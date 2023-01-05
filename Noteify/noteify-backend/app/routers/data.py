from fastapi import (
    Body,
    FastAPI,
    Response,
    status,
    HTTPException,
    Depends,
    APIRouter,
    Request,
)
from sqlalchemy.orm import Session
from pathlib import Path
from urllib.parse import urlparse
from fastapi.responses import FileResponse
from os import listdir
import os
import pyqrcode
import png
from pyqrcode import QRCode
from os.path import isfile, join
import json
from typing import List
from ..database import get_db
from ..config import settings
from .. import models, schemas, utils
from fastapi.responses import FileResponse
import io
from pathlib import Path
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import func
from sqlalchemy import and_
from sqlalchemy.orm.attributes import flag_modified
from fastapi import FastAPI, File, UploadFile
from urllib.parse import urlparse
from urllib.parse import quote
import unicodedata
import re

router = APIRouter(prefix="/data", tags=["Get data"])


def slugify(value, allow_unicode=False):
    """
    Taken from https://github.com/django/django/blob/master/django/utils/text.py
    Convert to ASCII if 'allow_unicode' is False. Convert spaces or repeated
    dashes to single dashes. Remove characters that aren't alphanumerics,
    underscores, or hyphens. Convert to lowercase. Also strip leading and
    trailing whitespace, dashes, and underscores.
    """
    value = str(value)
    if allow_unicode:
        value = unicodedata.normalize("NFKC", value)
    else:
        value = (
            unicodedata.normalize("NFKD", value)
            .encode("ascii", "ignore")
            .decode("ascii")
        )
    value = re.sub(r"[^\w\s-]", "", value.lower())
    return re.sub(r"[-\s]+", "-", value).strip("-_")


@router.get("/file/{filename}")
def get_file(
    filename: str,
    db: Session = Depends(get_db),
):
    filename = filename.strip()
    post_query = db.query(models.Files).filter(
        and_(
            models.Files.published == False,  # True, #TODO
            models.Files.filename == filename,
        )
    )
    post_q = post_query.first()
    if post_q:
        return FileResponse(post_q.filepath, filename=filename)
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with filename: {filename} was not found",
        )


@router.get("/versions/{sub}")
def get_versions(
    sub: str,
    db: Session = Depends(get_db),
):
    subsplit = sub.strip().split("_")
    if len(subsplit) > 1:
        sub, _ = subsplit
    else:
        sub = subsplit[0]
    print(sub)
    if not sub.strip().upper() in settings.supported_subcodes:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail=f"Posts on subject: {sub} is not accepted yet.",
        )
    post_query = db.query(models.Post).filter(
        and_(
            models.Post.published == False,  # True, #TODO
            models.Post.subject_code == sub,
        )
    )
    post_q = post_query.all()
    if not post_q:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with subject name: {sub} was not found",
        )
    versions = ["@{}".format(x.owner_username) for x in post_q]
    print(versions)
    return Response(content=json.dumps(versions), media_type="application/json")


@router.get("/revisions/{uniquecode}")
def get_revisions(
    uniquecode: str,
    db: Session = Depends(get_db),
):
    (uname, sub) = uniquecode.strip().split("]_[")
    uname = uname.replace("@", "")
    print((uname, sub))
    dfolder = "@{}".format(uname)
    folderpath = os.path.abspath(os.path.join(*["data", sub, dfolder]))
    # if os.path.isdir(folderpath):
    post_query = db.query(models.Files).filter(
        and_(
            models.Files.owner_username == uname,
            models.Files.subject_code == sub,
        )
    )
    post_q = post_query.all()
    all_files = [x.filename for x in post_q if x.published == False]  # True] # TODO
    return Response(content=json.dumps(all_files), media_type="application/json")


@router.get("/qr/{filename}")
def get_qr(filename: str, request: Request, db: Session = Depends(get_db)):
    filename = filename.strip()
    post_query = db.query(models.Files).filter(
        and_(
            models.Files.published == False,  # True, #TODO
            models.Files.filename == filename,
        )
    )
    post_q = post_query.first()
    if post_q:
        url_request = str(request.url)
        url = urlparse(url_request)
        uri_string = "{}://{}/data/file/{}".format(
            url.scheme, url.netloc, quote(filename)
        )
        print(uri_string)
        # Generate QR code
        qrcode = pyqrcode.create(uri_string)
        # Create and save the png file
        orgfilepath = Path(post_q.filepath)
        qrfilename = "{}_qr.png".format(orgfilepath.stem)
        qrfilepath = os.path.join(str(orgfilepath.parents[0]), qrfilename)
        qrcode.png(qrfilepath, scale=6)
        return FileResponse(qrfilepath, filename=qrfilename)
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with filename: {filename} was not found",
        )


@router.post("/download/{filename}")
def download_file(filename: str, db: Session = Depends(get_db)):
    filename = filename.strip()
    post_query = db.query(models.Files).filter(
        and_(
            models.Files.published == False,  # True, #TODO
            models.Files.filename == filename,
        )
    )
    post_q = post_query.first()
    if post_q:
        orgfilepath = Path(post_q.filepath)
        return FileResponse(orgfilepath, filename=orgfilepath.name)
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with filename: {filename} was not found",
        )


@router.get("/status/{user}")
async def get_users_logged(user: str):
    return utils.log_stat.is_logged_auth(user)
