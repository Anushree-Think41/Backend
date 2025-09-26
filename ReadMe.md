# Bhoruka Backend
This project is a FastAPI application that provides basic user registration and login functionality.
## Tech Stack

- [FastAPI](https://fastapi.tiangolo.com/)
- [Uvicorn](https://www.uvicorn.org/)
- [SQLAlchemy](https://www.sqlalchemy.org/)
- [PostgreSQL](https://www.postgresql.org/)
- [Psycopg2](https://www.psycopg.org/docs/)
- [Alembic](https://alembic.sqlalchemy.org/en/latest/)
- [Pydantic](https://pydantic-docs.helpmanual.io/)
- [Passlib](https://passlib.readthedocs.io/en/stable/)
- [Python-JOSE](https://python-jose.readthedocs.io/en/latest/)
- [Pytest](https://docs.pytest.org/en/7.1.x/)
- [HTTPX](https://www.python-httpx.org/)

## API Endpoints

### User Registration

- **URL:** `/auth/register`
- **Method:** `POST`
- **Request Body:**
  ```json
  {
    "email": "user@example.com",
    "password": "yourpassword"
  }
  ```
- **Response:**
  ```json
  {
    "email": "user@example.com"
  }
  ```

### User Login

- **URL:** `/auth/login`
- **Method:** `POST`
- **Request Body:**
  ```json
  {
    "username": "user@example.com",
    "password": "yourpassword"
  }
  ```
- **Response:**
  ```json
  {
    "access_token": "your_jwt_token",
    "token_type": "bearer"
  }
  ```