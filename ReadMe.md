# Bhoruka Backend

Backend service for user registration and authentication. It features JWT-based authentication, custom error handling, and a PostgreSQL database integration using SQLAlchemy.

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

## Getting Started

### Prerequisites

- Python 3.10+
- PostgreSQL

### Installation

1.  Clone the repository:
    ```bash
    git clone <repository_url>
    cd owner-onboarding-service
    ```
2.  Install the dependencies:
    ```bash
    pip install -r requirements.txt
    ```

### Database Setup

This project uses a PostgreSQL database. You will need to have a PostgreSQL server running. The database connection string is configured in the application (for a production setup, it is recommended to use environment variables).

The database tables are created automatically when the application starts.

### Running the Application

To run the application locally, use the following command:

```bash
uvicorn app.main:app --reload
```

The application will be available at `http://localhost:8000`.

## API Endpoints

The following endpoints are available:

- `POST /auth/user/create`: Create a new user.
- `POST /auth/user/verify`: Log in and get an access token.
- `GET /auth/user/{user_id}`: Get a user's details by ID.

## Error Handling

The API uses a custom error handling mechanism to provide detailed error information to the client. When an error occurs, the API will return a JSON response with an `error_code` and a `detail` message.

**Example Error Response:**

```json
{
  "detail": "Email already registered",
  "error_code": "EMAIL_ALREADY_EXISTS"
}
```
