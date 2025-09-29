from fastapi import FastAPI, Request, status, Depends, Response,APIRouter
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.db.db_handler import get_db
from app.auth import routes as user_router
from app.owners import routes as owners
import uvicorn
from app.db.db_handler import engine
from app.auth.models import Base
from app.core.exceptions import CustomException


Base.metadata.create_all(bind=engine)
app = FastAPI()

# Health Check Router
health_router = APIRouter()

@health_router.get("/health", tags=["Health Check"], status_code=status.HTTP_200_OK)
def perform_health_check(response: Response, db: Session = Depends(get_db)):
    try:
        # Execute a simple query to check DB connection
        db.execute(text('SELECT 1'))
        return {"status": "ok", "database": "ok"}
    except Exception as e:
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
        return {"status": "error", "database": "error", "details": str(e)}


async def custom_exception_handler(request: Request, exc: CustomException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "detail": exc.detail,
            "error_code": exc.error_code,
        },
    )

app.add_exception_handler(CustomException, custom_exception_handler)


app.include_router(health_router) # Add health check router
app.include_router(user_router.router)
app.include_router(owners.router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)