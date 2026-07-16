# Notes API

A RESTful backend API for creating and managing personal notes, with secure JWT-based authentication, refresh token rotation, and per-user data isolation.

## Tech Stack

- **FastAPI** — web framework
- **PostgreSQL** — database
- **SQLAlchemy** — ORM
- **Alembic** — database migrations
- **JWT (python-jose)** — authentication
- **Pydantic** — request/response validation

## Features

- User registration and login
- JWT access tokens + refresh token rotation
- Secure logout with refresh token revocation
- Full CRUD for notes, scoped to the authenticated user (ownership enforced on every operation)
- Pagination and sorting on the notes list
- Centralized exception handling with consistent HTTP status codes

## Getting Started

### Prerequisites

- Python 3.11+
- PostgreSQL running locally or accessible via connection string

### Setup

1. Clone the repo and enter the project directory:
   ```bash
   git clone https://github.com/KarimmHmaidan/notes-api.git
   cd notes-api
   ```

2. Create a virtual environment and install dependencies:
   ```bash
   python -m venv venv
   source venv/bin/activate  # on Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the project root:
   ```
   DATABASE_URL=postgresql://<user>:<password>@localhost:5432/notes_db
   secret_key=your-secret-key
   jwt_algorithm=HS256
   ```

   Access tokens default to a 1 hour lifetime and refresh tokens to 7 days — these are currently hardcoded in `security.py` rather than read from `.env`.

4. Run database migrations:
   ```bash
   alembic upgrade head
   ```

5. Start the server:
   ```bash
   uvicorn app.main:app --reload
   ```

6. Open the interactive API docs at [http://localhost:8000/docs](http://localhost:8000/docs)

## API Endpoints

### Auth

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/register` | Create a new user account |
| POST | `/login` | Authenticate and receive access + refresh tokens |
| POST | `/refresh` | Exchange a valid refresh token for a new token pair |
| POST | `/logout` | Revoke a refresh token |

### Notes

All notes endpoints require a valid `Authorization: Bearer <access_token>` header and only operate on the authenticated user's own notes.

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/notes` | List notes (paginated, sortable — see below) |
| POST | `/notes` | Create a new note |
| GET | `/notes/{note_id}` | Retrieve a single note |
| PUT | `/notes/{note_id}` | Update a note |
| DELETE | `/notes/{note_id}` | Delete a note |

#### `GET /notes` query parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `skip` | int | `0` | Number of records to skip |
| `limit` | int | `10` | Max records to return (1–100) |
| `sort_by` | string | `created_at` | One of: `created_at`, `updated_at`, `title` |
| `order` | string | `desc` | `asc` or `desc` |

**Example:**
```
GET /notes?skip=0&limit=10&sort_by=updated_at&order=desc
```

**Response:**
```json
{
  "total": 42,
  "skip": 0,
  "limit": 10,
  "items": [
    {
      "id": 1,
      "title": "Grocery list",
      "content": "Eggs, milk, bread",
      "created_at": "2026-07-10T14:35:00",
      "updated_at": "2026-07-15T02:07:00"
    }
  ]
}
```

## Project Structure

```
app/
├── main.py               # FastAPI app entrypoint
├── database.py           # DB engine and session setup
├── models.py             # SQLAlchemy models
├── dependencies.py       # Shared dependencies (e.g. get_current_user)
├── security.py           # JWT creation/verification helpers
├── exceptions.py         # Custom exception classes
├── routers/
│   ├── auth.py           # Auth endpoints
│   └── notes.py          # Notes endpoints
├── schemas/
│   ├── users.py          # User-related Pydantic schemas
│   └── notes.py          # Note-related Pydantic schemas
└── services/
    ├── users.py           # User business logic
    ├── notes.py           # Notes business logic
    └── refresh_tokens.py  # Refresh token storage/rotation logic
```

## Roadmap

- [ ] Automated tests (pytest)
- [ ] Docker + docker-compose for one-command setup
- [ ] Rate limiting on auth endpoints
