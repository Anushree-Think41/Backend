from fastapi import APIRouter, Depends
from app.core.exceptions import CustomException
from sqlalchemy.orm import Session
from app.auth import schemas as user_schema
from app.auth import services as user_service
from app.auth import auth as auth_service
from app.db.db_handler import get_db
from fastapi.security import OAuth2PasswordRequestForm
from datetime import datetime
import logging
logger = logging.getLogger(__name__)


router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)


@router.post("/user/create", response_model=user_schema.UserBase)
def create_user(user: user_schema.UserCreate, db: Session = Depends(get_db)) -> user_schema.UserBase:
    try:
        logger.info(f"Request received to create user with email: {user.email}")

        db_user = user_service.get_user_by_email(db, email=user.email)
        if db_user:
            logger.warning(f"User with email '{user.email}' already exists.")
            raise CustomException(
                status_code=400,
                detail="Email already registered",
                error_code="EMAIL_ALREADY_EXISTS"
            )

        created_user = user_service.create_user(db=db, user=user)
        logger.info(f"Successfully created user with ID: {created_user.id}")
        
        return created_user
    
    except Exception as e:
        logger.error(f"An unexpected error occurred while creating user: {e}", exc_info=True)

        raise CustomException(
            status_code=500,
            detail="An internal server error occurred. Please try again later.",
            error_code="INTERNAL_SERVER_ERROR"
        )


@router.post("/user/verify")
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db))-> dict:

    try:
        logger.info(f"Login attempt for user: {form_data.username}")
    
        user = user_service.get_user_by_email(db, email=form_data.username)

        if not user or not auth_service.verify_password(form_data.password, user.hashed_password):
            raise CustomException(
                status_code=401,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
                error_code="INVALID_CREDENTIALS"
            )
        user.last_login = datetime.utcnow()
        db.commit()
        access_token = auth_service.create_access_token(
            data={"sub": user.email, "last_login": user.last_login.isoformat()}
        )
        return {"access_token": access_token, "token_type": "bearer"}
    

    except Exception as e:
        logger.error(f"Logging error: {e}", exc_info=True)
        raise CustomException(
            status_code=500,
            detail="An internal server error occurred. Please try again later.",
            error_code="INTERNAL_SERVER_ERROR"
        )
    

@router.get("/user/{user_id}", response_model=user_schema.UserBase)
def read_user(user_id: int, db: Session = Depends(get_db))-> user_schema.UserBase:
    try:
        logger.info(f"Fetching user with ID: {user_id}")

        db_user = user_service.get_user(db, user_id=user_id)
        if db_user is None:
            raise CustomException(status_code=404, detail="User not found",error_code="USER_NOT_FOUND")
        return db_user
    
    except Exception as e:
        logger.error(f"Error fetching user with ID {user_id}: {e}", exc_info=True)
        raise CustomException(
            status_code=500,
            detail="An internal server error occurred. Please try again later.",
            error_code="INTERNAL_SERVER_ERROR"
        )
    


