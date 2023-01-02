from fastapi import Body, FastAPI, Response, status, HTTPException, Depends, APIRouter
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from .. import models, schemas, utils, oauth2
from ..database import get_db
from ..config import settings
from sqlalchemy import and_

router = APIRouter(prefix="/mods", tags=["Moderators"])


@router.post(
    "/", status_code=status.HTTP_201_CREATED, response_model=schemas.ModeratorOut
)
def create_moderator(moderator: schemas.ModeratorCreate, db: Session = Depends(get_db)):
    if moderator.email in settings.regmod_emails:
        new_user = models.Moderator(**moderator.dict())
        print(new_user)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Moderator with username {username} does not exist. Kindly ask system adminstrator for the access",
        )


@router.post("/login", response_model=schemas.Token)
def moderator_login(
    moderator_credentials: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    moderator = (
        db.query(models.Moderator)
        .filter(
            and_(
                models.Moderator.username == moderator_credentials.username,
                models.Moderator.uuid_pwd == moderator_credentials.password,
            )
        )
        .first()
    )
    if not moderator:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid credentials"
        )
    access_token = oauth2.create_access_token(data={"user_name": moderator.username})
    utils.log_stat.login(moderator.username, moderator.role, token=access_token)
    return {
        "username": moderator.username,
        "name": moderator.name,
        "email": moderator.email,
        "access_token": access_token,
        "token_type": "bearer",
    }


@router.post("/logout", response_model=schemas.ModeratorOut)
async def moderator_logout(
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_moderator),
):
    if utils.log_stat.logout(current_user.username):
        return {
            "username": current_user.username,
            "email": current_user.email,
            "created_at": current_user.created_at,
        }
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You're not authorized to perform this action",
        )
