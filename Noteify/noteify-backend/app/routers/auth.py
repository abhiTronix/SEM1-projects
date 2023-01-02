from fastapi import APIRouter, Depends, status, HTTPException, Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from http.client import HTTPConnection
from sqlalchemy.orm import Session
from sqlalchemy import or_
from .. import database, schemas, models, utils, oauth2

router = APIRouter(tags=["User Authentication"])


@router.post("/login", response_model=schemas.Token)
def login(
    user_credentials: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(database.get_db),
):
    user = (
        db.query(models.User)
        .filter(
            or_(
                models.User.email == user_credentials.username,
                models.User.username == user_credentials.username,
            )
        )
        .first()
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid credentials"
        )
    if not utils.verify_pwd(user_credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid Credentials"
        )
    access_token = oauth2.create_access_token(data={"user_name": user.username})
    utils.log_stat.login(user.username, user.role, token=access_token)
    return {
        "username": user.username,
        "name": user.name,
        "email": user.email,
        "access_token": access_token,
        "token_type": "bearer",
    }


@router.post("/logout", response_model=schemas.UserOut)
async def logout(
    db: Session = Depends(database.get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    print(current_user)
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
