from datetime import datetime, timedelta
from typing import Optional
from app.core.exceptions import CustomException
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from app.db.db_handler import get_db
from sqlalchemy.orm import Session
from app.auth import services as user_service
import logging
import os   
from dotenv import load_dotenv
load_dotenv()


ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))
SECRET_KEY = os.getenv("SECRET_KEY", "your_secret_key")
ALGORITHM = os.getenv("ALGORITHM", "HS256") 

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/verify")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")



def verify_password(plain_password, hashed_password)-> bool:
    logging.debug("Verifying password.")
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password)-> str:
    logging.debug("Hashing password.")
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    logging.debug("Access token created.")
    return encoded_jwt

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