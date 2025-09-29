from jose import JWTError, jwt
from app.core.exceptions import CustomException
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from app.db.db_handler import get_db
from sqlalchemy.orm import Session
from app.auth.security import ALGORITHM, SECRET_KEY
from app.auth import services as user_service
import logging
import os
from dotenv import load_dotenv

load_dotenv()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/verify")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = CustomException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
        error_code="INVALID_TOKEN"
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if not isinstance(username, str) or username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = user_service.get_user_by_email(db, email=username)
    if user is None:
        raise CustomException(
            status_code=404,
            detail="User not found",
            error_code="USER_NOT_FOUND")

    logging.debug(f"Current user: {user.email}")

    return user