import logging
from sqlalchemy.orm import Session
from app.auth import models as user_model
from app.auth import schemas as user_schema
from app.auth.security import get_password_hash
from app.core.exceptions import CustomException

logger = logging.getLogger(__name__)

def get_user_by_email(db: Session, email: str):
    try:
        return db.query(user_model.User).filter(user_model.User.email == email).first()
    except Exception as e:
        logger.error(f"Error fetching user by email {email}: {e}", exc_info=True)
        db.rollback()
        raise CustomException(
            status_code=500,
            detail="An error occurred while fetching user data.",
            error_code="DB_ERROR_FETCHING_USER"
        ) from e

def create_user(db: Session, user: user_schema.UserCreate):
    try:
        hashed_password = get_password_hash(user.password)
        db_user = user_model.User(username=user.username, email=user.email, hashed_password=hashed_password)
        if not db_user:
            raise CustomException(
                status_code=500,
                detail="Failed to create user instance.",
                error_code="USER_CREATION_FAILED"
            )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    
    except Exception as e:
        logger.error(f"Error creating user with email {user.email}: {e}", exc_info=True)
        db.rollback()
        raise CustomException(
            status_code=500,
            detail="Failed to create user.",
            error_code="USER_CREATION_FAILED"
        ) from e

def get_user(db: Session, user_id: int):
    try:
        return db.query(user_model.User).filter(user_model.User.id == user_id).first()
    except Exception as e:
        logger.error(f"Error fetching user by ID {user_id}: {e}", exc_info=True)
        db.rollback()
        raise CustomException(
            status_code=500,
            detail="An error occurred while fetching user data.",
            error_code="DB_ERROR_FETCHING_USER"
        ) from e
