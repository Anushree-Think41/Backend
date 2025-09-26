from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from app.auth import routes as user_router
import uvicorn
from app.db.db_handler import engine
from app.auth.models import Base
from app.core.exceptions import CustomException


Base.metadata.create_all(bind=engine)
app = FastAPI()

async def custom_exception_handler(request: Request, exc: CustomException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "detail": exc.detail,
            "error_code": exc.error_code,
        },
    )

app.add_exception_handler(CustomException, custom_exception_handler)


app.include_router(user_router.router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)