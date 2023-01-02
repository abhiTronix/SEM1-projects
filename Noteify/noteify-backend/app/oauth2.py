from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi import status, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from . import schemas, database, models, utils
from .config import settings

SECRET_KEY = settings.secret_key
ALGORITHM = settings.encryption_algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

oath2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_name: str = payload.get("user_name")
        if user_name is None:
            raise credentials_exception
        token_data = schemas.TokenData(username=user_name)
    except JWTError:
        raise credentials_exception
    return token_data


def get_current_user(
    token: str = Depends(oath2_scheme), db: Session = Depends(database.get_db)
):
    if not utils.log_stat.is_loggedin():
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Logged out. Kindly login again!",
        )
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=f"Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    token = verify_access_token(token, credentials_exception)
    user = db.query(models.User).filter(models.User.username == token.username).first()
    return user


def get_current_moderator(
    token: str = Depends(oath2_scheme), db: Session = Depends(database.get_db)
):
    if not utils.log_stat.is_loggedin():
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Logged out. Kindly login again!",
        )
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=f"Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    token = verify_access_token(token, credentials_exception)
    moderator = (
        db.query(models.Moderator)
        .filter(models.Moderator.username == token.username)
        .first()
    )
    return moderator
